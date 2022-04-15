"""
Kanka Tag API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class TagAPI(BaseManager):
    """Kanka Tag API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.tags = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/tags'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/tags/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_tags(self) -> list:
        """
        Retrieves the available tags from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            tags: the requested tags
        """
        if self.tags:
            return self.tags

        tags = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve tags from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        tags = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return tags


    def get_tag(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired tag by name

        Args:
            name_or_id (str or int): the name or id of the tag

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            tag: the requested tag
        """
        tag = None
        if type(name_or_id) is int:
            tag = self.get_tag_by_id(name_or_id)
        else:
            tags = self.get_tags()
            for _tag in tags:
                if _tag.get('name') == name_or_id:
                    tag = _tag
                    break

        if tag is None:
            raise self.KankaException(reason=f'Tag not found: {name_or_id}', code=404, message='Not Found')

        return tag


    def get_tag_by_id(self, id: int) -> dict:
        """
        Retrieves the requested tag from Kanka

        Args:
            id (int): the tag id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            tag: the requested tag
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve tag %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        tag = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return tag


    def create_tag(self, tag: dict) -> dict:
        """
        Creates the provided tag in Kanka

        Args:
            tag (dict): the tag to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            tag: the created tag
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(tag))

        if not response.ok:
            self.logger.error('Failed to create tag %s in campaign %s', tag.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        tag = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return tag


    def update_tag(self, tag: dict) -> dict:
        """
        Updates the provided tag in Kanka

        Args:
            tag (dict): the tag to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            tag: the updated tag
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % tag.get('id'), request=PUT, data=json.dumps(tag))

        if not response.ok:
            self.logger.error('Failed to update tag %s in campaign %s', tag.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        tag = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return tag


    def delete_tag(self, id: int) -> bool:
        """
        Deletes the provided tag in Kanka

        Args:
            id (int): the tag id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the tag is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete tag %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
