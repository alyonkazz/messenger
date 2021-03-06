import argparse
import datetime
import select
import sys
import threading
from socket import AF_INET, SOCK_STREAM, socket

from PyQt5.QtWidgets import QApplication

import server_logs.server_log_config as log
from server_config.utils import send_message, get_message
from serverapp.errors import ServerError
from server_database.database_server import ServerDB
from serverapp.decorators import func_to_log, login_required
from serverapp.descrptrs_server import GetPort
from serverapp.metaclss_server import ServerVerifier
from server_config.settings import MAX_CONNECTION, TIMEOUT, \
    MESSAGE, ACTION, PRESENCE, TIME, USER, MESSAGE_TEXT, ACCOUNT_NAME, RESPONSE, ERROR, SENDER, DESTINATION, EXIT, \
    GET_USERS_PACKAGE, ALL_USERS, ADD_CONTACT, REMOVE_CONTACT, SERVER, CONTACTS, GET_ALL_USERS, PASSWORD, REGISTRATION, \
    DEFAULT_HOST, DEFAULT_PORT, MESSAGE_ID, MESSAGE_DATETIME, MESSAGE_HISTORY
from serverapp.server_gui import UsersStatistic


@func_to_log
def arg_parser(default_address, default_port):
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=default_address, nargs='?')
    parser.add_argument('--port', default=default_port, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_host = namespace.host
    server_port = namespace.port

    return server_host, server_port


@func_to_log
def start_gui(users):
    app = QApplication(sys.argv)
    mw = UsersStatistic(users)
    mw.show()
    app.exec_()


class Server(threading.Thread, metaclass=ServerVerifier):
    port = GetPort()

    def __init__(self, listen_host, port, database):
        threading.Thread.__init__(self)

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = listen_host
        self.port = port

        # база данных сервера
        self.database = database

        # список клиентов, очередь сообщений
        self.all_clients = []
        self.all_messages = []
        self.active_users = {}

    @login_required
    def process_client_message(self, message, client_sock):
        log.SERVER_LOG.debug(f'Разбор сообщения от клиента : {message}')
        # ------------------------ Разбор registration сообщения ------------------------ #
        if (ACTION and TIME and USER) in message \
                and message[ACTION] == REGISTRATION:
            try:

                self.database.user_registration(message[USER][SENDER], message[USER][PASSWORD])
            except ServerError as e:
                answer = {
                    RESPONSE: 400,
                    ACTION: REGISTRATION,
                    ERROR: e.text,
                }
                send_message(client_sock, answer)
                client_sock.close()
            else:
                answer = {
                    RESPONSE: 200,
                    ACTION: REGISTRATION,
                }
                send_message(client_sock, answer)
            return

        # ------------------------ Разбор presence сообщения ------------------------ #
        if (ACTION and TIME and USER) in message \
                and message[ACTION] == PRESENCE:
            if message[USER][SENDER] not in self.active_users.keys():
                client_ip, client_port = client_sock.getpeername()
                try:
                    self.database.user_login(message[USER][SENDER], client_ip, client_port, message[USER][PASSWORD])
                except ServerError as e:
                    answer = {
                        RESPONSE: 400,
                        ACTION: PRESENCE,
                        ERROR: e.text,
                    }
                    send_message(client_sock, answer)
                    self.all_clients.remove(client_sock)
                    client_sock.close()
                else:
                    self.active_users[message[USER][SENDER]] = {
                        'socket': client_sock,
                        'ip_addr': client_ip,
                        'port': client_port,
                        'login_time': datetime.datetime.now()
                    }

                    answer = {
                        RESPONSE: 200,
                        ACTION: PRESENCE
                    }
                    send_message(client_sock, answer)

            else:
                answer = {
                    ACTION: PRESENCE,
                    RESPONSE: 400,
                    ERROR: 'Пользователь уже подключен',
                }

                send_message(client_sock, answer)
                self.all_clients.remove(client_sock)
                client_sock.close()
            return

        # ------------------------ Разбор запроса списка контактов пользователя ------------------------ #
        elif (ACTION and TIME and SENDER) in message \
                and message[ACTION] == GET_USERS_PACKAGE:
            contacts = {contact: 'online' for contact in self.database.get_contacts(message[SENDER])
                        if contact in list(self.active_users.keys())}
            offline_contacts = {contact: 'offline' for contact in self.database.get_contacts(message[SENDER])
                                if contact not in list(self.active_users.keys())}
            contacts.update(offline_contacts)

            messages_history = self.database.get_messages_history(message[SENDER])
            print(messages_history)

            answer = {
                RESPONSE: 202,
                CONTACTS: contacts,
                MESSAGE_HISTORY: messages_history
            }
            send_message(client_sock, answer)
            return

        # ------------------------ Разбор запроса списка всех пользователей ------------------------ #
        elif (ACTION and TIME and SENDER) in message \
                and message[ACTION] == GET_ALL_USERS:
            users = [user for user in self.database.get_all_users() if user != message[SENDER]]
            answer = {
                RESPONSE: 200,
                SENDER: SERVER,
                ACTION: GET_ALL_USERS,
                ALL_USERS: users,
                MESSAGE_TEXT: f'GET_ALL_USERS for {message[SENDER]}'
            }
            send_message(client_sock, answer)
            return

        # ------------------------ Разбор ADD_CONTACT - добавление пользователя ------------------------ #
        elif (ACTION and TIME and SENDER) in message \
                and message[ACTION] == ADD_CONTACT:
            self.database.add_contact(message[SENDER], message[ACCOUNT_NAME])
            answer = {
                RESPONSE: 200,
                SENDER: SERVER,
                ACTION: ADD_CONTACT,
                ACCOUNT_NAME: message[ACCOUNT_NAME],
                MESSAGE_TEXT: f'Пользователь {message[ACCOUNT_NAME]} добавлен в контакты'
            }
            send_message(client_sock, answer)
            return

        # ------------------------ Разбор REMOVE_CONTACT - удаление пользователя ------------------------ #
        elif (ACTION and TIME and SENDER) in message \
                and message[ACTION] == REMOVE_CONTACT:
            self.database.remove_contact(message[SENDER], message[ACCOUNT_NAME])
            answer = {
                RESPONSE: 200,
                SENDER: SERVER,
                ACTION: REMOVE_CONTACT,
                ACCOUNT_NAME: message[ACCOUNT_NAME],
                MESSAGE_TEXT: f'Пользователь {message[ACCOUNT_NAME]} удален из списка контактов'
            }
            send_message(client_sock, answer)
            return

        # ------------------------ Разбор отправленного сообщения ------------------------ #
        elif (ACTION and TIME and MESSAGE_TEXT and DESTINATION and SENDER) in message \
                and message[ACTION] == MESSAGE:
            datetime_ = datetime.datetime.now()

            self.database.save_message(
                message[SENDER],
                message[DESTINATION],
                message[MESSAGE_TEXT],
                message[MESSAGE_ID],
                datetime_
            )
            log.SERVER_LOG.info(f'msg id:{message[MESSAGE_ID]} from {message[SENDER]} save to db')

            answer = {
                RESPONSE: 200,
                SENDER: SERVER,
                ACTION: MESSAGE,
                MESSAGE_ID: message[MESSAGE_ID],
                MESSAGE_DATETIME: f'{datetime_}'
            }
            send_message(client_sock, answer)
            log.SERVER_LOG.debug('send 200 & datetime: ', answer)

            message[TIME] = f'{datetime_}'
            self.all_messages.append(message)

            return

        # ------------------------ Разбор сообщения о выходе ------------------------ #
        elif (ACTION and SENDER) in message \
                and message[ACTION] == EXIT:
            print(f'exit {message[SENDER]}')
            # self.database.user_logout(message[SENDER])
            self.all_clients.remove(self.active_users[message[SENDER]]['socket'])
            self.active_users[message[SENDER]]['socket'].close()
            del self.active_users[message[SENDER]]
            return
        else:
            answer = {
                RESPONSE: 400,
                ERROR: 'Bad Request',
                'msg': message
            }
            send_message(client_sock, answer)
            return

    def run(self):
        print('Консольный месседжер. Серверный модуль.')

        # поключение к сокету и обмен данными
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(TIMEOUT)
        self.sock.listen(MAX_CONNECTION)

        while True:
            try:
                # Проверка на подключение
                client_sock, client_addr = self.sock.accept()

            except OSError:
                # log.SERVER_LOG.error(f'{OSError}')
                pass

            else:
                log.SERVER_LOG.info(f'Connecting {client_addr} started')
                # вносим в список добавившегося клиента
                self.all_clients.append(client_sock)

            finally:

                clients_read, clients_write, errors = [], [], []

                try:
                    clients_read, clients_write, errors = select.select(self.all_clients, self.all_clients, [], 0)
                    log.SERVER_LOG.debug(f'Clients: {self.all_clients}')
                except Exception:
                    pass

                if clients_read:
                    for client_with_message in clients_read:
                        try:
                            message = get_message(client_with_message)
                            self.process_client_message(message, client_with_message)
                        except:
                            log.SERVER_LOG.info(f'Client {client_with_message.getpeername()} disconnected.')
                            self.all_clients.remove(client_with_message)

                for msg in self.all_messages:
                    if msg[DESTINATION] in self.active_users \
                            and self.active_users[msg[DESTINATION]]['socket'] in clients_write:
                        send_message(self.active_users[msg[DESTINATION]]['socket'], msg)
                        log.SERVER_LOG.info(f'Sending message from {msg[SENDER]} to {msg[DESTINATION]}')
                    elif msg[DESTINATION] in self.active_users \
                            and self.active_users[msg[DESTINATION]]['socket'] not in clients_write:
                        raise ConnectionError
                    else:
                        log.SERVER_LOG.error(
                            f'{msg[DESTINATION]} not found!!. {self.active_users}')
                self.all_messages.clear()


def main():
    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_host, port = arg_parser(DEFAULT_HOST, DEFAULT_PORT)

    # Инициализация базы данных
    database = ServerDB()

    # listen_host, port = arg_parser()
    # database = ServerDB()

    server = Server(listen_host, port, database)
    server.daemon = True
    server.start()

    start_gui(server.active_users)

    print(server.active_users)


if __name__ == '__main__':
    main()
