from core.constants import Price


def usd_to_huf(usd):
    return round(usd * Price.USD_TO_HUF.value)


def huf_to_usd(huf):
    return round(huf / Price.USD_TO_HUF.value, 2)
