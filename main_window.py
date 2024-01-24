from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox, QComboBox

import serial

import plot_canvas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        stylesheet = """
        QLabel {
            font-size: 12pt;
        }

        QComboBox {
            font-size: 12pt;
        }

        QLineEdit {
            font-size: 12pt;
        }
        
        QPushButton {
            font-size: 12pt;
        }
        """
        self.setStyleSheet(stylesheet)
        self.setWindowTitle("Просмотр сигналов")
        # self.setFixedSize(QSize(1440, 810))
        self.setFixedSize(QSize(1200, 350))

        self.initUI()
        self.initData()

    def initUI(self):
        self.start_btn = QPushButton('Старт')
        self.start_btn.setMinimumWidth(150)
        self.start_btn.clicked.connect(self.start_generate)

        self.mode_cb = QComboBox()
        self.mode_cb.addItem('Интерфейс 0', 0)
        self.mode_cb.addItem('Интерфейс 1', 1)
        self.mode_cb.addItem('Интерфейс 2', 2)
        self.mode_cb.setMinimumWidth(150)
        self.mode_cb.setCurrentIndex(0)

        control_lt = QHBoxLayout()
        control_lt.addWidget(self.mode_cb)
        control_lt.addStretch()
        control_lt.addWidget(self.start_btn)

        control_frame = QFrame(self)
        control_frame.setLayout(control_lt)
        control_frame.setFrameShape(QFrame.Panel)
        control_frame.setMaximumHeight(100)

        self.graph_canvas = plot_canvas.GraphCanvas(self)

        main_lt = QVBoxLayout()
        main_lt.addWidget(self.graph_canvas.frame)
        main_lt.addWidget(control_frame)

        self.setLayout(main_lt)

    def initData(self):
        self.serial_port = serial.Serial('COM1', 9600, timeout=1)

        self.timer_flag = False
        timer = QTimer(self)
        timer.timeout.connect(self.read_serial)
        timer.start(1000)

    def start_generate(self):
        current_mode = self.mode_cb.currentIndex()
        byte_mode = (current_mode).to_bytes(1)

        self.serial_port.write(byte_mode)

        print(f'***На МК отправлен байт {byte_mode}***')

        self.start_timer()

        self.start_btn.setText('Стоп')
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.stop_timer)
    
    def start_timer(self):
        print('---Начинаем прием данных от МК---')
        self.timer_flag = True

    def stop_timer(self):
        self.timer_flag = False

        print('---Заканчиваем прием данных от МК---')

        self.start_btn.setText('Старт')
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_generate)

    def read_serial(self):
        if self.timer_flag:
            data = ''
            i = 1
            while True:
                line = self.serial_port.readline()
                if not line:
                    print('Ожидание данных от МК..')
                    break
                
                print(f'Получение данных от МК.. {i}')
                i += 1
                data += bin(int.from_bytes(line)).split('0b')[-1].zfill(8)
            
            if data:
                self.stop_timer()
                self.graph_canvas.go_plot(data)

