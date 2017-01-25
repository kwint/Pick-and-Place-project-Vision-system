# Geschreven door Quinty van Dijk

import cv2
import block
import color
import connect
import calibrate
from easygui import *
import numpy as np
from time import sleep

str1 = "\x1b[0;30;44m"
str2 = "\x1b[0m"


def nothing(x):
    pass


def init():
    print(str1 + "Start init" + str2)
    # ghallow kwintie
    # Make windows to show webcam image, gray image etc
    cv2.WINDOW_AUTOSIZE

    cv2.namedWindow("beeld1", cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow("beeld1", 0, 0)

    cv2.namedWindow("beeld2", cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow("beeld2", 640, 0)

    cv2.namedWindow("beeld3", cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow("beeld3", 640 * 2, 0)

    cv2.namedWindow("beeld4", cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow("beeld4", 640 * 2, 480)

    # cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    # cv2.moveWindow('image', 640, 0)
    # cv2.createTrackbar('B', 'image', 0, 255, nothing)
    # cv2.createTrackbar('G', 'image', 0, 255, nothing)
    # cv2.createTrackbar('R', 'image', 0, 255, nothing)
    #
    # cv2.createTrackbar('B1', 'image', 0, 255, nothing)
    # cv2.createTrackbar('G1', 'image', 0, 255, nothing)
    # cv2.createTrackbar('R1', 'image', 0, 255, nothing)

    # Make connection to webcam
    webcam = cv2.VideoCapture(1)

    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    webcam.get(cv2.CAP_PROP_FRAME_WIDTH)

    # return webcam info
    print(str1 + "Init Done" + str2)
    return webcam


def calibration(cam, threshold):
    print(str1 + "Start calibration" + str2)
    while True:
        retval, img = cam.read()
        if retval:
            b, x, y = calibrate.calibrate(img, threshold)
            print(str1 + "Calibration done" + str2)
            return b, x, y


def next_color(code):
    code += 1
    if code >= 3:
        code = 1
    return code


def get_color(code):
    if code == 1:
        return "yellow"
    if code == 2:
        return "red"


def get_edges(img):
    cv2.imwrite("C:/image.jpg", img)

    imggray_temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("C:/grayscale.jpg", imggray_temp)

    # Maak imggray "smoother" voor minder ruis en dus betere detectie
    imggray = cv2.GaussianBlur(imggray_temp, (5, 5), 0)
    cv2.imwrite("C:/blur.jpg", imggray)

    # Voor canny methode uit, geeft afbeelding met randen
    img_edges = cv2.Canny(imggray, 60, 100)
    cv2.imwrite("C:/edges.jpg", img_edges)
    print(str1 + "IMG processing done, edges made" + str2)

    return img_edges


def get_image(webcam):
    while True:
        retval, img = webcam.read()
        if retval:
            return img


def to_mm(x, y, img):
    # y_img, x_img, bin = img.shape
    # print(199/y_img)
    # print(278/x_img)
    # y_mm = 198 / y_img * y
    # x_mm = 2786 / x_img * x
    # x_mm -= 159
    # y_mm -= 158

    # vector = np.array([[x], [y]])
    # print(vector)
    # trans_matrix = np.array([[-158, 120], [-159, 40]])
    # print(trans_matrix)
    # trans_vector = trans_matrix * vector
    # print(trans_vector)

    cx = int((x / 1.73) - 136)
    if cx < 0:
        cx = int(cx * 0.965)

    if cx > 0:
        cx = int(cx * 0.88)

    cy = int(((y / 1.69) - 175) * 0.93)

    return cx, cy


# Main:
# init and calibration
color_code = 1
webcam = init()
calibrated = False
cal_threshold = 0.7
y_mm_save = []
x_mm_save = []
delay = 3

# # Wait for PLC
while not connect.from_plc():
    print(str1 + "Waiting for PLC before calibration" + str2)
img_warped = 0
while not calibrated:
    # calibration:
    try:
        b_cal, x_cal, y_cal = calibration(webcam, cal_threshold)
        # show calibration status
        img = get_image(webcam)
        img_warped = calibrate.warp(img, b_cal, x_cal, y_cal)

        print("show images:")
        cv2.imshow("beeld4", img_warped)
        cv2.waitKey(10)

        user = boolbox(msg="Calibratie oke?", title="Calibratie", choices=("[J]a", "[N]ee"), default_choice="Yes")
        if not user:
            cal_threshold = enterbox(msg="Threshold nu is" + str(cal_threshold), title="Threshold check",
                                     default=str(cal_threshold))
        if user:
            calibrated = True


    except Exception:
        print("calibratie mislukt!")

# main loop
print(str1 + "Start loop" + str2)
while True:
    if cv2.waitKey(10) == 27:
        break
    print(str1 + "Top of loop. Waiting for plc" + str2)
    # Wait for connection from PLC
    while not connect.from_plc():
        img = get_image(webcam)
        img_warped = calibrate.warp(img, b_cal, x_cal, y_cal)
    ready = True
    count_red = 0
    count_mov_red = 0
    count_yellow = 0
    count_mov_yellow = 0

    while ready:

        # img = cv2.imread("C:/Users/kwint/Documents/1. School/Python dingen/project/test.jpg")

        # Get image from webcam
        img = get_image(webcam)

        # warp image from with data gotten from calibration
        img_warped = calibrate.warp(img, b_cal, x_cal, y_cal)

        # Filter one color out image
        img_color = color.mask_img(color_code, img_warped)

        # convert img color to edges.
        img_edges = get_edges(img_color)

        # Check for a shape in image
        tmp = block.recognize(img_edges, img_warped)

        # If shape found, send it to PLC
        if tmp:
            x_got, y_got, shape, degree = tmp

            print(str1 + "Found a shape!" + str2, get_color(color_code))

            x_mm, y_mm = to_mm(x_got, y_got, img_warped)
            print(y_mm, x_mm)

            cv2.putText(img_warped, str(y_mm), (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(img_warped, str(x_mm), (80, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(img_warped, str(degree), (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(img_warped, str(shape), (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(img_warped, str(color_code), (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv2.putText(img_warped, get_color(color_code), (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            print(type(x_mm), type(y_mm), type(shape), type(degree), type(color_code), color_code)
            if color_code == 1:
                if count_yellow == 0:
                    x_mm_temp_yellow = x_mm
                    y_mm_temp_yellow = y_mm
                    count_yellow = 1
                elif count_yellow == 1:

                    x_change_yellow = abs(x_mm_temp_yellow - x_mm)
                    y_change_yellow = abs(y_mm_temp_yellow - y_mm)
                    count_yellow = 0
                    print("x_change: ", x_change_yellow)
                    print("y_change: ", y_change_yellow)
                    if x_change_yellow < 3 and y_change_yellow < 3:
                        count_mov_yellow += 1
                    else:
                        count_mov_yellow = 0

                if count_mov_yellow > delay:
                    print("sending to plc")
                    connect.to_plc(int(y_mm), int(x_mm), shape, color_code,
                                   degree)  # veranderd naar int (tim) was eerst floats
                    ready = False
                    count_yellow = 0
                    count_mov_yellow = 0
                    count_mov_rd = 0

            if color_code == 2:
                if count_red == 0:
                    x_mm_temp_red = x_mm
                    y_mm_temp_red = y_mm
                    count_red = 1
                elif count_red == 1:

                    x_change_red = abs(x_mm_temp_red - x_mm)
                    y_change_red = abs(y_mm_temp_red - y_mm)
                    count_red = 0
                    print("x_change: ", x_change_red)
                    print("y_change: ", y_change_red)
                    if x_change_red < 3 and y_change_red < 3:
                        count_mov_red += 1
                    else:
                        count_mov_red = 0

                if count_mov_red > delay:
                    print("sending to plc")
                    connect.to_plc(int(y_mm), int(x_mm), shape, color_code,
                                   degree)  # veranderd naar int (tim) was eerst floats
                    ready = False
                    count_red = 0
                    count_mov_red = 0
                    count_mov_yellow = 0

            print("Count: ", count_red)
            print("Count_mov", count_mov_red)



        # If shape not found, tmp == false, print error message and go on
        else:
            print(str1 + "Didn't found a shape with color: " + str2, get_color(color_code))

        # Shape found or not, let's check the next color
        color_code = next_color(color_code)

        # Show images to windows
        cv2.putText(img_warped, "X_mm:", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img_warped, "Y_mm:", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img_warped, "Angle:", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img_warped, "Block:", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img_warped, "Color:", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.imshow("beeld1", img)
        cv2.imshow("beeld2", img_color)
        cv2.imshow("beeld3", img_edges)
        cv2.imshow("beeld4", img_warped)
        cv2.imwrite("C:/gevonden.jpg", img)

        # Press esc to exit program
        if cv2.waitKey(10) == 27:
            break

webcam.release()
cv2.destroyAllWindows()
