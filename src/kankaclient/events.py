"""
Kanka Event API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class EventAPI(BaseManager):
    """Kanka Event API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.events = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/events'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/events/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_events(self) -> list:
        """
        Retrieves the available events from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            events: the requested events
        """
        if self.events:
            return self.events

        events = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve events from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        events = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return events


    def get_event(self, name: str) -> dict:
        """
        Retrives the desired event by name

        Args:
            name (str): the name of the event

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the requested event
        """
        event = None
        events = self.get_events()
        for event in events:
            if event.get('name') == name:
                event = event
                break

        if event is None:
            raise self.KankaException(reason=None, code=404, message=f'event not found: {name}')

        return event


    def get_event_by_id(self, id: int) -> dict:
        """
        Retrieves the requested event from Kanka

        Args:
            id (int): the event id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the requested event
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve event %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        event = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return event


    def create_event(self, event: dict) -> dict:
        """
        Creates the provided event in Kanka

        Args:
            event (dict): the event to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the created event
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=event)

        if not response.ok:
            self.logger.error('Failed to create event %s in campaign %s', event.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        event = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return event


    def update_event(self, event: dict) -> dict:
        """
        Updates the provided event in Kanka

        Args:
            event (dict): the event to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            event: the updated event
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=event)

        if not response.ok:
            self.logger.error('Failed to update event %s in campaign %s', event.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        event = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return event


    def delete_event(self, id: int) -> bool:
        """
        Deletes the provided event in Kanka

        Args:
            id (int): the event id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the event is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete event %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
