"""
Kanka Campaign API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL
from kankaclient.base import BaseManager

class CampaignAPI(BaseManager):
    """Kanka Campaign API"""

    GET_ALL = BASE_URL
    GET_SINGLE = BASE_URL+'/campaigns/%s'
    GET_MEMBERS = BASE_URL+'/campaigns/%s/members'

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaigns = None

        self.campaign = self.get_campaign(campaign)

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_campaigns(self) -> list:
        """
        Retrives the projects in the current context

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            campaigns (list): a list of available campaigns
        """
        if self.campaigns:
            return self.campaigns

        campaigns = list()
        response = self._get(url=self.GET_ALL)

        if not response.ok:
            self.logger.error('Failed to retrieve campaigns from host')
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        campaigns = json.loads(response.text)['data']
        self.logger.debug(response)

        return campaigns


    def get_campaign(self, name: str) -> int:
        """
        Retrives the desired campaign by name

        Args:
            name (str): the name of the campaign

        Raises:
            KankaException: Harbor Api Interface Exception

        Returns:
            campaign: the requested campaign id
        """
        campaign = None
        campaigns = self.get_campaigns()
        for campaign in campaigns:
            if campaign['name'] == name:
                campaign = campaign
                break
        
        if campaign is None:
            raise self.KankaException(reason=None, code=404, message=f'Campaign not found: {name}')

        return campaign
