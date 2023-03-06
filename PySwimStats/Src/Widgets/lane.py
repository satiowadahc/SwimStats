"""
Lane.py

   Display widget to imitate the Lane Data

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""
import sys

from typing import Optional
from PyQt5 import QtWidgets, QtCore

from records import SwimRecords


class LaneHighlight:

    def __init__(self):
        self.parent: Optional[QtWidgets.QWidget] = None
        self.layout: Optional[QtWidgets.QBoxLayout] = None
        self.line_1_layout: Optional[QtWidgets.QBoxLayout] = None
        self.line_2_layout: Optional[QtWidgets.QBoxLayout] = None
        self.name_label: Optional[QtWidgets.QLabel] = None
        self.team_label: Optional[QtWidgets.QLabel] = None
        self.lane_label: Optional[QtWidgets.QLabel] = None
        self.place_label: Optional[QtWidgets.QLabel] = None
        self.split_label: Optional[QtWidgets.QLabel] = None
        self.lengths_label: Optional[QtWidgets.QLabel] = None

    def setupUi(self, parent):
        self.parent = parent

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, parent)
        self.layout.setObjectName("MainLayout")

        self.line_1_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight, parent)
        self.line_2_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight, parent)

        # OS2 Avail data - Specific to lane
        self.name_label = QtWidgets.QLabel()
        self.team_label = QtWidgets.QLabel()
        self.lane_label = QtWidgets.QLabel()
        self.place_label = QtWidgets.QLabel()
        self.split_label = QtWidgets.QLabel()
        self.lengths_label = QtWidgets.QLabel()

        self.line_1_layout.addWidget(self.name_label)
        self.line_1_layout.addWidget(self.split_label)
        self.line_2_layout.addWidget(self.team_label)
        self.line_2_layout.addWidget(self.lengths_label)

        self.layout.addLayout(self.line_1_layout)
        self.layout.addLayout(self.line_2_layout)


class LaneWidget(QtWidgets.QWidget):
    """Display Current Positions from linuxcnc"""

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        records=None,
        flags: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ):
        super().__init__(parent, flags)

        self.ui = LaneHighlight()
        self.ui.setupUi(self)

        self.refresh(records)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def refresh(self, records):
        """Refresh data"""

        self.ui.name_label.setText(records.data["222"]["value"])
        self.ui.team_label.setText(records.data["237"]["value"])
        self.ui.lane_label.setText(records.data["242"]["value"])
        self.ui.place_label.setText(records.data["244"]["value"])
        self.ui.split_label.setText(records.data["247"]["value"])
        self.ui.lengths_label.setText(records.data["256"]["value"])


if __name__ == "__main__":
    q_app = QtWidgets.QApplication(sys.argv)

    testrecords = SwimRecords()
    testrecords.load_config("../OS2-Swimming.txt")

    window = LaneWidget(records=testrecords)
    window.show()
    sys.exit(q_app.exec_())
