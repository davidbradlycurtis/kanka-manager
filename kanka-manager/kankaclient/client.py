"""
Kanka Client

"""
# pylint: disable=bare-except
from __future__ import absolute_import

import logging

from kankaclient.abilities import AbilityAPI
from kankaclient.base import BaseManager
from kankaclient.calendars import CalendarAPI
from kankaclient.campaigns import CampaignAPI
from kankaclient.characters import CharacterAPI
from kankaclient.conversations import ConversationAPI
from kankaclient.dice import DiceRollAPI
from kankaclient.events import EventAPI
from kankaclient.families import FamilyAPI
from kankaclient.items import ItemAPI
from kankaclient.journals import JournalAPI
from kankaclient.locations import LocationAPI
from kankaclient.maps import MapAPI
from kankaclient.organizations import OrganizationAPI
from kankaclient.quests import QuestAPI
from kankaclient.races import RaceAPI
from kankaclient.tags import TagAPI
from kankaclient.timelines import TimelineAPI



class KankaClient(BaseManager):
    """Kanka Client"""

    entities: dict

    def __init__(self, token: str, campaign: str, verbose: str=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.campaigns = CampaignAPI(token=token, campaign=campaign, verbose=verbose)
        self.abilities = AbilityAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.calendars = CalendarAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.characters = CharacterAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.conversations = ConversationAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.dice = DiceRollAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.events = EventAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.families = FamilyAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.items = ItemAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.journals = JournalAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.locations = LocationAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.maps = MapAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.organizations = OrganizationAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.quests = QuestAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.races = RaceAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.tags = TagAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.timelines = TimelineAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)

        global entities
        entities = {
            'campaign': self.campaigns,
            'abilities': self.abilities,
            'calendars': self.calendars,
            'character': self.characters,
            'conversations': self.conversations,
            'dice': self.dice,
            'events': self.events,
            'families': self.families,
            'items': self.items,
            'journals': self.journals,
            'locations': self.locations,
            'maps': self.maps,
            'organizations': self.organizations,
            'quests': self.quests,
            'races': self.races,
            'tags': self.tags,
            'timelines': self.timelines
        }

        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.logger.debug('Kanka Client initialized')

    
    def get(self, entity: str, **kwargs: str) -> dict:
        """
        TODO

        Args:
            entity (str): _description_

        Returns:
            dict: _description_
        """
        result = entities.get(entity).get(**kwargs)
        return result
