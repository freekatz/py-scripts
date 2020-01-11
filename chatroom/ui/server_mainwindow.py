# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(397, 493)
        MainWindow.setStyleSheet("background-color: rgb(255, 170, 0);\n"
"background-color: rgb(85, 255, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.serverEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.serverEdit.setGeometry(QtCore.QRect(30, 30, 331, 311))
        self.serverEdit.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.serverEdit.setObjectName("serverEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 81, 16))
        self.label.setStyleSheet("font: 9pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.beginServer = QtWidgets.QPushButton(self.centralwidget)
        self.beginServer.setGeometry(QtCore.QRect(210, 370, 151, 51))
        self.beginServer.setStyleSheet("background-color: rgb(0, 170, 127);\n"
"border-color: rgb(0, 0, 0);")
        self.beginServer.setObjectName("beginServer")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 397, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "服务器Log"))
        self.beginServer.setText(_translate("MainWindow", "连接聊天服务器"))

