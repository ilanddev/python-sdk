# -*- coding: utf-8 -*-

"""A library that provides a Python interface to the iland cloud API."""

import json
import time

import requests

from .constant import BASE_URL, ACCESS_URL, REFRESH_URL
from .log import LOG
from .exception import ApiException, UnauthorizedException


class Api(object):
    """A Python interface into the iland cloud API
    """

    _client_id = None
    _client_secret = None
    _username = None
    _password = None
    _base_url = BASE_URL
    _access_token_url_ = ACCESS_URL
    _refresh_token_url = REFRESH_URL
    _proxies = None

    _token = None
    _token_expiration_time = None

    _verify_ssl = True
    _session = None

    def __init__(self, client_id, client_secret, username, password):
        """Instantiate a new iland.Api object.

        :param client_id: the client identifier
        :param client_secret: the client secret
        :param username: the iland cloud username
        :param password: the iland cloud password
        :return: Api Object
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self._session = requests.Session()

    @property
    def _access_token_url(self):
        return self._access_token_url_

    @_access_token_url.setter
    def _access_token_url(self, access_token_url):
        if access_token_url is not None:
            self._access_token_url_ = access_token_url
            self._refresh_token_url = access_token_url + '?refresh=1'

    def _get_access_token(self):

        if self._valid_token():
            return self._token

        LOG.info("SSO Request %s" % self._access_token_url)

        params = {'client_id': self._client_id,
                  'client_secret': self._client_secret,
                  'username': self._username,
                  'password': self._password,
                  'grant_type': 'password'}
        r = self._session.post(
            self._access_token_url, data=params, verify=self._verify_ssl)
        json_payload = json.loads(r.content.decode('ascii'))
        if r.status_code not in [200, 201, 202]:
            raise UnauthorizedException(json_payload)
        self._token = json_payload
        self._set_token_expiration_time()
        return self._token

    def _set_token_expiration_time(self):
        time_buffer = 10
        self._token_expiration_time = \
            ((self._token['expires_in'] - time_buffer) * 1000) + \
            int(round(time.time() * 1000))

    def _refresh_token(self):
        if not self._valid_token():
            if self._token is not None:
                LOG.info("SSO Request %s" % self._refresh_token_url)
                params = {'client_id': self._client_id,
                          'client_secret': self._client_secret,
                          'grant_type': 'refresh_token',
                          'refresh_token': self._token['refresh_token']
                          }
                r = self._session.post(self._refresh_token_url, data=params,
                                       verify=self._verify_ssl)
                json_payload = json.loads(r.content.decode('ascii'))
                if r.status_code not in [200, 201, 202]:
                    raise UnauthorizedException(json_payload)
                self._token = json_payload
                self._set_token_expiration_time()
            else:
                self._get_access_token()
        return self._token

    def _valid_token(self):
        if self._token is not None:
            return int(round(time.time() * 1000)) < self._token_expiration_time
        return False

    def _get_access_token_string(self):
        token_string = self._get_access_token()['access_token']
        return token_string

    def _do_request(self, rpath, verb='GET', form_data=None, headers=None):
        self._refresh_token()
        data = None
        if form_data is not None:
            data = json.dumps(form_data, ensure_ascii=False).encode("UTF8")
        url = self._base_url + rpath

        LOG.info("Request %s rpath %s" % (verb, url))

        default_headers = {
            'Authorization': 'Bearer %s' % self._get_access_token_string(),
            'Accept': 'application/vnd.ilandcloud.api.v1.0+json'
        }
        if verb in ('PUT', 'POST'):
            default_headers[
                'Content-Type'] = 'application/json'

        merged_headers = default_headers.copy()

        if headers and isinstance(headers, dict):
            for header, value in headers.items():
                # don't allow overriding of our default headers
                if header in default_headers:
                    LOG.warning("Header '%s' can't be overridden" % header)
                else:
                    merged_headers[header] = value

        request_params = {
            'headers': merged_headers,
            'verify':  self._verify_ssl
        }

        if verb in ('PUT', 'POST'):
            request_params['data'] = data

        if self._proxies and isinstance(self._proxies, dict):
            request_params['proxies'] = self._proxies

        if verb == 'GET':
            r = self._session.get(url, **request_params)
        elif verb == 'PUT':
            r = self._session.put(url, **request_params)
        elif verb == 'POST':
            r = self._session.post(url, **request_params)
        elif verb == 'DELETE':
            r = self._session.delete(url, **request_params)
        else:
            raise ApiException({'message': 'Unsupported HTTP verb %s' % verb})

        try:
            json_obj = r.json()
        except ValueError:
            raise ApiException(r.content)
        if r.status_code not in [200, 201, 202, 204]:
            raise ApiException(json_obj)
        return json_obj

    def get(self, rpath, headers=None):
        """ Perform a GET request against the iland cloud API given its
        resource path.

        `iland.Api` will refresh the access token if non valid.

        :param rpath: the resource path as a Python builtin String object
        :param headers: an optional dictionary of http headers to send with \
                        the request
        :raises: ApiException: API requests returns an error
        :raises: UnauthorizedException: credentials / grants invalids
        :return: a JSON Object or a list of JSON Objects.
        """
        return self._do_request(rpath, headers=headers)

    def put(self, rpath, form_data=None, headers=None):
        """ Perform a PUT request against the iland cloud API given its
        resource path.

        `iland.Api` will refresh the access token if non valid.

        :param rpath: the resource path as a Python builtin String object
        :param form_data: a Python builtin dict object
        :param headers: an optional dictionary of http headers to send with \
                        the request
        :raises: ApiException: API requests returns an error
        :raises: UnauthorizedException: credentials / grants invalids
        :return: a JSON Object or a list of JSON Objects.
        """
        return self._do_request(rpath, verb='PUT', form_data=form_data,
                                headers=headers)

    def post(self, rpath, form_data=None, headers=None):
        """ Perform a POST request against the iland cloud API given its
        resource path.

        `iland.Api` will refresh the access token if non valid.

        :param rpath: the resource path as a Python builtin String object
        :param form_data: a Python builtin dict object
        :param headers: an optional dictionary of http headers to send with \
                        the request
        :raises: ApiException: API requests returns an error
        :raises: UnauthorizedException: credentials / grants invalids
        :return: a JSON Object or a list of JSON Objects.
        """
        return self._do_request(rpath, verb='POST', form_data=form_data,
                                headers=headers)

    def delete(self, rpath, headers=None):
        """ Perform a DELETE request against the iland cloud API given its
        resource path.

        `iland.Api` will refresh the access token if non valid.

        :param rpath:  the resource path as a Python builtin String object
        :param headers: an optional dictionary of http headers to send with \
                        the request
        :raises: ApiException: API requests returns an error
        :raises: UnauthorizedException: credentials / grants invalids
        :return: a JSON Object or a list of JSON Objects.
        """
        return self._do_request(rpath, verb='DELETE', headers=headers)

    def get_access_token(self):
        """ Returns the access token in use for this session.

        This method is exposed in case you are interested in managing the
        token life cycle yourself. `iland.Api` will refresh the token on your
        behalf while performing queries.

        :raises: UnauthorizedException: credentials / grants invalids
        :return: JSON Object containing the actual access token
        """
        return self._get_access_token()

    def refresh_access_token(self):
        """ Refresh token if token is not valid: None or expired.

        This method is exposed in case you are interested in managing the
        token life cycle yourself. `iland.Api` will refresh the token on your
        behalf while performing queries.

        :raises: UnauthorizedException: credentials / grants invalids
        :return: JSON Object containing the actual access token
        """
        return self._refresh_token()

    def login(self):
        """ Requests an access token.

        This method is exposed in case you are interested in managing the
        token life cycle yourself. `iland.Api` will refresh the token on your
        behalf while performing queries.

        :raises: UnauthorizedException: credentials / grants invalids
        :return: JSON Object containing the actual access token
        """
        return self._get_access_token()
