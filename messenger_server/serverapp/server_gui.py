from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel, QFileDialog, \
    QHBoxLayout
from PyQt5.QtCore import QSize, Qt

from server_config.settings import DEFAULT_HOST, DEFAULT_PORT, SERVER_DATABASE


# Наследуемся от QMainWindow
class UsersStatistic(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self, users_json):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
        self.users_json = users_json

        self.setMinimumSize(QSize(480, 80))  # Устанавливаем размеры
        self.setWindowTitle("Список подключенных клиентов")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(4)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["Пользователь", "IP адрес", "Порт", "Последний логин"])

        # # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("Пользователь")
        self.table.horizontalHeaderItem(1).setToolTip("IP адрес")
        self.table.horizontalHeaderItem(2).setToolTip("Порт")
        self.table.horizontalHeaderItem(3).setToolTip("Последний логин")

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)

        # заполняем таблицу данными
        self.fill_table()

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        # refresh button
        refresh_btn = QPushButton('Обновить', self)
        refresh_btn.setToolTip('Обновить')
        refresh_btn.clicked.connect(self.fill_table)

        grid_layout.addWidget(self.table, 0, 0)  # Добавляем таблицу в сетку
        grid_layout.addWidget(refresh_btn, 0, 1)  # Добавляем кнопку Обновить в сетку

        # refresh timer
        self.timer_status = QtCore.QTimer()
        self.timer_status.timeout.connect(self.fill_table)

        # check every half-second
        self.timer_status.start(1000)

    def clear_table(self):
        self.table.clear()

    def fill_table(self):
        if len(self.users_json) == 0:
            self.table.setRowCount(1)  # Устанавливаем количество строк в таблице
            # заполняем первую строку
            self.table.setItem(0, 0, QTableWidgetItem(""))
            self.table.setItem(0, 1, QTableWidgetItem(""))
            self.table.setItem(0, 2, QTableWidgetItem(""))
        else:
            users_list = list(self.users_json.keys())

            self.table.setRowCount(len(users_list))  # Устанавливаем количество строк в таблице

            for i in range(len(users_list)):
                self.table.setItem(i, 0, QTableWidgetItem(users_list[i]))
                self.table.setItem(i, 1, QTableWidgetItem(self.users_json[users_list[i]]['ip_addr']))
                self.table.setItem(i, 2, QTableWidgetItem(str(self.users_json[users_list[i]]['port'])))
                self.table.setItem(i, 3,
                                   QTableWidgetItem(
                                       self.users_json[users_list[i]]['login_time'].strftime("%Y-%m-%d-%H.%M.%S")))


if __name__ == "__main__":
    import sys
    import datetime

    app = QApplication(sys.argv)
    dialog = StartServer()
    dialog.show()
    # dialog.exec_()

    all_users = {
        "client1": {
            'socket': "<socket.socket fd=784, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, "
                      "laddr=('127.0.0.1', 7777), raddr=('127.0.0.1', 50165)>",
            'ip_addr': '127.0.0.1',
            'port': 50165,
            'login_time': datetime.datetime(2020, 2, 28, 19, 25, 34, 276014)
        }
    }
    # mw = UsersStatistic(all_users)
    # mw.show()
    sys.exit(app.exec())

