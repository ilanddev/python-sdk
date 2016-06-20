#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import time
import unittest

import requests_mock

import iland

BASE_URL = 'http://mock.com/ecs'

VALID_TOKEN_PAYLOAD = {'expires_in': 12,
                       'access_token': 'AZERTYUIOP',
                       'refresh_token': 'BLABLABLA'}

VALID_REFRESH_TOKEN_PAYLOAD = {'expires_in': 12,
                               'access_token': 'QWERTYUIOP',
                               'refresh_token': 'BLOBLOBLO'}


class TestIland(unittest.TestCase):
    session = None
    adapter = None

    def setUp(self):
        self.api = iland.Api(client_id='fake',
                             client_secret='fake',
                             username='fake',
                             password='fake',
                             base_url=BASE_URL)

    def test_login_ok_200(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            self.api.login()
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())

    def test_login_ok_201(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=201)
            self.api.login()
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())

    def test_login_ok_202(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=202)
            self.api.login()
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())

    def test_login_ko_500(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps({'error': 'an error occured'}),
                   status_code=500)
            with self.assertRaises(iland.UnauthorizedException):
                self.api.login()

    def test_login_ko_400(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps({'error': 'an error occured'}),
                   status_code=400)
            with self.assertRaises(iland.UnauthorizedException):
                self.api.login()

    def test_refresh_token_ok(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            m.post(iland.REFRESH_URL,
                   text=json.dumps(VALID_REFRESH_TOKEN_PAYLOAD),
                   status_code=200)
            self.api.login()
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())

            # manually refresh token
            self.api.refresh_access_token()
            # still the same since not expired therefore not renewed
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())

            # let's wait for expiration
            time.sleep(5)
            self.api.refresh_access_token()
            self.assertEqual(VALID_REFRESH_TOKEN_PAYLOAD,
                             self.api.get_access_token())

            # manually remove the actual token so that we refetch an access
            # token
            self.api._token = None
            self.api.refresh_access_token()
            self.assertEqual(VALID_TOKEN_PAYLOAD,
                             self.api.get_access_token())

    def test_refresh_token_ko_400(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            m.post(iland.REFRESH_URL,
                   text=json.dumps(VALID_REFRESH_TOKEN_PAYLOAD),
                   status_code=400)
            self.api.login()
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())
            # let's wait for expiration
            time.sleep(5)
            with self.assertRaises(iland.UnauthorizedException):
                self.api.refresh_access_token()

    def test_refresh_token_ko_500(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            m.post(iland.REFRESH_URL,
                   text=json.dumps(VALID_REFRESH_TOKEN_PAYLOAD),
                   status_code=500)
            self.api.login()
            self.assertEqual(VALID_TOKEN_PAYLOAD, self.api.get_access_token())
            # let's wait for expiration
            time.sleep(5)
            with self.assertRaises(iland.UnauthorizedException):
                self.api.refresh_access_token()

    def test_get_ok_200(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=200)
            req = self.api.get(rpath)
            self.assertEquals(user_data, req)

    def test_get_ok_201(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=201)
            req = self.api.get(rpath)
            self.assertEquals(user_data, req)

    def test_get_ok_202(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=202)
            req = self.api.get(rpath)
            self.assertEquals(user_data, req)

    def test_get_ok_204(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=204)
            req = self.api.get(rpath)
            self.assertEquals(user_data, req)

    def test_get_ko_400(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=400)
            with self.assertRaises(iland.ApiException):
                self.api.get(rpath)

    def test_get_ko_500(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=500)
            with self.assertRaises(iland.ApiException):
                self.api.get(rpath)

    def test_post_ok(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.post(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                   status_code=200)
            req = self.api.post(rpath, form_data={'a': 'b'})
            self.assertEquals(user_data, req)

    def test_post_ok_no_formdata(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.post(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                   status_code=200)
            req = self.api.post(rpath)
            self.assertEquals(user_data, req)

    def test_put_ok(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.put(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=200)
            req = self.api.put(rpath, form_data={'a': 'b'})
            self.assertEquals(user_data, req)

    def test_put_ok_no_formdata(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.put(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=200)
            req = self.api.put(rpath)
            self.assertEquals(user_data, req)

    def test_delete_ok(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.delete(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                     status_code=200)
            req = self.api.delete(rpath)
            self.assertEquals(user_data, req)

    def test_unknown_verb_internal(self):
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.delete(BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                     status_code=200)
            with self.assertRaises(iland.ApiException):
                self.api._do_request(rpath, verb='ACK')

    def test_with_default_base_url(self):
        self.api = iland.Api(client_id='fake',
                             client_secret='fake',
                             username='fake',
                             password='fake')
        with requests_mock.mock() as m:
            m.post(iland.ACCESS_URL,
                   text=json.dumps(VALID_TOKEN_PAYLOAD),
                   status_code=200)
            rpath = '/user/jchirac'
            user_data = {'username': 'jchirac'}
            m.get(iland.BASE_URL + rpath, text='XXXXX' + json.dumps(user_data),
                  status_code=200)
            req = self.api.get(rpath)
            self.assertEquals(user_data, req)
