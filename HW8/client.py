"""
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера;параметры командной
строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777.
"""

from common.variables import *
from time import time, sleep
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from json import JSONDecodeError
import logging
import log.client_log_config
import argparse
from decos import log
import threading

CLIENT_LOGGER = logging.getLogger('client')


@log
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time(),
        ACCOUNT_NAME: account_name
    }


@log
def message_from_server(sock, my_username):
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'Получено сообщение от пользователя '
                      f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                                   f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, account_name='Guest'):
    # message = input('Введите текст для отправки или для завершения работы: \'111\'  ')
    # if message == '111':
    #     sock.close()
    #     CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
    #     print('!!!Спасибо за использование нашего сервиса!!!')
    #     exit(0)
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        TIME: time(),
        ACCOUNT_NAME: account_name,
        DESTINATION: to_user,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'сообщение: {message_dict}')
    # return message_dict
    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except Exception as e:
        print(e)
        CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
        exit(1)


def print_help():
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE}'
                        f' сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера : {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise Exception(f'400 : {message[ERROR]}')
    raise ValueError


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen , send')
        exit(1)

    return server_address, server_port, client_mode


def main():
    server_address, server_port, client_name = arg_parser()

    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_name}')

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: '
                       f'{server_address}, порт: {server_port}, режим работы: {client_name}')

    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера: {answer}')
        print('Соединение установлено.')
    except JSONDecodeError:
        CLIENT_LOGGER.error(f'Не удалось декодировать Json строку')
        exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}')
        exit(1)
    else:
        # if client_name == 'send':
        #     print('Режим работы - отправка сообщений.')
        # else:
        #     print('Режим работы - приём сообщений.')
        # while True:
        #     if client_name == 'send':
        #         try:
        #             send_message(transport, create_message(transport))
        #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #             CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
        #             exit(1)
        #
        #     if client_name == 'listen':
        #         try:
        #             message_from_server(get_message(transport))
        #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #             CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
        #             exit(1)
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
