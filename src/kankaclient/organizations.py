"""
Kanka Organization API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, POST, DELETE, PUT
from kankaclient.base import BaseManager

class OrganizationAPI(BaseManager):
    """Kanka Organization API"""

    GET_ALL_CREATE_SINGLE: str
    GET_UPDATE_DELETE_SINGLE: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.organizations = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/organizations'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/organizations/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_organizations(self) -> list:
        """
        Retrieves the available organizations from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            organizations: the requested organizations
        """
        if self.organizations:
            return self.organizations

        organizations = list()
        response = self._request(url=GET_ALL_CREATE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve organizations from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        organizations = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return organizations


    def get_organization(self, name: str) -> dict:
        """
        Retrives the desired organization by name

        Args:
            name (str): the name of the organization

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            organization: the requested organization
        """
        organization = None
        organizations = self.get_organizations()
        for organization in organizations:
            if organization.get('name') == name:
                organization = organization
                break

        if organization is None:
            raise self.KankaException(reason=None, code=404, message=f'organization not found: {name}')

        return organization


    def get_organization_by_id(self, id: int) -> dict:
        """
        Retrieves the requested organization from Kanka

        Args:
            id (int): the organization id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            organization: the requested organization
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve organization %s from campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        organization = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return organization


    def create_organization(self, organization: dict) -> dict:
        """
        Creates the provided organization in Kanka

        Args:
            organization (dict): the organization to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            organization: the created organization
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=POST, body=organization)

        if not response.ok:
            self.logger.error('Failed to create organization %s in campaign %s', organization.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        organization = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return organization


    def update_organization(self, organization: dict) -> dict:
        """
        Updates the provided organization in Kanka

        Args:
            organization (dict): the organization to create

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            organization: the updated organization
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=PUT, body=organization)

        if not response.ok:
            self.logger.error('Failed to update organization %s in campaign %s', organization.get('name', 'None'), self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        organization = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return organization


    def delete_organization(self, id: int) -> bool:
        """
        Deletes the provided organization in Kanka

        Args:
            id (int): the organization id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            bool: whether the organization is successfully deleted
        """
        response = self._request(url=GET_UPDATE_DELETE_SINGLE, request=DELETE)

        if not response.ok:
            self.logger.error('Failed to delete organization %s in campaign %s', id, self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        self.logger.debug(response.json())
        return True
