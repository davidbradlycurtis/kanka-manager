"""
Kanka Client

"""
# pylint: disable=bare-except
from __future__ import absolute_import

import logging

from kankaclient.abilities import AbilityAPI
from kankaclient.base import BaseManager, Entity
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

    def __init__(self, config, verbose: str=False):
        super().__init__(token=config.get('token'), verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign_dir = config.get('campaign_dir')

        self.campaigns = CampaignAPI(token=config.get('token'), campaign=config.get('campaign'), verbose=verbose)
        self.abilities = AbilityAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.calendars = CalendarAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.characters = CharacterAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.conversations = ConversationAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.dice = DiceRollAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.events = EventAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.families = FamilyAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.items = ItemAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.journals = JournalAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.locations = LocationAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.maps = MapAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.organizations = OrganizationAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.quests = QuestAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.races = RaceAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.tags = TagAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)
        self.timelines = TimelineAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose)

        self.entities = {
            'campaign': self.campaigns,
            'abilities': self.abilities,
            'calendars': self.calendars,
            'characters': self.characters,
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


    def get(self, entity: str, name_or_id: str or int) -> dict:
        """
        TODO

        Args:
            entity (str): the entity to retrieve
            name_or_id (str or int): the name or id of the character

        Returns:
            dict: _description_
        """
        result = self.entities.get(entity).get(name_or_id)
        return result


    def get_all(self, entity: str) -> dict:
        """
        TODO

        Args:
            entity (str): the entity to retrieve

        Returns:
            dict: _description_
        """
        result = self.entities.get(entity).get_all()
        return result


    def create(self, entity: str, data: dict) -> dict:
        """
        TODO

        Args:
            entity (str): the entity to create
            data (dict): the entity's data

        Returns:
            dict: _description_
        """
        result = self.entities.get(entity).create(data)
        return result


    def update(self, entity: str, data: dict or Entity) -> dict:
        """
        TODO

        Args:
            entity (str): the entity to update
            data (dict or Entity): the entity's data

        Returns:
            dict: _description_
        """
        result = self.entities.get(entity).update(data)
        return result


    def delete(self, entity: str, name_or_id: str or int) -> dict:
        """
        TODO

        Args:
            entity (str): the entity to update
            name_or_id (str or int): the name or id of the entity to delete

        Returns:
            dict: _description_
        """
        result = self.entities.get(entity).delete(name_or_id)
        return result

    # def smart_substitute(self, entities):
    #     for attribute in SUBSTITUTION_LIST:
    #         if hasattr(entities[0], attribute)
    #     for entity in entities:

    #     pass
