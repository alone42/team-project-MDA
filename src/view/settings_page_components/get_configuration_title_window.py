from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QWidget


class GetConfigurationTitleWindow(QWidget):
    btn_clicked_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create new configuration")
        self.setFixedSize(500, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_layout = QHBoxLayout()
        layout.addLayout(self.name_layout)

        self.name_label = QLabel("Name: ")
        self.name_layout.addWidget(self.name_label)

        self.name_line_edit = QLineEdit("New configuration")
        self.name_layout.addWidget(self.name_line_edit)

        self.accept_cancel_layout = QHBoxLayout()
        layout.addLayout(self.accept_cancel_layout)

        self.accept_btn = QPushButton("OK")
        self.accept_btn.clicked.connect(self.accept)
        self.accept_cancel_layout.addWidget(self.accept_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel)
        self.accept_cancel_layout.addWidget(self.cancel_btn)

    def accept(self):
        if self.name_line_edit.text():
            self.btn_clicked_signal.emit(True)

    def cancel(self):
        self.btn_clicked_signal.emit(False)

