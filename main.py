import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, \
    QMenu, QAction, QStyle

from main_window import Control_Panel


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.hand_tray_activated)
        self.ui = Control_Panel()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.show()
        self.ui.th.hide_signal.connect(self.minimize_to_tray)

    def hand_tray_activated(self, reason):
        # On double clicking the tray icon the windows is shown again
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def minimize_to_tray(self):
        # when go button is clicked the app is minimized to tray
        self.hide()
        self.tray_icon.showMessage(
            "Hand of The King",
            "Application was minimized to tray",
            QSystemTrayIcon.Information,
            2000
        )

    def closeEvent(self, event):
        # overriding the closeEvent function of the window to cleanup all open windows and release the camera
        self.tray_icon.hide()
        self.ui.application_on = False
        self.ui.gesture_detector.camera.release()
        self.ui.hand_window.close()
        event.accept()


app = QApplication(sys.argv)

mainwindow = AppWindow()

mainwindow.show()
sys.exit(app.exec_())
