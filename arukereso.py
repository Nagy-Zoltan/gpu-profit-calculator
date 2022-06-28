import re

import requests_html

from constants import Arukereso


class ArukeresoHandler:

    graphic_card_url = f'{Arukereso.BASE_URL.value}/{Arukereso.GRAPHIC_CARD.value}'
    order_param = Arukereso.QUERY_PARAMS.value['order']
    name_param = Arukereso.QUERY_PARAMS.value['name']

    def __init__(self, graphic_card_name):
        self.session = requests_html.HTMLSession()
        self.graphic_card_name = graphic_card_name
        self.raw_html = self.get_raw_html(graphic_card_name)
        self.descriptions = self.get_descriptions()
        self.prices = self.get_prices()
        print(len(self.prices))
        print(len(self.descriptions))
        self._clean_results()

    def get_raw_html(self, graphic_card_name, order_by='cheap'):
        url = self.graphic_card_url
        params = {
            self.order_param['name']: self.order_param['values'][order_by],
            self.name_param['name']: graphic_card_name
        }

        res = self.session.get(url=url, params=params)

        return res.html

    def get_descriptions(self):
        return [
            elem.text for elem in
            self.raw_html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "top-center", " " ))]')
        ]

    def get_prices(self):
        raw_prices = [
            elem.text for elem in
            self.raw_html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "price", " " ))]')
        ]

        return [int(''.join(re.findall('[\d]+?', price))) for price in raw_prices[::2]]

    def _name_present_in_description(self, description):
        parts = self.graphic_card_name.lower().split()
        print(parts)
        description_lower = description.splitlines()[0].lower()
        for part in parts:
            if part + ' ' not in description_lower:
                return False

        if 'ti' in parts:
            ti_place = parts.index('ti')
            ti_name = ' '.join(parts[ti_place - 1: ti_place + 1])
            if ti_name not in description_lower:
                return False

        if 'lhr' not in parts and 'lhr' in description_lower:
            return False

        return True

    def _clean_results(self):
        descriptions = self.descriptions
        prices = self.prices

        if not descriptions or not prices:
            return

        filtered_descriptions = []
        filtered_prices = []

        for d, p in zip(descriptions, prices):
            print('-'*50)
            if self._name_present_in_description(d):
                filtered_descriptions.append(d)
                filtered_prices.append(p)

        self.descriptions = filtered_descriptions
        self.prices = filtered_prices


arukereso_handler = ArukeresoHandler('RTX 3090 Ti')


print(len(arukereso_handler.prices))
print(len(arukereso_handler.descriptions))
