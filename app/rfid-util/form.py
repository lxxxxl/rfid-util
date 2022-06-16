# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListView,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_RfidUtil(object):
    def setupUi(self, RfidUtil):
        if not RfidUtil.objectName():
            RfidUtil.setObjectName(u"RfidUtil")
        RfidUtil.resize(511, 394)
        self.centralwidget = QWidget(RfidUtil)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lbl_uid_tip = QLabel(self.centralwidget)
        self.lbl_uid_tip.setObjectName(u"lbl_uid_tip")
        self.lbl_uid_tip.setEnabled(False)
        self.lbl_uid_tip.setGeometry(QRect(10, 15, 31, 17))
        font = QFont()
        font.setBold(True)
        self.lbl_uid_tip.setFont(font)
        self.le_uid = QLineEdit(self.centralwidget)
        self.le_uid.setObjectName(u"le_uid")
        self.le_uid.setEnabled(False)
        self.le_uid.setGeometry(QRect(40, 10, 113, 25))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QRect(160, 10, 51, 25))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QRect(220, 10, 51, 25))
        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName(u"listView")
        self.listView.setEnabled(False)
        self.listView.setGeometry(QRect(0, 40, 511, 331))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QRect(320, 10, 80, 25))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setGeometry(QRect(420, 10, 80, 25))
        RfidUtil.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(RfidUtil)
        self.statusbar.setObjectName(u"statusbar")
        RfidUtil.setStatusBar(self.statusbar)

        self.retranslateUi(RfidUtil)

        QMetaObject.connectSlotsByName(RfidUtil)
    # setupUi

    def retranslateUi(self, RfidUtil):
        RfidUtil.setWindowTitle(QCoreApplication.translate("RfidUtil", u"RfidUtil", None))
        self.lbl_uid_tip.setText(QCoreApplication.translate("RfidUtil", u"UID:", None))
        self.pushButton.setText(QCoreApplication.translate("RfidUtil", u"Read", None))
        self.pushButton_2.setText(QCoreApplication.translate("RfidUtil", u"Write", None))
        self.pushButton_3.setText(QCoreApplication.translate("RfidUtil", u"Read data", None))
        self.pushButton_4.setText(QCoreApplication.translate("RfidUtil", u"Write data", None))
    # retranslateUi

