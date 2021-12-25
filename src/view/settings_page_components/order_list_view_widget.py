import configparser
import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QLineEdit, \
    QCheckBox, QScrollArea


class OrderListViewWidget(QWidget):
    save_settings = QtCore.pyqtSignal(list)
    get_tasks_signal = QtCore.pyqtSignal()
    change_tasks_order_signal = QtCore.pyqtSignal(int, bool)

    def __init__(self):
        super(OrderListViewWidget, self).__init__()

        self.task_order_list = []
        self.selected_task_idx = -1

        layout = QGridLayout()
        self.setLayout(layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1, 1, 1, -1)

        self.no_file_path_label = QLabel("No file selected")
        self.scroll_layout.addWidget(self.no_file_path_label)

        self.move_up_task_btn = QPushButton("Up")
        self.move_up_task_btn.clicked.connect(self.move_up_task)
        self.move_up_task_btn.setEnabled(False)
        layout.addWidget(self.move_up_task_btn, 2, 1)

        self.move_down_task_btn = QPushButton("Down")
        self.move_down_task_btn.clicked.connect(self.move_down_task)
        self.move_down_task_btn.setEnabled(False)
        layout.addWidget(self.move_down_task_btn, 2, 2)

    def load_selected_configuration(self):
        self.get_tasks_signal.emit()

    def update_task_list(self, task_list):
        self.task_order_list = task_list
        self.update_task_widgets()

    def update_task_widgets(self):
        self.clear_all()
        if self.task_order_list:
            self.no_file_path_label.hide()
            for idx, item in enumerate(self.task_order_list):
                task_widget = QWidget()
                task_widget_layout = QHBoxLayout()
                task_widget.setLayout(task_widget_layout)

                check_task_box = QCheckBox(self)
                check_task_box.index = idx + 1
                check_task_box.stateChanged.connect(self.check_task_line)
                task_widget_layout.addWidget(check_task_box)

                task = QLineEdit(item[1])
                task_widget_layout.addWidget(task)

                stimulus_type_line = QLineEdit(item[2])
                task_widget_layout.addWidget(stimulus_type_line)

                self.scroll_layout.addWidget(task_widget)

    def check_task_line(self, state):
        if state == QtCore.Qt.Checked:
            self.move_up_task_btn.setEnabled(True)
            self.move_down_task_btn.setEnabled(True)
            check_task_box = self.sender()
            self.selected_task_idx = check_task_box.index
            for idx in range(1, self.scroll_layout.count()):
                widget = self.scroll_layout.itemAt(idx).widget()
                layout = widget.layout()
                child_widget = layout.itemAt(0).widget()
                if child_widget.index != self.selected_task_idx:
                    child_widget.setChecked(False)
        else:
            self.move_up_task_btn.setEnabled(False)
            self.move_down_task_btn.setEnabled(False)

    def move_up_task(self):
        if self.selected_task_idx - 1 >= 1:
            self.change_tasks_order_signal.emit(self.task_order_list[self.selected_task_idx - 1][0], True)
            self.move_up_task_btn.setEnabled(False)
            self.move_down_task_btn.setEnabled(False)

    def move_down_task(self):
        if self.selected_task_idx + 1 <= len(self.task_order_list):
            self.change_tasks_order_signal.emit(self.task_order_list[self.selected_task_idx - 1][0], False)
            self.move_up_task_btn.setEnabled(False)
            self.move_down_task_btn.setEnabled(False)

    def clear_all(self):
        for index in range(1, self.scroll_layout.count()):
            self.scroll_layout.itemAt(index).widget().deleteLater()
        self.no_file_path_label.show()

