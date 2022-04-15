"""
Kanka Campaign API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL, GET, PATCH, POST, DELETE, PUT
from kankaclient.base import BaseManager

class CampaignAPI(BaseManager):
    """Kanka Campaign API"""

    GET_ALL = BASE_URL
    GET_SINGLE: str
    GET_MEMBERS: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaigns = None

        self.campaign = self.get_campaign(campaign)
        campaign_id = self.campaign.get('id')

        global GET_SINGLE
        global GET_MEMBERS
        GET_SINGLE = BASE_URL + f'/{campaign_id}'
        GET_MEMBERS = BASE_URL + f'/{campaign_id}/users'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_campaigns(self) -> list:
        """
        Retrieves the available campaigns from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            campaigns: the requested campaigns
        """
        if self.campaigns:
            return self.campaigns

        campaigns = list()
        response = self._request(url=self.GET_ALL, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve campaigns %s', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        campaigns = json.loads(response.text).get('data')
        self.logger.debug(response.json())

        return campaigns


    def get_campaign(self, name_or_id: str or int) -> dict:
        """
        Retrives the desired campaign by name

        Args:
            name_or_id (str or int): the name or id of the campaign

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            campaign: the requested campaign
        """
        campaign = None
        if type(name_or_id) is int:
            campaign = self.get_campaign_by_id(name_or_id)
        else:
            campaigns = self.get_campaigns()
            for _campaign in campaigns:
                if _campaign.get('name') == name_or_id:
                    campaign = _campaign
                    break

        if campaign is None:
            raise self.KankaException(reason=f'Campaign not found: {name_or_id}', code=404, message='Not Found')

        return campaign


    def get_members(self) -> list:
        """
        Retrieves the available members from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            members (list): a list of available members
        """
        members = list()
        response = self._request(url=self.GET_MEMBERS, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve members from campaign: ', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        members = json.loads(response.text).get('data')
        self.logger.debug(response)

        return members
