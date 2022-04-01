"""
Kanka Timeline API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class TimelineAPI(BaseManager):
    """Kanka Timeline API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.timelines = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/timelines'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/timelines/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_timelines(self) -> list:
        """
        Retrieves the available timelines from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timelines: the requested timelines
        """
        if self.timelines:
            return self.timelines

        timelines = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve timelines from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        timelines = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timelines


    def get_timeline(self, name: str) -> dict:
        """
        Retrives the desired timeline by name

        Args:
            name (str): the name of the timeline

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the requested timeline
        """
        timeline = None
        timelines = self.get_timelines()
        for timeline in timelines:
            if timeline.get('name') == name:
                timeline = timeline
                break

        if timeline is None:
            raise self.KankaException(reason=None, code=404, message=f'timeline not found: {name}')

        return timeline


    def get_timeline_by_id(self, id: int) -> dict:
        """
        Retrieves the requested timeline from Kanka

        Args:
            id (int): the timeline id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the requested timeline
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve timeline %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        timeline = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timeline


    def create_timeline(self, timeline: dict) -> dict:
        """
        Creates the provided timeline in Kanka

        Args:
            timeline (dict): the timeline to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the created timeline
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=timeline)

        if not response.ok:
            self.logger.error('Failed to create timeline %s in campaign %s', timeline.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        timeline = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timeline


    def update_timeline(self, timeline: dict) -> dict:
        """
        Updates the provided timeline in Kanka

        Args:
            timeline (dict): the timeline to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the updated timeline
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=timeline)

        if not response.ok:
            self.logger.error('Failed to update timeline %s in campaign %s', timeline.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        timeline = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timeline


    def delete_timeline(self, id: int) -> bool:
        """
        Deletes the provided timeline in Kanka

        Args:
            id (int): the timeline id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the timeline is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete timeline %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
