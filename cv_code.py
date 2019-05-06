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
        self.camera.set(10, 200)
        self.cap_btn_clicked = False
        self.region_center = 0
        self.helper = HelperFunctions()
        self.gui_frame = None

    def removeBG(self, frame):
        fgmask = self.bgModel.apply(frame, learningRate=self.learningRate)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res

    def calculateFingers(self, res, drawing):  # -> finished bool, cnt: angles count
        #  convexity defect
        final_defects = []
        hull = cv2.convexHull(res, returnPoints=False)
        hull2 = cv2.convexHull(res, returnPoints=True)
        # for point in hull2:
        #     cv2.circle(drawing, (point[0][0],point[0][1]), 8, [0, 84, 250], -1)
        if len(hull) > 3:
            defects = cv2.convexityDefects(res, hull)
            if type(defects) != type(None) and len(defects) > 0:  # avoid crashing.   (BUG not found)
                new_defects = self.helper.remove_noisy_defects(res, defects)
                candidate_finger_tips = self.helper.average_and_join_points(hull2, 25)
                # for point in candidate_finger_tips:
                #   cv2.circle(drawing, tuple(point), 8, [255, 0, 0], -1)
                if type(new_defects) != type(None) and len(new_defects) > 0:
                    cnt = 0
                    # for j in range(0, len(defects)):
                    #    if distance(defects[j][0], defects[j][1]) > 10:
                    #        new_defects.append(defects[j])
                    candidate_finger_tips = self.helper.closest_defects(candidate_finger_tips, new_defects)
                    for i in range(0, len(candidate_finger_tips)):  # calculate the angle
                        defect1, finger_tip, defect2 = candidate_finger_tips[i]
                        angle = self.helper.calculate_angle(defect1, finger_tip, defect2)
                        # angle less than 90 degree, treat as fingers
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
                    # if cnt != 0:
                    #     cnt += 1
                    # print(cnt)
                    return final_defects, True, cnt
        return final_defects, False, 0

    def get_direction(self, center_position, min_distance):

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

    def frame_with_ROI(self):
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

    def get_gesture(self):

        frame_no = 0
        cnts = []
        directions = []

        while self.camera.isOpened():

            ret, frame = self.frame_with_ROI()

            # cv2.imshow('original', frame)

            if self.isBgCaptured == 1:  # this part wont run until background captured
                img = self.removeBG(frame)
                img = img[0:int(self.cap_region_y_end * frame.shape[0]),
                      int(self.cap_region_x_begin * frame.shape[1]): frame.shape[1]]  # clip the ROI
                # cv2.imshow('mask', img)

                # convert the image into binary image
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (self.blurValue, self.blurValue), 0)
                # cv2.imshow('blur', blur)
                ret, thresh = cv2.threshold(blur, self.threshold, 255, cv2.THRESH_BINARY)
                # cv2.imshow('ori', thresh)

                # get the coutours
                thresh1 = copy.deepcopy(thresh)
                contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                length = len(contours)
                maxArea = -1
                if length > 0:
                    for i in range(length):  # find the biggest contour (according to area)
                        temp = contours[i]
                        area = cv2.contourArea(temp)
                        if area > maxArea:
                            maxArea = area
                            ci = i

                    res = contours[ci]
                    hull = cv2.convexHull(res)
                    drawing = np.zeros(img.shape, np.uint8)
                    cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

                    final_defects, isFinished, cnt = self.calculateFingers(res, drawing)
                    cnts.append(cnt)
                    palm_center = None
                    if len(final_defects) > 0:
                        palm_center = self.helper.get_avg_point(final_defects)

                    if palm_center is not None:
                        directions.append(self.get_direction(palm_center, 40))

                    frame_no += 1
                    if frame_no == 30:
                        try:
                            cnt = mode(cnts)
                            if len(directions) > 1:

                                if cnt == 0:
                                    direction = "left"
                                else:
                                    direction = mode(directions)
                                current_gesture = "finger_" + str(cnt) + "_" + direction

                                return current_gesture
                            else:
                                return "nth detected"

                        except:
                            pass

                        frame_no = 0
                        cnts = []
                        directions = []
                    cv2.circle(drawing, self.region_center, 8, [255, 255, 255], -1)
                    if palm_center is not None:
                        cv2.circle(drawing, palm_center, 8, [0, 0, 255], -1)
                    # winname = 'Region of Interest'
                    # cv2.namedWindow(winname)
                    # cv2.moveWindow(winname, 1000, 0)
                    # cv2.imshow(winname, drawing)
                    self.gui_frame = drawing
                    cv2.waitKey(10)


                else:
                    cv2.waitKey(10)

                    return "nth detected"

            if self.cap_btn_clicked:  # press 'b' to capture the background
                self.bgModel = None
                self.bgModel = cv2.createBackgroundSubtractorMOG2(0, self.bgSubThreshold)
                self.isBgCaptured = 1
                self.cap_btn_clicked = 0
