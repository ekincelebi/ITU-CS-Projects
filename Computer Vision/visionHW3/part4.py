import pyautogui
import time
import numpy as np
import cv2
import os.path
import math


def shrink_image(img):
    img_height = img.shape[0]
    img_width = img.shape[1]
    ratio = 360/img_height
    img = cv2.resize(img, (int(img_width*ratio), 360))
    #cv2.imwrite("shrinked.png", img)
    return img
    
def get_screenshot(latency=0):
    time.sleep(latency)
    ss = np.array(pyautogui.screenshot())
    ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
    return ss


def is_edge(edge):
    #take the result of get edges as param
    #top ve bottom arasındaki benzerlik fazlaysa dörtgen veya altıgen
    #top ve bottom alakasızsa ucgen veya altıgen

    top =  np.sum(edge[275:295, 250:310, :] == [255, 255, 255])
    top_middle = np.sum(edge[300:315, 250:310, :] == [255, 255, 255])
    bottom_middle = np.sum(edge[315:340, 250:310, :] == [255, 255, 255])
    bottom = np.sum(edge[340:360, 250:310, :] == [255, 255, 255])
    return np.array([top, top_middle, bottom_middle, bottom])

def is_corner(corner):
    # take the result of get corners as param
    top = np.sum(corner[270:300, 250:310] == 255)
    top_middle = np.sum(corner[300:315, 250:310] == 255)
    bottom_middle = np.sum(corner[315:340, 250:310] == 255)
    bottom = np.sum(corner[340:360, 250:310] == 255)
    return np.array([top,top_middle,bottom_middle,bottom])

def hold_a (hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.press('a')

def hold_s (hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.press('s')

def hold_d (hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.press('d')

def hold_f (hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.press('f')

def which_shape(corners,edges):
    #the case for sguare and triangle
    if corners[1] == 0 and corners[2] == 0:
        if corners[3] > 0 and corners[0] == 0:
            # only one corner is in the check region
            hold_a(0.25)
            print("triangle")
        elif corners[0] > 0 and corners[3] > 0 and corners[2] == 0 and edges[0] > edges[1]:
            # has a top and bottom corner no middle corner top edge is bigger than middle edges
            if edges[1] <= 100:
                hold_s(0.25)
                #print("square")
            elif edges[1] >= 100:
                hold_f(0.25)

            elif edges[3] > edges[0] and corners[0] > 0 and corners[0] < 25:
            # if bottom edge is wider than the top edge and only one top corner
                hold_a(0.25)
                print("triangle")
    else:
        if corners[2] > 0:
            hold_d(0.25)
            #print("star")
        
        else:
            #elif corners[2] == 0 and corners[1] > 0:
            hold_f(0.30)
            #print("hexagon")
            #print(edges[1])
            #print(edges[2])
    
    



def get_edges(image):
    edge_image = cv2.Canny(image, 0, 100)
    edge_image = np.expand_dims(edge_image, axis=2)
    edge_image = np.where(edge_image == 0, [0, 0, 0], [255, 255, 255])
    #cv2.imwrite(out_path, edge_image)
    return edge_image



def get_corners(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    image[dst<=0.03*dst.max()]=[0,0,0]
    image[dst>0.03*dst.max()]=[255,255,255]
    img2d = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #img2d = np.float32(img2d)
    #cv2.imwrite(out_path, image)
    return img2d



if __name__ == '__main__':
    # Start the game
    time.sleep(5)
    # Point(x=1394, y=392) shame
    # Point(x=1552, y=292) vabank
    pyautogui.click(x=1394, y=392)

    while True:
        # take screenshot
        
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        #screenshot = cv2.imread("tristar.png")
        # shrink
        shrinked = shrink_image(screenshot)


        # get edge point count
        edge = get_edges(shrinked)
        edges_list = is_edge(edge)

        # get corner point count
        corner = get_corners(shrinked)
        corners_list = is_corner(corner)

        # which shape
        which_shape(corners_list, edges_list)  
        #time.sleep(0.25)      
        








    
   


    
