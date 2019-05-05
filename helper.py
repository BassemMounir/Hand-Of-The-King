import numpy as np
import math
import cv2

# Helper functions used all around the code


class HelperFunctions():

    def distance(self, pt1, pt2):
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def calculate_angle(self, defect1, finger_tip, defect2):
        a = self.distance(defect1, defect2)
        b = self.distance(defect1, finger_tip)
        c = self.distance(defect2, finger_tip)
        angle = -1
        if b != 0 and c != 0:
            eq = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
            if eq > 1 or eq < -1:
                return angle
            angle = math.acos(eq) * (180 / math.pi)  # cosine theorem
        return angle
