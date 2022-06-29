from enum import Enum


PESSIMISTIC_MUL = 0.85
GROSS_TO_NET_DIV = 1.27


class Arukereso(Enum):

    BASE_URL = 'https://www.arukereso.hu'
    GRAPHIC_CARD = 'videokartya-c3142'
    QUERY_PARAMS = {
        'order': {
            'name': 'orderby',
            'values': {
                'cheap': 1,
                'expensive': 2
            }
        },
        'name': {
            'name': 'st'
        }
    }

    DESCRIPTIONS_XPATH = '//*[contains(concat( " ", @class, " " ), concat( " ", "top-center", " " ))]'
    PRICES_XPATH = '//*[contains(concat( " ", @class, " " ), concat( " ", "price", " " ))]'


class WhatToMine(Enum):

    BASE_URL = 'https://whattomine.com'
    GRAPHIC_CARD = 'gpus'
    QUERY_PARAMS = {
        'cost': {
            'name': 'cost'
        }
    }

    CARD_REGEX = r'href="/gpus/(.+?)\?'
    CARD_OVERVIEW_TABLE_XPATH = '//td'
    CARD_DETAILS_TABLE_XPATH = '//td'

    WHITELISTED_GPU_NAMES = [
        'rtx 3060 ti',
        'rtx 3060 ti lhr',
        'rtx 3060',
        'rtx 3070',
        'rtx 3070 ti',
        'rtx 3060 lhr',
        'rtx 3080 lhr',
        'rtx 3070 lhr',
        'rtx 3080',
        'rx 6700 xt',
        'rtx 3080 ti',
        'rtx 2060',
        'rx 6600',
        'gtx 1660 ti',
        'rtx 3080 12gb',
        'gtx 1660 super',
        'rx 6800',
        'rx 6600 xt',
        'rtx a2000 6gb',
        'rtx 2060 super',
        'gtx 1660',
        'rx 6800 xt',
        'rx 6750 xt',
        'rtx 3090',
        'rtx 3050',
        'rx 6900 xt',
        'rx 580 8gb',
        'rx 6650 xt',
        'rtx 3090 ti',
        'rtx a4000',
        'rtx a5000',
        'rx 6950 xt',
        'gtx 1050 ti',
        'rtx a4500',
        'rx 5500 xt 8gb'
    ]


class _GraphicCard(Enum):
    NVIDIA_PREFIX = 'NVIDIA '
    GEFORCE_PREFIX = 'GeForce '
    AMD_RADEON_PREFIX = 'AMD Radeon '
    STAR_SUFFIX = ' (*)'

    NUMBER_OF_THREADS = 8


class Price(Enum):
    USD_TO_HUF = 380
    ELECTRICITY_COST_IN_HUF = 25
