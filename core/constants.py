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


class _GraphicCard(Enum):
    NVIDIA_PREFIX = 'NVIDIA '
    GEFORCE_PREFIX = 'GeForce '
    AMD_RADEON_PREFIX = 'AMD Radeon '
    STAR_SUFFIX = ' (*)'

    NUMBER_OF_THREADS = 8


class Price(Enum):
    USD_TO_HUF = 380
    ELECTRICITY_COST_IN_HUF = 25
