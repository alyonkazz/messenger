import json
import time

from common_variables import ENCODING, MAX_PACKAGE_LENGTH
# from clientapp.decorators import func_to_log


# @func_to_log
def get_message(sock):
    """ загрузка ответа, если он в формате json """
    data = sock.recv(MAX_PACKAGE_LENGTH)
    try:
        js_data = json.loads(data)
        return js_data
    except json.JSONDecodeError:
        print('Не удалось декодировать полученную Json строку.')
        print(data)
        exit(1)


# @func_to_log
def send_message(sock, msg):
    """ кодировка json-сообщения и его отправка """
    js_msg = json.dumps(msg)
    enc_msg = js_msg.encode(ENCODING)
    sock.send(enc_msg)
    # time.sleep(0.2)

def message_from_server(self):
    """ Обработка сообщений от сервера и пользователей """
    while True:
        message = get_message(self.sock)
        try:
            # ------------------------ Разбор сообщений от сервера ------------------------ #
            if (RESPONSE and SENDER and MESSAGE_TEXT) in message \
                    and message[SENDER] == SERVER:

                if message[ACTION] == GET_ALL_USERS and message[RESPONSE] == 200:
                    ClientApp.all_users = message[ALL_USERS]

                elif message[ACTION] == ADD_CONTACT and message[RESPONSE] == 200:
                    self.database.add_contact(message[ACCOUNT_NAME])
                    self.fill_contacts()

                elif message[ACTION] == REMOVE_CONTACT and message[RESPONSE] == 200:
                    self.database.del_contact(message[ACCOUNT_NAME])
                    self.fill_contacts()

            # ------------------------ Разбор сообщений от других пользователей ------------------------ #
            elif (ACTION and SENDER and DESTINATION and MESSAGE_TEXT) in message \
                    and message[ACTION] == MESSAGE \
                    and message[DESTINATION] == self.client_name:
                msg = f'\nGet message from user {message[SENDER]}: {message[MESSAGE_TEXT]}'
                self.database.save_message(message[SENDER], 'in', message[MESSAGE_TEXT])
                log.info(msg)

                if self.list_contacts.currentItem() \
                        and self.list_contacts.currentItem().text() == message[SENDER]:
                    self.item_clicked_event()


            else:
                log.error(f'Invalid message received from server: {message}')
        except KeyError:
            log.error(KeyError)
