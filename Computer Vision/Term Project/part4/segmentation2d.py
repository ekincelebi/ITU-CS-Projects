import cv2
import numpy as np
import math
import sys
import nibabel as nib

sys.setrecursionlimit(10 ** 7)

#read seed points
def read_seeds(path):
    array = []

    with open(path) as f:
        for line in f:  # read rest of lines
            array.append([int(x) for x in line.split()])

    return array

def segmentation(result):
    # Ground Truth
    gt = nib.load("V_seg.nii")
    gt_data = gt.get_fdata()

    return dice_score(result,gt_data)

def dice_score(seg, gt):
    return 2 * np.count_nonzero(np.logical_and(seg, gt)) / (np.count_nonzero(seg) + np.count_nonzero(gt))

def four_neigbourhood(max_row, max_col, x_in, y_in):
    neighbors = lambda x, y : [[x2, y2] for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x < max_row and
                                   -1 < y < max_col and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 < max_row) and
                                   (abs((x2+y2)-(x+y)) == 1 ) and
                                   (0 <= y2 < max_col))]
    return neighbors(x_in, y_in)

def eight_neigbourhood(max_row, max_col, x_in, y_in):
    neighbors = lambda x, y : [[x2, y2] for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x < max_row and
                                   -1 < y < max_col and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 < max_row) and
                                   (0 <= y2 < max_col))]
    return neighbors(x_in, y_in)


def six_neighbourhood(max_row, max_col, max_depth, x_in, y_in, z_in):
    neighbors = lambda x, y, z: [[x2, y2, z] for x2 in range(x - 1, x + 2)
                                 for y2 in range(y - 1, y + 2)
                                 if (-1 < x < max_row and
                                     -1 < y < max_col and
                                     (x != x2 or y != y2) and
                                     (0 <= x2 < max_row) and
                                     (abs((x2 + y2) - (x + y)) == 1) and
                                     (0 <= y2 < max_col))]

    z_neighbors = lambda x, y, z: [[x, y, z2]
                                   for z2 in range(z - 1, z + 2)
                                   if (-1 < z < max_depth and
                                       z != z2 and
                                       (0 <= z2 < max_depth))]

    x_y = neighbors(x_in, y_in, z_in)
    z = z_neighbors(x_in, y_in, z_in)
    res = np.concatenate((x_y, z), axis=0)
    return res


def twentysix_neighbourhood(max_row, max_col, max_depth, x_in, y_in, z_in):
    neighbors = lambda x, y, z: [[x2, y2, z2] for x2 in range(x - 1, x + 2)
                                 for y2 in range(y - 1, y + 2)
                                 for z2 in range(z - 1, z + 2)
                                 if (-1 < x < max_row and
                                     -1 < y < max_col and
                                     -1 < z < max_depth and
                                     (x != x2 or y != y2 or z != z2) and
                                     (0 <= x2 < max_row) and
                                     (0 <= z2 < max_depth) and
                                     (0 <= y2 < max_col))]

    return neighbors(x_in, y_in, z_in)


def four_region_growing(image, image_copy, seed):
    x, y = seed[0], seed[1]
    image_copy[x, y] = 1  # mark first seed
    values = four_neigbourhood(image.shape[0], image.shape[1], x, y)
    for point in values:
        n_x, n_y = point
        if image_copy[n_x, n_y] != 1:
            result = np.abs(image[x, y] - image[n_x, n_y]) / image[x, y] if image[x, y] != 0 else 0
            if result < 0.3:
                image_copy[n_x, n_y] = 1
                four_region_growing(image, image_copy, [n_x, n_y])

def eight_region_growing(image, image_copy, seed):
    x, y = seed[0], seed[1]
    image_copy[x, y] = 1  # mark first seed
    values = eight_neigbourhood(image.shape[0], image.shape[1], x, y)
    for point in values:
        n_x, n_y = point
        if image_copy[n_x, n_y] != 1:
            result = np.abs(image[x, y] - image[n_x, n_y]) / image[x, y] if image[x, y] != 0 else 0
            if result < 0.3:
                image_copy[n_x, n_y] = 1
                eight_region_growing(image, image_copy, [n_x, n_y])


# load image
epi_img = nib.load('V.nii')
image = epi_img.get_fdata()

seeds = [[100, 20, 46], [80, 40, 47], [20, 20, 48], [130, 20, 49], [150, 0, 50], [50, 30, 50], [170, 70, 51], [0, 20, 51], [100, 20, 52], [80, 40, 52]]

dst = np.full(image.shape, 0)
for index, seed in enumerate(seeds):
    x, y, z = seeds[index] #gets x, y, z values from seeds by index
    copy_img_layer = dst[:, :, z] #this is a array of zeros same shape of img_layer
    img_slice = image[:, :, z] #this is the zth slice of the img data
    seed = [x, y] #this is the seed that we obtain from the file
    four_region_growing(img_slice, copy_img_layer,seed) #recursively apply growing region algorithm

nib.save(nib.Nifti1Image(dst, affine=None), 'seg_4_3d.nii')
print("4N: ", segmentation(dst))

dst = np.full(image.shape, 0)

for index, seed in enumerate(seeds):
    x, y, z = seeds[index] #gets x, y, z values from seeds by index
    copy_img_layer = dst[:, :, z] #this is a array of zeros same shape of img_layer
    img_slice = image[:, :, z] #this is the zth slice of the img data
    seed = [x, y] #this is the seed that we obtain from the file
    eight_region_growing(img_slice, copy_img_layer,seed) #recursively apply growing region algorithm

nib.save(nib.Nifti1Image(dst, affine=None), 'seg_8_3d.nii')
print("8N: ", segmentation(dst))




