#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pathlib import Path

from enum import Enum
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QFile, QCoreApplication, QIODevice, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort

from form import Ui_RfidUtil

class ReaderCommand(Enum):
    READ_UID        = ord('1')
    WRITE_UID       = ord('2')
    READ_DATA       = ord('3')
    WRITE_DATA      = ord('4')
    VERSION_CHECK   = ord('9')

class RfidUtil(QMainWindow):
    COMMAND_TRAILER = [0x0D, 0x0A]
    def __init__(self):
        """Init main window"""
        super(RfidUtil, self).__init__()
        self.ui = Ui_RfidUtil()
        self.ui.setupUi(self)
        self.setFixedSize(511, 394)

        # init serial port
        self.port_rx_data = ''
        self.port_opened = False
        self.port = QSerialPort()
        self.port.setBaudRate(9600)
        self.port.readyRead.connect(self.port_probe_step2)
        # init timer for probing serial port
        self.port_probe_timer = QTimer()
        self.port_probe_timer.timeout.connect(self.port_probe_step1)

        # ports that will be checked for connected reader
        self.ports_to_check = []

        for port in QSerialPortInfo.availablePorts():
            self.ports_to_check.append(port.systemLocation())

        self.ui.statusbar.showMessage('Looking for reader...')
        self.port_probe_step1()

        # button signals
        self.ui.btn_uid_read.clicked.connect(self.uid_read_click)
        self.ui.btn_uid_write.clicked.connect(self.uid_write_click)
        self.ui.btn_data_read.clicked.connect(self.data_read_click)
        self.ui.btn_data_write.clicked.connect(self.data_write_click)

        # data model for displaying RFID contents
        self.data_model = QStandardItemModel()
        self.ui.lw_data.setModel(self.data_model)

    def port_probe_step1(self):
        """Try to open serial port and send vesrion_check cmd"""
        # close previously opened port
        self.port.close()

        if len(self.ports_to_check) == 0:
            self.ui.statusbar.showMessage('Reader not found')
            return
        # try to open port and send vesrion_check cmd
        self.port.setPortName(self.ports_to_check.pop())
        if self.port.open(QIODevice.ReadWrite):
            # start timer for probing serial port
            self.port_probe_timer.start(100)
            s = bytes([ReaderCommand.VERSION_CHECK.value, *self.COMMAND_TRAILER])
            self.port.write(s)
        else:
            self.port_probe_step1()


    def port_probe_step2(self):
        """Check answer for vesrion_check cmd"""
        self.port_probe_timer.stop()
        b = self.port.read(128)
        s = bytes(b).decode()
        if 'rfid-util' in s:
            self.port_opened = True
            self.ui.statusbar.showMessage('Reader connected')
            # disconnect probe signal and connect normal logic processing signal
            self.port.readyRead.disconnect(self.port_probe_step2)
            self.port.readyRead.connect(self.port_readyRead)
            self.enable_ui()
        else:
            self.port_probe_step1()

    def enable_ui(self):
        """Unlock UI elements"""
        for w in self.ui.centralwidget.children():
            if isinstance(w, QWidget):
                w.setEnabled(True)

    def port_readyRead(self):
        """Process data from serial port"""
        while True:
            b = self.port.readLine()
            if len(b) == 0:
                return

            # concat rx data if we received splitted string
            self.port_rx_data += bytes(b).decode('utf-8')
            if not self.port_rx_data.endswith('\n'):
                continue

            #print(self.port_rx_data)
            if self.port_rx_data.startswith(chr(ReaderCommand.READ_UID.value)):
                self.process_READ_UID_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.WRITE_UID.value)):
                self.process_WRITE_UID_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.READ_DATA.value)):
                self.process_READ_DATA_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.WRITE_DATA.value)):
                self.process_WRITE_DATA_response(self.port_rx_data)

            self.port_rx_data = ''

    def process_READ_UID_response(self, data):
        """Process response to READ_UID command"""
        if 'OK' in data:
            self.ui.statusbar.showMessage('Waiting for card...')
        elif 'UID:' in data:
            uid = data[data.find('UID:')+4:]
            self.ui.le_uid.setText(uid.replace('\r\n',''))
        elif 'Type:' in data:
            self.ui.statusbar.showMessage(data[data.find('Type:'):])

    def process_READ_DATA_response(self, data):
        """Process response to READ_UID command"""
        if 'OK' in data:
            self.ui.statusbar.showMessage('Waiting for card...')
        elif 'Done' in data:
            self.ui.statusbar.showMessage('Read Done')
        elif 'Fail' in data:
            self.ui.statusbar.showMessage('Read Fail')
        elif '3 B' in data:
            data = data[data.find(': ')+2:]
            data = data.replace('\r\n','')
            item = QStandardItem(data)
            self.data_model.appendRow(item)

    def process_WRITE_UID_response(self, data):
        """Process response to WRITE_UID command"""
        if 'OK' in data:
            self.ui.statusbar.showMessage('Waiting for card...')
        elif 'Done' in data:
            self.ui.statusbar.showMessage('Write Done')
        elif 'Fail' in data:
            self.ui.statusbar.showMessage('Write Fail')

    def process_WRITE_DATA_response(self, data):
        """Process response to WRITE_DATA command"""
        if 'OK' in data:
            self.ui.statusbar.showMessage('Waiting for card...')
        elif 'Done' in data:
            self.ui.statusbar.showMessage('Write Done')
        elif 'Fail' in data:
            self.ui.statusbar.showMessage('Write Fail')

    def uid_read_click(self):
        """Send READ_UID command"""
        if not self.port_opened:
            return
        self.port.write(bytes([ReaderCommand.READ_UID.value, 0x0D, 0x0A]))

    def uid_write_click(self):
        """Send WRITE_UID command"""
        if not self.port_opened:
            return
        #uid_str = self.ui.le_uid.text().replace(' ', '')
        uid = bytearray.fromhex(self.ui.le_uid.text())
        uid.insert(0, ReaderCommand.WRITE_UID.value)
        for b in self.COMMAND_TRAILER:
            uid.append(b)
        self.port.write(uid)

    def data_read_click(self):
        """Send READ_DATA command"""
        self.data_model.clear()
        if not self.port_opened:
            return
        self.port.write(bytes([ReaderCommand.READ_DATA.value, *self.COMMAND_TRAILER]))

    def data_write_click(self):
        """Send WRITE_DATA command"""
        if not self.port_opened:
            return
        for i in self.ui.lw_data.selectedIndexes():
            text = self.data_model.item(i.row()).text()
            cmd = bytearray.fromhex(text)
            cmd.insert(0, i.row())
            cmd.insert(0, ReaderCommand.WRITE_DATA.value)
            for b in self.COMMAND_TRAILER:
                cmd.append(b)
            self.port.write(cmd)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = RfidUtil()
    widget.show()
    sys.exit(app.exec())

