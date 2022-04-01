"""
Kanka Note API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class NoteAPI(BaseManager):
    """Kanka Note API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.notes = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/notes'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/notes/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_notes(self) -> list:
        """
        Retrieves the available notes from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            notes: the requested notes
        """
        if self.notes:
            return self.notes

        notes = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve notes from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        notes = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return notes


    def get_note(self, name: str) -> dict:
        """
        Retrives the desired note by name

        Args:
            name (str): the name of the note

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            note: the requested note
        """
        note = None
        notes = self.get_notes()
        for note in notes:
            if note.get('name') == name:
                note = note
                break

        if note is None:
            raise self.KankaException(reason=None, code=404, message=f'note not found: {name}')

        return note


    def get_note_by_id(self, id: int) -> dict:
        """
        Retrieves the requested note from Kanka

        Args:
            id (int): the note id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            note: the requested note
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve note %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        note = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return note


    def create_note(self, note: dict) -> dict:
        """
        Creates the provided note in Kanka

        Args:
            note (dict): the note to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            note: the created note
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=note)

        if not response.ok:
            self.logger.error('Failed to create note %s in campaign %s', note.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        note = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return note


    def update_note(self, note: dict) -> dict:
        """
        Updates the provided note in Kanka

        Args:
            note (dict): the note to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            note: the updated note
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=note)

        if not response.ok:
            self.logger.error('Failed to update note %s in campaign %s', note.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        note = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return note


    def delete_note(self, id: int) -> bool:
        """
        Deletes the provided note in Kanka

        Args:
            id (int): the note id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the note is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete note %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
