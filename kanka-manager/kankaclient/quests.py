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
        self.campaign_id = campaign.id
        self.quests = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/quests'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/quests/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
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
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        quests = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quests


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired quest by name

        Args:
            name_or_id (str or int): the name or id of the quest

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the requested quest
        """
        quest = None
        if type(name_or_id) is int:
            quest = self.get_quest_by_id(name_or_id)
        else:
            quests = self.get()
            for _quest in quests:
                if _quest.get('name') == name_or_id:
                    quest = _quest
                    break

        if quest is None:
            raise self.KankaException(reason=f'Quest not found: {name_or_id}', code=404, message='Not Found')

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
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve quest %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        quest = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quest


    def create(self, quest: dict) -> dict:
        """
        Creates the provided quest in Kanka

        Args:
            quest (dict): the quest to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the created quest
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(quest))

        if not response.ok:
            self.logger.error('Failed to create quest %s in campaign %s', quest.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        quest = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quest


    def update(self, quest: dict) -> dict:
        """
        Updates the provided quest in Kanka

        Args:
            quest (dict): the quest to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            quest: the updated quest
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % quest.get('id'), request=PUT, data=json.dumps(quest))

        if not response.ok:
            self.logger.error('Failed to update quest %s in campaign %s', quest.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        quest = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return quest


    def delete(self, id: int) -> bool:
        """
        Deletes the provided quest in Kanka

        Args:
            id (int): the quest id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the quest is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete quest %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
