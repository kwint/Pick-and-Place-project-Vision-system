import cv2
import blokje
import color
import connect


def nothing(x):
    pass


def init():
    print("Start init")

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

    cv2.namedWindow("trackbars", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("trackbars", 0, 450)

    # Make connection to webcam
    webcam = cv2.VideoCapture(0)

    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    webcam.get(cv2.CAP_PROP_FRAME_WIDTH)

    # create trackbars for low and high values canny method
    cv2.createTrackbar('laag', 'trackbars', 100, 1000, nothing)
    cv2.createTrackbar('hoog', 'trackbars', 200, 1000, nothing)

    # return webcam info
    return webcam


def next_color(code):
    code += 1
    if code >= 3:
        code = 1
    return code


def get_color(code):
    if code == 1:
        return "geel"
    if code == 2:
        return "rood"


def get_edges(img, low, high):
    imggray_temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Maak imggray "smoother" voor minder ruis en dus betere detectie
    imggray = cv2.GaussianBlur(imggray_temp, (5, 5), 0)

    # Voor canny methode uit, geeft afbeelding met randen
    img_edges = cv2.Canny(imggray, low, high)
    print("Img edges gemaakt")

    return img_edges


# kalibreer()


color_code = 1
webcam = init()

while True:

    connect.from_plc()

    retval, img = webcam.read()
    if retval:

        img_color = color.mask_img(color_code, img)

        # convert img color to edges
        low = cv2.getTrackbarPos('laag', 'trackbars')
        high = cv2.getTrackbarPos('hoog', 'trackbars')

        img_edges = get_edges(img_color, low, high)

        tmp = blokje.herken(img_edges, img)

        if tmp:
            x, y, shape, degree, side, img = tmp
            print("blokje gevonden")
            print("x: ", type(x))
            # send.to_plc(x, y, shape, color, degree, side)

        else:

            print("Geen blokje gevonden in de kleur", get_color(color_code))

        color_code = next_color(color_code)
        print("color_code main: ", color_code)

        cv2.imshow("beeld1", img)
        cv2.imshow("beeld2", img_color)
        cv2.imshow("beeld3", img_edges)

        if cv2.waitKey(10) == 27:
            break

webcam.release()
cv2.destroyAllWindows()

# wacht op PLC signaal voor volgende rotine
