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
    READ_DATA_ALL   = ord('4')
    WRITE_DATA      = ord('5')
    VERSION_CHECK   = ord('9')

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

class RfidUtil(QMainWindow):
    COMMAND_TRAILER = [0x0D, 0x0A]
    def __init__(self):
        """Init main window"""
        super(RfidUtil, self).__init__()
        self.ui = Ui_RfidUtil()
        self.ui.setupUi(self)
        self.setFixedSize(590, 350)

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

        self.show_message('Looking for reader...')
        self.port_probe_step1()

        # button signals
        self.ui.btn_uid_read.clicked.connect(self.uid_read_click)
        self.ui.btn_uid_write.clicked.connect(self.uid_write_click)
        self.ui.btn_data_raw_read.clicked.connect(self.data_read_raw_click)
        self.ui.btn_data_raw_write.clicked.connect(self.data_write_raw_click)
        self.ui.btn_data_read.clicked.connect(self.data_read_click)
        self.ui.btn_data_write.clicked.connect(self.data_write_click)
        self.ui.te_data.textChanged.connect(self.textedit_textChanged)

        # sector numbers
        for i in range(1,16):
            self.ui.cb_sector.addItem(str(i), i)

        # data model for displaying RFID contents
        self.data_model = QStandardItemModel()
        self.ui.lw_data.setModel(self.data_model)

    def show_message(self, text):
        """
        Show message in status bar
        
        :param text: text to show
        """
        self.ui.lbl_status.setText(text)

    def port_probe_step1(self):
        """Try to open serial port and send vesrion_check cmd"""
        # close previously opened port
        self.port.close()

        if len(self.ports_to_check) == 0:
            self.show_message('Reader not found')
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
            self.show_message('Reader connected')
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

            print(self.port_rx_data)

            # process common responses
            cmd = ord(self.port_rx_data[0])
            if ReaderCommand.has_value(cmd):
                self.process_response_common(self.port_rx_data)

            if self.port_rx_data.startswith(chr(ReaderCommand.READ_UID.value)):
                self.process_READ_UID_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.WRITE_UID.value)):
                self.process_WRITE_UID_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.READ_DATA.value)):
                self.process_READ_DATA_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.READ_DATA_ALL.value)):
                self.process_READ_DATA_ALL_response(self.port_rx_data)
            elif self.port_rx_data.startswith(chr(ReaderCommand.WRITE_DATA.value)):
                self.process_WRITE_DATA_response(self.port_rx_data)

            self.port_rx_data = ''

    def process_response_common(self, data):
        if 'OK' in data:
            self.show_message('Waiting for card...')
        elif 'Done' in data:
            self.show_message('Operation Done')
        elif 'Fail' in data:
            self.show_message('Operaion Failure')

    def process_READ_UID_response(self, data):
        """Process response to READ_UID command"""
        if 'UID:' in data:
            uid = data[data.find('UID:')+4:]
            self.ui.le_uid.setText(uid.replace('\r\n',''))
        elif 'Type:' in data:
            self.show_message(data[data.find('Type:'):].replace('\r\n',''))

    def process_READ_DATA_ALL_response(self, data):
        """Process response to READ_DATA_ALL command"""
        if '4 B' in data:
            data = data[data.find(': ')+2:]
            data = data.replace('\r\n','')
            item = QStandardItem(data)
            self.data_model.appendRow(item)

    def process_READ_DATA_response(self, data):
        """Process response to READ_DATA command"""
        if '3 B' in data:
            data = data[data.find(': ')+2:]
            self.hex_data_buf += data.replace('\r\n','')
        elif 'Done' in data:
            try:
                b = bytes.fromhex(self.hex_data_buf)
                self.ui.te_data.setText(b.decode())
            except UnicodeDecodeError:
                self.show_message('Invalid string data')


    def process_WRITE_UID_response(self, data):
        """Process response to WRITE_UID command"""
        # nothing to do special
        pass

    def process_WRITE_DATA_response(self, data):
        """Process response to WRITE_DATA command"""
        # nothing to do special
        pass

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

    def data_read_raw_click(self):
        """Send READ_DATA_ALL command"""
        self.data_model.clear()
        if not self.port_opened:
            return
        self.port.write(bytes([ReaderCommand.READ_DATA_ALL.value, *self.COMMAND_TRAILER]))

    def data_write_raw_click(self):
        """Send WRITE_DATA command from raw view"""
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

    def data_read_click(self):
        """Send READ_DATA command"""
        self.hex_data_buf = ''
        self.ui.te_data.clear()
        if not self.port_opened:
            return
        self.port.write(bytes([ReaderCommand.READ_DATA.value, self.ui.cb_sector.currentData(),  *self.COMMAND_TRAILER]))

    def data_write_click(self):
        """Send WRITE_DATA command from data view"""
        cmd = bytearray(self.ui.te_data.toPlainText().encode())
        # append null-terminator and align string by size of block (16)
        while len(cmd) % 16 != 0:
            cmd.append(0)
        blockno = self.ui.cb_sector.currentData() * 4
        cmd.insert(0, blockno)
        cmd.insert(0, ReaderCommand.WRITE_DATA.value)
        for b in self.COMMAND_TRAILER:
                cmd.append(b)
        
        self.port.write(cmd)

    def textedit_textChanged(self):
        """Limit max text length in te_data"""
        if len(self.ui.te_data.toPlainText()) > 47:
            self.ui.te_data.textCursor().deletePreviousChar()





if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = RfidUtil()
    widget.show()
    sys.exit(app.exec())

