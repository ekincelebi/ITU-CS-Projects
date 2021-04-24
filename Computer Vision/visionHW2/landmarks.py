import dlib
import cv2
####important
#### i had to remove shape predictor model, in order to make my code work
#### can you please add it to the main folder
### many thanks
def read_image(path):
    image = cv2.imread(path)
    return image

def check_rectangles(rectangles):
    return True if len(rectangles) == 1 else False

def landmark_points(img):
    # Load the detector
    detector = dlib.get_frontal_face_detector()
    # Load the predictor
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    # Convert image into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Use detector to find landmarks
    rectangles = detector(gray)
    #check if there is only one rectangle
    check_rectangles(rectangles)
    # Locate rectangle
    '''br_x = rectangles[0].br_corner().x
    br_y = rectangles[0].br_corner().y
    tl_x = rectangles[0].tl_corner().x
    tl_y = rectangles[0].tl_corner().y
    cv2.rectangle(img, (tl_x, tl_y), (br_x, br_y), (255, 0, 0), 2)'''
    # Create landmark object
    points = predictor(gray, rectangles[0])
    return points

def draw_circles(points,img):
    # Loop through all the points
    for i in range(0, 68):
        x = points.part(i).x
        y = points.part(i).y
        # Draw a circle
        cv2.circle(img=img, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)

def show_landmark_points(im_path):
    # Read the image
    img = cv2.imread(im_path)
    # Find landmark points
    points = landmark_points(img)
    # Draw the circles
    draw_circles(points, img)
    # Show the image
    cv2.imshow("landmarks", img)
    # Delay between every fram
    cv2.waitKey(0)


def circle_image(im_path):
    # Read the image
    img = cv2.imread(im_path)
    # Find landmark points
    points = landmark_points(img)
    # Draw the circles
    draw_circles(points, img)
    return img


#show_landmark_points("./images/kimbodnia.png")









