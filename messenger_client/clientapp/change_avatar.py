import os
import sys

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction, QPushButton
from PyQt5.QtGui import QPixmap


class ChangeAvatar(QMainWindow):

    def __init__(self, parent=None):
        super(ChangeAvatar, self).__init__(parent)

        self.parent = parent

        self.menu()

    def menu(self):
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('Файл')
        self.editMenu = self.menubar.addMenu('Изменить изображение')
        self.editMenu.setEnabled(False)
        self.resize(500, 500)

        self.openAction = QAction('Открыть изображение', self)
        self.openAction.triggered.connect(self.open_image)
        self.fileMenu.addAction(self.openAction)

        self.save_image_action = QAction('Сохранить', self)
        self.save_image_action.setEnabled(False)
        self.save_image_action.triggered.connect(self.save_image)
        self.fileMenu.addAction(self.save_image_action)

        convert_to_grey_action = QAction('Оттенки серого', self)
        convert_to_grey_action.triggered.connect(lambda: self.convert_image(self.to_grey))
        self.editMenu.addAction(convert_to_grey_action)

        convert_to_sepia_action = QAction('Эффект сепии', self)
        convert_to_sepia_action.triggered.connect(lambda: self.convert_image(self.to_sepia))
        self.editMenu.addAction(convert_to_sepia_action)

        convert_to_negative_action = QAction('Эффект негатива', self)
        convert_to_negative_action.triggered.connect(lambda: self.convert_image(self.to_negative))
        self.editMenu.addAction(convert_to_negative_action)

        convert_to_black_and_white_action = QAction('Черно-белое изображение', self)
        convert_to_black_and_white_action.triggered.connect(lambda: self.convert_image(self.to_black_and_white))
        self.editMenu.addAction(convert_to_black_and_white_action)

        convert_to_original_action = QAction('Отменить изменения', self)
        convert_to_original_action.triggered.connect(lambda: self.convert_image(self.to_original))
        self.editMenu.addAction(convert_to_original_action)

        self.label = QLabel()
        self.setCentralWidget(self.label)

    def open_image(self):
        self.image_path = QFileDialog.getOpenFileName(self, 'Open file',
                                                      '/', "Images (*.png *.xpm *.jpg)")[0]

        self.convert_image(lambda: self.convert_image(self.to_original))

        if self.image_path:
            self.editMenu.setEnabled(True)
            self.save_image_action.setEnabled(True)

    def convert_image(self, convert_action):
        image = Image.open(self.image_path)
        self.draw = ImageDraw.Draw(image)
        self.width = image.size[0]
        self.height = image.size[1]
        self.pix = image.load()

        convert_action()

        self.img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(self.img_tmp)

        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())
        self.adjustSize()

    def to_grey(self):

        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                S = (a + b + c) // 3
                self.draw.point((i, j), (S, S, S))

    def to_sepia(self):
        depth = 30
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                S = (a + b + c)
                a = S + depth * 2
                b = S + depth
                c = S
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                self.draw.point((i, j), (a, b, c))

    def to_negative(self):

        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                self.draw.point((i, j), (255 - a, 255 - b, 255 - c))

    def to_black_and_white(self):
        factor = 50
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                S = a + b + c
                if (S > (((255 + factor) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                self.draw.point((i, j), (a, b, c))

    def to_original(self):
        self.image_path

    def save_image(self):
        # TODO название аватара - ник
        name = '1111'
        new_img_name = os.path.join('../static', name + '.png')
        self.img_tmp.save(new_img_name, 'PNG')
        self.parent.label_avatar.setPixmap(QPixmap(new_img_name))
        self.close()


def main():
    app = QApplication(sys.argv)
    win = ChangeAvatar()
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
