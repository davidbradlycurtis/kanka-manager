"""
Kanka DiceRoll API

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
class DiceRoll(Entity):

    entry: Optional[Any]
    image: Optional[Any]
    image_full: Optional[Any]
    image_thumb: Optional[Any]
    is_private: bool
    entity_id: int
    character_id: Optional[int]
    system: Optional[str]
    rolls: Optional[list]

class DiceRollAPI(BaseManager):
    """Kanka DiceRoll API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.dice_rolls = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/dice_rolls'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/dice_rolls/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available dice_rolls from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            dice_rolls: the requested dice_rolls
        """
        if self.dice_rolls:
            return self.dice_rolls

        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve dice_rolls from campaign %s",
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        self.logger.debug(response.json())
        if response.text:
            self.dice_rolls = [
                from_dict(data_class=DiceRoll, data=dice_roll) for dice_roll in json.loads(response.text).get("data")
            ]

        return self.dice_rolls


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired dice_roll by name

        Args:
            name_or_id (str or int): the name or id of the dice_roll

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            dice_roll: the requested dice_roll
        """
        dice_roll = None
        if isinstance(name_or_id, int):
            dice_roll = self.get_dice_roll_by_id(name_or_id)
        else:
            dice_rolls = self.get_all()
            for _dice_roll in dice_rolls:
                if _dice_roll.name == name_or_id:
                    dice_roll = _dice_roll
                    break

        if dice_roll is None:
            raise self.raise_exception(
                reason=f"Dice roll not found: {name_or_id}",
                code=404,
                message="Not Found",
            )

        return dice_roll


    def get_dice_roll_by_id(self, id: int) -> DiceRoll:
        """
        Retrieves the requested dice roll from Kanka

        Args:
            id (int): the dice_roll id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            dice_roll: the requested dice_roll
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve dice_roll %s from campaign %s",
                id,
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        dice_roll = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=DiceRoll, data=dice_roll)


    def create(self, dice_roll: dict) -> dict:
        """
        Creates the provided dice_roll in Kanka

        Args:
            dice_roll (dict): the dice_roll to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            dice_roll: the created dice_roll
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(dice_roll))

        if not response.ok:
            self.logger.error('Failed to create dice_roll %s in campaign %s', dice_roll.get('name', None), self.campaign.name)
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        dice_roll = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return from_dict(data_class=DiceRoll, data=dice_roll)


    def update(self, dice_roll: dict) -> dict:
        """
        Updates the provided dice_roll in Kanka

        Args:
            dice_roll (dict): the dice_roll to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            dice_roll: the updated dice_roll
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % dice_roll.get('id'), request=PUT, data=json.dumps(dice_roll))

        if not response.ok:
            self.logger.error('Failed to update dice_roll %s in campaign %s', dice_roll.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        dice_roll = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return dice_roll


    def delete(self, id: int) -> bool:
        """
        Deletes the provided dice_roll in Kanka

        Args:
            id (int): the dice_roll id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the dice_roll is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete dice_roll %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
