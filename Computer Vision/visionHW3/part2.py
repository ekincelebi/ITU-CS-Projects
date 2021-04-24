
import pyautogui
import cv2
import numpy as np
import time



def canny(image):
    edge = cv2.Canny(image, 0, 100)
    edge= np.expand_dims(edge, axis=2)
    edge = np.where(edge == 0, [0, 0, 0], [255, 255, 255])
    return edge



time.sleep(5)
#print(pyautogui.position())
pyautogui.click(x=1534, y=166)
ss = np.array(pyautogui.screenshot())
#ss = cv2.imread('shapes.png')
ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
edge = canny(ss)
cv2.imwrite("part2.png", edge)
