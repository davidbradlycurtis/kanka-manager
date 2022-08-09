"""
Kanka Campaign API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json
from dataclasses import dataclass
from typing import Any, Optional

from dacite import from_dict

from kankaclient.constants import BASE_URL, GET
from kankaclient.base import BaseManager


@dataclass
class Campaign:

    id: int
    name: str
    locale: Optional[Any]
    entry_parsed: str
    image: Optional[Any]
    image_full: Optional[Any]
    visibility: str
    visibility_id: int
    created_at: Any
    updated_at: Optional[Any]
    settings: Optional[Any]
    ui_settings: Optional[Any]
    default_images: Optional[Any]
    follower: int
    boosted: bool
    superboosted: bool
    members: Optional[Any]


class CampaignAPI(BaseManager):
    """Kanka Campaign API"""

    GET_ALL = BASE_URL
    GET_SINGLE: str
    GET_MEMBERS: str

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaigns = list()
        self.members = list()

        self.campaign = self.get(campaign)
        campaign_id = self.campaign.id

        global GET_SINGLE
        global GET_MEMBERS
        GET_SINGLE = BASE_URL + f'/{campaign_id}'
        GET_MEMBERS = BASE_URL + f'/{campaign_id}/users'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_all(self) -> list:
        """
        Retrieves the available campaigns from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            campaigns: the requested campaigns
        """
        if self.campaigns:
            return self.campaigns

        response = self._request(url=self.GET_ALL, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve campaigns')
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.logger.debug(response.json())
        if response.text:
            self.campaigns = [
                from_dict(data_class=Campaign, data=campaign) for campaign in json.loads(response.text).get("data")
            ]

        return self.campaigns


    def get(self, name_or_id: str or int) -> Campaign:
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
            campaigns = self.get_all()
            for _campaign in campaigns:
                if _campaign.name == name_or_id:
                    campaign = _campaign
                    break

        if campaign is None:
            raise self.KankaException(reason=f'Campaign not found: {name_or_id}', code=404, message='Not Found')

        return campaign


    def get_campaign_by_id(self, id: int) -> Campaign:
        """
        Retrieves the requested campaign from Kanka

        Args:
            id (int): the campaign id

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            campaign: the requested campaign
        """
        response = self._request(url=GET_SINGLE % id, request=GET)

        if not response.ok:
            self.logger.error(
                "Failed to retrieve campaign %s",
                id,
            )
            raise self.KankaException(
                response.text, response.status_code, message=response.reason
            )

        campaign = json.loads(response.text).get("data")
        self.logger.debug(response.json())

        return from_dict(data_class=Campaign, data=campaign)


    def get_members(self) -> list:
        """
        Retrieves the available members from Kanka

        Raises:
            KankaException: Kanka Api Interface Exception

        Returns:
            members (list): a list of available members
        """
        if self.members:
            return self.members

        response = self._request(url=self.GET_MEMBERS, request=GET)

        if not response.ok:
            self.logger.error('Failed to retrieve members from campaign: ', self.campaign.get('name'))
            raise self.KankaException(response.text, response.status_code, message=response.reason)

        self.members = json.loads(response.text).get('data')
        self.logger.debug(response)

        return self.members
