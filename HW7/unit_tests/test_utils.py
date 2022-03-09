import sys
import os
import unittest
import json
sys.path.append('../')

from common.utils import *
from common.variables import *

class TestSocket:
    def __init__(self, test_dict):
        self.testdict = test_dict

    def send(self, message_to_send):
        json_test_message = json.dumps(self.testdict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.testdict)
        return json_test_message.encode(ENCODING)

class TestClass(unittest.TestCase):
    DICT_SEND = {
        ACTION: PRESENCE,
        TIME: 1,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    OK_DICT = {
        RESPONSE: 200
    }
    ERROR_DICT = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


    def test_send_message_ok(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_message(test_socket, self.DICT_SEND)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_bytes_send_message(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_message(test_socket, self.DICT_SEND)
        self.assertIsInstance(test_socket.encoded_message, bytes)

    def test_no_dict_send_message(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_message(test_socket, self.DICT_SEND)
        self.assertNotIsInstance(test_socket.encoded_message, dict)

    def test_get_message_ok(self):
        test_socket_ok = TestSocket(self.OK_DICT)
        self.assertEqual(get_message(test_socket_ok), self.OK_DICT)

    def test_get_message_err(self):
        test_socket_err = TestSocket(self.ERROR_DICT)
        self.assertEqual(get_message(test_socket_err), self.ERROR_DICT)

    def test_dict_get_message(self):
        test_socket_ok = TestSocket(self.OK_DICT)
        self.assertIsInstance(get_message(test_socket_ok), dict)

    def test_no_str_get_message(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_message(test_socket, self.DICT_SEND)
        self.assertNotIsInstance(test_socket.encoded_message, str)