import os

from PyQt5.QtCore import QUrl, Qt, QTime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QTextEdit, QPushButton, QStyle, QSlider, QHBoxLayout, \
    QFormLayout, QTimeEdit


class ItemViewWidget(QWidget):

    def __init__(self):
        super(ItemViewWidget, self).__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        self.task_index = 0
        self.task_type_list = []
        self.file_path = ''
        self.time = []
        self.form_widget = QWidget()
        self.form_widget_layout = QFormLayout()
        self.form_widget.setLayout(self.form_widget_layout)
        self.stimuli_type = ''
        layout.addWidget(self.form_widget, 1, 0)

        self.file_name_line = QLineEdit()
        self.file_name_line.textEdited.connect(self.edit_task_name)
        self.form_widget_layout.addRow("Name of task:", self.file_name_line)

        self.file_path_line = QLineEdit()
        self.file_path_line.setReadOnly(True)
        self.form_widget_layout.addRow("Path of file:", self.file_path_line)

        self.stimuli_type_line = QLineEdit()
        self.stimuli_type_line.setReadOnly(True)
        self.form_widget_layout.addRow("Type of stimuli:", self.stimuli_type_line)

        self.begin = QTimeEdit()
        self.begin.setDisplayFormat("hh:mm:ss")
        self.begin.timeChanged.connect(self.task_time_begin)
        self.form_widget_layout.addRow("Begin of the test:", self.begin)

        self.end = QTimeEdit()
        self.end.setDisplayFormat("hh:mm:ss")
        self.end.timeChanged.connect(self.task_time_end)
        self.form_widget_layout.addRow("End of the test:", self.end)

        self.text_file_content = QTextEdit("")
        self.text_file_content.setReadOnly(True)
        self.text_file_content.hide()
        layout.addWidget(self.text_file_content, 2, 0, 1, -1)

        self.video_file_content = QWidget()
        self.video_file_content_layout = QGridLayout()
        self.video_file_content.setLayout(self.video_file_content_layout)
        layout.addWidget(self.video_file_content, 2, 0, 1, -1)

        self.video_widget = QVideoWidget()
        self.video_file_content_layout.addWidget(self.video_widget, 1, 0, 1, -1)

        self.video_widget_layout = QHBoxLayout()
        self.video_widget.setLayout(self.video_widget_layout)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.play_btn = QPushButton()
        self.video_file_content_layout.addWidget(self.play_btn, 2, 0)

        self.position_slider = QSlider(Qt.Horizontal)
        self.video_file_content_layout.addWidget(self.position_slider, 2, 1)

        self.video_file_content_init()

        self.previous_btn = QPushButton("Previous")
        self.previous_btn.clicked.connect(lambda: self.show_task(False))
        layout.addWidget(self.previous_btn, 4, 0)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(lambda: self.show_task(True))
        layout.addWidget(self.next_btn, 4, 1)

    def edit_task_name(self):
        line = self.sender()
        self.task_type_list[self.task_index][0] = line.text()

    def task_time_begin(self):
        time = self.sender()
        self.task_type_list[self.task_index][3] = time.text()

    def task_time_end(self):
        time = self.sender()
        self.task_type_list[self.task_index][4] = time.text()

    def load_tasks(self, task_type_list, index, stimuli_type):
        self.task_type_list = task_type_list
        self.task_index = index - 1
        self.stimuli_type = stimuli_type
        if len(self.task_type_list) == 1:
            self.next_btn.setEnabled(False)
            self.previous_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(True)
            self.previous_btn.setEnabled(True)
        self.show_task(True)

    def show_task(self, state):
        if state:
            if self.task_index == len(self.task_type_list) - 1:
                self.task_index = 0
            else:
                self.task_index += 1
        else:
            if self.task_index == 0:
                self.task_index = len(self.task_type_list) - 1
            else:
                self.task_index -= 1
        self.hide_content()
        task_data = self.task_type_list[self.task_index]
        self.file_name_line.setText(task_data[0])
        self.file_path_line.setText(task_data[1])
        self.stimuli_type_line.setText(task_data[2])

        begin = task_data[3].split(":")
        self.begin.setTime(QTime(int(begin[0]), int(begin[1]), int(begin[2])))

        end = task_data[4].split(":")
        self.begin.setTime(QTime(int(end[0]), int(end[1]), int(end[2])))

        self.file_path = task_data[1]

        filename, file_extension = os.path.splitext(task_data[1])
        if file_extension == ".txt":
            self.show_text_file_content()
            self.begin.setReadOnly(True)
        elif file_extension == ".MP4" or file_extension == ".mp4":
            self.show_video_file_content()
            self.begin.setReadOnly(False)

    def hide_content(self):
        self.video_file_content.hide()
        self.play_btn.hide()
        self.position_slider.hide()
        self.text_file_content.hide()

    def show_text_file_content(self):
        self.text_file_content.show()
        self.text_file_content.setText("")
        with open(self.file_path, "r", encoding="utf8") as reader:
            for line in reader:
                self.text_file_content.insertPlainText(line)

    def show_video_file_content(self):
        self.video_file_content.show()
        self.play_btn.show()
        self.position_slider.show()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))

    def video_file_content_init(self):
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(None)))
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handle_error)

        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play)
        self.video_file_content_layout.addWidget(self.play_btn)

        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_btn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handle_error(self):
        self.play_btn.setEnabled(False)


