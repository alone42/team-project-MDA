from PyQt5.QtWidgets import QWidget
from win32api import GetSystemMetrics


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Team app")
        self.setFixedSize(GetSystemMetrics(0), GetSystemMetrics(1)-100)
