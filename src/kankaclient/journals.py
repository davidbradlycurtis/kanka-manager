"""
Kanka Journal API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class JournalAPI(BaseManager):
    """Kanka Journal API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False, throttle=False):
        super().__init__(token=token, verbose=verbose, throttle=throttle)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.id
        self.journals = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/journals'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/journals/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available journals from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journals: the requested journals
        """
        if self.journals:
            return self.journals

        journals = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve journals from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        journals = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journals


    def get(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired journal by name

        Args:
            name_or_id (str or int): the name or id of the journal

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the requested journal
        """
        journal = None
        if type(name_or_id) is int:
            journal = self.get_journal_by_id(name_or_id)
        else:
            journals = self.get()
            for _journal in journals:
                if _journal.get('name') == name_or_id:
                    journal = _journal
                    break

        if journal is None:
            raise self.KankaException(reason=f'Journal not found: {name_or_id}', code=404, message='Not Found')

        return journal


    def get_journal_by_id(self, id: int) -> dict:
        """
        Retrieves the requested journal from Kanka

        Args:
            id (int): the journal id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the requested journal
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve journal %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        journal = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journal


    def create(self, journal: dict) -> dict:
        """
        Creates the provided journal in Kanka

        Args:
            journal (dict): the journal to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the created journal
        """
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=POST, data=json.dumps(journal))

        if not response.ok:
            self.logger.error('Failed to create journal %s in campaign %s', journal.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        journal = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journal


    def update(self, journal: dict) -> dict:
        """
        Updates the provided journal in Kanka

        Args:
            journal (dict): the journal to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the updated journal
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % journal.get('id'), request=PUT, data=json.dumps(journal))

        if not response.ok:
            self.logger.error('Failed to update journal %s in campaign %s', journal.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        journal = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journal


    def delete(self, id: int) -> bool:
        """
        Deletes the provided journal in Kanka

        Args:
            id (int): the journal id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the journal is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE % id, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete journal %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response)
        return True
