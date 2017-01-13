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

    lower_yellow = np.array([22, 170, 0])
    upper_yellow = np.array([50, 255, 255])
    lower_red = np.array([0, 78, 60])
    upper_red = np.array([19, 231, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == 1:  # kleur is geel

        maskyellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellow = cv2.bitwise_and(img, img, mask=maskyellow)
        print(str1 + "yellow image gemaakt" + str2)
        return yellow

    if color == 2:  # keur is rood

        maskred = cv2.inRange(hsv, lower_red, upper_red)
        red = cv2.bitwise_and(img, img, mask=maskred)
        print(str1 + "red image gemaakt" + str2)
        return red
