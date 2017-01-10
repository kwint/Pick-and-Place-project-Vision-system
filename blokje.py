import cv2
import numpy as np


def herken(img_gray, img):
    _, bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
    bin, contours, hierachy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    shape = ""
    angle = 0
    height = 0

    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        center = rect[0]
        angle = rect[2]
        angle = round(angle, 2) + 180
        cx, cy = center
        cx = int(cx)
        cy = int(cy)

        epsilon = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * epsilon, True)

        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            print(ar)

            if 0.95 <= ar <= 1.05:
                shape = "kubus"
                height = 1
                cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

            else:
                shape = "plank"
                cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

                if 1.70 <= ar <= 2.00:  # ligt plat
                    height = 2
                if 0.40 <= ar <= 0.70:
                    height = 3
        else:
            shape = ""
            angle = 0
            height = 0

    return shape, angle, height, img
