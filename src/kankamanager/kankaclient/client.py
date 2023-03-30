"""
Kanka Client

"""
# pylint: disable=bare-except
from __future__ import absolute_import

import logging

from kankamanager.kankaclient.abilities import AbilityAPI
from kankamanager.kankaclient.base import BaseManager, Entity
from kankamanager.kankaclient.calendars import CalendarAPI
from kankamanager.kankaclient.campaigns import CampaignAPI
from kankamanager.kankaclient.characters import CharacterAPI
from kankamanager.kankaclient.conversations import ConversationAPI
from kankamanager.kankaclient.dice import DiceRollAPI
from kankamanager.kankaclient.events import EventAPI
from kankamanager.kankaclient.families import FamilyAPI
from kankamanager.kankaclient.items import ItemAPI
from kankamanager.kankaclient.journals import JournalAPI
from kankamanager.kankaclient.locations import LocationAPI
from kankamanager.kankaclient.maps import MapAPI
from kankamanager.kankaclient.organizations import OrganizationAPI
from kankamanager.kankaclient.quests import QuestAPI
from kankamanager.kankaclient.races import RaceAPI
from kankamanager.kankaclient.tags import TagAPI
from kankamanager.kankaclient.timelines import TimelineAPI


class KankaClient(BaseManager):
    """Kanka Client"""

    entities: dict

    def __init__(self, config, verbose: str=False):
        super().__init__(token=config.get('token'), verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign_dir = config.get('campaign_dir')

        self.campaigns = CampaignAPI(token=config.get('token'), campaign=config.get('campaign'), verbose=verbose, throttle=config.get('throttle'))
        self.abilities = AbilityAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.calendars = CalendarAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.characters = CharacterAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.conversations = ConversationAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.dice = DiceRollAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.events = EventAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.families = FamilyAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.items = ItemAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.journals = JournalAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.locations = LocationAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.maps = MapAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.organizations = OrganizationAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.quests = QuestAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.races = RaceAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.tags = TagAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))
        self.timelines = TimelineAPI(token=config.get('token'), campaign=self.campaigns.campaign, verbose=verbose, throttle=config.get('throttle'))

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

    # def smart_substitute(self, entity, entities):
    #     self.tags.get_all()
    #     tags = self.tags.tag_map
    #     self.entities.get(entity)._substitute_tags(tags)
    #     pass


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
        return self.entities.get(entity).create(data)


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
