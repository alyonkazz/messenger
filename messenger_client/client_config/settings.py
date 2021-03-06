import logging
import os

""" common settings """

# параметры для подключения по умолчанию
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 7777
MAX_CONNECTION = 1
TIMEOUT = 0.5

# тип кодировки
ENCODING = 'utf-8'

# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024

ROOT_PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
STATUS = 'status'
SENDER = 'sender'
DESTINATION = 'destination'
ALL_USERS = 'all_users'
ACTIVE_USERS = 'active_users'
CONTACTS = 'contacts'
MESSAGE_HISTORY = 'message_history'
PASSWORD = 'password'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
REGISTRATION = 'registration'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
MESSAGE_ID = 'message_id'
MESSAGE_DATETIME = 'message_datetime'
EXIT = 'exit'
GET_MESSAGES_HISTORY = 'get_messages_history'
GET_USERS_PACKAGE = 'get_users_package'
GET_ALL_USERS = 'get_all_users'
ADD_CONTACT = 'add_contact'
REMOVE_CONTACT = 'remove_contact'
SERVER = 'server'

""" logging """
LOG_DIR = os.path.join(ROOT_PATH, 'client_logs')
CLIENT_LOG_FILE = 'client.log'
SERVER_LOG_FILE = 'server.log'
LOGGING_LEVEL = logging.DEBUG

""" client database """
# CLIENT_DATABASE = f'sqlite:///client_{name}.db3'
POOL_RECYCLE = 3600

""" static """
STATIC_PATH = os.path.join(ROOT_PATH, 'static')
