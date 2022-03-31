"""
Kanka Character API

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import json

from kankaclient.constants import BASE_URL
from kankaclient.base import BaseManager

class CharacterAPI(BaseManager):
    """Kanka Character API"""

    GET_ALL_CREATE_SINGLE = None
    GET_UPDATE_DELETE_SINGLE = None

    def __init__(self, token, campaign, verbose=False):
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.campaign = campaign
        self.campaign_id = campaign.get('id')
        self.characters = list()

        global GET_ALL_CREATE_SINGLE
        global GET_UPDATE_DELETE_SINGLE
        GET_ALL_CREATE_SINGLE = BASE_URL + f'/{self.campaign_id}/characters'
        GET_UPDATE_DELETE_SINGLE = BASE_URL + f'/{self.campaign_id}/characters/%s'

        if verbose:
            self.logger.setLevel(logging.DEBUG)


    def get_characters(self):
        """
        Retrieves the available characters in Kanka

        Args:
            None

        Raises:
            HarborException: Harbor Api Interface Exception
        """
        if self.characters:
            return self.characters

        characters = list()
        response = self._get(url=GET_ALL_CREATE_SINGLE)

        if not response.ok:
            self.logger.error('Failed to retrieve characters from campaign %s', self.campaign.get('name'))
            raise self.KankaException(response.reason, response.status_code, message=response.json())

        characters = json.loads(response.text)['data']
        self.logger.debug(response)

        return characters




    def update_project(self, project, dry_run):
        """
        Updates the provided project in Harbor

        Args:
            project (dict): the project to update
            dry_run (bool): whether to simulate change

        Raises:
            HarborException: Harbor Api Interface Exception
        """
        url = self.DELETE_GET_UPDATE_API % project['project_name']
        self.session.cookies.clear_session_cookies()
        if not dry_run:
            response = self.api_request(self.session.put, self.session, url, body=json.dumps(project))

            if not response.ok:
                self.logger.error('Failed to update project %s', project['project_name'])
                raise self.HarborException(response.reason, response.status_code, message=response.json())

            self.logger.info('Project Updated: %s', project['project_name'])
        else:
            self.logger.info('(Skipped) Project Updated: %s', project['project_name'])


    def get_projects(self):
        """
        Retrives the projects in the current context

        Raises:
            HarborException: Harbor Api Interface Exception

        Returns:
            projects: list of projects
        """
        projects = list()
        url = self.GET_ALL_CREATE_API
        page = 1
        while True:
            params = {'page': page, 'page_size': config.PAGE_SIZE, 'with_detail': True}
            response = self.api_request(self.session.get, self.session, url, params=params)

            if not response.ok:
                self.logger.error('Failed to retrieve projects in host: %s', config.HARBOR_HOST)
                raise self.HarborException(response.reason, response.status_code, message=response.json())

            if response.json():
                projects.extend(response.json())
                page += 1
            else:
                break

        self.logger.info('Projects Received')
        return projects

    def get_project(self, project_name):
        """
        Retrives the project in the current context

        Args:
            project_name (str): the name of the project

        Raises:
            HarborException: Harbor Api Interface Exception

        Returns:
            project: list of projects
        """
        url = self.DELETE_GET_UPDATE_API % project_name
        response = self.api_request(self.session.get, self.session, url)

        if not response.ok:
            self.logger.error('Failed to retrieve project: %s', project_name)
            raise self.HarborException(response.reason, response.status_code, message=response.json())

        self.logger.info('Project Received')
        return response.json()


    def get_project_members(self, project):
        """
        Retrives the project members in the provided project

        Args:
            project (Project): the project

        Raises:
            HarborException: Harbor Api Interface Exception

        Returns:
            members: list of project members
        """
        url = self.MEMBERS_GET_CREATE_API % project['project_id']
        response = self.api_request(self.session.get, self.session, url)

        if not response.ok:
            self.logger.error('Failed to retrieve members in project: %s', project['project_name'])
            raise self.HarborException(response.reason, response.status_code, message=response.json())

        self.logger.info('Project members received for project %s', project['project_name'])
        return response.json()


    def create_project_member(self, project, member_name, member, dry_run):
        """
        Creates the provided member in the given project

        Args:
            project (Project): the project of the member to create
            member_name (str): the project member name
            member (dict): the project member to create
            dry_run (bool): whether to simulate change

        Raises:
            HarborException: Harbor Api Interface Exception
        """
        url = self.MEMBERS_GET_CREATE_API % project['project_id']
        del member['entity_name']
        self.session.cookies.clear_session_cookies()
        if not dry_run:
            response = self.api_request(self.session.post, self.session, url, body=json.dumps(member))

            if not response.ok:
                self.logger.error('Failed to create member in project: %s', project['project_name'])
                raise self.HarborException(response.reason, response.status_code, message=response.json())

            self.logger.info('->Project member %s created for project %s', member_name, project['project_name'])
        else:
            self.logger.info(
                '->(Skipped) Project member %s created for project %s', member_name, project['project_name']
            )


    def update_project_member_role(self, project, member, dry_run):
        """
        Update the provided member in the given project

        Args:
            project (Project): the project of the member to update
            member (dict): the project member to update
            dry_run (bool): whether to simulate change

        Raises:
            HarborException: Harbor Api Interface Exception
        """
        url = self.MEMBERS_UPDATE_DELETE_API % (project['project_id'], member['id'])
        body = {
            'role_id': member['role_id'],
        }
        self.session.cookies.clear_session_cookies()
        if not dry_run:
            response = self.api_request(self.session.put, self.session, url, body=json.dumps(body))

            if not response.ok:
                self.logger.error('Failed to update member role in project: %s', project['project_name'])
                raise self.HarborException(response.reason, response.status_code, message=response.json())

            self.logger.info(
                '->Project member %s role updated in project %s',
                member['entity_name'], project['project_name']
            )
        else:
            self.logger.info(
                '->(Skipped) Project member %s role updated in project %s',
                member['entity_name'], project['project_name']
            )


    def delete_project_member(self, project, member, dry_run):
        """
        Delete the provided member in the given project

        Args:
            project (Project): the project of the member to delete
            member (dict): the project member to delete
            dry_run (bool): whether to simulate change

        Raises:
            HarborException: Harbor Api Interface Exception
        """
        url = self.MEMBERS_UPDATE_DELETE_API % (project['project_id'], member['id'])
        self.session.cookies.clear_session_cookies()
        if not dry_run:
            response = self.api_request(self.session.delete, self.session, url)
            if not response.ok:
                self.logger.error('Failed to delete member in project: %s', project['project_name'])
                raise self.HarborException(response.reason, response.status_code, message=response.json())

            self.logger.info(
                '--Project member %s deleted from project %s', member['entity_name'], project['project_name']
            )
        else:
            self.logger.info(
                '--(Skipped) Project member %s deleted from project %s', member['entity_name'], project['project_name']
            )


    def delete_project(self, project_name, dry_run):
        """
        Deletes the provided project in Harbor

        Args:
            project_name (str): the project name
            dry_run (bool): whether to simulate change

        Raises:
            HarborException: Harbor Api Interface Exception
        """
        url = self.DELETE_GET_UPDATE_API % project_name
        self.session.cookies.clear_session_cookies()
        if not dry_run:
            response = self.api_request(self.session.delete, self.session, url)

            if not response.ok:
                self.logger.error('Failed to delete project %s', project_name)
                raise self.HarborException(response.reason, response.status_code, message=response.json())

            self.logger.info('Project Deleted: %s', project_name)
        else:
            self.logger.info('(Skipped) Project Deleted: %s', project_name)
