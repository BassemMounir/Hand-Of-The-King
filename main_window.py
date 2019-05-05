import os
import pickle
import shutil
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QThread, pyqtSignal)
from PyQt5.QtGui import QPixmap
from pynput.keyboard import Key, Controller

from cv_code import Gesture_detector
from prompt import PromptWindow

detector_obj = Gesture_detector() 


class Thread(QThread):
    #custom thread class that is used to update the camera frames in the gui
    changeframe = pyqtSignal(np.ndarray)

    def run(self):
        while True:
            ret, frame = detector_obj.frame_with_ROI() # get the current camera frame + Region of interest
            if ret:
                self.changeframe.emit(frame) # emit signal to send the frame to the view_image function
