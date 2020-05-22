Клонируем репозиторий 

git clone https://github.com/alyonkazz/messenger.git -b lesson1

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


Lesson1______________________________________
!!!!!! cd messenger_client/clientapp

1. Сделать программу, которая будет загружать изображения с компьютера и добавлять к ним эффекты.

change_image/change_image.py

Управление осуществляется через меню Файл/Изменить изображение:
  - Файл - Открыть изображение добавляет картинку в программу, активирует кнопки редактирования и сохранения изображения
  - Изменить изображения применяет выбранные эффекты
  - Сохранить сохраняет результат в папку со скриптом с подписью (converted)

2. Добавить форматирование в сообщения в вашем мессенджере.

messenger_client/clientapp/client_chat_window.py 
(можно запустить отдельно, ошибка треда не влияет проверяемый на функционал)

изменения шрифтов применяются кнопками "полужирный", "курсив", "подчеркнутый" (на картинки не заменила)
под полем ввода текста, в котором редактируют текст 

3. Реализовать возможность добавления фотографии в ваш профиль.

messenger_client/clientapp/client_chat_window.py 
(можно запустить отдельно, ошибка треда не влияет проверяемый на функционал)

Меню - Профиль (запускается messenger_client/clientapp/client_profile.py)
- Изменить аватар (запускается messenger_client/clientapp/change_avatar.py)

открывается окно аналогичное п.1, 
сохранение файла происходит в messenger_client/static  в формате имя_пользователя.png

при запуске окна профиля проверка наличия файла имя_пользователя.png подгружает его или
дефолтный аватар, если данный файл отсутствует

4. *Нужно сделать предыдущее задание и добавить смайлы в мессенджер.

messenger_client/clientapp/client_chat_window.py 
(можно запустить отдельно, ошибка треда не влияет проверяемый на функционал)

смайлики вставляются кнопками со смайликами, не стирая предыдующий текст.
Кнопки смайликов создаются динамически в зависимости от картинок в messenger_client/static/smiles

5. *Нужно сделать предыдущее задание и применить разные эффекты к изображению в профиле.

реализовано (п.3)

______________________________________
pyuic5 clientapp\client_login.ui -o clientapp\client_gui_login.py
