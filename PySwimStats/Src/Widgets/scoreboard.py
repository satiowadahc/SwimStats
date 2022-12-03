"""
Scoreboard.py

   Display widget to imitate the live scoreboard

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from records import SwimRecords


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, records):
        super(TableModel, self).__init__()
        self._data = data
        self._records = records
        self._columen_headers = ["Swimmer", "Team", "Lane", "Place", "Time", "Lengths"]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            try:
                return self._records.data[f"{self._data[index.row()][index.column()]}"]["value"]
            except Exception as e:
                print(e)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, p_int, Qt_Orientation, role=None):
        """Required abstraction"""
        if role == QtCore.Qt.DisplayRole:
            if Qt_Orientation == QtCore.Qt.Horizontal:
                return str(self._columen_headers[p_int])
            if Qt_Orientation == Qt.Vertical:
                return str(p_int)


class ScoreBoard:
    def __init__(self):
        self.layout_event_heat = None
        self.event_num_label = None
        self.heat_num_label = None
        self.event_heat_space = None
        self.table = None
        self.parent = None
        self.model = None
        self.layout = None
        self.event_title1 = None
        self.event_title2 = None
        self.event_number = None
        self.heat_number = None

    def setupUi(self, parent, data, records):

        self.parent = parent

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, parent)
        self.layout.setObjectName("MainLayout")

        self.event_title1 = QtWidgets.QLabel()
        self.event_title1.setText("EVENT")
        self.event_title2 = QtWidgets.QLabel()
        self.event_title2.setText("EVENT")

        self.layout_event_heat = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight, parent)
        self.event_num_label = QtWidgets.QLabel()
        self.event_num_label.setText("E")
        self.event_number = QtWidgets.QLabel()
        self.event_number.setText("01")
        self.heat_num_label = QtWidgets.QLabel()
        self.heat_num_label.setText("H")
        self.heat_number = QtWidgets.QLabel()
        self.heat_number.setText("01")
        self.event_heat_space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.time = QtWidgets.QLabel()


        self.layout.addWidget(self.event_title1)
        self.layout.addWidget(self.event_title2)
        self.layout_event_heat.addWidget(self.event_num_label)
        self.layout_event_heat.addWidget(self.event_number)
        self.layout_event_heat.addWidget(self.heat_num_label)
        self.layout_event_heat.addWidget(self.heat_number)
        self.layout_event_heat.addItem(self.event_heat_space)
        self.layout_event_heat.addWidget(self.time)
        self.layout.addLayout(self.layout_event_heat)

        self.model = TableModel(data, records)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.table.setAttribute(Qt.WA_TranslucentBackground)
        self.table.setStyleSheet("background: Translucent; QTableWidget::item {margin: 0px;}")
        self.table.setMinimumSize(640, 400)
        self.table.setMaximumSize(640, 400)

        self.layout.addWidget(self.table)


class ScoreBoardWidget(QtWidgets.QWidget):
    """Display Current Positions from linuxcnc"""

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        records=None,
        flags: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ):
        super().__init__(parent, flags)

        # Swimmer Name, Team Name, Lane Number, Place Number, Split Finish Time, Lengths Completed
        data = [
            [222, 237, 242, 244, 247, 256],  # Lane 1
            [258, 273, 278, 280, 283, 292],  # Lane 2
            [294, 309, 314, 316, 319, 328],  # Lane 3
            [330, 345, 350, 352, 355, 364],  # Lane 4
            [366, 381, 386, 388, 391, 400],  # Lane 5
            [402, 417, 422, 424, 427, 436],  # Lane 6
            [438, 453, 458, 460, 463, 472],  # Lane 7
            [474, 489, 494, 496, 499, 508],  # Lane 8
            [510, 525, 530, 532, 535, 544],  # Lane 9
            [546, 561, 566, 568, 571, 580]]  # Lane 10

        self.ui = ScoreBoard()
        self.ui.setupUi(self, data, records)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: Translucent; color: white")
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags())
        self.setFixedSize(self.ui.table.size())


if __name__ == "__main__":
    q_app = QtWidgets.QApplication(sys.argv)

    testrecords = SwimRecords()
    testrecords.load_config("../OS2-Swimming.txt")

    window = ScoreBoardWidget(records=testrecords)
    window.show()
    sys.exit(q_app.exec_())
