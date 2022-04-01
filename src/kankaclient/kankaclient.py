"""
Kanka Client

"""
# pylint: disable=bare-except
from __future__ import absolute_import

import logging

from kankaclient.base import BaseManager
from kankaclient.characters import CharacterAPI
from kankaclient.campaigns import CampaignAPI
from kankaclient.locations import LocationAPI
from kankaclient.organizations import OrganizationAPI
from kankaclient.races import RaceAPI



class KankaClient(BaseManager):
    """Kanka Client"""

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.campaigns = CampaignAPI(token=token, campaign=campaign, verbose=verbose)
        self.characters = CharacterAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.locations = LocationAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.organizations = OrganizationAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)
        self.races = RaceAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)


        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.logger.debug('Kanka Client initialized')
