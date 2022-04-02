"""
Kanka Calendar API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class CalendarAPI(BaseManager):
    """Kanka Calendar API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.calendars = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/calendars'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/calendars/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_calendars(self) -> list:
        """
        Retrieves the available calendars from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendars: the requested calendars
        """
        if self.calendars:
            return self.calendars

        calendars = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve calendars from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        calendars = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return calendars


    def get_calendar(self, name: str) -> dict:
        """
        Retrives the desired calendar by name

        Args:
            name (str): the name of the calendar

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the requested calendar
        """
        calendar = None
        calendars = self.get_calendars()
        for _calendar in calendars:
            if _calendar.get('name') == name:
                calendar = _calendar
                break

        if calendar is None:
            raise self.KankaException(reason=None, code=404, message=f'calendar not found: {name}')

        return calendar


    def get_calendar_by_id(self, id: int) -> dict:
        """
        Retrieves the requested calendar from Kanka

        Args:
            id (int): the calendar id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the requested calendar
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve calendar %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        calendar = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return calendar


    def create_calendar(self, calendar: dict) -> dict:
        """
        Creates the provided calendar in Kanka

        Args:
            calendar (dict): the calendar to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the created calendar
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=calendar)

        if not response.ok:
            self.logger.error('Failed to create calendar %s in campaign %s', calendar.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        calendar = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return calendar


    def update_calendar(self, calendar: dict) -> dict:
        """
        Updates the provided calendar in Kanka

        Args:
            calendar (dict): the calendar to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the updated calendar
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=calendar)

        if not response.ok:
            self.logger.error('Failed to update calendar %s in campaign %s', calendar.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        calendar = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return calendar


    def delete_calendar(self, id: int) -> bool:
        """
        Deletes the provided calendar in Kanka

        Args:
            id (int): the calendar id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the calendar is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete calendar %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
