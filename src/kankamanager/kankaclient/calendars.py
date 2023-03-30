"""
Kanka Calendar API

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
class Calendar(Entity):

    entry: Optional[Any]
    image: Optional[Any]
    image_full: Optional[Any]
    image_thumb: Optional[Any]
    has_custom_image: bool
    entity_id: int
    date: Optional[str]
    parameters: Optional[Any]
    months: Optional[list]
    years: Optional[list]
    seasons: Optional[list]
    moons: Optional[list]
    suffix: Optional[str]
    has_leap_year: Optional[bool]
    leap_year_amount: Optional[int]
    leap_year_month: Optional[int]
    leap_year_offset: Optional[int]
    leap_year_start: Optional[int]


class CalendarAPI(BaseManager):
    """Kanka Calendar API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.calendars = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/calendars'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/calendars/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available calendars from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendars: the requested calendars
        """
        if self.calendars:
            return self.calendars

        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve calendars from campaign %s",
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        self.logger.debug(response.json())
        if response.text:
            self.calendars = [
                from_dict(data_class=Calendar, data=calendar) for calendar in json.loads(response.text).get("data")
            ]

        return self.calendars


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired calendar by name

        Args:
            name_or_id (str or int): the name or id of the calendar

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the requested calendar
        """
        calendar = None
        if isinstance(name_or_id, int):
            calendar = self.get_calendar_by_id(name_or_id)
        else:
            calendars = self.get_all()
            for _calendar in calendars:
                if _calendar.name == name_or_id:
                    calendar = _calendar
                    break

        if calendar is None:
            raise self.raise_exception(
                reason=f"calendar not found: {name_or_id}",
                code=404,
                message="Not Found",
            )

        return calendar


    def get_calendar_by_id(self, id: int) -> Calendar:
        """
        Retrieves the requested calendar from Kanka

        Args:
            id (int): the calendar id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the requested calendar
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve calendar %s from campaign %s",
                id,
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        calendar = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Calendar, data=calendar)


    def create(self, calendar: dict) -> Calendar:
        """
        Creates the provided calendar in Kanka

        Args:
            calendar (dict): the calendar to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the created calendar
        """
        response = self._request(
            url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(calendar)
        )

        if not response.ok:
            self.logger.error(
                "Failed to create calendar %s in campaign %s",
                calendar.get("name", "None"),
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        calendar = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Calendar, data=calendar)


    def update(self, calendar: Calendar or dict) -> dict:
        """
        Updates the provided calendar in Kanka

        Args:
            calendar (calendar or dict): the calendar to update

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            calendar: the updated calendar
        """
        if isinstance(calendar, calendar):
            calendar = calendar._asdict()

        response = self._request(
            url=GET_UPDATE_DELETE_SINGLE % calendar.get("id"),
            request=PUT,
            data=json.dumps(calendar),
        )

        if not response.ok:
            self.logger.error(
                "Failed to update calendar %s in campaign %s",
                calendar.get("name", "None"),
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        calendar = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return calendar


    def delete(self, id: int) -> bool:
        """
        Deletes the provided calendar in Kanka

        Args:
            id (int): the calendar id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the calendar is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete calendar %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
