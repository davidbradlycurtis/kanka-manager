"""
Kanka Event API

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
class Event(Entity):

    entry: Optional[Any]
    image: Optional[Any]
    image_full: Optional[Any]
    image_thumb: Optional[Any]
    has_custom_image: bool
    entity_id: int
    date: Optional[Any]

class EventAPI(BaseManager):
    """Kanka Event API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.events = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/events'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/events/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available events from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            events: the requested events
        """
        if self.events:
            return self.events

        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve events from campaign %s",
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        self.logger.debug(response.json())
        if response.text:
            self.events = [
                from_dict(data_class=Event, data=event) for event in json.loads(response.text).get("data")
            ]

        return self.events


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired event by name

        Args:
            name_or_id (str or int): the name or id of the event

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the requested event
        """
        event = None
        if isinstance(name_or_id, int):
            event = self.get_event_by_id(name_or_id)
        else:
            events = self.get_all()
            for _event in events:
                if _event.name == name_or_id:
                    event = _event
                    break

        if event is None:
            raise self.raise_exception(
                reason=f"event not found: {name_or_id}",
                code=404,
                message="Not Found",
            )

        return event


    def get_event_by_id(self, id: int) -> Event:
        """
        Retrieves the requested event from Kanka

        Args:
            id (int): the event id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the requested event
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve event %s from campaign %s",
                id,
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        event = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Event, data=event)


    def create(self, event: dict) -> Event:
        """
        Creates the provided event in Kanka

        Args:
            event (dict): the event to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the created event
        """
        response = self._request(
            url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(event)
        )

        if not response.ok:
            self.logger.error(
                "Failed to create event %s in campaign %s",
                event.get("name", "None"),
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        event = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Event, data=event)


    def update(self, event: dict) -> dict:
        """
        Updates the provided event in Kanka

        Args:
            event (dict): the event to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the updated event
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % event.get('id'), request=PUT, data=json.dumps(event))

        if not response.ok:
            self.logger.error('Failed to update event %s in campaign %s', event.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        event = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return event


    def delete(self, id: int) -> bool:
        """
        Deletes the provided event in Kanka

        Args:
            id (int): the event id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the event is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete event %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
