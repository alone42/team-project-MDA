import copy
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QRadioButton, QPushButton, QHBoxLayout


class TestWidget(QWidget):
    task_ended = QtCore.pyqtSignal(list)

    def __init__(self):
        super(TestWidget, self).__init__()

        self.file_path = None
        self.test_data = ""
        self.characters = ["a", "b", "c", "d"]
        self.question_list = []
        self.correct_answers = []
        self.user_answers = []
        self.answer_list = []
        self.question_idx = 0
        self.answer_selection_btn_list = []

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.task_data = []

        self.time = []
        self.default_time = [0, 1, 30, 0]
        self.end_time = []
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timing)
        self.timer_label = QLabel("")
        self.timer_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.timer_label.setObjectName("timer")
        layout.addWidget(self.timer_label)

        self.question_label = QLabel(None)
        self.question_label.setObjectName("test_data")
        layout.addWidget(self.question_label)

        self.image_label = QLabel(self)
        self.pixmap = QPixmap(None)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.resize(300, 300) # self.pixmap.width(), self.pixmap.height())
        self.image_label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(self.image_label)

        for idx_characters in range(len(self.characters)):
            self.answer_selection_btn_list.append(QRadioButton("None"))
            self.answer_selection_btn_list[idx_characters].character = self.characters[idx_characters]
            self.answer_selection_btn_list[idx_characters].toggled.connect(self.answer_selection)
            layout.addWidget(self.answer_selection_btn_list[idx_characters])

        self.answer_selection_btn_0 = QRadioButton("None")
        layout.addWidget(self.answer_selection_btn_0)
        self.answer_selection_btn_0.hide()

        move_btn_layout = QHBoxLayout()
        move_btn_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(move_btn_layout)

        move_on_btn = QPushButton("Next")
        move_on_btn.clicked.connect(self.move_on)
        move_on_btn.setObjectName("welcome_btn")
        move_btn_layout.addWidget(move_on_btn)

    def reset(self):
        self.question_idx = 0
        self.timer.stop()
        self.time = copy.copy(self.end_time)

    def answer_selection(self):
        answer_selection_btn = self.sender()
        if answer_selection_btn.isChecked():
            self.user_answers[self.question_idx - 1] = answer_selection_btn.character

    def end(self):
        self.test_data.append(''.join(item for item in self.correct_answers))
        if self.user_answers:
            self.test_data.append(''.join(item for item in self.user_answers))
        else:
            self.test_data.append("empty")
        self.task_ended.emit(self.test_data)

    def move_on(self):
        if self.question_idx == len(self.answer_list):
            self.end()
        else:
            self.question_label.setText(self.question_list[self.question_idx])
            try:
                filename, file_extension = os.path.splitext(self.file_path)
                self.pixmap = QPixmap(filename + str(self.question_idx + 1)+".jpg")
                self.image_label.setPixmap(self.pixmap)
                self.image_label.show()
            except:
                self.image_label.hide()
            for idx_characters in range(len(self.characters)):
                self.answer_selection_btn_list[idx_characters]\
                    .setText(self.answer_list[self.question_idx][idx_characters])
            self.answer_selection_btn_0.setChecked(True)
            self.question_idx += 1

    def get_question(self):
        answer_list = []
        with open(self.file_path, "r", encoding="utf8") as reader:
            for line in reader:
                if line[0].isdigit():
                    self.question_list.append(line.strip())
                elif line[0] == "P":
                    self.correct_answers.append(line[20])
                    self.answer_list.append(answer_list)
                    answer_list = []
                elif line[0].isalpha():
                    answer_list.append(line.strip())
        self.user_answers = ['' for i in range(len(self.correct_answers))]

    def start(self, task):
        if task[4] != "00:00:00":
            end = list(task[4].split(":"))
            self.end_time = [int(item) for item in end] + [0]
            self.timer_label.setText(task[5])
        else:
            self.end_time = copy.copy(self.default_time)
        self.time = copy.copy(self.end_time)

        self.timer.start(1)
        self.question_idx = 0
        self.question_list = []
        self.correct_answers = []
        self.answer_list = []
        self.test_data = []
        self.file_path = task[3]
        self.get_question()
        self.move_on()

    def timing(self):
        self.time[3] -= 1
        if self.time[3] <= 0:
            self.time[2] -= 1
            self.time[3] += 1000
            show_time = True
        else:
            show_time = False
        if self.time[2] == -1:
            self.time[1] -= 1
            self.time[2] += 60
        if self.time[1] == -1:
            self.time[0] -= 1
            self.time[1] += 60
        if show_time:
            time_counter_str = ""
            for time_idx, time_item in enumerate(self.time[:-1]):
                if time_item < 10:
                    time_counter_str += "0" + str(time_item)
                else:
                    time_counter_str += str(time_item)
                if time_idx != 2:
                    time_counter_str += ":"
            self.timer_label.setText(time_counter_str)
            if self.time[:-1] == [0, 0, 0]:
                self.end()
