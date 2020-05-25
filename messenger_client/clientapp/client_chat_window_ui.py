# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tmp\client_chat_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(686, 541)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_underlined = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_underlined.setGeometry(QtCore.QRect(490, 420, 101, 23))
        self.pushButton_underlined.setObjectName("pushButton_underlined")
        self.text_new_msg = QtWidgets.QTextEdit(self.centralwidget)
        self.text_new_msg.setGeometry(QtCore.QRect(270, 320, 321, 91))
        self.text_new_msg.setObjectName("text_new_msg")
        self.pushButton_italic = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_italic.setGeometry(QtCore.QRect(380, 420, 101, 23))
        self.pushButton_italic.setObjectName("pushButton_italic")
        self.list_add_contact = QtWidgets.QListWidget(self.centralwidget)
        self.list_add_contact.setGeometry(QtCore.QRect(10, 420, 251, 71))
        self.list_add_contact.setObjectName("list_add_contact")
        self.line_find_contact = QtWidgets.QLineEdit(self.centralwidget)
        self.line_find_contact.setGeometry(QtCore.QRect(10, 380, 251, 31))
        self.line_find_contact.setText("")
        self.line_find_contact.setObjectName("line_find_contact")
        self.list_contacts = QtWidgets.QListWidget(self.centralwidget)
        self.list_contacts.setGeometry(QtCore.QRect(10, 10, 251, 361))
        self.list_contacts.setObjectName("list_contacts")
        self.pushButton_bold = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_bold.setGeometry(QtCore.QRect(270, 420, 101, 23))
        self.pushButton_bold.setObjectName("pushButton_bold")
        self.pushButton_send_msg = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send_msg.setGeometry(QtCore.QRect(600, 330, 71, 71))
        self.pushButton_send_msg.setObjectName("pushButton_send_msg")
        self.list_msgs = QtWidgets.QListWidget(self.centralwidget)
        self.list_msgs.setGeometry(QtCore.QRect(270, 10, 401, 301))
        self.list_msgs.setObjectName("list_msgs")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(270, 450, 321, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 686, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_profile = QtWidgets.QAction(MainWindow)
        self.action_profile.setObjectName("action_profile")
        self.menuMenu.addAction(self.action_profile)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_underlined.setText(_translate("MainWindow", "подчеркивание"))
        self.pushButton_italic.setText(_translate("MainWindow", "курсив"))
        self.list_add_contact.setToolTip(_translate("MainWindow", "Для добавления пользователя дважды кликните по его имени"))
        self.line_find_contact.setPlaceholderText(_translate("MainWindow", "Введите имя пользователя"))
        self.pushButton_bold.setText(_translate("MainWindow", "полужирный"))
        self.pushButton_send_msg.setText(_translate("MainWindow", "Отправить"))
        self.menuMenu.setTitle(_translate("MainWindow", "Меню"))
        self.action_profile.setText(_translate("MainWindow", "Профиль"))
