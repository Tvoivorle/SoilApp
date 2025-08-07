# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SoilAPP.ui'
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
    QSizePolicy, QStatusBar, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 617)
        # Создаем дополнительный виджет для фона с градиентным стилем
        self.gradient_widget = QWidget(MainWindow)
        self.gradient_widget.setObjectName(u"gradient_widget")
        self.gradient_widget.setGeometry(QRect(0, 0, MainWindow.width(), MainWindow.height()))
        gradient_style = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(212,123,74,1), stop:1 rgba(58,46,39,1));"
        self.gradient_widget.setStyleSheet(gradient_style)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.DF_choice = QPushButton(self.centralwidget)
        self.DF_choice.setObjectName(u"DF_choice")
        self.DF_choice.setGeometry(QRect(70, 10, 291, 31))
        self.DF_choice.setStyleSheet(u"QPushButton {\n"
"background-color:#eae0c2;\n"
"border-radius:9px;\n"
"border:1px solid #333029;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#505739;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);\n"
"background-color:#ccc2a6;\n"
"}\n"
"QPushButton:active {\n"
"position:relative;\n"
"top:1px;\n"
"}")
        self.Factor_info = QPushButton(self.centralwidget)
        self.Factor_info.setObjectName(u"Factor_info")
        self.Factor_info.setGeometry(QRect(10, 10, 41, 31))
        self.Factor_info.setStyleSheet(u"QPushButton {\n"
"box-shadow: 0px 1px 0px 0px #f0f7fa;\n"
"background:linear-gradient(to bottom, #33bdef 5%, #019ad2 100%);\n"
"background-color:#33bdef;\n"
"border-radius:6px;\n"
"border:1px solid #057fd0;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#ffffff;\n"
"font-family:Arial;\n"
"font-size:15px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"	background:linear-gradient(to bottom, #019ad2 5%, #33bdef 100%);\n"
"	background-color:#019ad2;\n"
"}\n"
"QPushButton:active {\n"
"	position:relative;\n"
"	top:1px;\n"
"}\n"
"")
        self.varX = QLabel(self.centralwidget)
        self.varX.setObjectName(u"varX")
        self.varX.setGeometry(QRect(10, 50, 331, 20))
        self.varX.setStyleSheet(u"QLabel{\n"
"color:#f0d13a;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}")
        self.Factor1_INPUT = QLineEdit(self.centralwidget)
        self.Factor1_INPUT.setObjectName(u"Factor1_INPUT")
        self.Factor1_INPUT.setGeometry(QRect(10, 70, 351, 21))
        self.Factor2_INPUT = QLineEdit(self.centralwidget)
        self.Factor2_INPUT.setObjectName(u"Factor2_INPUT")
        self.Factor2_INPUT.setGeometry(QRect(10, 120, 351, 21))
        self.varY = QLabel(self.centralwidget)
        self.varY.setObjectName(u"varY")
        self.varY.setGeometry(QRect(10, 100, 331, 16))
        self.varY.setStyleSheet(u"QLabel{\n"
"color:#f0d13a;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}")
        self.Elbow_BTM_2 = QPushButton(self.centralwidget)
        self.Elbow_BTM_2.setObjectName(u"Elbow_BTM_2")
        self.Elbow_BTM_2.setGeometry(QRect(10, 150, 351, 31))
        self.Elbow_BTM_2.setStyleSheet(u"QPushButton {\n"
"background-color:#eae0c2;\n"
"border-radius:9px;\n"
"border:1px solid #333029;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#505739;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);\n"
"background-color:#ccc2a6;\n"
"}\n"
"QPushButton:active {\n"
"position:relative;\n"
"top:1px;\n"
"}")
        self.Elbow_BTM = QPushButton(self.centralwidget)
        self.Elbow_BTM.setObjectName(u"Elbow_BTM")
        self.Elbow_BTM.setGeometry(QRect(10, 200, 351, 31))
        self.Elbow_BTM.setStyleSheet(u"QPushButton {\n"
"background-color:#eae0c2;\n"
"border-radius:9px;\n"
"border:1px solid #333029;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#505739;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);\n"
"background-color:#ccc2a6;\n"
"}\n"
"QPushButton:active {\n"
"position:relative;\n"
"top:1px;\n"
"}")
        self.Elbow_graph = QGraphicsView(self.centralwidget)
        self.Elbow_graph.setObjectName(u"Elbow_graph")
        self.Elbow_graph.setGeometry(QRect(10, 240, 351, 211))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 460, 351, 16))
        self.label_3.setStyleSheet(u"QLabel{\n"
"color:#f0d13a;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}")
        self.Elbow_INPUT = QLineEdit(self.centralwidget)
        self.Elbow_INPUT.setObjectName(u"Elbow_INPUT")
        self.Elbow_INPUT.setGeometry(QRect(10, 480, 351, 21))
        self.Clas_Stat = QPushButton(self.centralwidget)
        self.Clas_Stat.setObjectName(u"Clas_Stat")
        self.Clas_Stat.setGeometry(QRect(10, 510, 211, 31))
        self.Clas_Stat.setStyleSheet(u"QPushButton {\n"
"background-color:#eae0c2;\n"
"border-radius:9px;\n"
"border:1px solid #333029;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#505739;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);\n"
"background-color:#ccc2a6;\n"
"}\n"
"QPushButton:active {\n"
"position:relative;\n"
"top:1px;\n"
"}")
        self.Clasterization = QPushButton(self.centralwidget)
        self.Clasterization.setObjectName(u"Clasterization")
        self.Clasterization.setGeometry(QRect(380, 10, 561, 31))
        self.Clasterization.setStyleSheet(u"QPushButton {\n"
"background-color:#eae0c2;\n"
"border-radius:9px;\n"
"border:1px solid #333029;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#505739;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);\n"
"background-color:#ccc2a6;\n"
"}\n"
"QPushButton:active {\n"
"position:relative;\n"
"top:1px;\n"
"}")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(380, 50, 561, 321))
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(380, 390, 561, 151))
        self.Save_btm = QPushButton(self.centralwidget)
        self.Save_btm.setObjectName(u"Save_btm")
        self.Save_btm.setGeometry(QRect(230, 510, 131, 31))
        self.Save_btm.setStyleSheet(u"QPushButton {\n"
"background-color:#eae0c2;\n"
"border-radius:9px;\n"
"border:1px solid #333029;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#505739;\n"
"font-family:Arial;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"}\n"
"QPushButton:hover {\n"
"background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);\n"
"background-color:#ccc2a6;\n"
"}\n"
"QPushButton:active {\n"
"position:relative;\n"
"top:1px;\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u044f \u043f\u043e\u0447\u0432", None))
        self.DF_choice.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0434\u0430\u0442\u0430\u0441\u0435\u0442", None))
        self.Factor_info.setText(QCoreApplication.translate("MainWindow", u"i", None))
        self.varX.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0444\u0430\u043a\u0442\u043e\u0440\u0430", None))
        self.varY.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0432\u0442\u043e\u0440\u043e\u0433\u043e \u0444\u0430\u043a\u0442\u043e\u0440\u0430", None))
        self.Elbow_BTM_2.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u0440\u0430\u0441\u0441\u0435\u0438\u0432\u0430\u043d\u0438\u044f", None))
        self.Elbow_BTM.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a \u043c\u0435\u0442\u043e\u0434\u0430 \u043b\u043e\u043a\u0442\u044f", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u043e\u0432", None))
        self.Clas_Stat.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430 \u043f\u043e \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0430\u043c", None))
        self.Clasterization.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0432\u0435\u0441\u0442\u0438 \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u044e", None))
        self.Save_btm.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
    # retranslateUi

