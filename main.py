# Geschreven door Quinty van Dijk

import cv2
import block
import color
import connect
import calibrate
import numpy as np

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
    webcam = cv2.VideoCapture(0)

    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    webcam.get(cv2.CAP_PROP_FRAME_WIDTH)

    # return webcam info
    print(str1 + "Init Done" + str2)
    return webcam


def calibration(cam):
    print(str1 + "Start calibration" + str2)
    while True:
        retval, img = cam.read()
        if retval:
            b, x, y = calibrate.calibrate(img)
            print(str1 + "Calibration done" + str2)
            return b, x, y


def next_color(code):
    code += 1
    if code >= 3:
        code = 1
    return 2


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
        cx = int(cx*0.965)

    if cx > 0:
        cx = int(cx*0.88)

    cy = int(((y / 1.69) - 175) * 0.93)

    return cx, cy


# Main:
# init and calibration
color_code = 1
webcam = init()
b_cal, x_cal, y_cal = calibration(webcam)

# main loop
print(str1 + "Start loop" + str2)
while True:
    if cv2.waitKey(10) == 27:
        break
    print(str1 + "Top of loop. Waiting for plc" + str2)
    # Wait for connection from PLC
    # connect.from_plc()
    ready = True

    while ready:

        # img = cv2.imread("C:/Users/kwint/Documents/1. School/Python dingen/project/test.jpg")

        # Get image from webcam
        retval, img = webcam.read()
        if retval:

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

                cv2.putText(img_warped, str(y_mm), (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(img_warped, str(x_mm), (80, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                print(type(x_mm), type(y_mm), type(shape), type(degree), type(color_code), color_code)

                # connect.to_plc(x_mm, y_mm, shape, color_code, degree)
                ready = False

            # If shape not found, tmp == false, print error message and go on
            else:

                print(str1 + "Didn't found a shape with color: " + str2, get_color(color_code))

            # Shape found or not, let's check the next color
            color_code = next_color(color_code)

            # Show images to windows
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
