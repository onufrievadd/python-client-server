"""Утилиты"""
import sys
from json import dumps, loads
sys.path.append('../')
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decos import log

@log
def send_msg(sock, message):
    js_message = dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)


@log
def get_msg(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message() -> object:
    """

    :rtype: object
    """
    return None


def get_message():
    return None