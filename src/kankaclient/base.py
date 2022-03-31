"""
Base Manager

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import time
from urllib import request
import requests
import urllib3
#from urllib3.exceptions import InsecureRequestWarning

from kankaclient.constants import MAX_ATTEMPTS

# Suppress only the single warning from urllib3 needed.
#urllib3.disable_warnings(category=InsecureRequestWarning)

class BaseManager():
    """Base Manager"""
    def __init__(self, token, verbose=False):
        logging.basicConfig(format='%(asctime)s  %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.headers = {'Authorization': token, 'Content-type': 'application/json'}



    def _throttle(self, request, url, headers, body, params):
        """
        Wraps the provided api request in a retry-loop to catch
        internal/throttle server errors

        Args:
            request (request): the api request

        Returns:
            response: the request response
        """
        attempt = 0
        max_attemps = MAX_ATTEMPTS
        response = None
        while attempt < max_attemps:
            response = request(url, data=body, params=params)

            if str(response.status_code)[0] == '5' :
                self.logger.error('Failed to connect to Kanka API: Attempt %d', attempt + 1)
                self.logger.error('Status Code: %d', response.status_code)
                self.logger.error('Reason: %s', response.reason)
            else:
                break

            time.sleep(5)
            attempt += 1

        return response


    def _get(self, url, headers=None, params=None):
        """
        TODO

        Args:
            api_request (request): the api request
            url (str): the request url
            headers (dict, optional): the request headers. Defaults to None.
            params (dict, optional): the request params. Defaults to None.

        Returns:
            response: the request response
        """
        if headers is None:
            headers = self.headers

        response = requests.get(url=url, headers=headers, params=params)

        return response


    class KankaException(Exception):
        """Base class for exceptions in this module"""
        def __init__(self, reason, code, message):
            self.reason = reason
            self.code = code
            self.message = message['errors'][0]['message']
