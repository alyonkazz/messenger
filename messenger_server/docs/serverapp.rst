Server module
=================================================

Серверный модуль мессенджера. Обрабатывает словари - сообщения, хранит публичные ключи клиентов.

Использование

Модуль подерживает аргементы командной стороки:

1. -p - Порт на котором принимаются соединения
2. -a - Адрес с которого принимаются соединения.
3. --no_gui Запуск только основных функций, без графической оболочки.

* В данном режиме поддерживается только 1 команда: exit - завершение работы.

Примеры использования:

``python server.py -p 8080``

*Запуск сервера на порту 8080*

``python server.py -a localhost``

*Запуск сервера принимающего только соединения с localhost*

server.py
~~~~~~~~~

Запускаемый модуль,содержит парсер аргументов командной строки и функционал инициализации приложения.

server. **arg_parser** ()
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов:

	* адрес с которого принимать соединения
	* порт
	
.. autoclass:: serverapp.server.Server
	:members:

database_server.py
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: serverapp.database.ServerStServerDBorage
	:members:

decorators.py
~~~~~~~~~~~~~~

serverapp.decorators. **func_to_log** (server)


	Функция приёма записи логов.
	
serverapp.decorators. **login_required** (server)


	Функция проверки, что клиент авторизован на сервере
	Проверяет, что передаваемый объект сокета находится в списке клиентов. Если его там нет закрывает сокет

descrptrs_server.py
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: serverapp.descrptrs_server.GetPort
	:members:
	
Скрипт errors.py
---------------------
   
.. autoclass:: serverapp.errors.ServerError
   :members:

metaclss_server.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: serverapp.metaclss_server.ServerVerifier
	:members:
