"""
Kanka Map API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class MapAPI(BaseManager):
    """Kanka Map API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.maps = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/maps'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/maps/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available maps from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            maps: the requested maps
        """
        if self.maps:
            return self.maps

        maps = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve maps from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        maps = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return maps


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired map by name

        Args:
            name_or_id (str or int): the name or id of the map

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            map: the requested map
        """
        map = None
        if type(name_or_id) is int:
            map = self.get_map_by_id(name_or_id)
        else:
            maps = self.get()
            for _map in maps:
                if _map.get('name') == name_or_id:
                    map = _map
                    break

        if map is None:
            raise self.KankaException(reason=f'Map not found: {name_or_id}', code=404, message='Not Found')

        return map


    def get_map_by_id(self, id: int) -> dict:
        """
        Retrieves the requested map from Kanka

        Args:
            id (int): the map id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            map: the requested map
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve map %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        map = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return map


    def create(self, map: dict) -> dict:
        """
        Creates the provided map in Kanka

        Args:
            map (dict): the map to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            map: the created map
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(map))

        if not response.ok:
            self.logger.error('Failed to create map %s in campaign %s', map.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        map = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return map


    def update(self, map: dict) -> dict:
        """
        Updates the provided map in Kanka

        Args:
            map (dict): the map to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            map: the updated map
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % map.get('id'), request=PUT, data=json.dumps(map))

        if not response.ok:
            self.logger.error('Failed to update map %s in campaign %s', map.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        map = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return map


    def delete(self, id: int) -> bool:
        """
        Deletes the provided map in Kanka

        Args:
            id (int): the map id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the map is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete map %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
