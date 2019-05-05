import copy
from statistics import mode

import cv2
import numpy as np

from helper import HelperFunctions


class Gesture_detector:

    def __init__(self, source=0):
        self.cap_region_x_begin = 0.5  # start point/total width
        self.cap_region_y_end = 0.8  # start point/total width
        self.threshold = 40  # BINARY threshold
        self.blurValue = 41  # GaussianBlur parameter
        self.bgSubThreshold = 50 
        self.learningRate = 0
        self.isBgCaptured = 0  # bool, whether the background captured
        self.camera = cv2.VideoCapture(source)
        self.camera.set(10, 200) #adjusting brightness
        self.cap_btn_clicked = False #bool,whether the capture button is clicked
        self.region_center = 0   #center of ROI
        self.helper = HelperFunctions()

    def removeBG(self, frame):
        #returns the frame after background subtraction 
        fgmask = self.bgModel.apply(frame, learningRate=self.learningRate)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res
    
    def frame_with_ROI(self):
        #draws the region of interest on each frame and calculating the region center.
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
            frame = cv2.flip(frame, 1)  # flip the frame horizontally
            cv2.rectangle(frame, (int(self.cap_region_x_begin * frame.shape[1]), 0),
                          (frame.shape[1], int(self.cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
            self.region_center = (
                int((0.5 * (1 - self.cap_region_x_begin)) * frame.shape[1]),
                int((self.cap_region_y_end * 0.5 * frame.shape[0])))

        return ret, frame

    
