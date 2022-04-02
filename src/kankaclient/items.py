"""
Kanka Item API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class ItemAPI(BaseManager):
    """Kanka Item API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.items = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/items'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/items/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_items(self) -> list:
        """
        Retrieves the available items from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            items: the requested items
        """
        if self.items:
            return self.items

        items = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve items from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        items = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return items


    def get_item(self, name: str) -> dict:
        """
        Retrives the desired item by name

        Args:
            name (str): the name of the item

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            item: the requested item
        """
        item = None
        items = self.get_items()
        for _item in items:
            if _item.get('name') == name:
                item = _item
                break

        if item is None:
            raise self.KankaException(reason=None, code=404, message=f'item not found: {name}')

        return item


    def get_item_by_id(self, id: int) -> dict:
        """
        Retrieves the requested item from Kanka

        Args:
            id (int): the item id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            item: the requested item
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve item %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        item = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return item


    def create_item(self, item: dict) -> dict:
        """
        Creates the provided item in Kanka

        Args:
            item (dict): the item to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            item: the created item
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=item)

        if not response.ok:
            self.logger.error('Failed to create item %s in campaign %s', item.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        item = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return item


    def update_item(self, item: dict) -> dict:
        """
        Updates the provided item in Kanka

        Args:
            item (dict): the item to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            item: the updated item
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=item)

        if not response.ok:
            self.logger.error('Failed to update item %s in campaign %s', item.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        item = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return item


    def delete_item(self, id: int) -> bool:
        """
        Deletes the provided item in Kanka

        Args:
            id (int): the item id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the item is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete item %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
