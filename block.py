# Geschreven door Tim Busscher
# test 123

import cv2
import numpy as np

str1 = "\x1b[0;30;41m"
str2 = "\x1b[0m"


def recognize(img_gray, img):
    print(str1 + "Looking for block!" + str2)
    _, bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
    bin, contours, hierachy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    # img_show = img
    shape = 0
    angle = 0
    anglesend =0

    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        center = rect[0]
        angle = rect[2]
        angle = round(angle, 2)
        cx, cy = center
        cx = int(cx)
        cy = int(cy)

        epsilon = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * epsilon, True)

        # if abs(angle) >= 88 or abs(angle) <= 2:
        #     angle = 0
        #     if rect[1][0] < rect[1][1]:
        #         angle = 90

        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(len(approx))
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            if 0 < abs(rect[1][0] - rect[1][1]) < 10:
                shape = 1  # Shape 1  = kubus

            elif 35 < abs(rect[1][0] - rect[1][1]) < 48:  # ligt plat
                shape = 2
            elif 55 < abs(rect[1][0] - rect[1][1]) < 80:
                shape = 3
            elif 85 < abs(rect[1][0] - rect[1][1]) < 95:  # ligt plat grote plank (tim)
                shape = 4


            elif shape == 0:
                cv2.putText(img, "shape == 0", (80, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

            if rect[1][0] < rect[1][1]:
                angle = abs(angle) + 90
            elif rect[1][0] > rect[1][1]:
                angle = abs(angle) + 0

            if angle <= 90:
                anglesend = angle + 90
            if angle > 90:
                anglesend = angle - 90

        elif len(approx) >= 5 or len(approx) <= 12:
            shape = 5

            cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

            if rect[1][0] < rect[1][1]:
                angle = abs(angle) + 90
            elif rect[1][0] > rect[1][1]:
                angle = abs(angle) + 0

            if angle <= 90:
                anglesend = angle + 90
            if angle > 90:
                anglesend = angle - 90

        else:
            return False

        # cv2.putText(img_show, "Height :", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img, "Cor", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img_show, str(height), (80, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, str(angle), (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img, str(shape), (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img, str(anglesend), (80, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        #
        # cv2.imshow("beeld4", img_show)
        print(" lente breetblokje:", rect[1][0], rect[1][1])
        print(str1 + "Blokje gevonden met volgende gegevens:" + str2, "\nX: ", cx, "Y: ", cy, "Shape: ", shape,
              "Hoek: ", angle)
        return int(cx), int(cy), int(shape), int(anglesend)
