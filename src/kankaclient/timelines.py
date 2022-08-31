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

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.timelines = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/timelines'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/timelines/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
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
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        timelines = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timelines


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired timeline by name

        Args:
            name_or_id (str or int): the name or id of the timeline

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the requested timeline
        """
        timeline = None
        if type(name_or_id) is int:
            timeline = self.get_timeline_by_id(name_or_id)
        else:
            timelines = self.get()
            for _timeline in timelines:
                if _timeline.get('name') == name_or_id:
                    timeline = _timeline
                    break

        if timeline is None:
            raise self.KankaException(reason=f'Timeline not found: {name_or_id}', code=404, message='Not Found')

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
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve timeline %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        timeline = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timeline


    def create(self, timeline: dict) -> dict:
        """
        Creates the provided timeline in Kanka

        Args:
            timeline (dict): the timeline to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the created timeline
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(timeline))

        if not response.ok:
            self.logger.error('Failed to create timeline %s in campaign %s', timeline.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        timeline = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timeline


    def update(self, timeline: dict) -> dict:
        """
        Updates the provided timeline in Kanka

        Args:
            timeline (dict): the timeline to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            timeline: the updated timeline
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % timeline.get('id'), request=PUT, data=json.dumps(timeline))

        if not response.ok:
            self.logger.error('Failed to update timeline %s in campaign %s', timeline.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        timeline = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return timeline


    def delete(self, id: int) -> bool:
        """
        Deletes the provided timeline in Kanka

        Args:
            id (int): the timeline id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the timeline is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete timeline %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
