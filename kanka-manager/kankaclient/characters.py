"""
Kanka Character API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class CharacterAPI(BaseManager):
    """Kanka Character API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.characters = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/characters'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/characters/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available characters from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            characters: the requested characters
        """
        if self.characters:
            return self.characters

        characters = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve characters from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        characters = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return characters


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired character by name

        Args:
            name_or_id (str or int): the name or id of the character

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            character: the requested character
        """
        character = None
        if type(name_or_id) is int:
            character = self.get_character_by_id(name_or_id)
        else:
            characters = self.get_all()
            for _character in characters:
                if _character.get('name') == name_or_id:
                    character = _character
                    break

        if character is None:
            raise self.KankaException(reason=f'Character not found: {name_or_id}', code=404, message='Not Found')

        return character


    def get_character_by_id(self, id: int) -> dict:
        """
        Retrieves the requested character from Kanka

        Args:
            id (int): the character id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            character: the requested character
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve character %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        character = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return character


    def create(self, character: dict) -> dict:
        """
        Creates the provided character in Kanka

        Args:
            character (dict): the character to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            character: the created character
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(character))

        if not response.ok:
            self.logger.error('Failed to create character %s in campaign %s', character.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        character = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return character


    def update(self, character: dict) -> dict:
        """
        Updates the provided character in Kanka

        Args:
            character (dict): the character to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            character: the updated character
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % character.get('id'), request=PUT, data=json.dumps(character))

        if not response.ok:
            self.logger.error('Failed to update character %s in campaign %s', character.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        character = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return character


    def delete(self, id: int) -> bool:
        """
        Deletes the provided character in Kanka

        Args:
            id (int): the character id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the character is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete character %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
