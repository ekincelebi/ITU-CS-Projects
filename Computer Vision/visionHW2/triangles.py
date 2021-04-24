import cv2
import numpy as np
import landmarks
import landmarks_anim

def read_image(path):
    image = cv2.imread(path)
    return image

def get_triangular_corners(corners):

    corner_1 = tuple(corners[:2])
    corner_2 = tuple(corners[2:4])
    corner_3 = tuple(corners[4:6])


    return corner_1, corner_2, corner_3

def create_triangles(image, subdiv,points):
    #create triangles and gives id for each corner
    triangles = subdiv.getTriangleList()
    lineThickness = 1
    corner_ids = []
    for i in range(len(triangles)):
        corners = triangles[i].astype(np.int)
        corner_1, corner_2, corner_3 = get_triangular_corners(corners)

        for j in range(0, 76):
            if points[j][0] == corner_1[0] and points[j][1] == corner_1[1]:
                corner_id1 = j
            if points[j][0] == corner_2[0] and points[j][1] == corner_2[1]:
                corner_id2 = j
            if points[j][0] == corner_3[0] and points[j][1] == corner_3[1]:
                corner_id3 = j
        corner_ids.append([corner_id1,corner_id2,corner_id3])

        cv2.line(image, corner_1, corner_2, (0, 255, 0), lineThickness)
        cv2.line(image, corner_2, corner_3, (0, 255, 0), lineThickness)
        cv2.line(image, corner_3, corner_1, (0, 255, 0), lineThickness)

    return triangles,corner_ids

def get_center(point1, point2):
    center = [((point1[0] + point2[0]) / 2), ((point1[1] + point2[1]) / 2)]
    return tuple(center)

def get_corner_list(shape):
    #get corner points
    corner_list = []
    # main corners
    corner_list.append((0, 0))
    corner_list.append((shape[0] - 1, 0))
    corner_list.append((shape[0] - 1, shape[1] - 1))
    corner_list.append((0, shape[1] - 1))

    # middle points
    corner_list.append(get_center(corner_list[0], corner_list[1]))
    corner_list.append(get_center(corner_list[1], corner_list[2]))
    corner_list.append(get_center(corner_list[2], corner_list[3]))
    corner_list.append(get_center(corner_list[3], corner_list[0]))

    a = [(t[1], t[0]) for t in corner_list]

    return a

def insert_corners(subdiv, shape):
    corner_list = get_corner_list(shape)

    for corner in (corner_list):
        subdiv.insert(corner)


def insert_subdiv_points(points, subdiv, shape):
    #insert subdiv points human
    for i in range(68):
        p_x, p_y = points.part(i).x, points.part(i).y
        subdiv.insert((p_x, p_y))

    insert_corners(subdiv, shape)

def insert_animal_points(points, subdiv, shape):
    # insert subdiv points animals
    for i in range(68):
        p_x, p_y = points[i][0], points[i][1]
        subdiv.insert((p_x, p_y))

    insert_corners(subdiv, shape)

def create_animal_triangles(animal_path,landmark_path):
    animal = read_image(animal_path)
    subdiv = cv2.Subdiv2D((0, 0, animal.shape[1], animal.shape[0]))
    points = landmarks_anim.get_feature_points(landmark_path)
    #add edge points to landmarks
    edge_points = np.array([[0, 0], [199, 0], [0, 199], [399, 0],
                            [0, 399], [399, 199], [199, 399], [399, 399]])
    total_points = np.concatenate((points, edge_points))
    insert_animal_points(points, subdiv, animal.shape)
    triangles,ids = create_triangles(animal, subdiv,total_points)
    ids = np.array(ids)
    return triangles, animal, ids

def create_human_triangles(image_path):
    image = read_image(image_path)
    subdiv = cv2.Subdiv2D((0, 0, image.shape[1], image.shape[0]))
    points = landmarks.landmark_points(image)
    hum_points = np.zeros((68,2))
    for i in range(0, 68):
        x = points.part(i).x
        y = points.part(i).y
        hum_points[i][0] = x
        hum_points[i][1] = y
    edge_points = np.array([[0, 0], [199, 0], [0, 199], [399, 0],
                            [0, 399], [399,199], [199, 399], [399, 399]])
    insert_subdiv_points(points, subdiv, image.shape)
    total_points = np.concatenate((hum_points, edge_points))
    triangles,ids = create_triangles(image, subdiv,total_points)
    ids = np.array(ids)
    #print("human ids",ids)
    return triangles,image, ids

def secondary_triangles_human(image_path,primary_ids):
    # sort the corners of the second image by given id's
    secondary_triangles = []
    image = read_image(image_path)
    points = landmarks.landmark_points(image)
    hum_points = np.zeros((68, 2), dtype=int)
    for i in range(0, 68):
        x = points.part(i).x
        y = points.part(i).y
        hum_points[i][0] = x
        hum_points[i][1] = y
    # add edge points to landmarks
    edge_points = np.array([[0, 0], [199, 0], [0, 199], [399, 0],
                            [0, 399], [399,199], [199, 399], [399, 399]])
    total_points = np.concatenate((hum_points, edge_points))
    for i in range(len(primary_ids)):
        first_id = primary_ids[i][0]
        second_id = primary_ids[i][1]
        third_id = primary_ids[i][2]
        x1 = total_points[first_id][0]
        y1 = total_points[first_id][1]
        x2 = total_points[second_id][0]
        y2 = total_points[second_id][1]
        x3 = total_points[third_id][0]
        y3 = total_points[third_id][1]
        arr = [x1,y1,x2,y2,x3,y3]
        secondary_triangles.append(arr)
    return np.array(secondary_triangles)



def secondary_triangles_animal(animal_path,landmark_path,primary_ids):
    #sort the corners of the second image by given id's
    secondary_triangles = []
    points = landmarks_anim.get_feature_points(landmark_path)
    edge_points = np.array([[0, 0], [199, 0], [0, 199], [399, 0],
                            [0, 399], [399, 199], [199, 399], [399, 399]])
    total_points = np.concatenate((points, edge_points))
    for i in range(len(primary_ids)):
        first_id = primary_ids[i][0]
        second_id = primary_ids[i][1]
        third_id = primary_ids[i][2]
        x1 = total_points[first_id][0]
        y1 = total_points[first_id][1]
        x2 = total_points[second_id][0]
        y2 = total_points[second_id][1]
        x3 = total_points[third_id][0]
        y3 = total_points[third_id][1]
        arr = [x1,y1,x2,y2,x3,y3]
        secondary_triangles.append(arr)
    return np.array(secondary_triangles)

