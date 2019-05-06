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

    def calculateFingers(self, res, drawing):  # -> finished bool, cnt: fingers count
        # using convexity defect to get angle between candidate finger tip and neighbouring defects
        # if this angle is < 60 then it's a real finger tip
        final_defects = []
        hull = cv2.convexHull(res, returnPoints=False)
        hull2 = cv2.convexHull(res, returnPoints=True)
        if len(hull) > 3:
            defects = cv2.convexityDefects(res, hull)
            if type(defects) != type(None) and len(defects) > 0:  # avoid crashing.
                new_defects = self.helper.remove_noisy_defects(res, defects)
                candidate_finger_tips = self.helper.average_and_join_points(hull2, 25)
                if type(new_defects) != type(None) and len(new_defects) > 0:
                    cnt = 0
                    candidate_finger_tips = self.helper.closest_defects(candidate_finger_tips, new_defects)
                    for i in range(0, len(candidate_finger_tips)):  # calculate the angle
                        defect1, finger_tip, defect2 = candidate_finger_tips[i]
                        angle = self.helper.calculate_angle(defect1, finger_tip, defect2)
                        # angle less than 60 degree, treat as fingers
                        dist_thrsh = 20
                        if angle <= 60 and angle != -1 and (
                            finger_tip[1] < defect1[1] or finger_tip[1] < defect2[1]) and self.helper.distance(
                                finger_tip,
                                defect1) > dist_thrsh and self.helper.distance(
                                finger_tip, defect2) > dist_thrsh:
                            cv2.circle(drawing, defect1, 8, [255, 0, 0], -1)
                            cv2.circle(drawing, defect2, 8, [255, 0, 0], -1)
                            if defect1 not in final_defects:
                                final_defects.append(defect1)
                            if defect2 not in final_defects:
                                final_defects.append(defect2)
                            cv2.circle(drawing, finger_tip, 8, [0, 255, 0], -1)
                            cnt += 1
                    return final_defects, True, cnt
        return final_defects, False, 0

    def get_direction(self, center_position, min_distance):
        # getting direction of the hand by comparing the mean defect position and center of the page position

        start = self.region_center
        end = center_position
        dist = self.helper.distance(start, end)

        if dist > min_distance:
            x1, y1 = start
            x2, y2 = end
            xdiff, ydiff = np.subtract(start, end)

            if x1 > x2:
                xdirection = "left"
            elif x2 > x1:
                xdirection = "right"
            if y1 > y2:
                ydirection = "up"
            elif y2 > y1:
                ydirection = "down"
            if abs(xdiff) > abs(ydiff):
                return xdirection
            else:
                return ydirection
        else:
            return "no motion"

