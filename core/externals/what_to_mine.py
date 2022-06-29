import re

import requests_html
import more_itertools

from core.constants import WhatToMine, Price
from core.utils import huf_to_usd


class WhatToMineHandler:

    graphic_cards_url = f'{WhatToMine.BASE_URL.value}/{WhatToMine.GRAPHIC_CARD.value}'
    cost_param = WhatToMine.QUERY_PARAMS.value['cost']

    def __init__(self):
        self.session = requests_html.HTMLSession()
        self.asession = requests_html.AsyncHTMLSession()
        self.gpus_raw_html = self.session.get(self.graphic_cards_url)
        self.gpu_url_names = self._get_graphic_cards_names_in_url()
        self.graphic_card_overviews = self.get_graphic_card_overviews()
        self.tasks = self._get_tasks_to_get_profits()
        self.profits = dict.fromkeys(self.gpu_url_names)
        self.get_profits()

    def _get_graphic_cards_names_in_url(self):
        return re.findall(WhatToMine.CARD_REGEX.value, self.gpus_raw_html.text)

    def get_graphic_card_overviews(self):
        table = self.gpus_raw_html.html.xpath(WhatToMine.CARD_OVERVIEW_TABLE_XPATH.value)
        values = [elem.text for elem in table]
        return list(more_itertools.chunked(values, 6))

    async def get_profits_for_graphic_card(self, graphic_card):
        url = f'{self.graphic_cards_url}/{graphic_card}'
        params = {
            self.cost_param['name']: huf_to_usd(Price.ELECTRICITY_COST_IN_HUF.value)
        }

        res = await self.asession.get(url=url, params=params)

        td = res.html.xpath(WhatToMine.CARD_DETAILS_TABLE_XPATH.value)

        max_profit_usd = min(float(num) for num in td[5].text.replace('$', '').split())

        return max_profit_usd

    def _get_tasks_to_get_profits(self):
        tasks = []

        for name in self.gpu_url_names:
            async def task(name=name):
                max_profit_usd = await self.get_profits_for_graphic_card(name)
                self.profits[name] = max_profit_usd
            tasks.append(task)

        return tasks

    def get_profits(self):
        self.asession.run(*self.tasks)
