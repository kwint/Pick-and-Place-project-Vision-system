import cv2
import numpy as np

str1 = "\x1b[0;30;41m"
str2 = "\x1b[0m"

def recognize(img_gray, img):
    _, bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
    bin, contours, hierachy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    img_show = img
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

            if 0.95 <= ar <= 1.05:
                shape = 1 # Shape 1  = kubus
                height = 1
                cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

            else:
                shape = 2 # Shape 2 = kubus
                cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

                if 1.70 <= ar <= 2.00:  # ligt plat
                    height = 2
                if 0.40 <= ar <= 0.70:
                    height = 3
        else:
            return False

        # cv2.putText(img_show, "Height :", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img_show, "Graden:", (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img_show, "Shape :", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img_show, str(height), (80, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img_show, str(angle), (80, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # cv2.putText(img_show, str(shape), (80, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #
        # cv2.imshow("beeld4", img_show)

        print(str1 + "Blokje gevonden met volgende gegevens:" + str2, "\nX: ", cx, "Y: ", cy, "Shape: ", shape, "Hoek: ", angle,
              'Hoogte/kant: ', height)
        return cx, cy, shape, angle, height
