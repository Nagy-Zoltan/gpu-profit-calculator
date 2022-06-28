import pandas as pd

from what_to_mine import WhatToMineHandler
from graphic_card import GraphicCard
from constants import GROSS_TO_NET_DIV

what_to_mine_handler = WhatToMineHandler()


def get_graphic_cards():
    graphic_cards = []

    for profit, overview in zip(what_to_mine_handler.profits, what_to_mine_handler.graphic_card_overviews):
        graphic_card = GraphicCard(profit, *overview)
        graphic_cards.append(graphic_card)

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
    graphic_cards = get_graphic_cards()
    payoffs = get_payoffs(graphic_cards)
    payoff_df = create_payoff_df(payoffs)

    payoff_df.to_csv('results.csv', index=False)
    payoff_df.to_excel('results.xlsx', index=False)


if __name__ == '__main__':
    main()
