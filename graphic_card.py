class GraphicCard:

    def __init__(self, *args):

        """
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

        self.name = args[0]
        self.arukereso_name = self.name.removeprefix('NVIDIA ').removeprefix('GeForce ').removeprefix(
            'AMD Radeon ').removesuffix(' (*)')
        self.arukereso_url = ARUKERESO_BASEURL + self.arukereso_name.replace(' ', '+')
        self.release_date = args[1]
        self.hashrate = args[2]
        self.revenue_24h = args[3]
        self.profit_24h = args[4]
        # self.max_profit_number = float(args[4][1:])

        self.top_coins_profit = dict(list(
            more_itertools.chunked(args[5].replace(' $', '\n$').replace(' -$', '\n-$').replace('$', '').split('\n'),
                                   2)))

    def _name_present_in_description(self, description):
        parts = self.arukereso_name.lower().split()
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

    def _filter_arukereso_results(self):
        descriptions = self.descriptions
        prices = self.prices

        if not descriptions or not prices:
            return

        filtered_desctriptions = []
        filtered_prices = []

        for d, p in zip(descriptions, prices):
            if self._name_present_in_description(d):
                filtered_desctriptions.append(d)
                filtered_prices.append(p)

        self.descriptions = filtered_desctriptions
        self.prices = filtered_prices

    def __repr__(self):
        return str(vars(self))