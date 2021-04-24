import numpy as np
import cv2 as cv
import pyautogui
import time


def hough_circles(image):
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1.2, 100)
    if circles is None:
        return 0
    else:
        circles = np.uint16(np.around(circles))
        return len(circles[0, :])

def get_screenshot(latency=0):
    time.sleep(latency)
    ss = np.array(pyautogui.screenshot())
    ss = cv.cvtColor(np.array(ss), cv.COLOR_RGB2BGR)
    return ss

time.sleep(3)
while True:
    im = np.array(pyautogui.screenshot())
    im = cv.GaussianBlur(im, (5, 5), 0)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 200, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(im, contours, -1, 255, 3)

    contours.sort(key=cv.contourArea, reverse=True)
    hold_list = []
    for contour in contours[:3]:
        extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
        extRight = tuple(contour[contour[:, :, 0].argmax()][0])
        extTop = tuple(contour[contour[:, :, 1].argmin()][0])
        extBot = tuple(contour[contour[:, :, 1].argmax()][0])

        ###bounding rectangle points
        x, y, w, h = cv.boundingRect(contour)

        ###perspectivce transform
        rows, cols = imgray.shape
        pts1 = np.float32([extLeft, extTop, extBot, extRight])
        pts2 = np.float32([[x, y], [x + w, y], [x, y + w], [x + w, y + w]])

        M = cv.getPerspectiveTransform(pts1, pts2)
        imgray = cv.warpPerspective(imgray, M, (cols, rows))
        imgray = imgray[y:y + w, x:x + w]

        ###calculate circles
        circles = hough_circles(imgray)
        hold_list.append((x, circles))
        imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)  # restore

    hold_list.sort(key=lambda tup: tup[0])  # sort the list by left to right dice
    index = [i for i, tupl in enumerate(hold_list) if tupl == max(hold_list, key=lambda tup: tup[1])][0]  # find the position of the dice with the most circles

    if index == 0:
        print("a pressed")
        pyautogui.press('a')
    elif index == 1:
        print("s pressed")
        pyautogui.press('s')
    elif index == 2:
        print("d pressed")
        pyautogui.press('d')
    else:
        print("nothing pressed")

