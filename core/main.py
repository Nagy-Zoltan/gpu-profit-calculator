from threading import Thread

import pandas as pd

from core.externals.what_to_mine import WhatToMineHandler
from core.graphic_card import GraphicCard
from core.constants import GROSS_TO_NET_DIV, NUMBER_OF_THREADS
from core.utils import divide_list_to_sublists


def get_graphic_cards(what_to_mine_handler):
    threads = []
    graphic_cards = []

    profits = list(what_to_mine_handler.profits)
    overviews = what_to_mine_handler.graphic_card_overviews

    profit_chunks = divide_list_to_sublists(profits, NUMBER_OF_THREADS)
    overview_chunks = divide_list_to_sublists(overviews, NUMBER_OF_THREADS)

    def add_to_graphic_cards(profits, overviews):
        for profit, overview in zip(profits, overviews):
            graphic_card = GraphicCard(profit, *overview)
            graphic_cards.append(graphic_card)

    for pc, oc in zip(profit_chunks, overview_chunks):
        thread = Thread(target=add_to_graphic_cards, args=(pc, oc))
        threads.append(thread)

    print(f'Number of threads: {len(threads)}')

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return graphic_cards


def get_payoffs(graphic_cards):
    return [[gc.arukereso_name, gc.price, gc.monthly_profit_huf_pessimistic, gc.payoff_huf_pessimistic] \
            for gc in sorted(graphic_cards, key=lambda gc: gc.payoff_huf_pessimistic)]


def create_payoff_df(payoffs):
    df = pd.DataFrame(payoffs, columns=['graphic card', 'price', 'monthly profit (HUF)', 'payoff'])
    df = df[df['payoff'] != float('inf')]
    df['monthly profit (HUF)'] = [int(round(price, -2)) for price in df['monthly profit (HUF)']]
    df['price'] = round(df['price'], -3)
    df['payoff'] = round(df['payoff'], 1)
    df.insert(2, 'net price', [int(price) for price in round(df['price'] / GROSS_TO_NET_DIV, -3)])
    df['net payoff'] = round(df['payoff'] / GROSS_TO_NET_DIV, 1)
    df['10 month payoff price'] = [int(price) for price in round(10 / df['net payoff'] * df['net price'], -3)]
    df['11 month payoff price'] = [int(price) for price in round(11 / df['net payoff'] * df['net price'], -3)]
    df['12 month payoff price'] = [int(price) for price in round(12 / df['net payoff'] * df['net price'], -3)]
    return df


def main():
    what_to_mine_handler = WhatToMineHandler()

    graphic_cards = get_graphic_cards(what_to_mine_handler)
    payoffs = get_payoffs(graphic_cards)
    payoff_df = create_payoff_df(payoffs)

    payoff_df.to_csv('/gpu_profits/results/results.csv', index=False)
    payoff_df.to_excel('/gpu_profits/results/results.xlsx', index=False)
