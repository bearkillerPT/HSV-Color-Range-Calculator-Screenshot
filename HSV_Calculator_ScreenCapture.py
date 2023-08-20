import cv2
import numpy as np
import pyautogui
from fpstimer import FPSTimer

def nothing(x):
    pass

def hsv_calc():
    active_trackbar = "lh"  # Start with the lower hue trackbar as active

    fps_manager = FPSTimer(5)  # Make a timer that is set for 10 fps.
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("lh", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("ls", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("lv", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("uh", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("us", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("uv", "Trackbars", 255, 255, nothing)

    while True:
        fps_manager.sleep()
        frame = pyautogui.screenshot()
        frame = np.array(frame)     
        # transform to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        # transform to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lh = cv2.getTrackbarPos("lh", "Trackbars")
        ls = cv2.getTrackbarPos("ls", "Trackbars")
        lv = cv2.getTrackbarPos("lv", "Trackbars")
        uh = cv2.getTrackbarPos("uh", "Trackbars")
        us = cv2.getTrackbarPos("us", "Trackbars")
        uv = cv2.getTrackbarPos("uv", "Trackbars")

        l_blue = np.array([lh, ls, lv])
        u_blue = np.array([uh, us, uv])
        mask = cv2.inRange(hsv, l_blue, u_blue)

        cv2.imshow("mask", mask)

        key = cv2.waitKey(1)

        if key == 27:  # ESC key to exit
            break
        elif key == 82:  # Up arrow key
            current_value = cv2.getTrackbarPos(active_trackbar, "Trackbars")
            cv2.setTrackbarPos(active_trackbar, "Trackbars", min(current_value + 1, 255))
        elif key == 84:  # Down arrow key
            current_value = cv2.getTrackbarPos(active_trackbar, "Trackbars")
            cv2.setTrackbarPos(active_trackbar, "Trackbars", max(current_value - 1, 0))
        elif key == ord('t'):  # Toggle active trackbar
            active_trackbar = "lh" if active_trackbar == "uh" else "uh"

    cv2.destroyAllWindows()

hsv_calc()
