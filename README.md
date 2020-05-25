1. Python 3.8.0

apt install python3.8-venv python3-venv
pip3 install --upgrade pip

Клонируем репозиторий 

git clone https://github.com/alyonkazz/messenger.git

Переходим в папку с проектом и создаем venv

cd messenger 
python3.8 -m venv venv

Проваливаемся в venv и устанавливаем зависимости 

source venv/bin/activate
pip3 install -r requirements.txt


Запуск сервера 

Из сновной папки messenger переходим в папку приложения 

cd messenger_server

Запускаем сервер 
python3.8 server.py

По умолчанию сервер доступен на 127.0.0.1:7777

Для запуска с указанием IP и порта 
python3.8 server.py --host xx.xx.xx.xx --port yyy

Логи по умочанию в папке ${appdir}/logs


Запуск клиента 

Из основной папки messenger переходим в папку приложения 
(если это новая терминальная сессия, не забываем перейти в venv, source venv/bin/activate)

cd messenger_client/

Запускаем клиент 
python3 client.py

По умолчанию подключается к 127.0.0.1:7777




______________________________________
pyuic5 clientapp\client_login.ui -o clientapp\client_gui_login.py

______________________________________ 
#TODO Добавить аватар в окно чата
#TODO 1. Сделать сохранение аватара в базу.
#TODO 2. Применить масштабирование к аватару и сохранить его в локальную базу.
#TODO 3. Применить обрезку к аватару и сохранить его в локальную базу.
#TODO 4. *Применить масштабирование и обрезку к аватару. Передать файл на сервер и записать его в базу.
#TODO 5. *Сделать сохранение в базу текстовых сообщений.
#TODO Добавить аватар в окно сообщений
