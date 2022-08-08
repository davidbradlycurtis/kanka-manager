""" Application Configuration """

import logging
import os
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

DEFAULT_CONFIG = '''
# Default KankaManager configuration file

campaign: None
campaign_dir: None
token: None
throttle: True
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
