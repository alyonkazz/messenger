import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QAction, QFileDialog

from clientapp.change_avatar import ChangeAvatar
from clientapp import client_profile_gui as desing


class ClientProfile(QMainWindow, desing.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.pushButton_edit_avatar.clicked.connect(self.edit_avatar)

    def edit_avatar(self):
        self.change_image = ChangeAvatar(self)
        self.change_image.show()


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ClientProfile()  # Создаём объект класса ClientApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
