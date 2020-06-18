import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
# Для использования декларативного стиля необходима функция declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common_variables import POOL_RECYCLE, ROOT_PATH


class DBController:
    base = declarative_base()

    # таблица со списком контактов
    class Contacts(base):
        __tablename__ = 'Contacts'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, username):
            self.username = username

        def __repr__(self):
            return f'<User({self.username})>'

    # таблица истории сообщений
    class MessagesHistory(base):
        __tablename__ = 'Messages_history'
        id = Column(Integer, primary_key=True)
        from_ = Column(String)
        to = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, from_, to, message, date):
            self.from_ = from_
            self.to = to
            self.message = message
            self.date = date

        def __repr__(self):
            return f'<User({self.from_}, {self.to}, {self.message}, {self.date})>'

    def __init__(self, name):
        self.engine = create_engine(f'sqlite:///{ROOT_PATH}/client_database/client_{name}.db3',
                                    echo=False,
                                    pool_recycle=POOL_RECYCLE,
                                    connect_args={'check_same_thread': False})

        # Создаём таблицы
        self.base.metadata.create_all(self.engine)

        session = sessionmaker(bind=self.engine)
        self.session = session()

        # при запуске БД очищаем список контактов
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # Функция добавления списка контактов при подключении базы
    def fill_contacts(self, contacts):
        for contact in contacts:
            self.add_contact(contact)

    # Функция добавления нового контакта
    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(username=contact).count():
            new_contact = self.Contacts(contact)
            self.session.add(new_contact)
            self.session.commit()

    # Функция удаления контакта
    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(username=contact).delete()
        self.session.commit()

    # Функция, сохраняющяя сообщения
    def save_message(self, from_, to, message):
        new_message = self.MessagesHistory(from_, to, message, datetime.datetime.now())
        self.session.add(new_message)
        self.session.commit()

    # Функция возвращающяя контакты
    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.username).all()]

    # Функция возвращающая историю переписки
    def get_history(self, contact):
        query = self.session.query(self.MessagesHistory).filter_by(contact=contact)
        return [
            [history_row.from_,
             history_row.to,
             history_row.message,
             history_row.date.strftime("%Y-%m-%d-%H.%M.%S")]
            for history_row in query.all()
        ]


if __name__ == '__main__':
    test_db = DBController('test1')
    # test_db.add_contact('test2')
    # test_db.fill_contacts(['test3', 'test4'])
    # test_db.del_contact('n')
    # test_db.save_message('test1', 'test2', 'in_msg')
    # print(test_db.get_history('test1'))
    print(test_db.get_contacts())
