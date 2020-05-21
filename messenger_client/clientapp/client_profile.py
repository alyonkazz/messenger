import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QAction, QFileDialog

from change_image.change_image import ChangeImage
from clientapp import client_profile_gui as desing


class ClientProfile(QMainWindow, desing.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.pushButton_edit_avatar.clicked.connect(self.edit_avatar)

    def edit_avatar(self):
        self.change_image = ChangeImage()

        save_avatar_action = QAction('Сохранить', self)
        save_avatar_action.triggered.connect(self.save_edit)
        self.change_image.fileMenu.addAction(save_avatar_action)

        self.change_image.show()

    def save_edit(self):
        print(self.change_image.image_path)
        # TODO название аватара - ник
        name = '1111'
        new_img_name = os.path.join('../static', name + '.png')
        self.change_image.img_tmp.save(new_img_name, 'PNG')
        self.change_image.close()

        self.label_avatar.setPixmap(QtGui.QPixmap(new_img_name))


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ClientProfile()  # Создаём объект класса ClientApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
