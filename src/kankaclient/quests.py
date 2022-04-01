"""
Kanka Quest API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class QuestAPI(BaseManager):
    """Kanka Quest API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.quests = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/quests'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/quests/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_quests(self) -> list:
        """
        Retrieves the available quests from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quests: the requested quests
        """
        if self.quests:
            return self.quests

        quests = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve quests from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        quests = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quests


    def get_quest(self, name: str) -> dict:
        """
        Retrives the desired quest by name

        Args:
            name (str): the name of the quest

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the requested quest
        """
        quest = None
        quests = self.get_quests()
        for quest in quests:
            if quest.get('name') == name:
                quest = quest
                break

        if quest is None:
            raise self.KankaException(reason=None, code=404, message=f'quest not found: {name}')

        return quest


    def get_quest_by_id(self, id: int) -> dict:
        """
        Retrieves the requested quest from Kanka

        Args:
            id (int): the quest id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the requested quest
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve quest %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        quest = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quest


    def create_quest(self, quest: dict) -> dict:
        """
        Creates the provided quest in Kanka

        Args:
            quest (dict): the quest to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the created quest
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=quest)

        if not response.ok:
            self.logger.error('Failed to create quest %s in campaign %s', quest.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        quest = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quest


    def update_quest(self, quest: dict) -> dict:
        """
        Updates the provided quest in Kanka

        Args:
            quest (dict): the quest to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the updated quest
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=quest)

        if not response.ok:
            self.logger.error('Failed to update quest %s in campaign %s', quest.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        quest = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quest


    def delete_quest(self, id: int) -> bool:
        """
        Deletes the provided quest in Kanka

        Args:
            id (int): the quest id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the quest is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete quest %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
