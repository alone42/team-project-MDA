from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLabel, QVBoxLayout, QHBoxLayout

from src.model import configuration_settings
from src.view import calibration_window


class WelcomePage(QWidget):
    measurement_page = QtCore.pyqtSignal(str)
    settings_page = QtCore.pyqtSignal(str)

    def __init__(self):
        super(WelcomePage, self).__init__()

        self.configuration_settings = configuration_settings.ConfigurationSettings()

        layout = QVBoxLayout()

        self.calibration_layout = QHBoxLayout()
        layout.addLayout(self.calibration_layout)
        self.calibration_layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.calibration_btn = QPushButton("Calibration")
        self.calibration_btn.clicked.connect(self.calibration)
        self.calibration_btn.setObjectName("welcome_btn")
        self.calibration_layout.addWidget(self.calibration_btn)

        self.form_layout = QHBoxLayout()
        layout.addLayout(self.form_layout)
        self.form_layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.configuration_label = QLabel("Configuration :")
        self.configuration_label.setObjectName("configuration_label")
        self.form_layout.addWidget(self.configuration_label)

        self.configuration_dropdown_btn = QComboBox()
        self.configuration_dropdown_btn.setObjectName("configuration_dropdown_btn")
        self.form_layout.addWidget(self.configuration_dropdown_btn)

        self.horizontal_layout = QHBoxLayout()
        layout.addLayout(self.horizontal_layout)

        self.switch_measurement_page_btn = QPushButton("Test")
        self.switch_measurement_page_btn.clicked.connect(self.switch_measurement_page)
        self.switch_measurement_page_btn.setObjectName("welcome_btn")
        self.horizontal_layout.addWidget(self.switch_measurement_page_btn)

        self.switch_settings_page_btn = QPushButton("Settings")
        self.switch_settings_page_btn.clicked.connect(self.switch_settings_page)
        self.switch_settings_page_btn.setObjectName("welcome_btn")
        self.horizontal_layout.addWidget(self.switch_settings_page_btn)

        self.setLayout(layout)

        self.calibration_window = calibration_window.CalibrationWindow()

    def calibration(self):
        self.calibration_window.reset(True)
        self.calibration_window.show()
        self.calibration_window.start()

    def update_config_list(self):
        self.configuration_dropdown_btn.clear()
        if not self.configuration_settings.select_available_configurations():
            self.switch_measurement_page_btn.setEnabled(False)
            self.configuration_dropdown_btn.addItem('None')
        else:
            self.switch_measurement_page_btn.setEnabled(True)
            for item in self.configuration_settings.select_available_configurations():
                self.configuration_dropdown_btn.addItem(''.join(item[1]))

    def switch_measurement_page(self):
        self.measurement_page.emit(self.configuration_dropdown_btn.currentText())

    def switch_settings_page(self):
        self.settings_page.emit(self.configuration_dropdown_btn.currentText())
