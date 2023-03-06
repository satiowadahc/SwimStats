"""
main.py

   Data Display Program for collecting stats out of an AllStats 5000 RTD interface

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""

from typing import Optional
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
        self.layout: Optional[QtWidgets.QBoxLayout] = None

        self.scbd_layout: Optional[QtWidgets.QBoxLayout] = None
        self.show_hide_scoreboard: Optional[QtWidgets.QPushButton] = None
        self.scbd_display_picker: Optional[QtWidgets.QComboBox] = None
        self.scbd_x_lab : Optional[QtWidgets.QLabel] = None
        self.scbd_x_pos : Optional[QtWidgets.QSpinBox] = None
        self.scbd_y_lab : Optional[QtWidgets.QLabel] = None
        self.scbd_y_pos : Optional[QtWidgets.QSpinBox] = None

        self.display_refresh: Optional[QtWidgets.QPushButton] = None

    def setupUi(self, parent):
        """Override PyQt5 Requirements"""
        self.parent = parent

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, parent)
        self.layout.setObjectName("MainLayout")

        self.scbd_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight, parent)
        self.show_hide_scoreboard = QtWidgets.QPushButton()
        self.show_hide_scoreboard.setText("Show/Hide Scoreboard")
        self.scbd_layout.addWidget(self.show_hide_scoreboard)

        self.scbd_display_picker = QtWidgets.QComboBox()
        self.scbd_layout.addWidget(self.scbd_display_picker)

        self.scbd_x_lab = QtWidgets.QLabel()
        self.scbd_x_lab.setText("X:")
        self.scbd_x_pos = QtWidgets.QSpinBox()
        self.scbd_y_lab = QtWidgets.QLabel()
        self.scbd_y_lab.setText("Y:")
        self.scbd_y_pos = QtWidgets.QSpinBox()

        self.scbd_layout.addWidget(self.scbd_x_lab)
        self.scbd_layout.addWidget(self.scbd_x_pos)
        self.scbd_layout.addWidget(self.scbd_y_lab)
        self.scbd_layout.addWidget(self.scbd_y_pos)

        self.layout.addLayout(self.scbd_layout)

        self.display_refresh = QtWidgets.QPushButton()
        self.display_refresh.setText("Refresh Displays")
        self.layout.addWidget(self.display_refresh)


class MainWidget(QtWidgets.QWidget):
    """Main Program Controller"""
    def __init__(self):
        super().__init__()

        # Initialize Self
        self.ui = MainUi()
        self.ui.setupUi(self)

        # Initialize data
        self.records = SwimRecords()
        self.records.load_config("OS2-Swimming.txt")
        self.displays = {}

        # Initialize widgets
        self.table = ScoreBoardWidget(records=self.records)
        self.table.setWindowModality(Qt.WindowModal)
        self.table.hide()

        # Start Processes
        self.network_thread = Snooper()
        self.thread = QtCore.QThread()  # a new thread to run our background tasks in
        self.network_thread.moveToThread(self.thread)
        self.thread.started.connect(self.network_thread.run)
        self.connect_signals()
        self.update_displays()
        self.thread.start()

    def connect_signals(self):
        """Pyqt5 Signal Connections"""
        self.network_thread.message.connect(self.update_record)

        self.ui.display_refresh.clicked.connect(self.update_displays)
        self.ui.show_hide_scoreboard.clicked.connect(self.show_scbd)

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

    def update_displays(self):
        """Refresh the active displays"""

        self.displays = {}

        for idx, scr in enumerate(QtWidgets.QApplication.screens()):
            self.displays[f"{idx}"] = (f"{idx}: {scr.size().width()}x{scr.size().height()}",
                                       QtWidgets.QApplication.screens())
            self.ui.scbd_display_picker.addItem(self.displays[f"{idx}"][0])
            # TODO Max/Min might need offsets based on screen positions
            # TODO test with multiple displays
            self.ui.scbd_x_pos.setMaximum(scr.size().width())
            self.ui.scbd_y_pos.setMaximum(scr.size().height())

    def show_scbd(self):
        """Display scoreboard"""
        if self.table.isVisible():
            self.table.hide()
        else:
            self.table.move(self.ui.scbd_x_pos.value(), self.ui.scbd_y_pos.value())
            self.table.show()


class MainWindow(QtWidgets.QMainWindow): # pylint: disable=too-few-public-methods
    """Main Window for overriding necessary Pyqt5 signals, may be removed later"""

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
