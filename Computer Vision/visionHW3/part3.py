import part1
import cv2
import numpy as np


def get_structure_tensor(image, window_x, window_y, window_width, window_height):
    structure_tensor = np.zeros((2, 2))
    for x_i in range(window_width):
        for y_i in range(window_height):
            x_index = window_x + x_i
            y_index = window_y + y_i
            Ix = np.abs(image[x_index + 1, y_index] - image[x_index - 1, y_index]) / 2
            Iy = np.abs(image[x_index, y_index + 1] - image[x_index, y_index - 1]) / 2
            structure_tensor[0, 0] += Ix * Ix
            structure_tensor[0, 1] += Ix * Iy
            structure_tensor[1, 1] += Iy * Iy
            structure_tensor[1, 0] += Ix * Iy
    return structure_tensor

def corner_detector(image, kernel_width, kernel_height):
    image_copy = np.copy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    harris_array = np.zeros((image.shape[0],image.shape[1]))
    k = 0.03
    for x in range(kernel_width, image.shape[0] - kernel_width):
        for y in range(kernel_height, image.shape[1] - kernel_height):
            structure_tensor = get_structure_tensor(image, x, y, kernel_width, kernel_height)
            eigenvalues = np.linalg.eigvals(structure_tensor)
            det = eigenvalues[0] * eigenvalues[1]
            # lamda1*lambda2
            trace = eigenvalues[0] + eigenvalues[1]
            # lambda1+lambda2
            R = det - k * (trace ** 2)
            harris_array[x,y] = R

    # maximum value
    maximum_val = harris_array.max()
    limitation = 0.1 * maximum_val
    # highlights maximum values only
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if harris_array[x,y] > limitation:
                cv2.circle(image_copy, (y, x), 3, (255, 0, 0))
    return image_copy



def shrink_image(img):
    img_height = img.shape[0]
    img_width = img.shape[1]
    ratio = 360/img_height
    img = cv2.resize(img, (int(img_width*ratio), 360))
    return img

'''time.sleep(5)
    #print(pyautogui.position())
    pyautogui.click(x=1534, y=166)
    ss = np.array(pyautogui.screenshot())'''
ss = image = cv2.imread('shapes.png')
ss = shrink_image(ss)
ss = corner_detector(ss, 4, 4)
cv2.imwrite("part3.png", ss)
    
    
