1. Python 3.7
2. Mongo 4.2

### Клонируем репозиторий ###

git clone https://github.com/alyonkazz/messenger.git -b kivy_client


### По необходимости: ###

apt install python3-venv
pip3 install --upgrade pip


### Переходим в папку с проектом и создаем venv ###

cd messenger
python3 -m venv venv


### Проваливаемся в venv и устанавливаем зависимости ###

source venv/bin/activate
pip3 install -r requirements.txt




_________________ Kv language _________________

There are three keywords specific to the Kv language:
    app: always refers to the instance of your application.
    root: refers to the base widget/template in the current rule
    self: always refer to the current widget


______________________________________
pyuic5 clientapp\client_login.ui -o clientapp\client_gui_login.py

______________________________________ 

https://python-scripts.com/kivy-android-ios-exe#kivy-install
#TODO 1. Создать графический интерфейс мессенджера на kivy.
#TODO 2. Сделать смайлы в интерфейсе мессенджера.
#TODO 3. Продолжить переносить базу данных приложения на mongodb.
#TODO 4. *Сделать игру «Крестики-нолики» или «Змейка».
#TODO 5. **Сделать текстовый редактор на kivy.

#TODO 2. Сделать чат для всех пользователей.
#TODO 4. *Сделать асинхронными все запросы к базе данных.
#TODO 5. *Сделать сохранение результатов поиска.
#TODO 6. *Сделать асинхронный поиск строки в тексте.

#TODO 1. В мессенджере сделать отправку сообщений серверу с помощью асинхронности.
#TODO 2. На сервере сделать асинхронное принятие сообщений от клиента.
#TODO 3. *На сервере сделать добавление записей в базу данных с помощью асинхронности.
#TODO 4. *Сделать удаление и редактирование записей в базе данных с помощью асинхронности.

#TODO 4. *Применить масштабирование и обрезку к аватару. Передать файл на сервер и записать его в базу.
#TODO 5. *Сделать сохранение в базу текстовых сообщений.

#TODO удалить сохранение аватара в файл и подтягивание аватара из файла
#TODO добавить автосохранение логина/пароля
#TODO добавить отмену поиска контакта/сообщения
#TODO поле поиска - если неактивно, очищать его
