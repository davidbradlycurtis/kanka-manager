"""
Kanka Location API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json
from dataclasses import dataclass
from typing import Any, Optional

from dacite import from_dict

from kankamanager.kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankamanager.kankaclient.base import BaseManager, Entity


@dataclass
class Location(Entity):

    entry: Optional[Any]
    image: Optional[Any]
    image_full: Optional[Any]
    image_thumb: Optional[Any]
    has_custom_image: bool
    is_template: bool
    entity_id: int
    location_id: Optional[Any]
    tags: list
    parent_location_id: Optional[int]
    map: Optional[Any]
    is_map_private: Optional[int]


class LocationAPI(BaseManager):
    """Kanka Location API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.locations = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/locations'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/locations/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available locations from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            locations: the requested locations
        """
        if self.locations:
            return self.locations

        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve locations from campaign %s",
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        self.logger.debug(response.json())
        if response.text:
            self.locations = [
                from_dict(data_class=Location, data=location) for location in json.loads(response.text).get("data")
            ]

        return self.locations


    def get(self, name_or_id: str or int) -> dict:
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
        if isinstance(name_or_id, int):
            location = self.get_location_by_id(name_or_id)
        else:
            locations = self.get_all()
            for _location in locations:
                if _location.name == name_or_id:
                    location = _location
                    break

        if location is None:
            raise self.raise_exception(
                reason=f"Location not found: {name_or_id}",
                code=404,
                message="Not Found",
            )

        return location



    def get_location_by_id(self, id: int) -> Location:
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
            self.logger.error(
                "Failed to retrieve location %s from campaign %s",
                id,
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        location = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Location, data=location)


    def create(self, location: dict) -> dict:
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


    def update(self, location: dict) -> dict:
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


    def delete(self, id: int) -> bool:
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
