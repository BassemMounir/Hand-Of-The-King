import numpy as np
import math
import cv2

# Helper functions used all around the code


class HelperFunctions():

    def distance(self, pt1, pt2):
        #calculate the euclidean distance between 2 points
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def calculate_angle(self, defect1, finger_tip, defect2):
        #calculate the angle between the candidate finger tip and neighbouring defects using cosine law
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
    
    def average_and_join_points(self, points, min_distance):  # for clustering defects near to each other
        final_points = []
        avg_array = []
        if points is not None:
            for i in range(1, points.shape[0]):  # calculate the angle
                x1 = points[i - 1][0][0]
                y1 = points[i - 1][0][1]
                x2 = points[i][0][0]
                y2 = points[i][0][1]
                point1 = (x1, y1)
                point2 = (x2, y2)
                if self.distance(point1, point2) < min_distance:
                    if point1 not in avg_array:
                        avg_array.append(point1)
                    if point2 not in avg_array:
                        avg_array.append(point2)
                else:
                    if len(avg_array) > 0:
                        final_points.append(self.get_avg_point(avg_array))
                        avg_array.clear()
                    else:
                        if point1 not in avg_array:
                            final_points.append(point1)
        return final_points

    def remove_noisy_defects(self, res, defects):  # for removing defects not on the hand
        new_defects = []
        for j in range(0, len(defects)):
            s1, e1, f1, d1 = defects[j][0]
            start1 = tuple(res[s1][0])
            end1 = tuple(res[e1][0])
            far1 = tuple(res[f1][0])
            if self.distance(start1, end1) > 10:
                new_defects.append((start1, end1, far1))
        return new_defects


