"""
Kanka Location API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class LocationAPI(BaseManager):
    """Kanka Location API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.locations = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/locations'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/locations/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_locations(self) -> list:
        """
        Retrieves the available locations from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            locations: the requested locations
        """
        if self.locations:
            return self.locations

        locations = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve locations from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        locations = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return locations


    def get_location(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired location by name

        Args:
            name_or_id (str or int): the name or id of the location

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            location: the requested location
        """
        location = None
        if type(name_or_id) is int:
            location = self.get_location_by_id(name_or_id)
        else:
            locations = self.get_locations()
            for _location in locations:
                if _location.get('name') == name_or_id:
                    location = _location
                    break

        if location is None:
            raise self.KankaException(reason=f'Location not found: {name_or_id}', code=404, message='Not Found')

        return location


    def get_location_by_id(self, id: int) -> dict:
        """
        Retrieves the requested location from Kanka

        Args:
            id (int): the location id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            location: the requested location
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve location %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        location = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return location


    def create_location(self, location: dict) -> dict:
        """
        Creates the provided location in Kanka

        Args:
            location (dict): the location to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            location: the created location
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(location))

        if not response.ok:
            self.logger.error('Failed to create location %s in campaign %s', location.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        location = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return location


    def update_location(self, location: dict) -> dict:
        """
        Updates the provided location in Kanka

        Args:
            location (dict): the location to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            location: the updated location
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % location.get('id'), request=PUT, data=json.dumps(location))

        if not response.ok:
            self.logger.error('Failed to update location %s in campaign %s', location.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        location = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return location


    def delete_location(self, id: int) -> bool:
        """
        Deletes the provided location in Kanka

        Args:
            id (int): the location id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the location is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete location %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
