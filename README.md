Клонируем репозиторий 

git clone https://github.com/alyonkazz/messenger.git

Переходим в папку с проектом и создаем venv

cd messenger 
python3 -m  venv venv

Проваливаемся в venv и устанавливаем зависимости 

source venv/bin/activate
pip3  install -r requirements.txt


Запуск сервера 

Из сновной папки messenger переходим в папку приложения 

cd messenger_server

Запускаем сервер 
python3 server.py

По умолчанию сервер доступен на 127.0.0.1:7777

Для запуска с указанием ИП и порта 
python3 server.py --host xx.xx.xx.xx --port yyy

Логи по умочанию в папке ${appdir}/logs


Запуск клиента 

Из основной папки messenger переходим в папку приложения (если это новая терминальная сессия не забываем перейти в vnen, source venv/bin/activate)

cd messenger_client/

Запускаем клиент 
python3 client.py

По умолчанию подключается к 127.0.0.1:7777




______________________________________
pyuic5 clientapp\client_login.ui -o clientapp\client_gui_login.py
