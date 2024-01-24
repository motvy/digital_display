from PyQt5.QtWidgets import QApplication
import sys

import main_window

app = QApplication(sys.argv)

window = main_window.MainWindow()
window.show()

app.exec()