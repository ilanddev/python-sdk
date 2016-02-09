#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_iland
----------------------------------

Tests for `iland-sdk` module.
"""

import time
import unittest

import iland
from .apicreds import (CLIENT_ID,
                       CLIENT_SECRET,
                       USERNAME,
                       PASSWORD)

VDC_UUID = \
    'res01.ilandcloud.com:urn:vcloud:vdc:a066325d-6be0-4733-8d9f-7687c36f4536'


@unittest.skipIf(not CLIENT_ID and not CLIENT_SECRET and not USERNAME and not
                 PASSWORD, "No credentials provided")
class TestIland(unittest.TestCase):
    def setUp(self):
        self._api = iland.Api(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              username=USERNAME,
                              password=PASSWORD)

    def tearDown(self):
        pass

    def test_get(self):
        user = self._api.get('/user/' + USERNAME)
        self.assertEqual(USERNAME, user.get('name'))
        self.assertTrue(len(user.keys()) > 20)

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

        self.assertEquals(len(vdc_md), 1)

        new_md = [{'type': 'string',
                   'value': 'B',
                   'access': 'READ_WRITE',
                   'key': 'AAA'}]
        new_md.extend(vdc_md)
        task = self._api.put('/vdc/' + vdc_uuid + '/metadata',
                             form_data=new_md)
        if task is None:
            tasks = self._api.get(
                '/task/res01.ilandcloud.com/entity/' + VDC_UUID + '/active')
            if len(tasks) > 0:
                task = tasks[0]
        while task is not None:
            task = self._api.get('/task/res01.ilandcloud.com/' + task[
                'task_id'])
            if task is not None and task['sychronized'] is True:
                break

        time.sleep(10)

        updated_md = self._api.get('/vdc/' + vdc_uuid + '/metadata')
        self.assertEquals(len(updated_md), 2)

        task = self._api.delete('/vdc/' + vdc_uuid + '/metadata/' + 'AAA')
        if task is None:
            tasks = self._api.get(
                '/task/res01.ilandcloud.com/entity/' + VDC_UUID + '/active')
            if len(tasks) > 0:
                task = tasks[0]
        while task is not None:
            task = self._api.get(
                '/task/res01.ilandcloud.com/' + task['task_id'])
            if task is not None and task['sychronized'] is True:
                break

        time.sleep(10)

        updated_md = self._api.get('/vdc/' + vdc_uuid + '/metadata')
        self.assertEquals(len(updated_md), 1)

    def test_refresh_token(self):
        self._api.login()
        expires_in = self._api._token_expiration_time

        # force expires for tests.
        self._api._token_expiration_time = 0
        self._api._refresh_token()

        new_expires_in = self._api._token_expiration_time
        self.assertTrue(new_expires_in > expires_in)
