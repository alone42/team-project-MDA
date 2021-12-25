import copy
import os.path
import csv
import random
from datetime import datetime

from PyQt5.QtGui import QMovie
from pymediainfo import MediaInfo
from PyQt5 import QtCore, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QFormLayout, QLineEdit, QComboBox, QSpinBox, \
    QTextEdit, QHBoxLayout, QVBoxLayout

from src.view.measurement_page_components import video_widget, test_widget


class MeasurementPage(QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(MeasurementPage, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.task_idx = 0
        self.task_list = []
        self.csv_name = "measurements.csv"
        self.csv_path = ""
        self.character = ","
        self.test_time_now = ""
        self.stimuli_type = ""
        self.user_id = ""
        self.csv_headers = ["id", "system time", "user", "gender", "age", "additional information", "file name",
                            "stimuli type", "user answers"]
        self.task_measurements = []
        self.title = ''

        self.horizontal_layout = QHBoxLayout()
        layout.addLayout(self.horizontal_layout)

        self.menu_btn = QPushButton("Back to menu")
        self.menu_btn.clicked.connect(self.switch)
        self.horizontal_layout.addWidget(self.menu_btn)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start)
        self.horizontal_layout.addWidget(self.start_btn)

        # self.resume_pause_btn = QPushButton("Pause")
        # self.resume_pause_btn.clicked.connect(self.resume_pause)
        # self.horizontal_layout.addWidget(self.resume_pause_btn)
        # self.resume_pause_btn.hide()

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset)
        self.horizontal_layout.addWidget(self.reset_btn)

        self.finish_btn = QPushButton("Finish")
        self.finish_btn.clicked.connect(self.finish)
        self.horizontal_layout.addWidget(self.finish_btn)
        self.finish_btn.setEnabled(False)

        self.tasks_layout = QVBoxLayout()
        layout.addLayout(self.tasks_layout)
        self.tasks_layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.video_flag = False
        self.video_widget = video_widget.VideoWidget()
        self.video_widget.move(160, 100)
        #self.video_widget.setAlignment(QtCore.Qt.AlignHCenter)
        self.video_widget.task_ended.connect(self.switch_task)
        layout.addWidget(self.video_widget)
        self.video_widget.hide()

        self.test_flag = False
        self.test_widget = test_widget.TestWidget()
        self.test_widget.task_ended.connect(self.switch_task)
        layout.addWidget(self.test_widget)
        self.test_widget.hide()

        self.user_data = QWidget()
        self.tasks_layout.addWidget(self.user_data)

        self.user_name = QLineEdit()
        self.user_gender = QComboBox()
        self.user_gender.addItems(['Man', 'Woman'])
        self.user_age = QSpinBox()
        self.user_age.setValue(25)
        self.user_age.setRange(1, 100)
        self.user_age.setSingleStep(1)
        self.user_additional_information = QTextEdit()

        self.user_data.setObjectName("user_data")
        self.user_data_layout = QFormLayout()
        self.user_data.setLayout(self.user_data_layout)
        self.user_data_layout.addRow("User name: ", self.user_name)
        self.user_data_layout.addRow("Gender: ", self.user_gender)
        self.user_data_layout.addRow("Age: ", self.user_age)
        self.user_data_layout.addRow("Additional information: ", self.user_additional_information)

        self.no_file_path_label = QLabel("Lack of tasks, please go to settings and add.")
        self.no_file_path_label.setObjectName("measurement_page_label")
        self.no_file_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tasks_layout.addWidget(self.no_file_path_label)

        self.pause_label = QLabel()
        self.movie = QMovie("resources/qoobee.gif")
        self.pause_label.setMovie(self.movie)
        self.movie.finished.connect(self.start_movie)
        self.movie.start()
        self.pause_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tasks_layout.addWidget(self.pause_label)
        self.pause_label.hide()

        self.results_label = QLabel("Good job! You scored " + str(random.randint(70, 99)) + "/100!")
        self.results_label.setObjectName("measurement_page_label")
        self.tasks_layout.addWidget(self.results_label)
        self.results_label.hide()

        self.time = [0, 0, 0, 0]
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timing)

    def start_movie(self):
        self.movie.start()

    def get_title(self, task_list):
        self.task_list = task_list
        if self.task_list:
            self.no_file_path_label.hide()
            self.user_data.show()
            self.start_btn.setEnabled(True)
            self.reset_btn.setEnabled(True)

            # file_info = QtCore.QFileInfo(self.task_list[0][3])
            # self.csv_path = copy.copy(file_info.path())
            # if not os.path.exists(self.csv_path + "/" + self.csv_name):
            #     self.write_to_csv(self.csv_headers)
        else:
            self.no_file_path_label.show()
            self.user_data.hide()
            self.start_btn.setEnabled(False)
            self.reset_btn.setEnabled(False)

    def start(self):
        self.finish_btn.setEnabled(True)
        self.start_btn.hide()
        self.results_label.hide()
        self.user_data.hide()
        # self.resume_pause_btn.show()
        now = datetime.now()
        self.test_time_now = ":".join([str(idx) for idx in self.time[:-1]])
        self.test_time_now += "." + str(self.time[-1])
        self.timer.start(1)
        if self.user_name.text() == '':
            self.user_id = "user" + str(now.strftime("%d%m%y%H%M%S"))
        else:
            self.user_id = copy.copy(self.user_name.text())
        self.task_display()

    def timing(self):
        self.time[3] += 1
        if self.time[3] >= 1000:
            self.time[2] += 1
            self.time[3] -= 1000
        if self.time[2] == 60:
            self.time[1] += 1
            self.time[2] -= 60
        if self.time[1] == 60:
            self.time[0] += 1
            self.time[1] -= 60

    def task_display(self):
        self.video_flag = False
        self.test_flag = False
        self.test_widget.hide()
        self.video_widget.hide()
        if self.user_additional_information.toPlainText() == "":
            additional_information = 'empty'
        else:
            additional_information = self.user_additional_information.toPlainText()
        # self.write_to_txt([datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3], 'none', self.task_idx,
        #                    self.task_list[self.task_idx][2], 'aplikacja', 'teamProjectMDA.exe', 'stymulacja.txt',
        #                    self.task_list[self.task_idx][1], self.task_list[self.task_idx][3], self.user_id,
        #                    self.user_gender.currentText(), self.user_age.value(), additional_information, 'none',
        #                    'none', 'none', 'none', 'none'])
        self.task_measurements = [self.task_idx, str(datetime.now())[:-3], self.user_id, self.user_gender.currentText(),
                                  self.user_age.value(), additional_information, self.task_list[self.task_idx][1],
                                  self.task_list[self.task_idx][2]]
        self.task_measurements.append(self.test_time_now)
        filename, file_extension = os.path.splitext(self.task_list[self.task_idx][3])
        self.stimuli_type = self.task_list[self.task_idx][2]

        file_info = MediaInfo.parse(self.task_list[self.task_idx][3])
        track_type_list = list(track.track_type for track in file_info.tracks)
        if 'Video' in track_type_list:
            self.video_flag = True
            self.video_widget.show()
            self.video_widget.start(self.task_list[self.task_idx])
        elif file_extension == ".txt":
            self.test_flag = True
            self.test_widget.show()
            self.test_widget.start(self.task_list[self.task_idx])
        else:
            self.switch_task(["error", "error"])
            print("error: cannot load the file", self.task_list[self.task_idx][3])

    # def write_to_txt(self, content):
    #     path = "resources/stymulacja.txt"
    #     counter = 0
    #     while os.path.exists(path):
    #         counter += 1
    #         if counter >= 500:
    #             counter = 0
    #             print(".", end=" ")
    #     with open(path, "a", newline="") as csvfile:
    #         writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=',')
    #         writer.writerow(content)

    # def resume_pause(self):
    #     resume_pause_btn = self.sender()
    #     if resume_pause_btn.text() == "Pause":
    #         self.resume_pause_btn.setText("Resume")
    #         self.pause_label.show()
    #         self.timer.stop()
    #         if self.test_flag:
    #             self.test_widget.hide()
    #             self.test_widget.timer.stop()
    #         elif self.video_flag:
    #             self.video_widget.hide()
    #             self.video_widget.play_pause_video()
    #     else:
    #         self.resume_pause_btn.setText("Pause")
    #         self.pause_label.hide()
    #         self.timer.start(1)
    #         if self.test_flag:
    #             self.test_widget.show()
    #             self.test_widget.timer.start(1)
    #         elif self.video_flag:
    #             self.video_widget.show()
    #             self.video_widget.play_pause_video()

    def write_to_csv(self, content):
        with open("resources/measurements.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=',')
            writer.writerow(content)

    def reset(self):
        self.pause_label.hide()
        self.user_name.clear()
        self.user_age.setValue(25)
        self.user_gender.setCurrentIndex(0)
        self.user_additional_information.clear()
        self.user_data.show()
        self.start_btn.setEnabled(True)
        self.results_label.hide()
        # self.resume_pause_btn.setText("Pause")
        # self.resume_pause_btn.hide()
        self.start_btn.show()
        self.task_idx = 0
        self.timer.stop()
        self.time = [0, 0, 0, 0]
        if self.video_flag:
            self.video_flag = False
            self.video_widget.hide()
            self.video_widget.media_player.stop()
        elif self.test_flag:
            self.test_flag = False
            self.test_widget.hide()
            self.test_widget.reset()

    def switch_task(self, data):
        self.test_time_now = ":".join([str(idx) for idx in self.time[:-1]])
        self.test_time_now += "." + str(self.time[-1])
        self.task_measurements.append(self.test_time_now)
        self.task_measurements.append(data[0])
        self.task_measurements.append(data[1])
        self.write_to_csv(self.task_measurements)
        self.task_idx += 1
        if self.task_idx < len(self.task_list):
            self.task_display()
        else:
            self.finish_btn.setEnabled(False)
            self.reset()
            self.user_data.hide()
            self.start_btn.setEnabled(False)
            self.results_label.show()
            # self.write_to_txt([datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3], 'flag', 'none', 'end scenario',
            #                    'aplikacja', 'teamProjectMDA.exe', 'stymulacja.txt', 'none', 'none', 'none', 'none',
            #                    'none', 'none', 'none', 'none', 'none', 'none', 'none'])

    def finish(self):
        self.finish_btn.setEnabled(False)
        self.reset()
        self.user_data.hide()
        self.start_btn.setEnabled(False)
        self.results_label.show()
        # self.write_to_txt([datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3], 'flag', 'none', 'end scenario',
        #                    'aplikacja', 'teamProjectMDA.exe', 'stymulacja.txt', 'none', 'none', 'none', 'none',
        #                    'none', 'none', 'none', 'none', 'none', 'none', 'none'])

    def switch(self):
        self.reset()
        self.switch_window.emit()
