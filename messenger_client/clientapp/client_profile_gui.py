# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tmp\client_profile_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ChangeImage")
        MainWindow.resize(407, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_avatar = QtWidgets.QLabel(self.centralwidget)
        self.label_avatar.setGeometry(QtCore.QRect(120, 50, 151, 151))
        self.label_avatar.setText("")
        self.label_avatar.setPixmap(QtGui.QPixmap("static/defaul_avatar.jpg"))
        self.label_avatar.setScaledContents(True)
        self.label_avatar.setObjectName("label_avatar")
        self.label_username = QtWidgets.QLabel(self.centralwidget)
        self.label_username.setGeometry(QtCore.QRect(170, 300, 47, 13))
        self.label_username.setObjectName("label_username")
        self.pushButton_edit_avatar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_edit_avatar.setGeometry(QtCore.QRect(160, 220, 81, 31))
        self.pushButton_edit_avatar.setObjectName("pushButton_edit_avatar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 407, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("ChangeImage", "Профиль"))
        self.label_username.setText(_translate("ChangeImage", "username"))
        self.pushButton_edit_avatar.setText(_translate("ChangeImage", "Изменить\n"
"аватар"))
