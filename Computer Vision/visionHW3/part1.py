import pyautogui
import time
import numpy as np
import cv2
import os.path
import math

#apply sobel filter to the all shapes page
def apply_kernel(image, axis):
    SOBEL_X = np.array((
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]), dtype="int32")

    # Sobel y-axis kernel
    SOBEL_Y = np.array((
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]), dtype="int32")

    if axis == 'x':
        kernel = SOBEL_X
    elif axis == 'y':
        kernel = SOBEL_Y


    kernel_width = SOBEL_Y.shape[0]
    kernel_height = SOBEL_Y.shape[1]
    image_copy = np.zeros(image.shape)
    for x in range(0, image.shape[0] - kernel.shape[0]):
        for y in range(0, image.shape[1] - kernel.shape[1]):
            window = image[x:x+kernel_width, y:y+kernel_height]
            image_copy[x, y] = np.abs(np.sum(np.multiply(window, kernel)))

    return image_copy

def shrink_image(img):
    img_height = img.shape[0]
    img_width = img.shape[1]
    ratio = 360/img_height
    img = cv2.resize(img, (int(img_width*ratio), 360))
    #cv2.imwrite("shrinked.png", img)
    return img



time.sleep(5)
#print(pyautogui.position())
pyautogui.click(x=1534, y=166)
ss = np.array(pyautogui.screenshot())
#ss = cv2.imread('shapes.png')
ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
ss = shrink_image(ss)

x_kernel_ss = apply_kernel(ss, 'x')
y_kernel_ss = apply_kernel(ss, 'y')

#calculate Sobel x
cv2.imwrite('x_image.png', x_kernel_ss)
#calculate Sobel y
cv2.imwrite('y_image.png', y_kernel_ss)

cv2.imwrite('part1.png', x_kernel_ss + y_kernel_ss)
