"""
Kanka Client

"""
# pylint: disable=bare-except
from __future__ import absolute_import

import logging

from kankaclient.base import BaseManager
from kankaclient.characters import CharacterAPI
from kankaclient.campaigns import CampaignAPI
# from api.projects import ProjectAPI
# from api.repositories import RepositoryAPI
# from api.robot_accounts import RobotAccountAPI
# from api.garbage_collection import GarbageCollectionAPI
# from api.users import UserAPI
# from api.usergroups import UserGroupAPI


class KankaClient(BaseManager):
    """Kanka Client"""

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)

        # Get campaign
        self.campaigns = CampaignAPI(token=token, campaign=campaign, verbose=verbose)
        self.characters = CharacterAPI(token=token, campaign=self.campaigns.campaign, verbose=verbose)


        #self.characters = CharacterAPI(campaign= verbose=verbose)


        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.logger.info('Kanka Client initialized')
