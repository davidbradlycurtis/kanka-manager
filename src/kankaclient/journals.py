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

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.journals = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/journals'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/journals/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_journals(self) -> list:
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
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        journals = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journals


    def get_journal(self, name: str) -> dict:
        """
        Retrives the desired journal by name

        Args:
            name (str): the name of the journal

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the requested journal
        """
        journal = None
        journals = self.get_journals()
        for _journal in journals:
            if _journal.get('name') == name:
                journal = _journal
                break

        if journal is None:
            raise self.KankaException(reason=None, code=404, message=f'journal not found: {name}')

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
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve journal %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        journal = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journal


    def create_journal(self, journal: dict) -> dict:
        """
        Creates the provided journal in Kanka

        Args:
            journal (dict): the journal to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the created journal
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=journal)

        if not response.ok:
            self.logger.error('Failed to create journal %s in campaign %s', journal.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        journal = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journal


    def update_journal(self, journal: dict) -> dict:
        """
        Updates the provided journal in Kanka

        Args:
            journal (dict): the journal to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            journal: the updated journal
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=journal)

        if not response.ok:
            self.logger.error('Failed to update journal %s in campaign %s', journal.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        journal = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return journal


    def delete_journal(self, id: int) -> bool:
        """
        Deletes the provided journal in Kanka

        Args:
            id (int): the journal id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the journal is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete journal %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
