# import time
# import sys
import cv2
import numpy as np

str1 = "\x1b[0;30;42m"
str2 = "\x1b[0m"


def mask_img(color, img):
    # gooi mask (afhankelijk van kleur) over img
    # if kleur == 1:
    #     img_masked = mask geel
    # if kleur == 2:
    #     img_masked = mask rood
    # etc

    b = cv2.getTrackbarPos('B', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    r = cv2.getTrackbarPos('R', 'image')
    b1 = cv2.getTrackbarPos('B1', 'image')
    g1 = cv2.getTrackbarPos('G1', 'image')
    r1 = cv2.getTrackbarPos('R1', 'image')

    lower_unit = np.array([b, g, r])
    upper_unit = np.array([b1, g1, r1])

    lower_yellow = np.array([26, 108, 187])
    upper_yellow = np.array([33, 255, 255])
    lower_red = np.array([0, 103, 31])
    upper_red = np.array([24, 248, 236])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == 1:  # kleur is geel

        maskyellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellow = cv2.bitwise_and(img, img, mask=maskyellow)
        print(str1 + "yellow image gemaakt" + str2)
        cv2.imwrite("C:/Users/kwint/Documents/1. School/Python dingen/project/yellow.jpg", yellow)
        return yellow

    if color == 2:  # keur is rood

        maskred = cv2.inRange(hsv, lower_red, upper_red)
        red = cv2.bitwise_and(img, img, mask=maskred)
        print(str1 + "red image gemaakt" + str2)
        cv2.imwrite("C:/Users/kwint/Documents/1. School/Python dingen/project/red.jpg", red)
        return red
