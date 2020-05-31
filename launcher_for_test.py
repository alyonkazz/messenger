import sys
import subprocess

from PyQt5.QtWidgets import (QGridLayout, QPushButton, QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QCheckBox)

from messenger_server.server_config.settings import DEFAULT_HOST, DEFAULT_PORT
from messenger_server.server_database.database_server import ServerDB
from messenger_server.serverapp.errors import ServerError

interpreter = 'python3'


class LauncherForTest(QMainWindow):

    def __init__(self, parent=None):
        super(LauncherForTest, self).__init__(parent)

        self.process = []

        self.setWindowTitle('Launcher for test')

        widget = QWidget()
        grid_layout = QGridLayout()

        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)

        label_host = QLabel('Хост: ')
        grid_layout.addWidget(label_host, 1, 1)

        self.line_host = QLineEdit(DEFAULT_HOST)
        grid_layout.addWidget(self.line_host, 1, 2)

        label_port = QLabel('Порт: ')
        grid_layout.addWidget(label_port, 2, 1)

        self.line_port = QLineEdit(f'{DEFAULT_PORT}')
        grid_layout.addWidget(self.line_port, 2, 2)

        label_clients_count = QLabel('Количество клиентов: ')
        grid_layout.addWidget(label_clients_count, 3, 1)

        self.line_clients_count = QLineEdit('2')
        grid_layout.addWidget(self.line_clients_count, 3, 2)

        self.check_box_client = QCheckBox('Показать консоль клиента')
        grid_layout.addWidget(self.check_box_client, 4, 1)

        self.check_box_server = QCheckBox('Показать консоль сервера')
        grid_layout.addWidget(self.check_box_server, 5, 1)

        p_button_run_messenger = QPushButton('Подключиться')
        grid_layout.addWidget(p_button_run_messenger, 6, 1)
        p_button_run_messenger.clicked.connect(self.run_messenger)

        p_button_close_wins = QPushButton('Закрыть все окна')
        grid_layout.addWidget(p_button_close_wins, 6, 2)
        p_button_close_wins.clicked.connect(self.close_wins)

    def run_messenger(self):
        creationflags_client = 0
        creationflags_server = 0

        if self.check_box_client.isChecked():
            creationflags_client = subprocess.CREATE_NEW_CONSOLE

        if self.check_box_server.isChecked():
            creationflags_server = subprocess.CREATE_NEW_CONSOLE

        self.process.append(subprocess.Popen([f'{interpreter}', '../messenger/messenger_server/server.py'],
creationflags=creationflags_server))

        for i in range(int(self.line_clients_count.text())):

            server_db = ServerDB()
            try:
                server_db.user_registration(f"test{i + 1}", '123')
            except:
                pass
            finally:
                self.process.append(subprocess.Popen([f'{interpreter}', '../messenger/messenger_client/client.py'],
                                                     creationflags=creationflags_client))

    def close_wins(self):
        while self.process:
            self.process.pop().kill()


def main():
    app = QApplication(sys.argv)
    win = LauncherForTest()
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
