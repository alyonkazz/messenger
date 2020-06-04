import asyncio
import functools
import os
import re
import sys  # sys нужен для передачи argv в QApplication
import threading
import time
from socket import AF_INET, SOCK_STREAM, socket

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtGui import QFont, QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QPushButton, QAbstractItemView, QAction, \
    QShortcut

import clientapp.client_chat_window_ui as desing
from client_config.utils import send_message, get_message
from clientapp.client_profile import ClientProfile
from client_database.database_client import ClientDB
from clientapp.decorators import func_to_log
from client_logs.client_log_config import CLIENT_LOG as log
from client_config.settings import ACTION, TIME, ACCOUNT_NAME, MESSAGE, \
    MESSAGE_TEXT, SENDER, DESTINATION, RESPONSE, ADD_CONTACT, REMOVE_CONTACT, \
    SERVER, GET_ALL_USERS, ALL_USERS, ROOT_PATH, STATIC_PATH


@func_to_log
def create_message(sock, database, acc_name, to_user, message):
    """ Отправка сообщения пользователю """
    message = {
        ACTION: MESSAGE,
        TIME: time.time(),
        SENDER: acc_name,
        DESTINATION: to_user,
        MESSAGE_TEXT: message
    }
    log.debug(f'Create message to {to_user}: {message}')

    send_message(sock, message)
    log.debug(f'Send message to {to_user}')

    database.save_message(message[DESTINATION], 'out', message[MESSAGE_TEXT])
    log.debug(f'Save message to {to_user}  to database')


@func_to_log
def users_list_request(sock, client_name):
    message = {
        ACTION: GET_ALL_USERS,
        TIME: time.time(),
        SENDER: client_name
    }
    log.debug(f'{client_name}: users_list_request created')

    send_message(sock, message)
    log.debug(f'{client_name}: users_list_request send')


@func_to_log
def add_contact_request(sock, client_name, new_contact):
    message = {
        ACTION: ADD_CONTACT,
        TIME: time.time(),
        SENDER: client_name,
        ACCOUNT_NAME: new_contact
    }
    log.debug(f'{client_name}: add_contact_request created')

    send_message(sock, message)
    time.sleep(0.5)
    log.debug(f'{client_name}: add_contact_request send')


@func_to_log
def remove_contact_request(sock, client_name, remove_account):
    message = {
        ACTION: REMOVE_CONTACT,
        TIME: time.time(),
        SENDER: client_name,
        ACCOUNT_NAME: remove_account
    }
    log.debug(f'{client_name}: remove_contact_request created')

    send_message(sock, message)
    log.debug(f'{client_name}: remove_contact_request send')


class ClientApp(QMainWindow, desing.Ui_MainWindow):
    all_users = []

    def __init__(self, client_name, sock, database):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.client_name = client_name
        self.sock = sock
        self.database = database

        # отправка сообщения
        self.pushButton_send_msg.clicked.connect(self.click_send)

        self.setWindowTitle(self.client_name)

        # заполняем список контактов и сообщений из базы
        self.fill_contacts()
        try:
            self.list_contacts.setCurrentRow(0)
            self.item_clicked_event(self.database.get_history(self.list_contacts.currentItem().text()))
        except:
            pass

        # выбор контакта в списке контактов
        self.list_contacts.itemClicked.connect(
            lambda: self.item_clicked_event(self.database.get_history(self.list_contacts.currentItem().text())))

        # поле поиска контактов
        self.list_add_contact.setHidden(True)
        self.line_search.textChanged.connect(self.search_slot)

        # получение сообщений
        client_process = threading.Thread(target=self.message_from_server)
        client_process.daemon = True
        client_process.start()

        self.list_contacts.installEventFilter(self)

        self.pushButton_bold.clicked.connect(self.actionBold)
        self.pushButton_italic.clicked.connect(self.actionItalic)
        self.pushButton_underlined.clicked.connect(self.actionUnderlined)

        self.action_profile.triggered.connect(self.open_profile)

        if os.path.exists(os.path.join(STATIC_PATH, self.client_name + '.png')):
            self.label_avatar.setPixmap(QtGui.QPixmap(os.path.join(STATIC_PATH, self.client_name)))
        else:
            self.label_avatar.setPixmap(QtGui.QPixmap(os.path.join(STATIC_PATH, 'defaul_avatar.jpg')))

        self.add_smiles()

        # поиск сообщений
        self.label_msg_not_found.setHidden(True)
        self.shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut.activated.connect(self.search_line_in_msgs)
        self.pushButton_search_up.setHidden(True)
        self.pushButton_search_down.setHidden(True)
        self.pushButton_search_cancel.setHidden(True)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Shift+F"), self)
        self.shortcut.activated.connect(self.search_all_lines_in_msgs)

    def search_all_lines_in_msgs(self):
        self.line_search.setPlaceholderText('Поиск во всём чате')
        self.line_search.setObjectName("line_find_msg")

        def find_this():
            search_obj = self.line_search.text()
            contact = self.list_contacts.currentItem().text()

            if search_obj:
                self.item_clicked_event(self.database.get_selection_from_history(contact, search_obj))

        self.line_search.returnPressed.connect(find_this)

    def search_line_in_msgs(self):
        self.line_search.setPlaceholderText('Поиск в чате')
        self.line_search.setObjectName("line_find_msg")

        self.pushButton_search_cancel.setHidden(False)

        def find_this():
            # TODO jump from last to previous found lines
            search_obj = self.line_search.text()
            search_obj = '.*' + search_obj + '.*'
            if search_obj:
                items = self.list_msgs.findItems(search_obj, QtCore.Qt.MatchRegExp)
                item_id = -1

                item = items[-1]

                def search_up(item_id):
                    item_id += 1
                    print(item_id)
                    return item_id

                if items:
                    if len(items) > 1:
                        self.pushButton_search_up.setHidden(False)
                        # self.pushButton_search_up.setCheckable(True)

                        print(item_id)

                        self.pushButton_search_down.setHidden(False)

                        item.setSelected(True)
                        self.list_msgs.scrollToItem(item, QAbstractItemView.PositionAtTop)
                        self.pushButton_search_up.clicked.connect(lambda: search_up(item_id))

                        # if self.pushButton_search_up.isChecked():
                        #     print('check')

                # item = self.list_msgs.findItems
                # (search_obj, QtCore.Qt.MatchRegExp)[0]
                # if item:
                #     item.setSelected(True)
                #     self.list_msgs.scrollToItem(item, QAbstractItemView.PositionAtTop)

        self.line_search.returnPressed.connect(find_this)

    def add_smiles(self):
        path_to_smiles = os.path.join(STATIC_PATH, 'smiles')

        for smile in os.listdir(path_to_smiles):
            url = os.path.join(path_to_smiles, smile)

            pushButton_smile = QPushButton(self.horizontalLayoutWidget)
            rMyIcon = QtGui.QPixmap(url)
            pushButton_smile.setIcon(QtGui.QIcon(rMyIcon))
            pushButton_smile.setObjectName(url)
            self.horizontalLayout.addWidget(pushButton_smile)

            pushButton_smile.clicked.connect(self.insert_smile)

    def insert_smile(self):
        # """
        # Returns the QPushButton instance
        # :param text: the button text
        # :return the QPushButton object
        # """
        clicked_button = self.sender()
        url = clicked_button.objectName()
        self.text_new_msg.insertHtml('<img src="%s" />' % url)

    def open_profile(self):
        self.ciient_profile = ClientProfile(self)
        self.ciient_profile.show()

    def actionBold(self):
        myFont = QFont()
        myFont.setBold(True)
        self.text_new_msg.setFont(myFont)

    def actionItalic(self):
        myFont = QFont()
        myFont.setItalic(True)
        self.text_new_msg.setFont(myFont)

    def actionUnderlined(self):
        myFont = QFont()
        myFont.setUnderline(True)
        self.text_new_msg.setFont(myFont)

    def item_clicked_event(self, user_msgs_history):
        # история сообщений с выбранными пользователем
        # TODO заменить sleep на проверку обработки ответа от сервера
        self.list_msgs.clear()  # очищаем окно чата

        if not user_msgs_history:
            self.list_msgs.addItem('Сообщений нет')

        for msg in user_msgs_history:
            if msg[1] == 'in':
                text_color = '#beaed4'
                text_align = QtCore.Qt.AlignLeft
                text_direction = 'от'
            elif msg[1] == 'out':
                text_color = 'yellow'
                text_align = QtCore.Qt.AlignRight
                text_direction = 'для'

            msg_info = QListWidgetItem(f'{msg[3]} Сообщение {text_direction} {msg[0]}:')
            msg_text = QListWidgetItem(f'{msg[2]}')
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            msg_info.setFont(font)
            msg_text.setFont(font)
            msg_info.setTextAlignment(text_align)
            msg_text.setTextAlignment(text_align)
            msg_info.setBackground(QtGui.QColor(text_color))
            msg_text.setBackground(QtGui.QColor(text_color))
            self.list_msgs.addItem(msg_info)
            self.list_msgs.addItem(msg_text)

            time.sleep(0.01)
            self.list_msgs.scrollToBottom()

    def get_selected_layers(self):
        selectedLayers = self.list_contacts.selectedItems()
        print(selectedLayers)

    def click_send(self):
        # отправка сообщений из поля ввода текста и его очищение
        contact = self.list_contacts.currentItem().text()
        text_message = self.text_new_msg.toPlainText()
        if text_message:
            create_message(self.sock, self.database, self.client_name, contact, text_message)
            self.text_new_msg.clear()
            self.item_clicked_event(self.database.get_history(self.list_contacts.currentItem().text()))
        else:
            log.warning('Attempting to send an empty message')

    def search_slot(self):
        # строка поиска контакта
        # TODO при введении 3х символов делать запрос к базе, от базы получать отсортированный список
        users_list_request(self.sock, self.client_name)
        time.sleep(0.5)
        if self.line_search.text() and self.line_search.objectName() == "line_search":
            user_name = self.line_search.text()
            regex = fr"^{user_name}"
            matching_names = [user for user in self.all_users if re.match(regex, user)]
            self.list_add_contact.setHidden(False)
            self.list_add_contact.clear()
            self.list_add_contact.addItems(matching_names)
            self.list_add_contact.doubleClicked.connect(self.add_new_contact)
        else:
            self.list_add_contact.setHidden(True)

    def add_new_contact(self):
        # добавление контакта в базу сервера, базу клиента и в gui
        new_contact = self.list_add_contact.currentItem().text()
        add_contact_request(self.sock, self.client_name, new_contact)

    def fill_contacts(self):
        # получаем список контактов для окна с контактами
        user_contacts = self.database.get_contacts()
        self.list_contacts.clear()
        self.list_contacts.addItems(user_contacts)

    def eventFilter(self, source, event):
        # удаление контакта из базы сервера, базы клиента и client gui
        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.list_contacts):
            menu = QtWidgets.QMenu()
            menu.addAction('Удалить контакт')
            if menu.exec_(event.globalPos()):
                remove_account = source.itemAt(event.pos()).text()
                remove_contact_request(self.sock, self.client_name, remove_account)
            return True
        return super(ClientApp, self).eventFilter(source, event)

    # @func_to_log
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
                        self.item_clicked_event(self.database.get_history(self.list_contacts.currentItem().text()))

                else:
                    log.error(f'Invalid message received from server: {message}')
            except KeyError:
                log.error(KeyError)


def main():
    server_host, server_port, client_name = '127.0.0.1', 7777, 'test1'
    sock = socket(AF_INET, SOCK_STREAM)
    database = ClientDB(client_name)

    app = QApplication(sys.argv)  # Новый экземпляр QApplication

    window = ClientApp(client_name, sock, database)  # Создаём объект класса ClientApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
