import cv2
import numpy as np

def get_feature_points(path):
    points = np.load(path)
    return points

def draw_circles(points,img):
    for i in range(0, 68):
        cv2.circle(img=img, center=(points[i][0], points[i][1]), radius=3, color=(0, 255, 0), thickness=-1)


def circle_image(im_path,landmark_path):
    # Read the image
    img = cv2.imread(im_path)
    # Find landmark points
    points = get_feature_points(landmark_path)
    # Draw the circles
    draw_circles(points, img)
    return img


def show_landmark_points(im_path,landmark_path):
    # Read the image
    img = cv2.imread(im_path)
    # Find landmark points
    points = get_feature_points(landmark_path)
    # Draw the circles
    draw_circles(points, img)
    # Show the image
    cv2.imshow("animal_landmarks", img)
    # Delay between every fram
    cv2.waitKey(0)




#show_landmark_points("./images/panda.jpg","./images/panda_landmarks.npy")