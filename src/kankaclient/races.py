"""
Kanka Race API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class RaceAPI(BaseManager):
    """Kanka Race API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.races = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/races'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/races/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_races(self) -> list:
        """
        Retrieves the available races from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            races: the requested races
        """
        if self.races:
            return self.races

        races = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve races from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        races = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return races


    def get_race(self, name: str) -> dict:
        """
        Retrives the desired race by name

        Args:
            name (str): the name of the race

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            race: the requested race
        """
        race = None
        races = self.get_races()
        for _race in races:
            if _race.get('name') == name:
                race = _race
                break

        if race is None:
            raise self.KankaException(reason=None, code=404, message=f'race not found: {name}')

        return race


    def get_race_by_id(self, id: int) -> dict:
        """
        Retrieves the requested race from Kanka

        Args:
            id (int): the race id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            race: the requested race
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve race %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        race = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return race


    def create_race(self, race: dict) -> dict:
        """
        Creates the provided race in Kanka

        Args:
            race (dict): the race to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            race: the created race
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=race)

        if not response.ok:
            self.logger.error('Failed to create race %s in campaign %s', race.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        race = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return race


    def update_race(self, race: dict) -> dict:
        """
        Updates the provided race in Kanka

        Args:
            race (dict): the race to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            race: the updated race
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=race)

        if not response.ok:
            self.logger.error('Failed to update race %s in campaign %s', race.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        race = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return race


    def delete_race(self, id: int) -> bool:
        """
        Deletes the provided race in Kanka

        Args:
            id (int): the race id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the race is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete race %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
