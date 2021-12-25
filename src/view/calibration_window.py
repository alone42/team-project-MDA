import csv
import os
import random
import time
from datetime import datetime

from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QTextEdit
from win32api import GetSystemMetrics


class CalibrationWindow(QWidget):
    btn_clicked_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calibration")
        self.setFixedSize(GetSystemMetrics(0), GetSystemMetrics(1)-100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)
        # self.video_widget.setMaximumSize(800, 600)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(None)))
        self.media_player.stateChanged.connect(self.video_ended)

        self.question_label = QLabel("None")
        layout.addWidget(self.question_label)
        font = "font-size: 30px;"
        self.question_label.setStyleSheet(font)
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_label.hide()

        self.stroop_test_widget = QWidget()
        self.stroop_test_layout = QHBoxLayout()
        self.stroop_test_widget.setLayout(self.stroop_test_layout)
        layout.addWidget(self.stroop_test_widget)
        self.stroop_test_widget.hide()

        self.left_choice_btn = QPushButton("None")
        self.left_choice_btn.index = 0
        self.left_choice_btn.clicked.connect(self.choice_made)
        self.stroop_test_layout.addWidget(self.left_choice_btn)

        self.right_choice_btn = QPushButton("None")
        self.right_choice_btn.index = 0
        self.right_choice_btn.clicked.connect(self.choice_made)
        self.stroop_test_layout.addWidget(self.right_choice_btn)

        self.time = 0
        self.choice_time = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timing)
        self.event_id = 1000
        self.time_start = 0
        self.time_stop = 0

        self.play_sound = "resources/calibration_resources/error_sound.wav"
        # self.play_alarm = "resources/calibration_resources/alarm_2.wav"

        self.wrong_answers_counter = 0
        self.colors = ["black", "cyan", "blue", "gold", "pink", "yellow", "khaki", "green", "gray", "lavender", "lime"]

        self.calibration_ended_label = QLabel("The calibration is complete.")
        layout.addWidget(self.calibration_ended_label)
        self.calibration_ended_label.setStyleSheet(font)
        self.calibration_ended_label.setAlignment(QtCore.Qt.AlignCenter)
        self.calibration_ended_label.hide()

        self.instruction_widget = QWidget()
        self.instruction_widget_layout = QVBoxLayout()
        self.instruction_widget.setLayout(self.instruction_widget_layout)
        layout.addWidget(self.instruction_widget)
        self.instruction_widget.hide()

        self.instruction_label = QLabel(self)
        self.instruction_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = QPixmap("resources/calibration_resources/instrukcja_size1.jpg")
        self.instruction_label.setPixmap(self.pixmap)
        self.instruction_label.resize(150, 150)
        self.instruction_widget_layout.addWidget(self.instruction_label)

        self.skip_instruction_btn = QPushButton("Ok, skip ;)")
        self.skip_btn_box = QVBoxLayout()
        self.skip_btn_box.setAlignment(QtCore.Qt.AlignCenter)
        self.skip_btn_box.addWidget(self.skip_instruction_btn)
        self.skip_instruction_btn.clicked.connect(self.instruction_is_skipped)
        self.instruction_widget_layout.addLayout(self.skip_btn_box)

        self.csv_headers = ["id", "system time", "user", "gender", "age", "additional information", "file name",
                            "stimuli type", "user answer"]

        self.blinking = False
        self.blinking_count = 0

    def start(self):
        self.relax_event()
        #self.stress_event()

    def relax_event(self):
        self.event_id += 1
        content = [self.event_id, str(datetime.now())[:-3], "empty", "empty",
                                  "empty", "empty", "jez_morze", "relax", "empty", "empty", "empty", "empty"]
        self.write_to_csv(content)
        self.video_widget.setFullScreen(True)
        self.video_widget.show()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("resources/calibration_resources/jez_morze.mp4")))
        self.media_player.play()

    def video_ended(self):
        if self.media_player.state() == QMediaPlayer.StoppedState:
            self.video_widget.hide()
            self.video_widget.setFullScreen(False)
            if self.event_id < 1002:
                self.stress_event()
            else:
                self.calibration_ended_label.show()

    def stress_event(self):
        self.video_widget.hide()
        self.event_id += 1
        content = [self.event_id, str(datetime.now())[:-3], "empty", "empty",
                                  "empty", "empty", "test_stroopa", "stress", "empty", "empty", "empty", "empty"]
        self.write_to_csv(content)
        self.time_start = [datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]]
        self.time_stop = 0
        self.question_label.show()
        self.stroop_test_widget.show()
        self.stroop_test()
        self.timer.start(1000)

    def instruction_event(self):

        self.event_id += 1
        content = [self.event_id, str(datetime.now())[:-3], "empty", "empty",
                   "empty", "empty", "instrukcja", "relax", "empty", "empty", "empty", "empty"]
        self.write_to_csv(content)
        self.instruction_widget.show()

    def instruction_is_skipped(self):
        self.instruction_widget.hide()
        self.relax_event()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reset(True)
            # self.get_time("kalibracja_zakonczona", -1)
            event.accept()
        else:
            event.ignore()

    def timing(self):
        self.choice_time += 1
        self.time += 1
        if self.time >= 120 or self.wrong_answers_counter >= 5:
            self.timer.stop()
            self.question_label.hide()
            self.stroop_test_widget.hide()
            self.instruction_event()
            self.blinking = False
            self.setStyleSheet('background-color: #3d3e3f')
        elif self.choice_time == 2:
            QtMultimedia.QSound.play(self.play_sound)
            self.stroop_test()

        if self.blinking:
            self.blinking_count += 1
            if self.blinking_count % 2 == 0:
                self.setStyleSheet('background-color: green')
            else:
                self.setStyleSheet('background-color: yellow')
            if self.blinking_count >= 3:
                self.blinking = True
                self.blinking_count = 0
                self.setStyleSheet('background-color: #3d3e3f')

    def write_to_csv(self, content):
        with open("resources/measurements.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=',')
            writer.writerow(content)

    def choice_made(self):
        button = self.sender()
        if button.index == 0:
            QtMultimedia.QSound.play(self.play_sound)
            self.setStyleSheet('background-color: yellow')
            self.blinking = True
            self.blinking_count += 1
            self.wrong_answers_counter += 1
        self.event_id += 1
        content = [self.event_id, str(datetime.now())[:-3], "empty", "empty", "empty",
                   "empty", "test_stroopa", "stress", "empty", "empty", "empty", button.index]
        self.write_to_csv(content)
        self.choice_time = 0
        self.stroop_test()

    def stroop_test(self):
        color = random.choice(self.colors)
        style = "border-radius: 20px; background-color: white; font-size: 30px; " \
                "width: 150px; height: 50px; " "color: " + color + ";"
        self.question_label.setText("Please choose " + color + " color.")

        if random.choice([True, False]):
            self.left_choice_btn.index = 1
            self.right_choice_btn.index = 0

            self.right_choice_btn.setStyleSheet(style)
            self.right_choice_btn.setText(random.choice(self.colors))

            self.left_choice_btn.setText(color)
            self.left_choice_btn.setStyleSheet("border-radius: 20px; background-color: white; font-size: 30px; " \
                                               "width: 150px; height: 50px; " "color: " + random.choice(self.colors)
                                               + ";")

        else:
            self.left_choice_btn.index = 0
            self.right_choice_btn.index = 1

            self.left_choice_btn.setStyleSheet(style)
            self.left_choice_btn.setText(random.choice(self.colors))

            self.right_choice_btn.setText(color)
            self.right_choice_btn.setStyleSheet("border-radius: 20px; background-color: white; font-size: 30px; " \
                                                "width: 150px; height: 50px; " "color: " + random.choice(self.colors)
                                                + ";")

    def reset(self, state):
        self.time = 0
        self.choice_time = 0
        self.blinking_count = 0
        self.wrong_answers_counter = 0
        self.video_widget.hide()
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.stop()
        self.question_label.hide()
        self.stroop_test_widget.hide()
        self.instruction_widget.hide()
        self.event_id = 1000
        if state:
            self.calibration_ended_label.hide()