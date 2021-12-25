import sys

from PyQt5.QtWidgets import QApplication
from src.controller import Controller
from src.view import style_sheet


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet.style)
    controller = Controller()
    controller.main_window.show()
    app.exec()
    controller.configuration_settings.close_connection()
    sys.exit(0)


if __name__ == '__main__':
    main()
