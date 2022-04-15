"""
Base Manager

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import time
import requests
from typing import Callable

from kankaclient.constants import MAX_ATTEMPTS, GET, PATCH, POST, DELETE, PUT

_requests = {
    GET: requests.get,
    PATCH: requests.patch,
    POST: requests.post,
    DELETE: requests.delete,
    PUT: requests.put
}

class BaseManager():
    """Base Manager"""
    def __init__(self, token, verbose=False):
        logging.basicConfig(format='%(asctime)s  %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.headers = {'Authorization': token, 'Content-type': 'application/json'}


    def _throttle(self, request: Callable, throttle: bool, **kwargs: str) -> dict:
        """
        Wraps the provided 

        Args:
            request (function): the request (GET/PUSH/CREATE/DELETE...)
            throttle (bool): enable request throttling

        Returns:
            response: the request response
        """
        attempt = 0
        max_attemps = MAX_ATTEMPTS
        response = None
        while attempt < max_attemps:
            
            if throttle:
                time.sleep(.5)

            response = request(**kwargs)

            # Check if response has been throttled by Kanka API
            if response.status_code != 429:
                break

            self.logger.debug(f'{response}: Too many requests, trying again')
            time.sleep(5)
            attempt += 1

        return response


    def _request(self, url: str, request: str, throttle: bool=False, headers: dict=None, **kwargs: str) -> dict:
        """
        Makes a GET request to the provided url

        Args:
            url (str): the request url
            request (str): the type of request
            throttle (bool): enable request throttling
            headers (dict, optional): the request headers. Defaults to None.
            params (dict, optional): the request params. Defaults to None.

        Returns:
            response: the request response
        """
        if headers is None:
            headers = self.headers

        response = self._throttle(_requests.get(request), throttle=throttle, url=url, headers=headers, **kwargs)

        return response


    class KankaException(Exception):
        """Base class for exceptions in this module"""
        def __init__(self, reason, code, message):
            self.reason = reason
            self.code = code
            self.message = message
