import configparser

from PyQt5 import QtCore
from PyQt5.QtCore import QFileInfo, QTime
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QCheckBox, QFileDialog, QScrollArea, QTimeEdit


class StimuliListViewWidget(QWidget):
    view_task = QtCore.pyqtSignal(list, int, str)
    get_tasks_signal = QtCore.pyqtSignal(str)
    add_task_signal = QtCore.pyqtSignal(list)
    include_task_signal = QtCore.pyqtSignal(int)
    exclude_task_signal = QtCore.pyqtSignal(int)
    delete_all_tasks_signal = QtCore.pyqtSignal(str)
    delete_task_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(StimuliListViewWidget, self).__init__()

        self.stimuli_task_list = []
        self.checked_tasks_id = []
        layout = QGridLayout()
        self.setLayout(layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1, 1, 1, -1)

        self.stimuli_type = ""
        self.file_number = 0
        self.no_file_path_label = QLabel("No file added.")
        self.no_file_path_label.setObjectName("no_file_path_label")
        self.no_file_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_layout.addWidget(self.no_file_path_label)

        self.add_file_btn = QPushButton("Add file")
        self.add_file_btn.clicked.connect(self.add_new_task)
        layout.addWidget(self.add_file_btn, 2, 1)

        self.save_user_settings_btn = QPushButton("Clear all")
        self.save_user_settings_btn.clicked.connect(self.clear_file_path_list)
        layout.addWidget(self.save_user_settings_btn, 2, 3)

    def load_all_tasks(self):
        self.get_tasks_signal.emit(self.stimuli_type)
        self.file_number = 0

    def update_task_list(self, task_list):
        self.stimuli_task_list = task_list
        self.update_task_widgets()

    def update_task_widgets(self):
        self.clear_all()
        if self.stimuli_task_list:
            self.add_task_widgets(self.stimuli_task_list)
            self.no_file_path_label.hide()
        else:
            self.no_file_path_label.show()

    def add_new_task(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        if dialog.exec():
            file_paths = dialog.selectedFiles()
            for file_path in file_paths:
                file = QFileInfo(file_path)
                new_task = [file.baseName(), self.stimuli_type, file.filePath(), '00:00:00', '00:00:00']
                self.file_number += 1
                self.add_task_signal.emit(new_task)
                # new_task_with_id = [-1] + new_task
                # self.add_task_widgets([new_task_with_id])

    def add_task_widgets(self, task_list):
        self.no_file_path_label.hide()
        for idx, item in enumerate(task_list):
            task_widget = QWidget()
            task_widget_layout = QHBoxLayout()
            task_widget.setLayout(task_widget_layout)

            add_task_box = QCheckBox(self)
            add_task_box.index = idx + 1

            if item[0] in self.checked_tasks_id:
                add_task_box.setChecked(True)
            add_task_box.stateChanged.connect(self.include_task)
            task_widget_layout.addWidget(add_task_box)

            file_name_line = QLineEdit(item[1])
            file_name_line.index = self.file_number
            #file_name_line.textEdited.connect(self.edit_task_name)
            task_widget_layout.addWidget(file_name_line)

            begin = QTimeEdit()
            begin.setTime(QTime.fromString(item[3]))
            begin.index = idx + 1

            file = QFileInfo(item[2])
            # if file.suffix() == 'txt':
            #     begin.setReadOnly(True)
            begin.setReadOnly(True)
            begin.timeChanged.connect(self.task_time_begin)
            task_widget_layout.addWidget(begin)

            end = QTimeEdit()
            end.setTime(QTime.fromString(item[4]))
            end.index = idx + 1
            end.setReadOnly(True)
            end.timeChanged.connect(self.task_time_end)
            task_widget_layout.addWidget(end)

            view_task_btn = QPushButton("View")
            view_task_btn.index = self.file_number
            view_task_btn.setEnabled(False)
            view_task_btn.clicked.connect(self.switch_to_item_view)
            task_widget_layout.addWidget(view_task_btn)

            remove_task_btn = QPushButton("Remove")
            remove_task_btn.index = self.file_number
            remove_task_btn.clicked.connect(self.remove_task)
            task_widget_layout.addWidget(remove_task_btn)

            self.scroll_layout.addWidget(task_widget)

    def update_configuration(self):
        pass

    def edit_task_name(self):
        line = self.sender()
        index = line.index
        self.stimuli_task_list[index - 1] = line.text()
        self.update_configuration()

    def task_time_begin(self):
        time = self.sender()
        index = time.index
        self.stimuli_tasks_time_start[index - 1] = time.text()
        self.update_configuration()

    def task_time_end(self):
        time = self.sender()
        index = time.index
        self.stimuli_tasks_time_stop[index-1] = time.text()
        self.update_configuration()

    def include_task(self, state):
        include_task_box = self.sender()
        index = include_task_box.index
        if state == QtCore.Qt.Checked:
            self.include_task_signal.emit(self.stimuli_task_list[index-1][0])
        else:
            self.exclude_task(self.stimuli_task_list[index-1][0])

    def exclude_task(self, task_id):
        self.exclude_task_signal.emit(task_id)

    def remove_task(self):
        btn = self.sender()
        index = btn.index
        self.delete_task_signal.emit(self.stimuli_task_list[index][0])
        self.load_all_tasks()

    def clear_file_path_list(self):
        for idx in range(len(self.stimuli_task_list)):
            self.exclude_task(idx)
        self.stimuli_task_list = []
        self.clear_all()
        self.file_number = 0
        self.no_file_path_label.show()
        self.delete_all_tasks_signal.emit(self.stimuli_type)

    def clear_all(self):
        for index in range(1, self.scroll_layout.count()):
            self.scroll_layout.itemAt(index).widget().deleteLater()

    def switch_to_item_view(self):
        btn = self.sender()
        index = btn.index
        # self.view_task.emit(self.stimuli_task_list, index - 1, self.stimuli_type)

    def check_added_tasks(self, checked_tasks_id):
        self.checked_tasks_id = checked_tasks_id

    def unchecked_all(self):
        for idx in range(1, self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(idx).widget()
            layout = widget.layout()
            child_widget = layout.itemAt(0).widget()
            child_widget.setCheckState(False)
