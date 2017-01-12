# Importeren van de Librarys
import cv2
import numpy as np


def calibrate(img):
    # De X en Y coordinaten array aanmaken:
    y = []
    x = []

    # De verschillende hoekpunten van de afbeelding declareren:
    point1 = [0, 0]  # Linksbovenhoek
    point2 = [320, 0]  # Boven midden
    point3 = [640, 0]  # Rechtsbovenhoek
    point4 = [0, 240]  # Links midden
    point5 = [320, 240]  # middenpunt
    point6 = [640, 240]  # Rechtsmidden
    point7 = [0, 480]  # Linksonder
    point8 = [320, 480]  # Middenonder
    point9 = [640, 480]  # Rechtsonder

    # Commented because img comes from main
    # img declareren als een camera beeld:
    # img = cv2.VideoCapture(0)
    # img.read(cv2.waitKey(1000))
    # retval, img = img.read()

    pts1 = np.float32([point1, point2, point4, point5])
    pts2 = np.float32([point1, point2, point4, point5])
    pts3 = np.float32([point2, point3, point5, point6])
    pts4 = np.float32([point1, point2, point4, point5])
    pts5 = np.float32([point4, point5, point7, point8])
    pts6 = np.float32([point1, point2, point4, point5])
    pts7 = np.float32([point5, point6, point8, point9])
    pts8 = np.float32([point1, point2, point4, point5])

    A = cv2.getPerspectiveTransform(pts1, pts2)
    b = cv2.getPerspectiveTransform(pts3, pts4)
    C = cv2.getPerspectiveTransform(pts5, pts6)
    D = cv2.getPerspectiveTransform(pts7, pts8)

    corner1 = cv2.warpPerspective(img, A, (320, 240))
    corner2 = cv2.warpPerspective(img, b, (320, 240))
    corner3 = cv2.warpPerspective(img, C, (320, 240))
    corner4 = cv2.warpPerspective(img, D, (320, 240))

    cv2.imwrite('Corner1.jpg', corner1)
    cv2.imwrite('Corner2.jpg', corner2)
    cv2.imwrite('Corner3.jpg', corner3)
    cv2.imwrite('Corner4.jpg', corner4)

    for counter2 in range(1, 5):

        img_rgb = cv2.imread('Corner' + str(counter2) + '.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template = cv2.imread('templateGroen.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)

        # Slaat de coordinaten van de gevonden template match op in een array:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 255, 0), 2)
        cv2.imwrite('Cornerdetection' + str(counter2) + '.jpg', img_rgb)
        x.append(pt[0])
        y.append(pt[1])

    pts1 = np.float32([[x[0], y[0]],
                       [x[1] + 300 + w, y[1]]
                          , [x[2], y[2] + 220 + h]
                          , [x[3] + 300 + w, y[3] + 220 + h]])
    pts2 = np.float32([[0, 0],
                       [x[1] + 320 - x[0], 0]
                          , [0, y[2] + 240 - y[0]]
                          , [x[1] + 320 - x[0], y[2] + 240 - y[0]]])

    # De opgeslagen coordinaten worden gebruit om aleen het beeld tussen de template coordianten weer te geven:
    b = cv2.getPerspectiveTransform(pts1, pts2)

    # Commented because we don't need this :)
    # cam = cv2.VideoCapture(0)
    #
    # while True:
    #     retval, frame = cam.read()
    #     Plaat = cv2.warpPerspective(frame, b, (x[1] + 340 - x[0], y[2] + 260 - y[0]))
    #     if retval == True:
    #         cv2.imshow("Output", Plaat)
    #         if cv2.waitKey(10) == 27:
    #             break
    return b, x, y,


def warp(img, b, x, y):
    img_warped = cv2.warpPerspective(img, b, (x[1] + 340 - x[0], y[2] + 260 - y[0]))
    return img_warped
