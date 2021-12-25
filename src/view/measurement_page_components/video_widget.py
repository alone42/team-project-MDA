from pymediainfo import MediaInfo
from PyQt5 import QtCore, Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class VideoWidget(QWidget):
    task_ended = QtCore.pyqtSignal(list)

    def __init__(self):
        super(VideoWidget, self).__init__()

        self.video_data = []
        # self.video_duration = -1
        # self.video_end = -1
        # self.video_start = 0

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.video_widget = QVideoWidget()
        self.video_widget.setMaximumSize(800, 600)
        layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(None)))
        # self.media_player.setNotifyInterval(50)
        # self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.stateChanged.connect(self.video_ended)

    def video_ended(self):
        if self.media_player.state() == QMediaPlayer.StoppedState:
            self.video_data.append("empty")
            self.video_data.append("empty")
            self.video_widget.setFullScreen(False)
            self.task_ended.emit(self.video_data)

    def start(self, task):
        self.video_data = []
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(task[3])))
        # start_list = list(task[4].split(":"))
        # start_list_int = [int(item) for item in start_list]
        # self.video_start = ((start_list_int[0] * 60 + start_list_int[1]) * 60 + start_list_int[2]) * 1000
        # self.media_player.setPosition(self.video_start)
        # end_list = list(task[5].split(":"))
        # end_list_int = [int(item) for item in end_list]
        # self.video_end = ((end_list_int[0] * 60 + end_list_int[1]) * 60 + end_list_int[2]) * 1000
        # if self.video_end == 0:
        #     self.get_duration_of_video(task[3])
        try:
            self.video_widget.setFullScreen(True)
            self.media_player.play()
        except:
            print("error: wrong time range")
            self.video_data.append("empty")
            self.video_data.append("empty")
            self.task_ended.emit(self.video_data)

    # def position_changed(self, position):
    #     if position + 50 > self.video_end > position and self.video_end != -1:
    #         self.video_data.append("empty")
    #         self.video_data.append("empty")
    #         self.video_widget.setFullScreen(False)
    #         self.task_ended.emit(self.video_data)

    # def play_pause_video(self):
    #     if self.media_player.state() == QMediaPlayer.PlayingState:
    #         self.media_player.pause()
    #     else:
    #         self.media_player.play()

    # def get_duration_of_video(self, file_path):
    #     media_info = MediaInfo.parse(file_path)
    #     for track in media_info.tracks:
    #         if track.track_type == 'Video':
    #             self.video_end = track.duration
    #             break

    # def keyPressEvent(self, event):
    #     print("aaa")
    #     if event.key() == Qt.Key_Enter:
    #         self.video_data.append("empty")
    #         self.video_data.append("empty")
    #         self.video_widget.setFullScreen(False)
    #         self.task_ended.emit(self.video_data)
