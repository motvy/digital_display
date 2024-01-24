from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox, QComboBox
from PyQt5.QtGui import QFont

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

        self.__main_layout.addWidget(self.plot_graph)


    def initData(self):
        self.current_plot = None
    
    def go_plot(self, data):
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