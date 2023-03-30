"""
Kanka Family API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankamanager.kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankamanager.kankaclient.base import BaseManager

class FamilyAPI(BaseManager):
    """Kanka Family API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.families = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/families'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/families/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available families from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            families: the requested families
        """
        if self.families:
            return self.families

        families = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve families from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        families = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return families


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired family by name

        Args:
            name_or_id (str or int): the name or id of the family

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            family: the requested family
        """
        family = None
        if type(name_or_id) is int:
            family = self.get_family_by_id(name_or_id)
        else:
            families = self.get()
            for _family in families:
                if _family.get('name') == name_or_id:
                    family = _family
                    break

        if family is None:
            raise self.KankaException(reason=f'Family not found: {name_or_id}', code=404, message='Not Found')

        return family


    def get_family_by_id(self, id: int) -> dict:
        """
        Retrieves the requested family from Kanka

        Args:
            id (int): the family id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            family: the requested family
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve family %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        family = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return family


    def create(self, family: dict) -> dict:
        """
        Creates the provided family in Kanka

        Args:
            family (dict): the family to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            family: the created family
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(family))

        if not response.ok:
            self.logger.error('Failed to create family %s in campaign %s', family.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        family = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return family


    def update(self, family: dict) -> dict:
        """
        Updates the provided family in Kanka

        Args:
            family (dict): the family to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            family: the updated family
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % family.get('id'), request=PUT, data=json.dumps(family))

        if not response.ok:
            self.logger.error('Failed to update family %s in campaign %s', family.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        family = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return family


    def delete(self, id: int) -> bool:
        """
        Deletes the provided family in Kanka

        Args:
            id (int): the family id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the family is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete family %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
