# -*- coding: utf-8 -*-
import os
import pickle
import shutil

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QThread, pyqtSignal)
from PyQt5.QtGui import QPixmap
from pynput.keyboard import Controller,Key

from Hand_window import Hand_Window
from cv_code import Gesture_detector
from prompt import PromptWindow

detector_obj = Gesture_detector()


class Thread(QThread):
    changeframe = pyqtSignal(np.ndarray)
    hand_frame_change = pyqtSignal(np.ndarray)
    hide_signal = pyqtSignal()

    def run(self):
        while True:
            ret, frame = detector_obj.frame_with_ROI()
            if ret:
                self.changeframe.emit(frame)
            if detector_obj.gui_frame is not None:
                self.hand_frame_change.emit(detector_obj.gui_frame)


class Control_Panel(QtWidgets.QWidget):

    def setupUi(self, Form):
        self.gesture_detector = detector_obj
        self.profiles = self.load_profiles()
        Form.setObjectName("Form")
        Form.resize(810, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1.5)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Hand-of-the-king-pin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("QWidget {\n"
                           "   background-color: #383c41;\n"
                           "}\n"
                           "\n"
                           "QTextEdit {\n"
                           "   background-color: aliceblue;\n"
                           "   color: #000000;\n"
                           "   font-weight: bold;\n"
                           "   font-size: 7pt;\n"
                           "}\n"
                           "\n"
                           "QLabel {\n"
                           "   background-color: #383c41;\n"
                           "   color: #FFA500;\n"
                           "}\n"
                           "\n"
                           "QPushButton {\n"
                           "   background-color: #FFA500;\n"
                           "   color: #ffffff;\n"
                           "   border-radius: 5px;\n"
                           "   border-style: none;\n"
                           "   height: 25px;\n"
                           "}\n"
                           "QPushButton::pressed {background-color:#F0E68C;color: #000000}\n"
                           "QPushButton::hover::!pressed {background-color: #00ab66}\n"
                           "QGroupBox {\n"
                           "    color:#ffffff;\n"
                           "}\n"
                           "QComboBox{\n"
                           "   color: #FFA500;\n"
                           "}\n"
                           "\n"
                           "QComboBox QListView{\n"
                           "   color: #FFA500;\n"
                           "}\n"
                           "\n"
                           "QListView:item{\n"
                           "   color: #FFA500;\n"
                           "}\n"
                           "\n"

                           "QTabBar::tab{\n"
                           "    color:#000000;\n"
                           "}")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(-2, -2, 811, 641))
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tabWidget.setObjectName("tabWidget")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.textEdit_73 = QtWidgets.QTextEdit(self.widget)
        self.textEdit_73.setGeometry(QtCore.QRect(0, -20, 811, 641))
        self.textEdit_73.setStyleSheet("QTextEdit{\n"
                                       "    background-color: #383c41;\n"
                                       "    color:#ffffff;\n"
                                       "}\n"
                                       "\n"
                                       "")
        self.textEdit_73.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textEdit_73.setObjectName("textEdit_73")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(580, 60, 31, 61))
        self.frame.setStyleSheet("QFrame{\n"
                                 "    background: url(/home/tity/Hand-of-the-king-pin.png)\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tabWidget.addTab(self.widget, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_25 = QtWidgets.QLabel(self.tab)
        self.label_25.setGeometry(QtCore.QRect(20, 20, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.ComboBox_profiles = QtWidgets.QComboBox(self.tab)
        self.ComboBox_profiles.setGeometry(QtCore.QRect(410, 20, 181, 31))
        self.ComboBox_profiles.setObjectName("ComboBox_profiles")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(30, 70, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 48, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 80, 48, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.textEdit_1_left = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_1_left.setGeometry(QtCore.QRect(80, 40, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_1_left.setFont(font)
        self.textEdit_1_left.setObjectName("textEdit_1_left")
        self.textEdit_1_right = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_1_right.setGeometry(QtCore.QRect(80, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_1_right.setFont(font)
        self.textEdit_1_right.setObjectName("textEdit_1_right")
        self.textEdit_1_down = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_1_down.setGeometry(QtCore.QRect(80, 190, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_1_down.setFont(font)
        self.textEdit_1_down.setObjectName("textEdit_1_down")
        self.textEdit_1_up = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_1_up.setGeometry(QtCore.QRect(80, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_1_up.setFont(font)
        self.textEdit_1_up.setObjectName("textEdit_1_up")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(250, 70, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_13 = QtWidgets.QLabel(self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(10, 40, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_4)
        self.label_14.setGeometry(QtCore.QRect(10, 190, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setGeometry(QtCore.QRect(10, 140, 48, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(10, 80, 48, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.textEdit_2_left = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_2_left.setGeometry(QtCore.QRect(80, 40, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_2_left.setFont(font)
        self.textEdit_2_left.setObjectName("textEdit_2_left")
        self.textEdit_2_right = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_2_right.setGeometry(QtCore.QRect(80, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_2_right.setFont(font)
        self.textEdit_2_right.setObjectName("textEdit_2_right")
        self.textEdit_2_down = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_2_down.setGeometry(QtCore.QRect(80, 190, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_2_down.setFont(font)
        self.textEdit_2_down.setObjectName("textEdit_2_down")
        self.textEdit_2_up = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_2_up.setGeometry(QtCore.QRect(80, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_2_up.setFont(font)
        self.textEdit_2_up.setObjectName("textEdit_2_up")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(470, 70, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(10, 40, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(10, 190, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(10, 140, 48, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(10, 80, 48, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.textEdit_3_left = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_3_left.setGeometry(QtCore.QRect(80, 40, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_3_left.setFont(font)
        self.textEdit_3_left.setObjectName("textEdit_3_left")
        self.textEdit_3_right = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_3_right.setGeometry(QtCore.QRect(80, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_3_right.setFont(font)
        self.textEdit_3_right.setObjectName("textEdit_3_right")
        self.textEdit_3_down = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_3_down.setGeometry(QtCore.QRect(80, 190, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_3_down.setFont(font)
        self.textEdit_3_down.setObjectName("textEdit_3_down")
        self.textEdit_3_up = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_3_up.setGeometry(QtCore.QRect(80, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_3_up.setFont(font)
        self.textEdit_3_up.setObjectName("textEdit_3_up")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setGeometry(QtCore.QRect(470, 330, 171, 121))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.textEdit_0_left = QtWidgets.QTextEdit(self.groupBox_5)
        self.textEdit_0_left.setGeometry(QtCore.QRect(40, 60, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_0_left.setFont(font)
        self.textEdit_0_left.setObjectName("textEdit_0_left")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setGeometry(QtCore.QRect(250, 330, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_21 = QtWidgets.QLabel(self.groupBox_6)
        self.label_21.setGeometry(QtCore.QRect(10, 40, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.groupBox_6)
        self.label_22.setGeometry(QtCore.QRect(10, 190, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.groupBox_6)
        self.label_23.setGeometry(QtCore.QRect(10, 140, 48, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_6)
        self.label_24.setGeometry(QtCore.QRect(10, 80, 48, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.textEdit_5_left = QtWidgets.QTextEdit(self.groupBox_6)
        self.textEdit_5_left.setGeometry(QtCore.QRect(80, 40, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_5_left.setFont(font)
        self.textEdit_5_left.setObjectName("textEdit_5_left")
        self.textEdit_5_right = QtWidgets.QTextEdit(self.groupBox_6)
        self.textEdit_5_right.setGeometry(QtCore.QRect(80, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_5_right.setFont(font)
        self.textEdit_5_right.setObjectName("textEdit_5_right")
        self.textEdit_5_down = QtWidgets.QTextEdit(self.groupBox_6)
        self.textEdit_5_down.setGeometry(QtCore.QRect(80, 190, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_5_down.setFont(font)
        self.textEdit_5_down.setObjectName("textEdit_5_down")
        self.textEdit_5_up = QtWidgets.QTextEdit(self.groupBox_6)
        self.textEdit_5_up.setGeometry(QtCore.QRect(80, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_5_up.setFont(font)
        self.textEdit_5_up.setObjectName("textEdit_5_up")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 330, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 190, 48, 14))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 140, 48, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(10, 80, 48, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.textEdit_4_left = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_4_left.setGeometry(QtCore.QRect(80, 40, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_4_left.setFont(font)
        self.textEdit_4_left.setObjectName("textEdit_4_left")
        self.textEdit_4_right = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_4_right.setGeometry(QtCore.QRect(80, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_4_right.setFont(font)
        self.textEdit_4_right.setObjectName("textEdit_4_right")
        self.textEdit_4_down = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_4_down.setGeometry(QtCore.QRect(80, 190, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_4_down.setFont(font)
        self.textEdit_4_down.setObjectName("textEdit_4_down")
        self.textEdit_4_up = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_4_up.setGeometry(QtCore.QRect(80, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)

        font.setWeight(75)
        self.textEdit_4_up.setFont(font)
        self.textEdit_4_up.setObjectName("textEdit_4_up")
        self.Btn_Save = QtWidgets.QPushButton(self.tab)
        self.Btn_Save.setGeometry(QtCore.QRect(620, 590, 80, 21))
        self.Btn_Save.setObjectName("Btn_Save")
        self.Btn_Save.setToolTip('Click to save key bindings to a profile')

        self.Btn_default = QtWidgets.QPushButton(self.tab)
        self.Btn_default.setGeometry(QtCore.QRect(520, 590, 90, 21))
        self.Btn_default.setObjectName("Btn_default")
        self.Btn_default.setToolTip('click to restore the default profile (note: need to restart app)')
        self.Btn_default.clicked.connect(self.restore_defaults)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame_2 = QtWidgets.QLabel(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 20, 711, 511))
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setAutoFillBackground(True)

        self.Btn_Go = QtWidgets.QPushButton(self.tab_2)
        self.Btn_Go.setGeometry(QtCore.QRect(610, 580, 81, 21))
        self.Btn_Go.setStyleSheet("QPushButton {\n"
                                  "   background-color: #00ab66;\n"
                                  "   color: #ffffff;\n"
                                  "   border-radius: 5px;\n"
                                  "   border-style: none;\n"
                                  "   height: 25px;\n"
                                  "}")
        self.Btn_Go.setObjectName("Btn_Go")
        self.Btn_Go.clicked.connect(self.go_on_click)
        self.Btn_Go.setVisible(False)

        self.Btn_Capture = QtWidgets.QPushButton(self.tab_2)
        self.Btn_Capture.setGeometry(QtCore.QRect(230, 580, 81, 21))
        self.Btn_Capture.setObjectName("Btn_Capture")
        self.Btn_Capture.setToolTip('Click to capture background')
        self.Btn_Capture.clicked.connect(self.capture_on_click)

        self.label_69 = QtWidgets.QLabel(self.tab_2)
        self.label_69.setGeometry(QtCore.QRect(10, 550, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_69.setFont(font)
        self.label_69.setObjectName("label_69")
        self.Slider_Senitivity = QtWidgets.QSlider(self.tab_2)
        self.Slider_Senitivity.setGeometry(QtCore.QRect(40, 580, 160, 31))
        self.Slider_Senitivity.setMaximum(100)
        self.Slider_Senitivity.setProperty("value", 40)
        self.Slider_Senitivity.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_Senitivity.setObjectName("Slider_Senitivity")
        self.tabWidget.addTab(self.tab_2, "")
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def get_text_values(self):
        finger_values = {}
        finger_values["finger_0_left"] = getattr(self, "textEdit_0_left").toPlainText()
        for i in range(1, 6):
            finger_values["finger_" + str(i) + "_left"] = getattr(self, "textEdit_" + str(i) + "_left").toPlainText()
            finger_values["finger_" + str(i) + "_right"] = getattr(self, "textEdit_" + str(i) + "_right").toPlainText()
            finger_values["finger_" + str(i) + "_up"] = getattr(self, "textEdit_" + str(i) + "_up").toPlainText()
            finger_values["finger_" + str(i) + "_down"] = getattr(self, "textEdit_" + str(i) + "_down").toPlainText()

        return finger_values

    def restore_defaults(self):
        os.remove('./saved_profiles.pkl')
        shutil.copy('./default_profiles.pkl', './saved_profiles.pkl')
        self.profiles = self.load_profiles()
        self.ComboBox_profiles.clear()
        for key, value in self.profiles.items():
            self.ComboBox_profiles.addItem(key)


    def go_on_click(self):
        action = self.Btn_Go.text()


        if action == "Go":
            self.th.hide_signal.emit()
            self.hand_window.show()

            self.application_on = True
            threshold = self.Slider_Senitivity.value()
            key_bindings_dict = self.get_text_values()
            self.Btn_Go.setText("Stop")
            self.Btn_Go.setStyleSheet("QPushButton {\n"
                                      "   background-color: #FF0000;\n"
                                      "   color: #ffffff;\n"
                                      "   border-radius: 5px;\n"
                                      "   border-style: none;\n"
                                      "   height: 25px;\n"
                                      "}")
            while self.application_on == True:
                # print(self.application_on)

                detector_obj.threshold = threshold
                current_gesture = detector_obj.get_gesture()
                # print(current_gesture)
                self.map_gesture_to_shortcut(key_bindings_dict, current_gesture)
        else:
            self.hand_window.close()
            self.application_on = False
            # print(self.application_on)
            self.Btn_Go.setText("Go")
            self.Btn_Go.setStyleSheet("QPushButton {\n"
                                      "   background-color: #00ab66;\n"
                                      "   color: #ffffff;\n"
                                      "   border-radius: 5px;\n"
                                      "   border-style: none;\n"
                                      "   height: 25px;\n"
                                      "}")

    def map_gesture_to_shortcut(self, finger_values, gesture):
        keyboard = Controller()
        special_keys_list = ["space", "up", "down", "right", "left", "tab", "esc", "enter", "page_down", "page_up", "f1",
                     "f4", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15",
                     "backspace"]
        chord_keys =["alt","ctrl","shift","cmd"]
        if gesture in finger_values:
            value = finger_values[gesture]
            value = value.replace(" ", "")
            if value == "":
                return
            if "+" in value:
                key1 = value[:value.index("+")]
                key2 = value[value.index("+") + 1:]
                if key1.lower() in chord_keys:
                    if key2.lower() in special_keys_list:
                        key1 = eval("Key." + key1.lower())
                        with keyboard.pressed(key1):
                            key2 = eval("Key." + key2.lower())
                            keyboard.press(key2)
                            keyboard.release(key2)
                    else:
                        key1 = eval("Key." + key1.lower())
                        with keyboard.pressed(key1):
                            keyboard.press(key2)
                            keyboard.release(key2)
            else:
                if value.lower() in special_keys_list:
                    value = eval("Key." + value.lower())
                    keyboard.press(value)
                    keyboard.release(value)
                else:
                    keyboard.press(value)
                    keyboard.release(value)

    def save_profile(self):
        self.prompt = PromptWindow()
        if self.prompt.exec_():
            if self.prompt.RadioButton_Yes.isChecked() == True:
                profile_name = str(self.ComboBox_profiles.currentText())
            else:
                profile_name = self.prompt.textEdit_New_Profile_Name.toPlainText()
                self.ComboBox_profiles.addItem(profile_name)
                self.ComboBox_profiles.setCurrentText(profile_name)
                self.ComboBox_profiles.currentTextChanged.connect(self.selectionchange)
            self.profiles[profile_name] = self.get_text_values()
            with open('saved_profiles.pkl', 'wb') as saved_profiles_file:
                pickle.dump(self.profiles, saved_profiles_file)

    def capture_on_click(self):
        detector_obj.cap_btn_clicked = 1
        self.Btn_Go.setVisible(True)



    def load_profiles(self):
        profiles = {}
        if os.path.exists('saved_profiles.pkl'):
            with open('saved_profiles.pkl', 'rb') as saved_profiles_file:
                profiles = pickle.load(saved_profiles_file)
        return profiles

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Hand of The King"))
        self.textEdit_73.setHtml(_translate("Form",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600; font-style:italic;\">\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; color:#ffaa00;\">Welcome to Hand of The King</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-style:normal;\">How to use:</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400; font-style:normal;\">1. From Key Binding tab, choose from preset profiles or create your own key binding profile.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400; font-style:normal;\">2. From Camera Settings tab, step aside and capture the background.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400; font-style:normal;\">3. Click Start.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:400; font-style:normal;\"><br />Note: make sure that you don\'t change the background while running.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("Form", "Hand of The King"))
        self.label_25.setText(_translate("Form", "Choose from saved profiles or create one"))
        for key, value in self.profiles.items():
            self.ComboBox_profiles.addItem(key)
        self.textEdit_73.setDisabled(True)
        self.ComboBox_profiles.currentTextChanged.connect(self.selectionchange)
        self.ComboBox_profiles.setCurrentIndex(-1)
        self.groupBox.setTitle(_translate("Form", "One Finger Gesture"))
        self.label_2.setText(_translate("Form", "Left"))
        self.label_4.setText(_translate("Form", "Down"))
        self.label_3.setText(_translate("Form", "Up"))
        self.label.setText(_translate("Form", "Right"))
        self.groupBox_4.setTitle(_translate("Form", "Two Finger Gesture"))
        self.label_13.setText(_translate("Form", "Left"))
        self.label_14.setText(_translate("Form", "Down"))
        self.label_15.setText(_translate("Form", "Up"))
        self.label_16.setText(_translate("Form", "Right"))
        self.groupBox_3.setTitle(_translate("Form", "Three Finger Gesture"))
        self.label_9.setText(_translate("Form", "Left"))
        self.label_10.setText(_translate("Form", "Down"))
        self.label_11.setText(_translate("Form", "Up"))
        self.label_12.setText(_translate("Form", "Right"))
        self.groupBox_5.setTitle(_translate("Form", "Closed Fist Gesture"))
        self.groupBox_6.setTitle(_translate("Form", "Five Finger Gesture"))
        self.label_21.setText(_translate("Form", "Left"))
        self.label_22.setText(_translate("Form", "Down"))
        self.label_23.setText(_translate("Form", "Up"))
        self.label_24.setText(_translate("Form", "Right"))
        self.groupBox_2.setTitle(_translate("Form", "Four Finger Gesture"))
        self.label_5.setText(_translate("Form", "Left"))
        self.label_6.setText(_translate("Form", "Down"))
        self.label_7.setText(_translate("Form", "Up"))
        self.label_8.setText(_translate("Form", "Right"))
        self.Btn_Save.setText(_translate("Form", "Save"))
        self.Btn_default.setText(_translate("Form", "Restore Defaults"))
        self.Btn_Save.clicked.connect(self.save_profile)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Key Bindings"))
        self.Btn_Go.setText(_translate("Form", "Go"))
        self.Btn_Capture.setText(_translate("Form", "Capture"))
        self.label_69.setText(_translate("Form", "Sensitivity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Camera Settings"))
        self.hand_window = Hand_Window()
        Form.show()
        self.th = Thread(self)
        self.th.changeframe.connect(self.view_image)
        self.th.hand_frame_change.connect(self.hand_window.view_image)
        self.th.start()

    def view_image(self, frame):
        height, width, colors = frame.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage
        image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = image.rgbSwapped()
        pixmap = QPixmap(image)
        self.frame_2.setPixmap(pixmap)

    def selectionchange(self, selecteditem):
        if selecteditem in self.profiles:
            values = self.profiles[selecteditem]
            getattr(self, "textEdit_0_left").setText(values["finger_0_left"])
            for i in range(1, 6):
                getattr(self, "textEdit_" + str(i) + "_left").setText(values["finger_" + str(i) + "_left"])
                getattr(self, "textEdit_" + str(i) + "_right").setText(values["finger_" + str(i) + "_right"])
                getattr(self, "textEdit_" + str(i) + "_up").setText(values["finger_" + str(i) + "_up"])
                getattr(self, "textEdit_" + str(i) + "_down").setText(values["finger_" + str(i) + "_down"])

    def __del__(self):
        detector_obj.camera.release()
