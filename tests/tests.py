import os
import json

import unittest

from coinsrpc_api import *

class CoinsrpcApiTestCase(unittest.TestCase):

    def setUp(self):
        self.reference_name = "halfmoon"
        self.reference_fake_name = "fakeName"
        self.reference_value = "halfmoonlabs.com"
        self.reference_code_true = "Yes"
        self.reference_code_false = "No"
        self.reference_status_code = 200
        self.reference_txid = "e5da4edff56e546619cf765ebbb72c7e586e036236247bae24ffd0a4d302c36e"
        self.reference_address = "NBb6yLNQfTExU5kZKSSPDcefJeZ6m6HYUk"
        self.reference_is_name_registered_message_true = 'The name is registered'
        self.reference_is_name_registered_message_false = 'The name is not registered'
        pass

    def tearDown(self):
        pass

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, self.reference_status_code)

    def test_bitcoind_blocks(self):
        tester = app.test_client(self)
        response = tester.get('/bitcoind/blocks', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("blocks" in data)
        expected_block = data["blocks"]
        self.assertIsNotNone(expected_block)

    def test_namecoind_blocks(self):
        tester = app.test_client(self)
        response = tester.get('/namecoind/blocks', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("blocks" in data)
        expected_block = data["blocks"]
        self.assertIsNotNone(expected_block)

    def test_name_scan(self):
        tester = app.test_client(self)
        response = tester.get('/namecoind/name_scan?start_name=' + self.reference_name + '&max_returned=10', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("name" in data[0] and "value" in data[0])
        expected_name = data[0]["name"]
        expected_value = str(data[0]["value"])
        self.assertTrue(expected_name == self.reference_name)
        self.assertTrue(self.reference_value in expected_value)
        self.assertTrue(len(data) == 10)

    def test_name_scan_without_parameters(self):
        tester = app.test_client(self)
        response = tester.get('/namecoind/name_scan', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("name" in data[0])
        self.assertFalse("value" in data[0])
        expected_name = data[0]["name"]
        self.assertTrue(expected_name == 'g/m')
        self.assertTrue(len(data) == 500)

    def test_is_name_registered_true(self):
        tester = app.test_client(self)
        response = tester.get('/namecoind/is_name_registered/' + self.reference_name, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("message" in data and "code" in data)
        expected_message = data["message"]
        expected_code = data["code"]
        self.assertTrue(expected_message == self.reference_is_name_registered_message_true)
        self.assertTrue(expected_code == self.reference_code_true)

    def test_is_name_registered_false(self):
        tester = app.test_client(self)
        response = tester.get('/namecoind/is_name_registered/' + self.reference_fake_name, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("message" in data and "code" in data)
        expected_message = data["message"]
        expected_code = data["code"]
        self.assertTrue(expected_message == self.reference_is_name_registered_message_false)
        self.assertTrue(expected_code == self.reference_code_false)

    def test_get_name_details(self):
        tester = app.test_client(self)
        response = tester.get('/namecoind/get_name_details/' + self.reference_name, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.reference_status_code)
        self.assertTrue("name" in data)
        self.assertTrue("value" in data)
        self.assertTrue("address" in data)
        self.assertTrue("txid" in data)
        self.assertTrue("expires_in" in data)
        expected_name = data["name"] 
        expected_value = str(data["value"])
        expected_address = data["address"]
        expected_txid = data["txid"]
        expected_expires_in = data["expires_in"]
        self.assertTrue(expected_name == self.reference_name)
        self.assertTrue(self.reference_value in expected_value)
        self.assertTrue(expected_address == self.reference_address)
        self.assertTrue(expected_txid == self.reference_txid)
        self.assertIsNotNone(expected_expires_in)

if __name__ == '__main__':
    unittest.main()