# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Info.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QListWidget, QListWidgetItem,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(299, 290)
        self.gradient_widget = QWidget(Dialog)
        self.gradient_widget.setObjectName(u"gradient_widget")
        self.gradient_widget.setGeometry(QRect(0, 0, Dialog.width(), Dialog.height()))
        gradient_style = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(212,123,74,1), stop:1 rgba(58,46,39,1));"
        self.gradient_widget.setStyleSheet(gradient_style)
        Dialog.setStyleSheet(u"background-color: rgba(170, 170, 127, 80)")
        self.listWidget = QListWidget(Dialog)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        font = QFont()
        font.setBold(True)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setFont(font);
        __qlistwidgetitem.setBackground(brush);
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setFont(font);
        __qlistwidgetitem2 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem2.setFont(font);
        __qlistwidgetitem3 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem3.setFont(font);
        __qlistwidgetitem4 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem4.setFont(font);
        __qlistwidgetitem5 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem5.setFont(font);
        __qlistwidgetitem6 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem6.setFont(font);
        __qlistwidgetitem7 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem7.setFont(font);
        __qlistwidgetitem8 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem8.setFont(font);
        __qlistwidgetitem9 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem9.setFont(font);
        __qlistwidgetitem10 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem10.setFont(font);
        __qlistwidgetitem11 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem11.setFont(font);
        __qlistwidgetitem12 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem12.setFont(font);
        __qlistwidgetitem13 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem13.setFont(font);
        __qlistwidgetitem14 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem14.setFont(font);
        __qlistwidgetitem15 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem15.setFont(font);
        __qlistwidgetitem16 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem16.setFont(font);
        __qlistwidgetitem17 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem17.setFont(font);
        __qlistwidgetitem18 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem18.setFont(font);
        __qlistwidgetitem19 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem19.setFont(font);
        __qlistwidgetitem20 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem20.setFont(font);
        __qlistwidgetitem21 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem21.setFont(font);
        __qlistwidgetitem22 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem22.setFont(font);
        __qlistwidgetitem23 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem23.setFont(font);
        __qlistwidgetitem24 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem24.setFont(font);
        __qlistwidgetitem25 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem25.setFont(font);
        __qlistwidgetitem26 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem26.setFont(font);
        __qlistwidgetitem27 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem27.setFont(font);
        __qlistwidgetitem28 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem28.setFont(font);
        __qlistwidgetitem29 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem29.setFont(font);
        __qlistwidgetitem30 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem30.setFont(font);
        __qlistwidgetitem31 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem31.setFont(font);
        __qlistwidgetitem32 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem32.setFont(font);
        __qlistwidgetitem33 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem33.setFont(font);
        __qlistwidgetitem34 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem34.setFont(font);
        __qlistwidgetitem35 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem35.setFont(font);
        __qlistwidgetitem36 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem36.setFont(font);
        __qlistwidgetitem37 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem37.setFont(font);
        __qlistwidgetitem38 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem38.setFont(font);
        __qlistwidgetitem39 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem39.setFont(font);
        __qlistwidgetitem40 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem40.setFont(font);
        __qlistwidgetitem41 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem41.setFont(font);
        __qlistwidgetitem42 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem42.setFont(font);
        __qlistwidgetitem43 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem43.setFont(font);
        __qlistwidgetitem44 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem44.setFont(font);
        __qlistwidgetitem45 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem45.setFont(font);
        __qlistwidgetitem46 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem46.setFont(font);
        __qlistwidgetitem47 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem47.setFont(font);
        __qlistwidgetitem48 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem48.setFont(font);
        __qlistwidgetitem49 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem49.setFont(font);
        __qlistwidgetitem50 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem50.setFont(font);
        __qlistwidgetitem51 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem51.setFont(font);
        __qlistwidgetitem52 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem52.setFont(font);
        __qlistwidgetitem53 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem53.setFont(font);
        __qlistwidgetitem54 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem54.setFont(font);
        __qlistwidgetitem55 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem55.setFont(font);
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(15, 11, 271, 261))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Dialog", u"Factor 1 - \u041f\u043e\u0447\u0432\u0435\u043d\u043d\u0430\u044f \u0432\u043b\u0430\u0436\u043d\u043e\u0441\u0442\u044c \u0438 \u044d\u043b\u0435\u043a\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u0432\u043e\u0439\u0441\u0442\u0432\u0430", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Dialog", u"Factor 2 - \u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u043e\u0441\u0442\u0430\u0432 \u0438\u043b\u043e\u0432\u044b\u0445 \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u043e\u0432", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Dialog", u"Factor 3 - \u0413\u0440\u0430\u043d\u0443\u043b\u043e\u043c\u0435\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u043e\u0441\u0442\u0430\u0432 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Dialog", u"Factor 4 - \u0424\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u0432\u043e\u0439\u0441\u0442\u0432\u0430 \u0438 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem4 = self.listWidget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Dialog", u"Factor 5 - \u041e\u0440\u0433\u0430\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u044b \u0421\u0424\u041a", None));
        ___qlistwidgetitem5 = self.listWidget.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Dialog", u"Factor 6 - \u041c\u0438\u043d\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u043e\u0441\u0442\u0430\u0432 \u043f\u043e\u0447\u0432\u044b \u043f\u043e \u0440\u0430\u0437\u043c\u0435\u0440\u0430\u043c \u0447\u0430\u0441\u0442\u0438\u0446", None));
        ___qlistwidgetitem6 = self.listWidget.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("Dialog", u"Factor 7 - \u0413\u043b\u0443\u0431\u0438\u043d\u0430 \u0438 \u043e\u0442\u0431\u043e\u0440 \u043e\u0431\u0440\u0430\u0437\u0446\u043e\u0432 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem7 = self.listWidget.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("Dialog", u"Factor 8 - \u0413\u0440\u0443\u043f\u043f\u044b \u0444\u043e\u0441\u0444\u0430\u0442\u043e\u0432 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem8 = self.listWidget.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("Dialog", u"Factor 9 - \u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u043e\u0441\u0442\u0430\u0432 \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u043e\u0432 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem9 = self.listWidget.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("Dialog", u"Factor 10 - \u041e\u0440\u0433\u0430\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u044b \u0421\u0413\u041a", None));
        ___qlistwidgetitem10 = self.listWidget.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("Dialog", u"Factor 11 - \u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043a\u043e\u0440\u043d\u0435\u0432\u043e\u0439 \u0441\u0438\u0441\u0442\u0435\u043c\u044b", None));
        ___qlistwidgetitem11 = self.listWidget.item(11)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("Dialog", u"Factor 12 - \u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 \u0446\u0432\u0435\u0442\u0430 \u043f\u043e \u0441\u0438\u0441\u0442\u0435\u043c\u0435 \u041c\u0430\u043d\u0441\u0435\u043b\u043b\u0430", None));
        ___qlistwidgetitem12 = self.listWidget.item(12)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("Dialog", u"Factor 13 - \u0424\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u0432\u043e\u0439\u0441\u0442\u0432\u0430 \u0432\u043b\u0430\u0436\u043d\u043e\u0441\u0442\u0438 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem13 = self.listWidget.item(13)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("Dialog", u"Factor 14 - \u0421\u0443\u043c\u043c\u0430 \u043a\u0430\u0442\u0438\u043e\u043d\u043e\u0432 \u0438 \u0430\u043d\u0438\u043e\u043d\u043e\u0432 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem14 = self.listWidget.item(14)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("Dialog", u"Factor 15 - \u041e\u0440\u0433\u0430\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0443\u0433\u043b\u0435\u0440\u043e\u0434 \u0438 \u043e\u0431\u0449\u0438\u0439 \u0430\u0437\u043e\u0442 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem15 = self.listWidget.item(15)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("Dialog", u"Factor 16 - \u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u043e\u0441\u0442\u0430\u0432 \u0438 \u043c\u0438\u043d\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u044b \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem16 = self.listWidget.item(16)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("Dialog", u"Factor 17 - \u041e\u0431\u043c\u0435\u043d\u043d\u044b\u0439 \u043a\u0430\u043b\u044c\u0446\u0438\u0439 \u0438 \u043c\u0430\u0433\u043d\u0438\u0439 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem17 = self.listWidget.item(17)
        ___qlistwidgetitem17.setText(QCoreApplication.translate("Dialog", u"Factor 18 - \u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u043d\u0430\u0440\u0443\u0448\u0435\u043d\u0438\u044f \u043f\u0440\u043e\u0444\u0438\u043b\u044f \u0438 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0441\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0438", None));
        ___qlistwidgetitem18 = self.listWidget.item(18)
        ___qlistwidgetitem18.setText(QCoreApplication.translate("Dialog", u"Factor 19 - \u0421\u043e\u0441\u0442\u0430\u0432 \u0438 \u0441\u0442\u0435\u043f\u0435\u043d\u044c \u043a\u0430\u043c\u0435\u043d\u0438\u0441\u0442\u043e\u0441\u0442\u0438 \u043c\u0438\u043d\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0441\u043a\u0435\u043b\u0435\u0442\u0430", None));
        ___qlistwidgetitem19 = self.listWidget.item(19)
        ___qlistwidgetitem19.setText(QCoreApplication.translate("Dialog", u"Factor 20 - \u041e\u0431\u043c\u0435\u043d\u043d\u044b\u0435 \u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u044f \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem20 = self.listWidget.item(20)
        ___qlistwidgetitem20.setText(QCoreApplication.translate("Dialog", u"Factor 21 - \u0418\u043d\u0442\u0435\u043d\u0441\u0438\u0432\u043d\u043e\u0441\u0442\u044c \u0438 \u0442\u0438\u043f \u044d\u0440\u043e\u0437\u0438\u0438 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem21 = self.listWidget.item(21)
        ___qlistwidgetitem21.setText(QCoreApplication.translate("Dialog", u"Factor 22 - \u0422\u0435\u043a\u0441\u0442\u0443\u0440\u043d\u044b\u0439 \u0430\u043d\u0430\u043b\u0438\u0437 \u043f\u043e\u0447\u0432", None));
        ___qlistwidgetitem22 = self.listWidget.item(22)
        ___qlistwidgetitem22.setText(QCoreApplication.translate("Dialog", u"Factor 23 - \u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0441\u043e\u0441\u0442\u0430\u0432 \u043f\u043e\u0447\u0432\u044b \u0432 \u0441\u043e\u043b\u0435\u0432\u044b\u0445 \u043e\u0442\u043b\u043e\u0436\u0435\u043d\u0438\u044f\u0445", None));
        ___qlistwidgetitem23 = self.listWidget.item(23)
        ___qlistwidgetitem23.setText(QCoreApplication.translate("Dialog", u"Factor 24 - \u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438 \u043f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u043e\u0431\u0440\u0430\u0437\u0446\u043e\u0432 \u0432 \u0433\u043e\u0440\u0438\u0437\u043e\u043d\u0442\u0435", None));
        ___qlistwidgetitem24 = self.listWidget.item(24)
        ___qlistwidgetitem24.setText(QCoreApplication.translate("Dialog", u"Factor 25 - \u041f\u043e\u0434\u0432\u0438\u0436\u043d\u044b\u0439 \u043a\u0430\u043b\u0438\u0439 \u0438 \u0444\u043e\u0441\u0444\u043e\u0440 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem25 = self.listWidget.item(25)
        ___qlistwidgetitem25.setText(QCoreApplication.translate("Dialog", u"Factor 26 - \u041f\u0440\u0438\u0441\u0443\u0442\u0441\u0442\u0432\u0438\u0435 \u043c\u0438\u0446\u0435\u043b\u0438\u044f \u0438 \u0432\u043e\u0434\u043e\u0440\u043e\u0441\u043b\u0435\u0432\u043e\u0439 \u043f\u043b\u0435\u043d\u043a\u0438 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem26 = self.listWidget.item(26)
        ___qlistwidgetitem26.setText(QCoreApplication.translate("Dialog", u"Factor 27 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u043a\u0430\u043b\u044c\u0446\u0438\u044f \u0438 \u043c\u0430\u0433\u043d\u0438\u044f \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem27 = self.listWidget.item(27)
        ___qlistwidgetitem27.setText(QCoreApplication.translate("Dialog", u"Factor 28 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0430\u043c\u043e\u0440\u0444\u043d\u043e\u0433\u043e \u0430\u043b\u044e\u043c\u0438\u043d\u0438\u044f \u0438 \u0436\u0435\u043b\u0435\u0437\u0430 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem28 = self.listWidget.item(28)
        ___qlistwidgetitem28.setText(QCoreApplication.translate("Dialog", u"Factor 29 - \u0413\u0438\u0434\u0440\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043a\u0438\u0441\u043b\u043e\u0442\u043d\u043e\u0441\u0442\u044c", None));
        ___qlistwidgetitem29 = self.listWidget.item(29)
        ___qlistwidgetitem29.setText(QCoreApplication.translate("Dialog", u"Factor 30 - \u0423\u0440\u043e\u0432\u0435\u043d\u044c \u043e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u044f \u0433\u0440\u0443\u043d\u0442\u043e\u0432\u044b\u0445 \u0432\u043e\u0434 \u0438 \u0433\u043b\u0443\u0431\u0438\u043d\u0430 \u0437\u0430\u043b\u0435\u0433\u0430\u043d\u0438\u044f", None));
        ___qlistwidgetitem30 = self.listWidget.item(30)
        ___qlistwidgetitem30.setText(QCoreApplication.translate("Dialog", u"Factor 31 - \u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 \u043f\u0440\u0435\u043e\u0431\u043b\u0430\u0434\u0430\u044e\u0449\u0435\u0433\u043e \u0446\u0432\u0435\u0442\u0430 \u043f\u043e \u041c\u0430\u043d\u0441\u0435\u043b\u043b\u0430", None));
        ___qlistwidgetitem31 = self.listWidget.item(31)
        ___qlistwidgetitem31.setText(QCoreApplication.translate("Dialog", u"Factor 32 - \u0422\u0438\u043f \u044d\u0440\u043e\u0437\u0438\u0438 \u0438 \u0440\u0430\u0437\u043c\u0435\u0440 \u0447\u0430\u0441\u0442\u0438\u0446 \u0442\u0435\u043a\u0441\u0442\u0443\u0440\u043d\u043e\u0433\u043e \u0430\u043d\u0430\u043b\u0438\u0437\u0430", None));
        ___qlistwidgetitem32 = self.listWidget.item(32)
        ___qlistwidgetitem32.setText(QCoreApplication.translate("Dialog", u"Factor 33 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u043e\u043a\u0441\u0438\u0434\u043e\u0432 \u043a\u0430\u043b\u044c\u0446\u0438\u044f \u0438 \u043c\u0430\u0433\u043d\u0438\u044f \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem33 = self.listWidget.item(33)
        ___qlistwidgetitem33.setText(QCoreApplication.translate("Dialog", u"Factor 34 - \u041f\u043e\u043b\u043d\u0430\u044f \u0432\u043b\u0430\u0433\u043e\u0435\u043c\u043a\u043e\u0441\u0442\u044c \u0438 \u0432\u043e\u0434\u043e\u043f\u0440\u043e\u043d\u0438\u0446\u0430\u0435\u043c\u043e\u0441\u0442\u044c \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem34 = self.listWidget.item(34)
        ___qlistwidgetitem34.setText(QCoreApplication.translate("Dialog", u"Factor 35 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u043e\u043a\u0441\u0438\u0434\u0430 \u043c\u0430\u0440\u0433\u0430\u043d\u0446\u0430 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem35 = self.listWidget.item(35)
        ___qlistwidgetitem35.setText(QCoreApplication.translate("Dialog", u"Factor 36 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u043e\u0440\u0433\u0430\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0436\u0435\u043b\u0435\u0437\u0430 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem36 = self.listWidget.item(36)
        ___qlistwidgetitem36.setText(QCoreApplication.translate("Dialog", u"Factor 37 - \u0424\u0440\u0430\u043a\u0446\u0438\u0438 \u043f\u043e\u0447\u0432\u0435\u043d\u043d\u043e\u0433\u043e \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430 (3-2 \u043c\u043c \u0438 5-3 \u043c\u043c)", None));
        ___qlistwidgetitem37 = self.listWidget.item(37)
        ___qlistwidgetitem37.setText(QCoreApplication.translate("Dialog", u"Factor 38 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0438\u043b\u0430 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem38 = self.listWidget.item(38)
        ___qlistwidgetitem38.setText(QCoreApplication.translate("Dialog", u"Factor 39 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0445\u043b\u043e\u0440\u0438\u0434-\u0438\u043e\u043d\u043e\u0432 \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem39 = self.listWidget.item(39)
        ___qlistwidgetitem39.setText(QCoreApplication.translate("Dialog", u"Factor 40 - \u0424\u043e\u0440\u043c\u0430 \u0441\u043a\u043b\u043e\u043d\u0430 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem40 = self.listWidget.item(40)
        ___qlistwidgetitem40.setText(QCoreApplication.translate("Dialog", u"Factor 41 - \u0424\u0430\u043a\u0442\u043e\u0440 \u0434\u0438\u0441\u043f\u0435\u0440\u0441\u043d\u043e\u0441\u0442\u0438 \u0438 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0447\u0430\u0441\u0442\u0438\u0446 \u043c\u0435\u043d\u044c\u0448\u0435 0,001 \u043c\u043c \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem41 = self.listWidget.item(41)
        ___qlistwidgetitem41.setText(QCoreApplication.translate("Dialog", u"Factor 42 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21161", None));
        ___qlistwidgetitem42 = self.listWidget.item(42)
        ___qlistwidgetitem42.setText(QCoreApplication.translate("Dialog", u"Factor 43 - \u0424\u0440\u0430\u043a\u0446\u0438\u044f \u043f\u043e\u0447\u0432\u0435\u043d\u043d\u043e\u0433\u043e \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430 \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u043c \u043e\u0442 10 \u0434\u043e 7 \u043c\u043c", None));
        ___qlistwidgetitem43 = self.listWidget.item(43)
        ___qlistwidgetitem43.setText(QCoreApplication.translate("Dialog", u"Factor 44 - \u0424\u0440\u0430\u043a\u0446\u0438\u044f \u043f\u043e\u0447\u0432\u0435\u043d\u043d\u043e\u0433\u043e \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430 \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u043c \u043c\u0435\u043d\u0435\u0435 0,25 \u043c\u043c", None));
        ___qlistwidgetitem44 = self.listWidget.item(44)
        ___qlistwidgetitem44.setText(QCoreApplication.translate("Dialog", u"Factor 45 - \u0424\u0440\u0430\u043a\u0446\u0438\u0438 \u043f\u043e\u0447\u0432\u0435\u043d\u043d\u043e\u0433\u043e \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430 \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u043c \u043e\u0442 1 \u0434\u043e 0,25 \u043c\u043c \u0438 \u043e\u0442 0,25 \u0434\u043e 0,05 \u043c\u043c", None));
        ___qlistwidgetitem45 = self.listWidget.item(45)
        ___qlistwidgetitem45.setText(QCoreApplication.translate("Dialog", u"Factor 46 - \u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u043e\u0440\u0438\u0437\u043e\u043d\u0442\u043e\u0432 \u0432 \u043f\u043e\u0447\u0432\u0435\u043d\u043d\u043e\u043c \u043f\u0440\u043e\u0444\u0438\u043b\u0435", None));
        ___qlistwidgetitem46 = self.listWidget.item(46)
        ___qlistwidgetitem46.setText(QCoreApplication.translate("Dialog", u"Factor 47 - \u0424\u0440\u0430\u043a\u0446\u0438\u044f \u043f\u043e\u0447\u0432\u0435\u043d\u043d\u043e\u0433\u043e \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430 \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u043c \u043e\u0442 2 \u0434\u043e 1 \u043c\u043c", None));
        ___qlistwidgetitem47 = self.listWidget.item(47)
        ___qlistwidgetitem47.setText(QCoreApplication.translate("Dialog", u"Factor 48 - \u0412\u044b\u0441\u043e\u0442\u0430 \u043d\u0430\u0434 \u0443\u0440\u043e\u0432\u043d\u0435\u043c \u043c\u043e\u0440\u044f", None));
        ___qlistwidgetitem48 = self.listWidget.item(48)
        ___qlistwidgetitem48.setText(QCoreApplication.translate("Dialog", u"Factor 49 - \u0417\u043e\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0438 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0444\u043e\u0441\u0444\u043e\u0440\u043d\u043e\u0439 \u043a\u0438\u0441\u043b\u043e\u0442\u044b (P2O5) \u0432 \u043f\u043e\u0447\u0432\u0435", None));
        ___qlistwidgetitem49 = self.listWidget.item(49)
        ___qlistwidgetitem49.setText(QCoreApplication.translate("Dialog", u"Factor 50 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21162", None));
        ___qlistwidgetitem50 = self.listWidget.item(50)
        ___qlistwidgetitem50.setText(QCoreApplication.translate("Dialog", u"Factor 51 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21163", None));
        ___qlistwidgetitem51 = self.listWidget.item(51)
        ___qlistwidgetitem51.setText(QCoreApplication.translate("Dialog", u"Factor 52 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21164", None));
        ___qlistwidgetitem52 = self.listWidget.item(52)
        ___qlistwidgetitem52.setText(QCoreApplication.translate("Dialog", u"Factor 53 - \u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0434\u0438\u043e\u043a\u0441\u0438\u0434\u0430 \u0442\u0438\u0442\u0430\u043d\u0430 (TiO2) \u0432 \u0438\u043b\u043e\u0432\u044b\u0445 \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u0430\u0445 \u043f\u043e\u0447\u0432\u044b", None));
        ___qlistwidgetitem53 = self.listWidget.item(53)
        ___qlistwidgetitem53.setText(QCoreApplication.translate("Dialog", u"Factor 54 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21165", None));
        ___qlistwidgetitem54 = self.listWidget.item(54)
        ___qlistwidgetitem54.setText(QCoreApplication.translate("Dialog", u"Factor 55 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21166", None));
        ___qlistwidgetitem55 = self.listWidget.item(55)
        ___qlistwidgetitem55.setText(QCoreApplication.translate("Dialog", u"Factor 56 - \u041d\u0435\u043e\u0434\u043d\u043e\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u0444\u0430\u043a\u0442\u043e\u0440 \u21167", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

