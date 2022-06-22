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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QListView, QMainWindow, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_RfidUtil(object):
    def setupUi(self, RfidUtil):
        if not RfidUtil.objectName():
            RfidUtil.setObjectName(u"RfidUtil")
        RfidUtil.resize(592, 352)
        self.centralwidget = QWidget(RfidUtil)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gb_uid = QGroupBox(self.centralwidget)
        self.gb_uid.setObjectName(u"gb_uid")
        self.gb_uid.setGeometry(QRect(10, 0, 171, 101))
        self.le_uid = QLineEdit(self.gb_uid)
        self.le_uid.setObjectName(u"le_uid")
        self.le_uid.setEnabled(True)
        self.le_uid.setGeometry(QRect(10, 30, 151, 25))
        self.btn_uid_read = QPushButton(self.gb_uid)
        self.btn_uid_read.setObjectName(u"btn_uid_read")
        self.btn_uid_read.setEnabled(True)
        self.btn_uid_read.setGeometry(QRect(10, 60, 71, 25))
        self.btn_uid_write = QPushButton(self.gb_uid)
        self.btn_uid_write.setObjectName(u"btn_uid_write")
        self.btn_uid_write.setEnabled(True)
        self.btn_uid_write.setGeometry(QRect(90, 60, 71, 25))
        self.gb_raw = QGroupBox(self.centralwidget)
        self.gb_raw.setObjectName(u"gb_raw")
        self.gb_raw.setGeometry(QRect(200, 0, 391, 351))
        self.btn_data_raw_read = QPushButton(self.gb_raw)
        self.btn_data_raw_read.setObjectName(u"btn_data_raw_read")
        self.btn_data_raw_read.setEnabled(True)
        self.btn_data_raw_read.setGeometry(QRect(10, 30, 80, 25))
        self.btn_data_raw_write = QPushButton(self.gb_raw)
        self.btn_data_raw_write.setObjectName(u"btn_data_raw_write")
        self.btn_data_raw_write.setEnabled(True)
        self.btn_data_raw_write.setGeometry(QRect(100, 30, 80, 25))
        self.lw_data = QListView(self.gb_raw)
        self.lw_data.setObjectName(u"lw_data")
        self.lw_data.setEnabled(True)
        self.lw_data.setGeometry(QRect(10, 60, 371, 281))
        font = QFont()
        font.setFamilies([u"Monospace"])
        self.lw_data.setFont(font)
        self.gb_data = QGroupBox(self.centralwidget)
        self.gb_data.setObjectName(u"gb_data")
        self.gb_data.setGeometry(QRect(10, 110, 171, 181))
        self.te_data = QTextEdit(self.gb_data)
        self.te_data.setObjectName(u"te_data")
        self.te_data.setEnabled(True)
        self.te_data.setGeometry(QRect(10, 30, 151, 70))
        self.cb_sector = QComboBox(self.gb_data)
        self.cb_sector.setObjectName(u"cb_sector")
        self.cb_sector.setEnabled(True)
        self.cb_sector.setGeometry(QRect(70, 110, 91, 25))
        self.label = QLabel(self.gb_data)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(15, 115, 41, 17))
        self.btn_data_read = QPushButton(self.gb_data)
        self.btn_data_read.setObjectName(u"btn_data_read")
        self.btn_data_read.setEnabled(True)
        self.btn_data_read.setGeometry(QRect(10, 140, 71, 25))
        self.btn_data_write = QPushButton(self.gb_data)
        self.btn_data_write.setObjectName(u"btn_data_write")
        self.btn_data_write.setEnabled(True)
        self.btn_data_write.setGeometry(QRect(90, 140, 71, 25))
        self.lbl_status = QLabel(self.centralwidget)
        self.lbl_status.setObjectName(u"lbl_status")
        self.lbl_status.setGeometry(QRect(10, 330, 181, 20))
        RfidUtil.setCentralWidget(self.centralwidget)

        self.retranslateUi(RfidUtil)

        QMetaObject.connectSlotsByName(RfidUtil)
    # setupUi

    def retranslateUi(self, RfidUtil):
        RfidUtil.setWindowTitle(QCoreApplication.translate("RfidUtil", u"RfidUtil", None))
        self.gb_uid.setTitle(QCoreApplication.translate("RfidUtil", u"UID", None))
        self.btn_uid_read.setText(QCoreApplication.translate("RfidUtil", u"Read", None))
        self.btn_uid_write.setText(QCoreApplication.translate("RfidUtil", u"Write", None))
        self.gb_raw.setTitle(QCoreApplication.translate("RfidUtil", u"Raw data", None))
        self.btn_data_raw_read.setText(QCoreApplication.translate("RfidUtil", u"Read data", None))
        self.btn_data_raw_write.setText(QCoreApplication.translate("RfidUtil", u"Write data", None))
        self.gb_data.setTitle(QCoreApplication.translate("RfidUtil", u"Data", None))
        self.label.setText(QCoreApplication.translate("RfidUtil", u"Sector", None))
        self.btn_data_read.setText(QCoreApplication.translate("RfidUtil", u"Read", None))
        self.btn_data_write.setText(QCoreApplication.translate("RfidUtil", u"Write", None))
        self.lbl_status.setText("")
    # retranslateUi

