from enum import Enum


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

