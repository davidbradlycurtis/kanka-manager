""" Application Configuration """

import logging
##################################################
#
# logging configs
DEFAULT_LOG_LEVEL = logging.WARN
LOG_FORMAT = "%(asctime)s  %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.000000"

BASE_URL = 'https://kanka.io/api/1.0/campaigns'
MAX_ATTEMPTS = 5

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'

# TODO: Re-work this input mapping
ENTITY_FORMAT = {
    'campaign': 'campaings',
    'campaigns': 'campaings',
    'ability': 'abilities',
    'abilities': 'abilities',
    'calendar': 'calendars',
    'calendars': 'calendars',
    'character': 'characters',
    'characters': 'characters',
    'conversation': 'conversations',
    'conversations': 'conversations',
    'dice': 'die',
    'die': 'die',
    'diceroll': 'die',
    'dicerolls': 'die',
    'event': 'events',
    'event': 'events',
    'family': 'families',
    'families': 'families',
    'items': 'items',
    'item': 'items',
    'journal': 'journals',
    'journals': 'journals',
    'location': 'locations',
    'locations': 'locations',
    'map': 'maps',
    'maps': 'maps',
    'organization': 'organizations',
    'organizations': 'organizations',
    'quest': 'quests',
    'quests': 'quests',
    'race': 'races',
    'races': 'races',
    'timeline': 'timelines',
    'timelines': 'timelines',
    'tag': 'tags',
    'tags': 'tags'
}

CONFIG = 'config'

CONFIG_FIELDS = {
    'campaign': 'Campaign name: ',
    'campaign_dir': 'Campaign folder: ',
    'token': 'API token: ',
    'throttle': 'Throttle? (true/false): '
}

CONFIG_FILE = '''# ---KankaManager configuration file---

# The name of the Kanka campaign to manage
campaign: {campaign}

# The folder/directory where to store campaign entities
campaign_dir: {campaign_dir}

# The campaign API token (https://kankaclient.io/en/api-docs/1.0/setup)
token: {token}

# Whether to throttle API requests (recommended for none boosted campaigns)
throttle: {throttle}
'''

DEFAULT_REMOVE = [
    'created_at',
    'created_by',
    'updated_at',
    'updated_by'
]

COMMANDS = [
    'get',
    'create',
    'update',
    'pull',
    'push',
    'delete'
]

OUTPUT_OPTIONS = [
    'yaml',
    'json',
]

ENTITIES = [
    'character'
]
