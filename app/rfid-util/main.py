# This Python file uses the following encoding: utf-8
import os
import sys

from pathlib import Path

from
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtCore import Qt, QFile, QCoreApplication, QIODevice, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort

from form import Ui_RfidUtil


class RfidUtil(QMainWindow):
    def __init__(self):
        """Init main window"""
        super(RfidUtil, self).__init__()
        self.ui = Ui_RfidUtil()
        self.ui.setupUi(self)
        lbl = QLabel('aaa')

        # init serial port
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

    def port_probe_step1(self):
        """Try to open serial port and send vesrion_check cmd"""
        # start timer for probing serial port
        self.port_probe_timer.start(100)
        # close previously opened port
        self.port.close()

        if len(self.ports_to_check) == 0:
            self.ui.statusbar.showMessage('Reader not found')
            return
        # try to open port and send vesrion_check cmd
        self.port.setPortName(self.ports_to_check.pop())
        if self.port.open(QIODevice.ReadWrite):
            s = bytes([ord('9')])
            print(s)
            self.port.write(s)
        else:
            self.port_probe_step1()


    def port_probe_step2(self):
        """Check answer for vesrion_check cmd"""
        self.port_probe_timer.stop()
        b = self.port.read(128)
        s = bytes(b).decode()
        if s.startswith('rfid-util'):
            self.port_opened = True
            self.ui.statusbar.showMessage('Reader connected')
            self.enable_ui()
        else:
            self.port_probe_step1()

    def enable_ui(self):
        """Unlock UI elements"""
        for w in self.ui.centralwidget.children():
            if isinstance(w, QWidget):
                w.setEnabled(True)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = RfidUtil()
    widget.show()
    sys.exit(app.exec())
