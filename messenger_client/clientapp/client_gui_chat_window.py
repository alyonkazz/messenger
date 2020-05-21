# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientapp\client_gui_chat_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(684, 509)
        Dialog.setToolTip("")
        self.list_contacts = QtWidgets.QListWidget(Dialog)
        self.list_contacts.setGeometry(QtCore.QRect(10, 10, 251, 361))
        self.list_contacts.setObjectName("list_contacts")
        self.list_msgs = QtWidgets.QListWidget(Dialog)
        self.list_msgs.setGeometry(QtCore.QRect(270, 10, 401, 301))
        self.list_msgs.setObjectName("list_msgs")
        self.pushButton_send_msg = QtWidgets.QPushButton(Dialog)
        self.pushButton_send_msg.setGeometry(QtCore.QRect(600, 330, 71, 71))
        self.pushButton_send_msg.setObjectName("pushButton_send_msg")
        self.text_new_msg = QtWidgets.QTextEdit(Dialog)
        self.text_new_msg.setGeometry(QtCore.QRect(270, 320, 321, 91))
        self.text_new_msg.setObjectName("text_new_msg")
        self.line_find_contact = QtWidgets.QLineEdit(Dialog)
        self.line_find_contact.setGeometry(QtCore.QRect(10, 380, 251, 31))
        self.line_find_contact.setText("")
        self.line_find_contact.setObjectName("line_find_contact")
        self.list_add_contact = QtWidgets.QListWidget(Dialog)
        self.list_add_contact.setGeometry(QtCore.QRect(10, 420, 251, 71))
        self.list_add_contact.setObjectName("list_add_contact")
        self.pushButton_bold = QtWidgets.QPushButton(Dialog)
        self.pushButton_bold.setGeometry(QtCore.QRect(270, 420, 101, 23))
        self.pushButton_bold.setObjectName("pushButton_bold")
        self.pushButton_italic = QtWidgets.QPushButton(Dialog)
        self.pushButton_italic.setGeometry(QtCore.QRect(380, 420, 101, 23))
        self.pushButton_italic.setObjectName("pushButton_italic")
        self.pushButton_underlined = QtWidgets.QPushButton(Dialog)
        self.pushButton_underlined.setGeometry(QtCore.QRect(490, 420, 101, 23))
        self.pushButton_underlined.setObjectName("pushButton_underlined")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_send_msg.setText(_translate("Dialog", "Отправить"))
        self.line_find_contact.setPlaceholderText(_translate("Dialog", "Введите имя пользователя"))
        self.list_add_contact.setToolTip(_translate("Dialog", "Для добавления пользователя дважды кликните по его имени"))
        self.pushButton_bold.setText(_translate("Dialog", "полужирный"))
        self.pushButton_italic.setText(_translate("Dialog", "курсив"))
        self.pushButton_underlined.setText(_translate("Dialog", "подчеркивание"))
