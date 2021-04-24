import triangles
import numpy as np
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import cv2


#(C)Each triangle consist of x1, y1, x2,y2, x3,y3 values.
# The function creates rows for x and y values and adds a bottom row with ones to create a 3x3 square matrix.
def make_homogeneous(triangle):
    homogeneous = np.array([triangle[::2],
                           triangle[1::2],
                            [1,1,1]])

    return homogeneous

def calc_transform(triangle1,triangle2):
    source = make_homogeneous(triangle1).T
    target = triangle2
    Mtx = np.array([np.concatenate((source[0], np.zeros(3))),
                    np.concatenate((np.zeros(3), source[0])),
                    np.concatenate((source[1], np.zeros(3))),
                    np.concatenate((np.zeros(3), source[1])),
                    np.concatenate((source[2], np.zeros(3))),
                    np.concatenate((np.zeros(3), source[2]))])
    #D the set of suitable control points are determined
    coefs = np.matmul(np.linalg.pinv(Mtx), target)
    #(E) from the control points transform paramaters are determined


    Transform = np.array([coefs[:3], coefs[3:], [0,0,1]], dtype=float)
    #(F) creates a 3x3 transformation matrix from the coefficients
    return Transform

def vectorised_Bilinear(coordinates, target_img, size):
    #We want to find a weighted average of the intensity values of the 4 neighboring points to copy the
    #intensities to the target image.
    coordinates[0] = np.clip(coordinates[0], 0, size[0]-1)
    coordinates[1] = np.clip(coordinates[1], 0, size[1]-1)
    lower = np.floor(coordinates).astype(np.uint32)
    upper = np.ceil(coordinates).astype(np.uint32)

    error = coordinates - lower
    resindual = 1 - error

    top_left = np.multiply(np.multiply(resindual[0],resindual[1]).reshape(coordinates.shape[1],1),
                           target_img[lower[0],lower[1],:])
    top_right = np.multiply(np.multiply(resindual[0], error[1]).reshape(coordinates.shape[1], 1),
                           target_img[lower[0], upper[1], :])

    bot_left = np.multiply(np.multiply(error[0], resindual[1]).reshape(coordinates.shape[1], 1),
                            target_img[upper[0], lower[1], :])

    bot_right = np.multiply(np.multiply(error[0], error[1]).reshape(coordinates.shape[1], 1),
                            target_img[upper[0], upper[1], :])
    #(G) Here calculates the weights of the 4 corners.

    #(H) the weighted average is returned
    return np.uint8(np.round(top_left+top_right+bot_left+bot_right))




def image_morph(image1,image2,triangles1,triangles2,transforms,t):
    inter_image_1 = np.zeros(image1.shape).astype(np.uint8)
    inter_image_2 = np.zeros(image2.shape).astype(np.uint8)

    #there are 142 triangles therefore we loop over 142 times
    #this step individually morphes each triangle
    for i in range(len(transforms)):
        homo_inter_tri = (1-t)*make_homogeneous(triangles1[i]) + t*make_homogeneous(triangles2[i])
        #(I) The loop iterates over all triangles of the both images.
        # This step takes the weighted average of the triangles of the same index

        polygon_mask = np.zeros(image1.shape[:2], dtype=np.uint8)
        arr = [np.int32(np.round(homo_inter_tri[1::-1,:].T))]
        cv2.fillPoly(polygon_mask, arr, color=255)
        #(J) A mask of the given image shape is created.
        # The corner points of the homo_inter_triangle creates a triangle.
        #The cells that fall inside the triangular area are assigned a value of 255.

        seg = np.where(polygon_mask == 255)

        mask_points = np.vstack((seg[0],seg[1],np.ones(len(seg[0]))))
        #(L) seg is the tuple that holds xy values of the triangular masked area
        # At this step the tuple another row of ones. Briefly the masked triangular area form a matrice.
        inter_tri = homo_inter_tri[:2].flatten(order="F")
        #homo_inter_tri matrix is vectorized and takes the form of (x1,y1,x2,y2,x3,y3)



        inter_to_img1 = calc_transform(inter_tri, triangles1[i])
        inter_to_img2 = calc_transform(inter_tri, triangles2[i])
        #Intermediate mapping functions are calculated.We need this to warp images to the same intermediate location


        mapped_to_img1 = np.matmul(inter_to_img1,mask_points)[:-1]
        mapped_to_img2 = np.matmul(inter_to_img2, mask_points)[:-1]
        #(N)We need to bring our images to the same intermediate locations, that is the reason we warph the images.
        # And here we calculate our coordinate parameters for warphing.


        inter_image_1[seg[0], seg[1], :] = vectorised_Bilinear(mapped_to_img1,image1,inter_image_1.shape)
        inter_image_2[seg[0], seg[1], :] = vectorised_Bilinear(mapped_to_img2, image2, inter_image_2.shape)
        #At this point warhphing happens. We do not want double
        #image effect instead we need blended images. We are aligning our points by warphing .

    result = (1-t)*inter_image_1 + t * inter_image_2
    #(P)Take the weighted combinations of the images, with an interpolation parameter.
    #In other words, the images are blended.

    return result.astype(np.uint8)




###########video1
'''image1 = cv2.imread("./images/deniro.jpg")
image2 = cv2.imread("./images/aydemirakbas.png")

img1_triangles,tri_img1,ids1 = triangles.create_human_triangles("./images/deniro.jpg")
img2_triangles = triangles.secondary_triangles_human("./images/aydemirakbas.png", ids1)'''

###########video2
'''
image1 = cv2.imread("./images/kimbodnia.png")
image2 = cv2.imread("./images/panda.jpg")

img1_triangles,tri_img1,ids1 = triangles.create_human_triangles("./images/kimbodnia.png")
img2_triangles = triangles.secondary_triangles_animal("./images/panda.jpg","./images/panda_landmarks.npy",ids1)
'''

###########video 3
image1 = cv2.imread("./images/cat.jpg")
image2 = cv2.imread("./images/gorilla.jpg")

img1_triangles,tri_img1,ids1 = triangles.create_animal_triangles("./images/cat.jpg","./images/cat_landmarks.npy")
img2_triangles = triangles.secondary_triangles_animal("./images/gorilla.jpg","./images/gorilla_landmarks.npy",ids1)


img1_triangles = img1_triangles[:,[1,0,3,2,5,4]]
img2_triangles = img2_triangles[:,[1,0,3,2,5,4]]


Transforms = np.zeros((len(img1_triangles),3,3), dtype=float)

for i in range(len(img1_triangles)):
    source = img1_triangles[i]
    target = img2_triangles[i]
    Transforms[i] = calc_transform(source ,target)

#(A)We have to determine the transformation between source annd target matrices,
#in order to apply the transform at every step.


morphs = []

#(B)
#The t value should be assigned so that convex combination cam be made.
#Inside the loop the by source image blends into the target image
#The function generates a smooth transition from source to target image

for t in np.arange(0, 1.0001, 0.02):
    print("processing:\t", t*100, "%")
    morphs.append(image_morph(image1, image2, img1_triangles,img2_triangles, Transforms, t)[:,:,::-1])


frames=[]
for i in range(len(morphs)):
    frames.append(morphs[i])
clip = ImageSequenceClip(frames, fps=12.0)
clip.write_videofile('video3.mp4', codec='mpeg4')







