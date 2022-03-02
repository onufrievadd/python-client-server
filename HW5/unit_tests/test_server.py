import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from server import process_client_message
from common.variables import *

class TestClass(unittest.TestCase):
    OK_DICT = {
        RESPONSE: 200
    }
    ERROR_DICT_SERVER = {
        ERROR: 'Bad Request',
        RESPONDEFAULT_IP_ADDRESSSE: 400
    }
    def test_process_client_message_200(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}), self.OK_DICT)

    def test_process_client_message_400(self):
        self.assertEqual(process_client_message({USER: {ACCOUNT_NAME: 'test_test'}}), self.ERROR_DICT_SERVER)

    def test_dict_client_message_200(self):
        self.assertIsInstance(process_client_message(
            {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'test_test'}}), dict)

    def test_dict_client_message_400(self):
        self.assertIsInstance(process_client_message({USER: {ACCOUNT_NAME: 'test_test'}}), dict)

    def test_no_str_client_message_200(self):
        self.assertNotIsInstance(process_client_message(
            {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'test_test'}}), str)

    def test_no_str_client_message_400(self):
        self.assertNotIsInstance(process_client_message({ACCOUNT_NAME: 'test_test'}), str)


if __name__ == '__main__':
    unittest.main()