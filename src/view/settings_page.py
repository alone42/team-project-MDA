import configparser
import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTabWidget, QLineEdit, QComboBox, QMessageBox, \
    QHBoxLayout, QVBoxLayout

from src.view.settings_page_components import stimuli_list_view_widget, item_view_widget, order_list_view_widget, \
    measurement_file_setting_widget, get_configuration_title_window


class SettingsPage(QWidget):
    switch_window = QtCore.pyqtSignal()
    save_settings = QtCore.pyqtSignal(list, list)
    close_connection = QtCore.pyqtSignal()
    get_configuration_list_signal = QtCore.pyqtSignal()
    add_new_configuration_signal = QtCore.pyqtSignal()
    delete_configuration_signal = QtCore.pyqtSignal(str)
    delete_all_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(SettingsPage, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.file_number = 0
        self.previous_state = -1
        self.task_list = []
        self.measurement_file_settings = ['', '', '']
        self.configuration_list = []
        self.configuration_name = ""

        self.back_create_layout = QHBoxLayout()
        layout.addLayout(self.back_create_layout)

        self.menu_btn = QPushButton('Back to menu')
        self.menu_btn.clicked.connect(self.switch)
        self.back_create_layout.addWidget(self.menu_btn)

        self.add_new_configuration_btn = QPushButton('Create new')
        self.add_new_configuration_btn.clicked.connect(self.add_new_configuration)
        self.back_create_layout.addWidget(self.add_new_configuration_btn)

        self.horizontal_layout = QHBoxLayout()
        layout.addLayout(self.horizontal_layout)
        self.horizontal_layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.configuration_dropdown_btn = QComboBox()
        self.configuration_dropdown_btn.currentIndexChanged.connect(self.load_data_for_selected_configuration)
        self.configuration_dropdown_btn.setObjectName("configuration_dropdown_btn")
        self.horizontal_layout.addWidget(self.configuration_dropdown_btn)

        self.delete_configuration_btn = QPushButton("Delete")
        self.delete_configuration_btn.setObjectName("delete_configuration_btn")
        self.delete_configuration_btn.clicked.connect(self.delete_configuration)
        self.horizontal_layout.addWidget(self.delete_configuration_btn)

        self.delete_all_btn = QPushButton("Delete all")
        self.delete_all_btn.clicked.connect(self.delete_all)
        self.horizontal_layout.addWidget(self.delete_all_btn)

        # self.save_user_settings_btn = QPushButton('Save configuration')
        # self.save_user_settings_btn.clicked.connect(self.save_user_settings)
        # layout.addWidget(self.save_user_settings_btn)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.order_list_view_widget = order_list_view_widget.OrderListViewWidget()
        self.tabs.addTab(self.order_list_view_widget, "Selected items")

        self.stress_list_view_widget = stimuli_list_view_widget.StimuliListViewWidget()
        self.stress_list_view_widget.stimuli_type = "stress"
        self.tabs.addTab(self.stress_list_view_widget, "Stress stimuli")

        self.relax_list_view_widget = stimuli_list_view_widget.StimuliListViewWidget()
        self.relax_list_view_widget.stimuli_type = "relax"
        self.tabs.addTab(self.relax_list_view_widget, "Relax stimuli")

        # self.item_view_widget = item_view_widget.ItemViewWidget()
        # self.tabs.addTab(self.item_view_widget, "Item view")

        # self.measurement_file_setting_widget = measurement_file_setting_widget.MeasurementFileSettingWidget()
        # self.measurement_file_setting_widget.measurement_file_settings = self.measurement_file_settings
        # self.tabs.addTab(self.measurement_file_setting_widget, "Measurement file setting")

        self.tabs.currentChanged.connect(self.update_task_list)

        self.get_configuration_title_window = get_configuration_title_window.GetConfigurationTitleWindow()
        self.get_configuration_title_window.btn_clicked_signal.connect(self.cancel_parent_window)

    def delete_all(self):
        self.delete_all_signal.emit()

    def delete_configuration(self):
        self.delete_configuration_signal.emit(self.configuration_dropdown_btn.currentText())
        self.get_configuration_list_signal.emit()
        self.load_data_for_selected_configuration()

    def add_new_configuration(self):
        self.get_configuration_title_window.show()

    def load_data_for_selected_configuration(self):
        self.configuration_name = copy.copy(self.get_configuration_title_window.name_line_edit.text())
        self.order_list_view_widget.load_selected_configuration()
        self.stress_list_view_widget.unchecked_all()
        self.relax_list_view_widget.unchecked_all()

    def get_configuration_list(self):
        self.get_configuration_list_signal.emit()

    def cancel_parent_window(self, state):
        if state:
            self.configuration_name = copy.copy(self.get_configuration_title_window.name_line_edit.text())
            self.add_new_configuration_signal.emit()
            self.stress_list_view_widget.unchecked_all()
            self.relax_list_view_widget.unchecked_all()
        self.get_configuration_title_window.name_line_edit.setText("New configuration")
        self.get_configuration_title_window.hide()

    def update_configuration_list(self, configuration_list):
        self.configuration_list = configuration_list
        self.configuration_dropdown_btn.clear()
        if self.configuration_list:
            for item in self.configuration_list:
                self.configuration_dropdown_btn.addItem(''.join(item[1]))
        else:
            self.configuration_dropdown_btn.addItem("None")

    def update_task_list(self, state):
        if state == 0:
            self.order_list_view_widget.load_selected_configuration()
        elif state == 1:
            self.stress_list_view_widget.load_all_tasks()
        elif state == 2:
            self.relax_list_view_widget.load_all_tasks()
        elif state == 3:
            pass
            # self.item_view_widget.load_selected_configuration()

    def get_title(self, title):
        try:
            self.configuration_dropdown_btn.setCurrentText(title)
        except:
            print("Error. Failed to load the selected configuration.")

    def save_user_settings(self):
        self.close_connection.emit()

    def switch(self):
        self.switch_window.emit()

    def switch_to_item_view(self, file_path, index, stimuli_type):
        self.tabs.setCurrentIndex(3)
        self.item_view_widget.load_tasks(file_path, index, stimuli_type)

