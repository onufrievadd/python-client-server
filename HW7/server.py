"""
Функции сервера: принимает сообщение клиента; формирует ответ клиенту;
отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт
для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает
все доступные адреса).
"""

from common.variables import *
from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from json import JSONDecodeError
import logging
import log.server_log_config
from decos import log
from select import select
from time import time

SERVER_LOGGER = logging.getLogger('server')

@log
def process_client_message(message, message_list, client):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message({RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        message_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return

def main():
    try:
        if '-p' in argv:
            listen_port = int(argv[argv.index('-p') + 1])
            SERVER_LOGGER.info(f'Слушаем порт : {listen_port}')
        else:
            listen_port = DEFAULT_PORT
            SERVER_LOGGER.info(f'Слушаем порт по умолчанию : {listen_port}')
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
        exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)

    try:
        if '-a' in argv:
            listen_address = argv[argv.index('-a') + 1]
            SERVER_LOGGER.info(f'Слушаем адрес : {listen_address}')
        else:
            listen_address = ''
            SERVER_LOGGER.info(f'Слушаем все адреса')
    except IndexError:
        SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать IP для сервера')
        exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)
    clients = []
    messages = []
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК : {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                       messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()}'
                                       f' отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
