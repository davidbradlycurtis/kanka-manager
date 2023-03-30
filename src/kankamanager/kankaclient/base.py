"""
Base Manager

"""
# pylint: disable=bare-except,super-init-not-called,no-else-break
from __future__ import absolute_import

import logging
import time
import requests
from typing import Callable, Any, Optional
from dataclasses import dataclass, asdict

from kankamanager.kankaclient.constants import MAX_ATTEMPTS, GET, PATCH, POST, DELETE, PUT, DEFAULT_REMOVE

_requests = {
    GET: requests.get,
    PATCH: requests.patch,
    POST: requests.post,
    DELETE: requests.delete,
    PUT: requests.put
}

from dataclasses import dataclass

@dataclass
class Entity:

    id: int
    name: str
    type: Optional[Any]
    tags: list
    is_private: bool
    tooltip: Any
    header_image: Optional[Any]
    image_uuid: Any
    created_at: Any
    created_by: Any
    updated_at: Optional[Any]
    updated_by: Optional[Any]


    def _asdict(self):
        """
        Returns the entity as a dictonary

        Returns:
            dic: the entity as a dict
        """
        return asdict(self)


    def _clean(self):
        """
        Returns the entity as a dict with all empty/blank
        attributes removed

        Returns:
            dict: the cleaned entity
        """
        _dict = self._asdict()
        for field in _dict.copy():
            if _dict[field] is None or _dict[field] == [] or _dict[field] == '' or field in DEFAULT_REMOVE:
                del _dict[field]

        return _dict


class BaseManager(object):
    """Base Manager"""
    def __init__(self, token: str, throttle: bool=False, verbose: bool=False):
        """
        Base Manager Constructor

        Args:
            token (str): the API token
            throttle (bool): enables API throttling
            verbose (bool): enables verbose logging
        """
        logging.basicConfig(format='%(asctime)s  %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
        self.throttle = throttle


    class KankaException(Exception):
        """Base class for exceptions in this module"""
        def __init__(self, reason: str, code: int, message: str):
            self.reason = reason
            self.code = code
            self.message = message


    def raise_exception(self, reason: str, code: int, message: str) -> Exception:
        """
        Raises a KankException

        Args:
            reason (str): the exception reason
            code (int): the exception status code
            message (str): the exception message

        Raises:
            self.KankaException: KankaException
        """
        raise self.KankaException(reason, code, message)


    def _throttle(self, request: Callable, **kwargs: str) -> dict:
        """
        Wraps the provided request and 

        Args:
            request (function): the request (GET/PUSH/CREATE/DELETE...)

        Returns:
            response: the request response
        """
        attempt = 0
        max_attemps = MAX_ATTEMPTS
        response = None
        while attempt < max_attemps:

            if self.throttle:
                time.sleep(1)

            response = request(**kwargs)

            # Check if response has been throttled by Kanka API
            if response.status_code != 429:
                break

            self.logger.debug(f'{response}: Too many requests, trying again')
            time.sleep(5)
            attempt += 1

        return response


    def _request(self, url: str, request: str, headers: dict=None, **kwargs: str) -> dict:
        """
        Makes a GET request to the provided url

        Args:
            url (str): the request url
            request (str): the type of request
            headers (dict, optional): the request headers. Defaults to None.
            params (dict, optional): the request params. Defaults to None.

        Returns:
            response: the request response
        """
        if headers is None:
            headers = self.headers

        response = self._throttle(_requests.get(request), url=url, headers=headers, **kwargs)

        return response
