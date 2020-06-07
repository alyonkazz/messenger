1. Python 3.7
2. Mongo 4.2

### Клонируем репозиторий ###

git clone https://github.com/alyonkazz/messenger.git -b lesson5-6


### По необходимости: ###

apt install python3-venv
pip3 install --upgrade pip


### Переходим в папку с проектом и создаем venv ###

cd messenger
python3 -m venv venv


### Проваливаемся в venv и устанавливаем зависимости ###

source venv/bin/activate
pip3 install -r requirements.txt




_________________ Lesson5-6 _________________

*Для упрощения проверки домашки реализована работа с базой без авторизации.
При необходимости хост и порт можно изменить в kivy_mongo/mongo.py

Реализовано автоматическое наполнение базы данных из папки kivy_mongo/static (только при старте приложения).


### Для проверки ДЗ: ###

python3 kivy_mongo/kivy_start.py

Можно полистать изображения (подгружаются из базы, а не из папки),
кнопки блокируются в конце и начале списка соответственно.


______________________________________
pyuic5 clientapp\client_login.ui -o clientapp\client_gui_login.py

______________________________________ 


