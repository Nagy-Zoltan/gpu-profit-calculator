import more_itertools

from arukereso import ArukeresoHandler
from constants import _GraphicCard, PESSIMISTIC_MUL
from utils import usd_to_huf


class GraphicCard:

    def __init__(self, max_profit_usd, *args):

        """
        :param max_profit_usd:
        1.4

        :param args:
        [
            'NVIDIA GeForce RTX 3090 Ti (*)',
            'Mar 2022',
            '128.00 Mh/s Ethash · 350W',
            '$1.93',
            '$1.09',
            'ETH Ethash\n$1.09\nNicehash Ethash\n$1.07\nNicehash Autolykos $0.92']
        ]
        """

        self.daily_profit_usd = max_profit_usd
        self.daily_profit_usd_pessimistic = max_profit_usd * PESSIMISTIC_MUL
        self.daily_profit_huf = usd_to_huf(self.daily_profit_usd)
        self.daily_profit_huf_pessimistic = self.daily_profit_huf * PESSIMISTIC_MUL
        self.monthly_profit_usd = self.daily_profit_usd * 30
        self.monthly_profit_usd_pessimistic = self.monthly_profit_usd * PESSIMISTIC_MUL
        self.monthly_profit_huf = self.daily_profit_huf * 30
        self.monthly_profit_huf_pessimistic = self.monthly_profit_huf * PESSIMISTIC_MUL

        self.name = args[0]
        self.release_date = args[1]
        self.hashrate = args[2]
        self.revenue_24h = args[3]
        self.profit_24h = args[4]

        self.top_coins_profit = dict(list(
            more_itertools.chunked(args[5].replace(' $', '\n$').replace(' -$', '\n-$').replace('$', '').split('\n'),
                                   2)))

        self.arukereso_name = self._get_arukereso_name()
        self.arukereso_handler = ArukeresoHandler(self.arukereso_name)
        self.price = self.arukereso_handler.cheapest

        if self.price is not None:
            self.payoff_huf = round(self.price / self.monthly_profit_huf, 1)
            self.payoff_huf_pessimistic = round(self.price / self.monthly_profit_huf_pessimistic, 1)
        else:
            self.payoff_huf = float('inf')
            self.payoff_huf_pessimistic = float('inf')

    def _get_arukereso_name(self):
        return self.name\
            .removeprefix(_GraphicCard.NVIDIA_PREFIX.value)\
            .removeprefix(_GraphicCard.GEFORCE_PREFIX.value)\
            .removeprefix(_GraphicCard.AMD_RADEON_PREFIX.value)\
            .removesuffix(_GraphicCard.STAR_SUFFIX.value)

    def __repr__(self):
        return str(vars(self))
