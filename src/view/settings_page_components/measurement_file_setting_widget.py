from PyQt5.QtWidgets import QWidget, QGridLayout, QFormLayout, QLineEdit


class MeasurementFileSettingWidget(QWidget):

    def __init__(self):
        super(MeasurementFileSettingWidget, self).__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        self.measurement_file_settings = ['', '', '']
        self.form_widget = QWidget()
        self.form_widget_layout = QFormLayout()
        self.form_widget.setLayout(self.form_widget_layout)
        layout.addWidget(self.form_widget, 1, 0)

        self.file_name_line = QLineEdit()
        self.file_name_line.textEdited.connect(self.edit_file_name)
        self.form_widget_layout.addRow("Name of file:", self.file_name_line)

        self.file_path_line = QLineEdit()
        self.file_path_line.textEdited.connect(self.edit_file_path)
        self.form_widget_layout.addRow("Path of file:", self.file_path_line)

        self.character_line = QLineEdit()
        self.character_line.textEdited.connect(self.edit_character)
        self.form_widget_layout.addRow("Character:", self.character_line)

    def edit_file_name(self):
        line = self.sender()
        self.measurement_file_settings[0] = line.text()

    def edit_file_path(self):
        line = self.sender()
        self.measurement_file_settings[1] = line.text()

    def edit_character(self):
        line = self.sender()
        self.measurement_file_settings[2] = line.text()
