from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox, QComboBox, QTableWidget, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets

import pyqtgraph as pg


class GraphCanvas():
    def __init__(self, widget):
        self.widget = widget
        self.initUI()
        self.initData()

    @property
    def layout(self):
        return self.__main_layout

    @property
    def frame(self):
        self.__main_frame = QFrame()
        self.__main_frame.setLayout(self.__main_layout)
        self.__main_frame.setFrameShape(QFrame.Panel)

        return self.__main_frame

    def initUI(self):
        self.__main_layout = QHBoxLayout()

        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground('#F0F0F0')
        self.plot_graph.setMouseEnabled(x=False, y=False)
        self.plot_graph.getPlotItem().hideAxis('bottom')
        self.plot_graph.getPlotItem().hideAxis('left')

        self.plot_layout = QHBoxLayout()
        self.plot_layout.addWidget(self.plot_graph)

        self.plot_frame = QFrame()
        self.plot_frame.setLayout(self.plot_layout)
        self.plot_frame.setFrameShape(QFrame.Panel)

        afont = QFont()
        afont.setPointSize(12)
        afont.setBold(True)

        self.table_valaues = QTableWidget()
        self.table_valaues.setColumnCount(2)
        self.table_valaues.setHorizontalHeaderLabels(['ID', 'Значение'])

        self.table_valaues.verticalHeader().setVisible(False)
        hheader = self.table_valaues.horizontalHeader()
        hheader.setFont(afont)
        hheader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hheader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # hheader.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        hheader.setFocusPolicy(Qt.NoFocus)

        # self.table_valaues.setFixedWidth(82)

        self.table_layout = QHBoxLayout()
        self.table_layout.addWidget(self.table_valaues)

        self.table_frame = QFrame()
        self.table_frame.setLayout(self.table_layout)
        self.table_frame.setFrameShape(QFrame.Panel)
        self.table_frame.setMaximumWidth(164)

        self.__main_layout.addWidget(self.plot_frame)
        self.__main_layout.addWidget(self.table_frame)

    def initData(self):
        self.current_plot = None
    
    def initTableData(self, data):
        self.table_valaues.setRowCount(0)
        for indx, value in enumerate(data):
            self.table_valaues.setRowCount(self.table_valaues.rowCount() + 1)

            indx_label = QLabel(str(indx))
            indx_label.setAlignment(Qt.AlignRight) 
            indx_label.setMaximumWidth(24)

            value_label = QLabel(str(value))
            value_label.setAlignment(Qt.AlignRight) 
            value_label.setMaximumWidth(60)

            self.table_valaues.setCellWidget(indx, 0, indx_label)
            self.table_valaues.setCellWidget(indx, 1, value_label)

    def go_plot(self, data, table_data):
        if self.current_plot:
            self.plot_graph.removeItem(self.current_plot)

        length = len(data)
        data += data[-1]
        x = []
        y = []
        for i, item in enumerate(data):
            x.extend([i]*2)
            y.extend([int(item)]*2)

        self.plot_graph.setLimits(xMin = 0.01, yMin = -0.01, xMax=length - 0.01, yMax=1.01)
        self.plot_graph.setMouseEnabled(x=True, y=False)
        self.plot_graph.setBackground('#F0F0F0')
        self.plot_graph.getPlotItem().showAxis('bottom')
        self.plot_graph.showGrid(True, True, 2)

        self.current_plot = self.plot_graph.plot(x[1:], y[:-1], pen={'color':'red', 'width': 2})

        self.initTableData(table_data)