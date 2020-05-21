import os
import sys

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.menu()

    def menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Файл')
        self.editMenu = menubar.addMenu('Изменить изображение')
        self.editMenu.setEnabled(False)
        self.resize(500, 500)

        openAction = QAction('Открыть изображение', self)
        openAction.triggered.connect(self.open_image)
        fileMenu.addAction(openAction)

        closeAction = QAction('Выход', self)
        closeAction.triggered.connect(self.close)
        fileMenu.addAction(closeAction)

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
        self.image_path = QFileDialog.getOpenFileName(self, 'Open file', os.path.abspath(__file__), "Images (*.png *.xpm *.jpg)")[0]
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())
        self.adjustSize()

        if self.image_path:
            self.editMenu.setEnabled(True)

    def convert_image(self, convert_action):
        image = Image.open(self.image_path)
        self.draw = ImageDraw.Draw(image)
        self.width = image.size[0]
        self.height = image.size[1]
        self.pix = image.load()

        convert_action()

        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)

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


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
