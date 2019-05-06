from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QDesktopWidget


class Hand_Window(QMainWindow):
    # a windows that shows only the ROI with the detected hand
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("QMainWindow{"
                           "background-color:#000000"
                           "}")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        lay = QVBoxLayout(self.central_widget)
        # self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWindowTitle("Detected Hand")
        self.frame_1 = QLabel(self)
        # self.frame_1.setGeometry(QtCore.QRect(10, 20, 600, 500))
        self.frame_1.setObjectName("frame_1")
        # self.frame_1.setAutoFillBackground(True)
        self.current_frame = None
        lay.addWidget(self.frame_1)
        spacerItem = QSpacerItem(20, 245, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lay.addItem(spacerItem)

    def view_image(self, frame):
        # fucntion to continously update the image in the window with new frames
        height, width, colors = frame.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage
        image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = image.rgbSwapped()
        pixmap = QPixmap(image)
        self.frame_1.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        screen = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width()
        y = 0
        self.move(x, y)
