"""
Kanka Ability API

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
class Ability(Entity):

    entry: Optional[Any]
    image: Optional[Any]
    image_full: Optional[Any]
    image_thumb: Optional[Any]
    has_custom_image: bool
    tags: list
    charges: Optional[Any]
    entity_id: int
    abilities: list


class AbilityAPI(BaseManager):
    """Kanka Ability API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.abilities = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/abilities'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/abilities/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available abilities from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            abilities: the requested abilities
        """
        if self.abilities:
            return self.abilities

        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve abilities from campaign %s",
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        self.logger.debug(response.json())
        if response.text:
            self.abilities = [
                from_dict(data_class=Ability, data=ability) for ability in json.loads(response.text).get("data")
            ]

        return self.abilities


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired ability by name

        Args:
            name_or_id (str or int): the name or id of the ability

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            ability: the requested ability
        """
        ability = None
        if isinstance(name_or_id, int):
            ability = self.get_ability_by_id(name_or_id)
        else:
            abilities = self.get_all()
            for _ability in abilities:
                if _ability.name == name_or_id:
                    ability = _ability
                    break

        if ability is None:
            raise self.raise_exception(
                reason=f"Ability not found: {name_or_id}",
                code=404,
                message="Not Found",
            )

        return ability


    def get_ability_by_id(self, id: int) -> Ability:
        """
        Retrieves the requested ability from Kanka

        Args:
            id (int): the ability id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            ability: the requested ability
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve ability %s from campaign %s",
                id,
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        ability = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Ability, data=ability)


    def create(self, ability: dict) -> Ability:
        """
        Creates the provided ability in Kanka

        Args:
            ability (dict): the ability to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            ability: the created ability
        """
        response = self._request(
            url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(ability)
        )

        if not response.ok:
            self.logger.error(
                "Failed to create ability %s in campaign %s",
                ability.get("name", "None"),
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        ability = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Ability, data=ability)


    def update(self, ability: dict) -> dict:
        """
        Updates the provided ability in Kanka

        Args:
            ability (dict): the ability to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            ability: the updated ability
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % ability.get('id'), request=PUT, data=json.dumps(ability))

        if not response.ok:
            self.logger.error('Failed to update ability %s in campaign %s', ability.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        ability = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return ability


    def delete(self, id: int) -> bool:
        """
        Deletes the provided ability in Kanka

        Args:
            id (int): the ability id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the ability is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete ability %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
