#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_iland_int
----------------------------------

Integration tests for the `iland` module.
"""

import time
import unittest

import iland
import iland.constant
from iland.exception import ApiException, UnauthorizedException

try:
    # only PyCharm w/ Python3 fails here without dot
    from apicreds import (CLIENT_ID,
                          CLIENT_SECRET,
                          USERNAME,
                          PASSWORD)
except ImportError:
    from .apicreds import (CLIENT_ID,
                           CLIENT_SECRET,
                           USERNAME,
                           PASSWORD)

VDC_UUID = \
    'res01.ilandcloud.com:urn:vcloud:vdc:a066325d-6be0-4733-8d9f-7687c36f4536'


@unittest.skipIf(not CLIENT_ID and not CLIENT_SECRET and not USERNAME and not
                 PASSWORD, "No credentials provided")
class TestIlandInt(unittest.TestCase):
    def setUp(self):
        self._api = iland.Api(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              username=USERNAME,
                              password=PASSWORD,
                              base_url=iland.constant.BASE_URL)

    def tearDown(self):
        pass

    def test_get(self):
        user = self._api.get('/user/' + USERNAME)
        self.assertEqual(USERNAME, user.get('name'))
        self.assertTrue(len(user.keys()) > 5)

    def test_post(self):
        user_alert_emails = self._api.get('/user/' + USERNAME +
                                          '/alert-emails')
        self.assertTrue(len(user_alert_emails['emails']) >= 1)
        self.assertEquals(user_alert_emails['username'], USERNAME)

        old_user_alert_emails = user_alert_emails
        user_alert_emails = {'emails': ['test@iland.com', 'test2@iland.com'],
                             'username': USERNAME}
        self._api.post('/user/' + USERNAME + '/alert-emails',
                       user_alert_emails)

        self.assertTrue(len(user_alert_emails['emails']) >= 1)
        self.assertEquals(user_alert_emails['username'], USERNAME)

        self._api.post('/user/' + USERNAME + '/alert-emails',
                       old_user_alert_emails)
        self.assertEquals(len(user_alert_emails['emails']), 2)
        self.assertEquals(user_alert_emails['username'], USERNAME)

    def test_put_delete(self):
        vdc_uuid = VDC_UUID
        vdc_md = self._api.get('/vdc/' + vdc_uuid + '/metadata')

        self.assertEquals(len(vdc_md), 0)

        new_md = [{'type': 'string',
                   'value': 'B',
                   'access': 'READ_WRITE',
                   'key': 'AAA'}]
        new_md.extend(vdc_md)
        self._api.put('/vdc/' + vdc_uuid + '/metadata',
                      form_data=new_md)

        time.sleep(10)

        updated_md = self._api.get('/vdc/' + vdc_uuid + '/metadata')
        self.assertEquals(len(updated_md), 1)

        self._api.delete('/vdc/' + vdc_uuid + '/metadata/' + 'AAA')

        time.sleep(10)

        updated_md = self._api.get('/vdc/' + vdc_uuid + '/metadata')
        self.assertEquals(len(updated_md), 0)

    def test_refresh_token(self):
        self._api.login()
        self.assertIsNotNone(self._api.get_access_token())
        expires_in = self._api._token_expiration_time

        # force expires for tests.
        self._api._token_expiration_time = 0
        self._api.refresh_access_token()

        new_expires_in = self._api._token_expiration_time
        self.assertTrue(new_expires_in > expires_in)

    def test_unauthorized_errors(self):
        wrongCredsApi = iland.Api(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  username='PYTHON_SDK_TEST',
                                  password='XXXX',
                                  base_url=iland.constant.BASE_URL)
        with self.assertRaises(UnauthorizedException):
            wrongCredsApi.login()

        with self.assertRaises(UnauthorizedException):
            wrongCredsApi.get_access_token()

        with self.assertRaises(UnauthorizedException):
            wrongCredsApi.refresh_access_token()

    def test_api_errors(self):
        with self.assertRaises(ApiException):
            self._api.get('/doesnotexist')
