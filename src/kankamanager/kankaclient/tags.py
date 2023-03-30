"""
Kanka Tag API

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
class Tag(Entity):

    entry: Optional[Any]
    image: Optional[Any]
    image_full: Optional[Any]
    image_thumb: Optional[Any]
    has_custom_image: bool
    entity_id: int
    colour: Optional[str]
    tag_id: Optional[Any]
    entities: list
    is_auto_applied: bool


class TagAPI(BaseManager):
    """Kanka Tag API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.tags = list()
        self.tag_map = dict()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/tags'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/tags/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available tags from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            tags: the requested tags
        """
        if self.tags:
            return self.tags

        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve tags from campaign %s",
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        self.logger.debug(response.json())
        if response.text:
            self.tags = [
                from_dict(data_class=Tag, data=tag) for tag in json.loads(response.text).get("data")
            ]
            for tag in self.tags:
                self.tag_map.update({tag.id: tag.name})

        return self.tags


    def get(self, name_or_id: str or int) -> dict:
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
        if isinstance(name_or_id, int):
            tag = self.get_tag_by_id(name_or_id)
        else:
            tags = self.get_all()
            for _tag in tags:
                if _tag.name == name_or_id:
                    tag = _tag
                    break

        if tag is None:
            raise self.raise_exception(
                reason=f"Tag not found: {name_or_id}",
                code=404,
                message="Not Found",
            )

        return tag


    def get_tag_by_id(self, id: int) -> Tag:
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
            self.logger.error(
                "Failed to retrieve tag %s from campaign %s",
                id,
                self.campaign.name,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        tag = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Tag, data=tag)


    def create(self, tag: dict) -> dict:
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


    def update(self, tag: dict) -> dict:
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


    def delete(self, id: int) -> bool:
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
