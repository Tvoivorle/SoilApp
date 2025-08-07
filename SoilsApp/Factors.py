# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Factors.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableView, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(984, 689)
        # Создаем дополнительный виджет для фона с градиентным стилем
        self.gradient_widget = QWidget(MainWindow)
        self.gradient_widget.setObjectName(u"gradient_widget")
        self.gradient_widget.setGeometry(QRect(0, 0, MainWindow.width(), MainWindow.height()))
        gradient_style = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(74,212,104,0.44), stop:1 rgba(58,136,45,0.64));"
        self.gradient_widget.setStyleSheet(gradient_style)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Df_choice_button = QPushButton(self.centralwidget)
        self.Df_choice_button.setObjectName(u"Df_choice_button")
        self.Df_choice_button.setGeometry(QRect(20, 10, 331, 31))
        self.Df_choice_button.setStyleSheet(u"QPushButton {\n"
"	box-shadow: 0px 10px 14px -7px #3e7327;\n"
"	background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);\n"
"	background-color:#77b55a;\n"
"	border-radius:4px;\n"
"	border:1px solid #4b8f29;\n"
"	display:inline-block;\n"
"	cursor:pointer;\n"
"	color:#ffffff;\n"
"	font-family:Arial;\n"
"	font-size:13px;\n"
"	font-weight:bold;\n"
"	padding:6px 12px;\n"
"	text-decoration:none;\n"
"	text-shadow:0px 1px 0px #5b8a3c;\n"
"}\n"
"QPushButton:hover {\n"
"	background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);\n"
"	background-color:#72b352;\n"
"}\n"
"QPushButton:active {\n"
"	position:relative;\n"
"	top:1px;\n"
"}\n"
"")
        self.Elbow_build_button = QPushButton(self.centralwidget)
        self.Elbow_build_button.setObjectName(u"Elbow_build_button")
        self.Elbow_build_button.setGeometry(QRect(20, 50, 331, 31))
        self.Elbow_build_button.setStyleSheet(u"QPushButton {\n"
"	box-shadow: 0px 10px 14px -7px #3e7327;\n"
"	background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);\n"
"	background-color:#77b55a;\n"
"	border-radius:4px;\n"
"	border:1px solid #4b8f29;\n"
"	display:inline-block;\n"
"	cursor:pointer;\n"
"	color:#ffffff;\n"
"	font-family:Arial;\n"
"	font-size:13px;\n"
"	font-weight:bold;\n"
"	padding:6px 12px;\n"
"	text-decoration:none;\n"
"	text-shadow:0px 1px 0px #5b8a3c;\n"
"}\n"
"QPushButton:hover {\n"
"	background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);\n"
"	background-color:#72b352;\n"
"}\n"
"QPushButton:active {\n"
"	position:relative;\n"
"	top:1px;\n"
"}\n"
"")
        self.ElbowView = QGraphicsView(self.centralwidget)
        self.ElbowView.setObjectName(u"ElbowView")
        self.ElbowView.setGeometry(QRect(20, 91, 331, 221))
        self.Factor_label = QLabel(self.centralwidget)
        self.Factor_label.setObjectName(u"Factor_label")
        self.Factor_label.setGeometry(QRect(20, 320, 221, 16))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Factor_label.setFont(font)
        self.Factor_input = QLineEdit(self.centralwidget)
        self.Factor_input.setObjectName(u"Factor_input")
        self.Factor_input.setGeometry(QRect(240, 320, 113, 21))
        self.Matrix_build_button = QPushButton(self.centralwidget)
        self.Matrix_build_button.setObjectName(u"Matrix_build_button")
        self.Matrix_build_button.setGeometry(QRect(360, 10, 301, 31))
        self.Matrix_build_button.setStyleSheet(u"QPushButton {\n"
"	box-shadow: 0px 10px 14px -7px #3e7327;\n"
"	background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);\n"
"	background-color:#77b55a;\n"
"	border-radius:4px;\n"
"	border:1px solid #4b8f29;\n"
"	display:inline-block;\n"
"	cursor:pointer;\n"
"	color:#ffffff;\n"
"	font-family:Arial;\n"
"	font-size:13px;\n"
"	font-weight:bold;\n"
"	padding:6px 12px;\n"
"	text-decoration:none;\n"
"	text-shadow:0px 1px 0px #5b8a3c;\n"
"}\n"
"QPushButton:hover {\n"
"	background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);\n"
"	background-color:#72b352;\n"
"}\n"
"QPushButton:active {\n"
"	position:relative;\n"
"	top:1px;\n"
"}\n"
"")
        self.MatrixView = QTableView(self.centralwidget)
        self.MatrixView.setObjectName(u"MatrixView")
        self.MatrixView.setGeometry(QRect(360, 50, 611, 291))
        self.Newvalue_button = QPushButton(self.centralwidget)
        self.Newvalue_button.setObjectName(u"Newvalue_button")
        self.Newvalue_button.setGeometry(QRect(670, 10, 301, 31))
        self.Newvalue_button.setStyleSheet(u"QPushButton {\n"
"	box-shadow: 0px 10px 14px -7px #3e7327;\n"
"	background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);\n"
"	background-color:#77b55a;\n"
"	border-radius:4px;\n"
"	border:1px solid #4b8f29;\n"
"	display:inline-block;\n"
"	cursor:pointer;\n"
"	color:#ffffff;\n"
"	font-family:Arial;\n"
"	font-size:13px;\n"
"	font-weight:bold;\n"
"	padding:6px 12px;\n"
"	text-decoration:none;\n"
"	text-shadow:0px 1px 0px #5b8a3c;\n"
"}\n"
"QPushButton:hover {\n"
"	background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);\n"
"	background-color:#72b352;\n"
"}\n"
"QPushButton:active {\n"
"	position:relative;\n"
"	top:1px;\n"
"}\n"
"")
        self.ValueView = QTableView(self.centralwidget)
        self.ValueView.setObjectName(u"ValueView")
        self.ValueView.setGeometry(QRect(360, 350, 611, 291))
        self.Save_button = QPushButton(self.centralwidget)
        self.Save_button.setObjectName(u"Save_button")
        self.Save_button.setGeometry(QRect(20, 350, 331, 24))
        self.Save_button.setStyleSheet(u"QPushButton {\n"
"	box-shadow: 0px 10px 14px -7px #3e7327;\n"
"	background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);\n"
"	background-color:#77b55a;\n"
"	border-radius:4px;\n"
"	border:1px solid #4b8f29;\n"
"	display:inline-block;\n"
"	cursor:pointer;\n"
"	color:#ffffff;\n"
"	font-family:Arial;\n"
"	font-size:13px;\n"
"	font-weight:bold;\n"
"	padding:6px 12px;\n"
"	text-decoration:none;\n"
"	text-shadow:0px 1px 0px #5b8a3c;\n"
"}\n"
"QPushButton:hover {\n"
"	background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);\n"
"	background-color:#72b352;\n"
"}\n"
"QPushButton:active {\n"
"	position:relative;\n"
"	top:1px;\n"
"}\n"
"")
        self.DescriptTable = QTableWidget(self.centralwidget)
        self.DescriptTable.setObjectName(u"DescriptTable")
        self.DescriptTable.setGeometry(QRect(20, 381, 331, 261))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 984, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Df_choice_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0434\u0430\u0442\u0430\u0441\u0435\u0442", None))
        self.Elbow_build_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u043b\u043e\u043a\u0442\u044f", None))
        self.Factor_label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u043b-\u0432\u043e \u0444\u0430\u043a\u0442\u043e\u0440\u043e\u0432:", None))
        self.Matrix_build_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u043c\u0430\u0442\u0440\u0438\u0446\u0443 \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u043e\u0432", None))
        self.Newvalue_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u043d\u043e\u0432\u044b\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f", None))
        self.Save_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0444\u0430\u0439\u043b\u044b", None))
    # retranslateUi

