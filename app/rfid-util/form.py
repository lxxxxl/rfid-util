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
        self.btn_uid_read = QPushButton(self.centralwidget)
        self.btn_uid_read.setObjectName(u"btn_uid_read")
        self.btn_uid_read.setEnabled(False)
        self.btn_uid_read.setGeometry(QRect(160, 10, 51, 25))
        self.btn_uid_write = QPushButton(self.centralwidget)
        self.btn_uid_write.setObjectName(u"btn_uid_write")
        self.btn_uid_write.setEnabled(False)
        self.btn_uid_write.setGeometry(QRect(220, 10, 51, 25))
        self.lw_data = QListView(self.centralwidget)
        self.lw_data.setObjectName(u"lw_data")
        self.lw_data.setEnabled(False)
        self.lw_data.setGeometry(QRect(0, 40, 511, 331))
        font1 = QFont()
        font1.setFamilies([u"Monospace"])
        self.lw_data.setFont(font1)
        self.btn_data_read = QPushButton(self.centralwidget)
        self.btn_data_read.setObjectName(u"btn_data_read")
        self.btn_data_read.setEnabled(False)
        self.btn_data_read.setGeometry(QRect(320, 10, 80, 25))
        self.btn_data_write = QPushButton(self.centralwidget)
        self.btn_data_write.setObjectName(u"btn_data_write")
        self.btn_data_write.setEnabled(False)
        self.btn_data_write.setGeometry(QRect(420, 10, 80, 25))
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
        self.btn_uid_read.setText(QCoreApplication.translate("RfidUtil", u"Read", None))
        self.btn_uid_write.setText(QCoreApplication.translate("RfidUtil", u"Write", None))
        self.btn_data_read.setText(QCoreApplication.translate("RfidUtil", u"Read data", None))
        self.btn_data_write.setText(QCoreApplication.translate("RfidUtil", u"Write data", None))
    # retranslateUi

