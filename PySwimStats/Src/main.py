"""
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


class MainUi:
    """Main UI Design"""

    def __init__(self):
        self.parent = None
        self.layout = None
        self.show_hide_scoreboard = None

        self.scbd_display_picker = None

        self.display_refresh = None
        self.displays = []

    def setupUi(self, parent):
        """Override PyQt5 Requirements"""
        self.parent = parent

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, parent)
        self.layout.setObjectName("MainLayout")

        self.show_hide_scoreboard = QtWidgets.QPushButton()
        self.show_hide_scoreboard.setText("Show/Hide Scoreboard")
        self.layout.addWidget(self.show_hide_scoreboard)

        self.scbd_display_picker = QtWidgets.QComboBox()
        self.layout.addWidget(self.scbd_display_picker)

        self.display_refresh = QtWidgets.QPushButton()
        self.display_refresh.setText("Refresh Displays")
        self.layout.addWidget(self.display_refresh)

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.ui = MainUi()
        self.ui.setupUi(self)

        self.records = SwimRecords()
        self.records.load_config("OS2-Swimming.txt")

        self.table = ScoreBoardWidget(records=self.records)
        self.table.setWindowModality(Qt.WindowModal)
        self.table.hide()

        self.network_thread = Snooper()
        self.thread = QtCore.QThread()  # a new thread to run our background tasks in
        self.network_thread.moveToThread(self.thread)
        self.thread.started.connect(self.network_thread.run)

        self.connect_signals()

        self.thread.start()

    def connect_signals(self):
        """Pyqt5 Signal Connections"""
        self.network_thread.message.connect(self.update_record)

    def update_record(self, offset: int, data: str):
        """Call back for network to add records
        :param offset: int - Index of data in records string
        :param data: str - Value of the string
        """
        process = True
        data_l = len(data)
        sub_offset = 0
        while process:
            sub_l = self.records.data[f"{offset}"]["length"]
            if data_l - sub_offset >= sub_l:
                self.records.data[f"{offset}"]["value"] = data[sub_offset:sub_offset + sub_l]
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


class MainWindow(QtWidgets.QMainWindow):
    """Main Window control"""

    def __init__(self):
        super().__init__()

        self.main_widget = MainWidget()

        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Scoreboard")
        self.setMinimumSize(1000, 500)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
