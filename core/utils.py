import more_itertools

from core.constants import Price


def usd_to_huf(usd):
    return round(usd * Price.USD_TO_HUF.value)


def huf_to_usd(huf):
    return round(huf / Price.USD_TO_HUF.value, 2)


def divide_list_to_sublists(L, num):
    q, r = divmod(len(L), num)
    last_size = q + r

    ret = []
    if r:
        last = L[-last_size:]
        rest = L[:-last_size]
    else:
        last = []
        rest = L

    ret += list(more_itertools.chunked(rest, q))
    if r:
        ret.append(last)

    return ret
