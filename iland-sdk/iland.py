# -*- coding: utf-8 -*-

import json
import time

import requests

from constant import BASE_URL, ACCESS_URL, REFRESH_URL
from log import LOG


class Api(object):
    """A python interface into the iland cloud API
    """

    _client_id = None
    _client_secret = None
    _username = None
    _password = None
    _base_url = BASE_URL

    _token = None
    _token_expiration_time = None

    def __init__(self, client_id, client_secret, username, password,
                 base_url=None):
        """Instantiate a new iland.Api object.

        :param client_id: the client identifier
        :param client_secret: the client secret
        :param username: the iland cloud username
        :param password: the iland cloud password
        :param base_url: [optional] base url to contact the iland cloud API
        :return: Api Object
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        if base_url is not None:
            self._base_url = base_url

    def _get_access_token(self):

        if self._valideToken():
            return self._token

        LOG.info("SSO Request %s" % ACCESS_URL)

        params = {'client_id': self._client_id,
                  'client_secret': self._client_secret,
                  'username': self._username,
                  'password': self._password,
                  'grant_type': 'password'}
        r = requests.post(ACCESS_URL, data=params)

        self._token = json.loads(r.content.decode('ascii'))
        self._set_token_expiration_time()
        return self._token

    def _set_token_expiration_time(self):
        time_buffer = 10
        self._token_expiration_time = \
            ((self._token['expires_in'] - time_buffer) * 1000) + \
            int(round(time.time() * 1000))

    def _refresh_token(self):
        if not self._valideToken():
            if self._token is not None:
                LOG.info("SSO Request %s" % REFRESH_URL)
                params = {'client_id': self._client_id,
                          'client_secret': self._client_secret,
                          'grant_type': 'refresh_token',
                          'refresh_token': self._token['refresh_token']
                          }
                r = requests.post(REFRESH_URL, data=params)
                self._token = json.loads(r.content.decode('ascii'))
                self._set_token_expiration_time()
            else:
                self._get_access_token()
        return self._token

    def _valideToken(self):
        if self._token is not None:
            return int(round(time.time() * 1000)) < self._token_expiration_time
        return False

    def _get_access_token_string(self):
        token_string = self._get_access_token()['access_token']
        return token_string

    def _do_request(self, rpath, verb='GET', form_data=None):
        self._refresh_token()
        data = None
        if form_data is not None:
            data = json.dumps(form_data, ensure_ascii=False).encode("UTF8")
        url = BASE_URL + rpath

        LOG.info("Request %s rpath %s" % (verb, url))

        headers = {
            'Authorization': 'Bearer %s' % self._get_access_token_string(),
            'content-type': 'application/json'}
        if verb == 'GET':
            r = requests.get(url, headers=headers)
        elif verb == 'PUT':
            r = requests.put(url, data=data, headers=headers)
        elif verb == 'POST':
            r = requests.post(url, data=data, headers=headers)
        elif verb == 'DELETE':
            r = requests.delete(url, headers=headers)
        else:
            pass
        # iland cloud API prefix have to be ignored because they are here to
        # prevent JSON Hijacking
        json_obj = json.loads(r.content[5:].decode('UTF8'))
        return json_obj

    def get_access_token(self):
        """ Returns the access token in use for this session.

        :return: JSON Object containing the actual access token
        """
        return self._get_access_token()

    def refresh_access_token(self):
        """ Refresh token if token is None or expired.

        :return: JSON Object containing the actual access token
        """
        return self._refresh_token()

    def login(self):
        """ Requests an access token.

        :return: JSON Object containing the actual access token
        """
        return self._get_access_token()

    def get(self, rpath):
        """ Perform a GET request agains the iland cloud API given its resource
        path.

        :param rpath: the resource path as a Python builtin String object
        :return: a JSON Object
        """
        return self._do_request(rpath)

    def put(self, rpath, form_data=None):
        """ Perform a PUT request agains the iland cloud API given its resource
        path.

        :param rpath: the resource path as a Python builtin String object
        :param form_data: a Python builtin dict object
        :return: a JSON Object
        """
        self._do_request(rpath, verb='PUT', form_data=form_data)

    def post(self, rpath, form_data=None):
        """ Perform a POST request agains the iland cloud API given its resource
        path.

        :param rpath: the resource path as a Python builtin String object
        :param form_data: a Python builtin dict object
        :return: a JSON Object
        """
        self._do_request(rpath, verb='POST', form_data=form_data)

    def delete(self, rpath):
        """ Perform a DELETE request agains the iland cloud API given its
        resource path.

        :param rpath:  the resource path as a Python builtin String object
        :return: a JSON Object
        """
        self._do_request(rpath, verb='DELETE')
