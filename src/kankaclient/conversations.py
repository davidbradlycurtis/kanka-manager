"""
Kanka Conversation API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class ConversationAPI(BaseManager):
    """Kanka Conversation API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.conversations = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/conversations'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/conversations/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_conversations(self) -> list:
        """
        Retrieves the available conversations from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            conversations: the requested conversations
        """
        if self.conversations:
            return self.conversations

        conversations = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve conversations from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        conversations = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return conversations


    def get_conversation(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired conversation by name

        Args:
            name_or_id (str or int): the name or id of the conversation

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            conversation: the requested conversation
        """
        conversation = None
        if type(name_or_id) is int:
            conversation = self.get_conversation_by_id(name_or_id)
        else:
            conversations = self.get_conversations()
            for _conversation in conversations:
                if _conversation.get('name') == name_or_id:
                    conversation = _conversation
                    break

        if conversation is None:
            raise self.KankaException(reason=None, code=404, message=f'Conversation not found: {name_or_id}')

        return conversation


    def get_conversation_by_id(self, id: int) -> dict:
        """
        Retrieves the requested conversation from Kanka

        Args:
            id (int): the conversation id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            conversation: the requested conversation
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve conversation %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        conversation = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return conversation


    def create_conversation(self, conversation: dict) -> dict:
        """
        Creates the provided conversation in Kanka

        Args:
            conversation (dict): the conversation to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            conversation: the created conversation
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(conversation))

        if not response.ok:
            self.logger.error('Failed to create conversation %s in campaign %s', conversation.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        conversation = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return conversation


    def update_conversation(self, conversation: dict) -> dict:
        """
        Updates the provided conversation in Kanka

        Args:
            conversation (dict): the conversation to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            conversation: the updated conversation
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % conversation.get('id'), request=PUT, data=json.dumps(conversation))

        if not response.ok:
            self.logger.error('Failed to update conversation %s in campaign %s', conversation.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        conversation = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return conversation


    def delete_conversation(self, id: int) -> bool:
        """
        Deletes the provided conversation in Kanka

        Args:
            id (int): the conversation id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the conversation is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete conversation %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
