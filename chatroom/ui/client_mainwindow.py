# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(393, 492)
        MainWindow.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.msgEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.msgEdit.setGeometry(QtCore.QRect(20, 50, 351, 321))
        self.msgEdit.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"background-color: rgb(170, 170, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.msgEdit.setObjectName("msgEdit")
        self.connServer = QtWidgets.QPushButton(self.centralwidget)
        self.connServer.setGeometry(QtCore.QRect(250, 400, 121, 61))
        self.connServer.setStyleSheet("background-color: rgb(0, 170, 127);\n"
"border-color: rgb(0, 0, 0);")
        self.connServer.setObjectName("connServer")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 21))
        self.label.setStyleSheet("font: 9pt \"微软雅黑\";")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.msgEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.connServer.setText(_translate("MainWindow", "连接聊天服务器"))
        self.label.setText(_translate("MainWindow", "消息框"))

