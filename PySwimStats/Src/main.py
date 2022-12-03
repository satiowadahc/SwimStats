x"""
main.py

   Data Display Program for collecting stats out of an AllStats 5000 RTD interface

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from records import SwimRecords

from network import Snooper
from Widgets.scoreboard import ScoreBoardWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def setupUi(self, parent):

        self.parent = parent

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, parent)
        self.layout.setObjectName("MainLayout")

        self.show_hide_scoreboard = QtWidgets.QPushButton()
        self.show_hide_scoreboard.setText("Show/Hide Scoreboard")

        self.layout.addWidget(self.show_hide_scoreboard)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.records = SwimRecords()
        self.records.load_config("OS2-Swimming.txt")

        self.main_widget = MainWidget()

        self.table = ScoreBoardWidget(records=self.records)
        self.table.hide()

        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Scoreboard")
        self.setMinimumSize(1000, 500)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.network_thread = Snooper()
        self.thread = QtCore.QThread()  # a new thread to run our background tasks in
        self.network_thread.moveToThread(self.thread)
        self.thread.started.connect(self.network_thread.run)

        self.connect_signals()

        self.thread.start()

    def connect_signals(self):
        self.network_thread.message.connect(self.update_record)

    def update_record(self, offset: int, data: str):

        process = True
        data_l = len(data)
        sub_offset = 0
        while process:
            sub_l = self.records.data[f"{offset}"]["length"]
            if data_l-sub_offset >= sub_l:
                self.records.data[f"{offset}"]["value"] = data[sub_offset:sub_offset+sub_l]
                sub_offset += sub_l
        print(offset, data, self.records.data[f"{offset}"])

        self.table.repaint()

        # Special Cases
        if offset == 0:
            self.table.ui.time.setText(data)
        if offset == 9:
            self.table.ui.event_title1.setText(data)
        if offset == 39:
            self.table.ui.event_title2.setText(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec_()
