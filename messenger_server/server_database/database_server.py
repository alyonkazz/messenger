"""
Начать реализацию класса «Хранилище» для серверной стороны. Хранение необходимо осуществлять в базе данных.
В качестве СУБД использовать sqlite. Для взаимодействия с БД можно применять ORM.
Опорная схема базы данных:
На стороне сервера БД содержит следующие таблицы:
a) клиент:
* логин;
* информация.
b) историяклиента:
* время входа;
* ip-адрес.
c) списокконтактов (составляется на основании выборки всех записей с id_владельца):
* id_владельца;
* id_клиента.
"""
import sys
import datetime
import hashlib

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Boolean, or_
# Для использования декларативного стиля необходима функция declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sys.path.append('../messenger/messenger_server/')
from serverapp.errors import ServerError
from server_config.settings import POOL_RECYCLE, SERVER_DATABASE, ROOT_PATH, COMMON_CHAT, COMMON_CHAT_PWD


class ServerDB:
    base = declarative_base()

    class AllUsers(base):
        """ Все пользователи месенджера """
        __tablename__ = 'All_users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
        last_login = Column(DateTime)
        password = Column(String)

        def __init__(self, username, last_login, password):
            self.username = username
            self.last_login = last_login
            self.password = password

        def __repr__(self):
            return f'<User({self.username}, {self.last_login}, {self.password})>'

    class UsersContacts(base):
        """ Контакты пользователей """
        __tablename__ = 'Users_contacts'
        id = Column(Integer, primary_key=True)
        username = Column(ForeignKey('All_users.id'))
        contact = Column(String)
        last_msg = Column(DateTime)

        def __init__(self, username, contact, last_msg):
            self.username = username
            self.contact = contact
            self.last_msg = last_msg

        def __repr__(self):
            return f'<User({self.username}, {self.contact}, {self.last_msg})>'

    class LoginHistory(base):
        """ История входов пользоватлей """
        __tablename__ = 'Users_login_history'
        id = Column(Integer, primary_key=True)
        username = Column(ForeignKey('All_users.id'))
        login_time = Column(DateTime)
        ip_address = Column(String)
        port = Column(Integer)

        def __init__(self, username, login_time, ip_address, port):
            self.username = username
            self.login_time = login_time
            self.ip_address = ip_address
            self.port = port

        def __repr__(self):
            return f'<User({self.username}, {self.login_time}, {self.ip_address}, {self.port})>'

    class MessagesHistory(base):
        __tablename__ = 'Messages_history'
        id = Column(Integer, primary_key=True)
        from_ = Column(String)
        to = Column(String)
        message = Column(Text)
        message_id = Column(Integer)
        date = Column(DateTime)
        accepted = Column(Boolean)

        def __init__(self, contact, direction, message, message_id, date, accepted):
            self.from_ = contact
            self.to = direction
            self.message = message
            self.message_id = message_id
            self.date = date
            self.accepted = accepted

        def __repr__(self):
            return f'<User({self.from_}, {self.to}, {self.message}, {self.message_id}, {self.date}, {self.accepted})>'

    def __init__(self):
        self.engine = create_engine(f'sqlite:///{ROOT_PATH}/server_database/{SERVER_DATABASE}',
                                    echo=False,
                                    pool_recycle=POOL_RECYCLE,
                                    connect_args={'check_same_thread': False})

        # Создаём таблицы
        self.base.metadata.create_all(self.engine)

        session = sessionmaker(bind=self.engine)
        self.session = session()

        self.add_common_chat_when_creating_db()

    def add_common_chat_when_creating_db(self):
        if not self.session.query(self.AllUsers).filter_by(username=COMMON_CHAT).count():
            self.user_registration(COMMON_CHAT, COMMON_CHAT_PWD)
            self.session.commit()

    def user_registration(self, name, password):

        check_user = self.session.query(self.AllUsers).filter_by(username=name)
        # если логин пользователя используется, создаем ошибку
        if check_user.count():
            raise ServerError(f'Пользователь с логином "{name}" уже существует')

        # если нет, добавляем его в список пользователей
        else:
            b_pass = bytes(password, encoding='utf-8')

            salt = name.lower().encode('utf-8')
            sha_pass = hashlib.pbkdf2_hmac('sha1', b_pass, salt, 1000)
            sha_pass_str = sha_pass.hex()

            user = self.AllUsers(name, datetime.datetime.now(), sha_pass_str)
            self.session.add(user)
            self.session.commit()

            self.add_contact(name, COMMON_CHAT)
            self.session.commit()

    def user_login(self, name, ip_address, port, password):

        # --------------------- проверка наличия пользователя в списке пользователей // начало --------------------- #

        check_user = self.session.query(self.AllUsers).filter_by(username=name)
        # если пользователь уже подключался ранее, обновляем дату последнего логина
        if check_user.count():
            user = check_user.first()

            b_pass = bytes(password, encoding='utf-8')

            salt = name.lower().encode('utf-8')
            sha_pass = hashlib.pbkdf2_hmac('sha1', b_pass, salt, 1000)
            sha_pass_str = sha_pass.hex()

            if user.password == sha_pass_str:
                user.last_login = datetime.datetime.now()
            else:
                raise ServerError('Введенные логин и пароль не совпадают')

        # если нет, возвращаем ошибку
        else:
            raise ServerError(f'Пользователь с логином "{name}" не существует. Зарегистрируйтесь')

        # --------------------- проверка наличия пользователя в списке пользователей // конец --------------------- #

        # добавляем текущий заход пользователя в общий список логинов
        user_history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(user_history)

        # сохраняем всю информацию в базу
        self.session.commit()

    def get_active_users(self):
        # Возвращаем список имен активных пользователей
        return self.session.query(self.AllUsers.username).join(self.ActiveUsers).all()

    def get_all_users(self):
        # Возвращаем список имен всех пользователей
        return [user[0] for user in self.session.query(self.AllUsers.username).all()]

    def add_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(username=user).first()
        contact = self.session.query(self.AllUsers).filter_by(username=contact).first()

        # Проверяем что не дубль и что контакт может существовать (полю пользователь мы доверяем)
        if not contact \
                or self.session.query(self.UsersContacts).filter_by(username=user.id,
                                                                    contact=contact.id).count():
            return

        # Создаём объект и заносим его в базу
        new_contact = self.UsersContacts(user.id, contact.id, datetime.datetime.now())
        self.session.add(new_contact)
        self.session.commit()

    def remove_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(username=user).first()
        contact = self.session.query(self.AllUsers).filter_by(username=contact).first()

        # Если контакт существует, удаляем его
        if contact:
            self.session.query(self.UsersContacts).filter(
                self.UsersContacts.username == user.id,
                self.UsersContacts.contact == contact.id
            ).delete()
            self.session.commit()

    def get_contacts(self, username):
        user = self.session.query(self.AllUsers).filter_by(username=username).one()
        contacts = self.session.query(self.UsersContacts, self.AllUsers.username). \
            filter_by(username=user.id).join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)

        return [contact[1] for contact in contacts.all()]

    def save_message(self, from_, to, message, message_id, date, accepted=False):
        new_msg = self.MessagesHistory(from_, to, message, message_id, date, accepted)
        self.session.add(new_msg)
        self.session.commit()

    def get_messages_history(self, contact):
        msgs_history = self.session.query(self.MessagesHistory).filter(
            or_(self.MessagesHistory.from_ == contact,
                self.MessagesHistory.to == contact,
                self.MessagesHistory.from_ == COMMON_CHAT,
                self.MessagesHistory.to == COMMON_CHAT),
        )

        return [
            [history_row.from_,
             history_row.to,
             history_row.message,
             history_row.date.strftime("%Y-%m-%d-%H.%M.%S")]
            for history_row in msgs_history.all()
        ]


if __name__ == '__main__':
    server_db = ServerDB()
    # server_db.user_registration("22222", '11')
    # test_db.user_login("client1", '192.168.1.4', 8888, '11')
    # test_db.user_logout("client2")
    # test_db.user_login("client2", '192.168.1.4', 8888)
    # print(test_db.get_active_users())
    # print(test_db.get_contacts('test1'))
    # print(server_db.get_all_users())
    # server_db.save_message('from_', 'to', 'message', 1, datetime.datetime.now())
    print(server_db.get_messages_history('t2'))
