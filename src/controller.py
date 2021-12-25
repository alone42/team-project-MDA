import copy

from PyQt5.QtWidgets import QStackedLayout
from src.model import user_settings
from src.view.main_window import MainWindow
from src.view.measurement_page import MeasurementPage
from src.view.settings_page import SettingsPage
from src.view.welcome_page import WelcomePage
from src.model import configuration_settings


class Controller:
    def __init__(self):
        self.configuration_settings = configuration_settings.ConfigurationSettings()

        # self.user_settings = user_settings.UserSettings()
        self.main_window = MainWindow()

        self.layout = QStackedLayout()
        self.main_window.setLayout(self.layout)

        self.welcome_page = WelcomePage()
        self.layout.addWidget(self.welcome_page)

        self.settings_page = SettingsPage()
        self.get_configuration_list()
        self.get_task_order_list()
        self.settings_page.get_configuration_list_signal.connect(self.get_configuration_list)
        self.settings_page.close_connection.connect(self.configuration_settings.close_connection)
        self.settings_page.add_new_configuration_signal.connect(self.add_new_configuration)
        self.settings_page.delete_configuration_signal.connect(self.delete_configuration)
        self.settings_page.delete_all_signal.connect(self.delete_all)

        self.settings_page.order_list_view_widget.get_tasks_signal.connect(self.get_task_order_list)
        self.settings_page.order_list_view_widget.change_tasks_order_signal.connect(self.change_tasks_order)

        self.settings_page.stress_list_view_widget.get_tasks_signal.connect(self.get_tasks)
        self.settings_page.stress_list_view_widget.add_task_signal.connect(self.add_task)
        self.settings_page.stress_list_view_widget.include_task_signal.connect(self.include_task)
        self.settings_page.stress_list_view_widget.exclude_task_signal.connect(self.delete_task_from_order_list)
        self.settings_page.stress_list_view_widget.delete_all_tasks_signal.connect(self.delete_all_tasks)
        self.settings_page.stress_list_view_widget.delete_task_signal.connect(self.delete_task)

        self.settings_page.relax_list_view_widget.get_tasks_signal.connect(self.get_tasks)
        self.settings_page.relax_list_view_widget.add_task_signal.connect(self.add_task)
        self.settings_page.relax_list_view_widget.include_task_signal.connect(self.include_task)
        self.settings_page.relax_list_view_widget.exclude_task_signal.connect(self.delete_task_from_order_list)
        self.settings_page.relax_list_view_widget.delete_all_tasks_signal.connect(self.delete_all_tasks)
        self.settings_page.relax_list_view_widget.delete_task_signal.connect(self.delete_task)
        self.layout.addWidget(self.settings_page)

        self.measurement_page = MeasurementPage()
        self.layout.addWidget(self.measurement_page)

        self.show_welcome_page()

    def change_tasks_order(self, task_id, is_up):
        id_order_rows = self.configuration_settings.get_tasks_order(self.settings_page.configuration_name)
        for idx, item in enumerate(id_order_rows):
            if item[0] == task_id:
                if is_up:
                    self.configuration_settings.update_task_order(item[0], id_order_rows[idx-1][1])
                    self.configuration_settings.update_task_order(id_order_rows[idx-1][0], item[1])
                else:
                    self.configuration_settings.update_task_order(item[0], id_order_rows[idx + 1][1])
                    self.configuration_settings.update_task_order(id_order_rows[idx + 1][0], item[1])
        self.get_task_order_list()

    def delete_all(self):
        self.configuration_settings.recreate_columns()
        self.get_configuration_list()
        self.settings_page.order_list_view_widget.clear_all()

    def show_welcome_page(self):
        self.layout.setCurrentIndex(0)
        self.welcome_page.update_config_list()
        self.welcome_page.measurement_page.connect(self.show_measurement_page)
        self.welcome_page.settings_page.connect(self.show_settings_page)

    def show_settings_page(self, title):
        self.layout.setCurrentIndex(1)
        self.settings_page.get_title(title)
        self.settings_page.switch_window.connect(self.show_welcome_page)

    def show_measurement_page(self, title):
        self.layout.setCurrentIndex(2)
        task_list_tuple = self.configuration_settings.select_data_by_selected_configuration(title)
        task_list = list(map(lambda x: list(x), task_list_tuple))
        self.measurement_page.get_title(task_list)
        self.measurement_page.switch_window.connect(self.show_welcome_page)

    def get_tasks(self, stimuli_type):
        try:
            title = self.settings_page.configuration_name
            tasks_id_tuple = self.configuration_settings.select_data_by_selected_configuration_and_type(title, stimuli_type)
            tasks_id = list(map(lambda x: int(x[0]), tasks_id_tuple))
            if stimuli_type == "stress":
                self.settings_page.stress_list_view_widget.check_added_tasks(tasks_id)
            else:
                self.settings_page.relax_list_view_widget.check_added_tasks(tasks_id)
        except:
            print("Error. Failed to load data from db.")
        task_list = list(map(lambda x: list(x), self.configuration_settings.select_tasks_by_type(stimuli_type)))
        if stimuli_type == "stress":
            self.settings_page.stress_list_view_widget.update_task_list(task_list)
        else:
            self.settings_page.relax_list_view_widget.update_task_list(task_list)

    def add_task(self, new_task):
        self.configuration_settings.add_new_task(new_task)
        self.get_tasks(new_task[1])

    def get_configuration_list(self):
        configuration_list = list(map(lambda x: list(x), self.configuration_settings.select_available_configurations()))
        self.settings_page.update_configuration_list(configuration_list)

    def include_task(self, task_id):
        title = self.settings_page.configuration_name
        for sublist in self.settings_page.configuration_list:
            if title == sublist[1]:
                configuration_id = sublist[0]
                order_number = len(self.settings_page.order_list_view_widget.task_order_list)
                self.configuration_settings.create_assignee([configuration_id, task_id, order_number])
                self.settings_page.order_list_view_widget.load_selected_configuration()

    def get_task_order_list(self):
        title = self.settings_page.configuration_dropdown_btn.currentText()
        task_order_list = self.configuration_settings.select_data_by_selected_configuration(title)
        self.settings_page.order_list_view_widget.update_task_list(list(map(lambda x: list(x), task_order_list)))

    def delete_task_from_order_list(self, task_id):
        self.configuration_settings.delete_task_from_configuration(task_id)

    def delete_all_tasks(self, stimuli_type):
        self.configuration_settings.delete_all_tasks(stimuli_type)

    def delete_task(self, task_id):
        self.configuration_settings.delete_task(task_id)

    def add_new_configuration(self):
        title = self.settings_page.configuration_name
        self.configuration_settings.add_new_configuration(title)
        self.get_configuration_list()
        # if self.settings_page.configuration_dropdown_btn.currentText() == "None":
        #     self.settings_page.configuration_dropdown_btn.clear()
        # self.settings_page.configuration_dropdown_btn.addItem(title)
        self.settings_page.configuration_dropdown_btn.setCurrentText(title)
        self.settings_page.load_data_for_selected_configuration()

    def delete_configuration(self, title):
        self.configuration_settings.delete_configuration(title)