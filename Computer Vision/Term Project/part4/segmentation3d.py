import numpy as np
import nibabel as nib
import sys
import segmentation2d
sys.setrecursionlimit(10**6)


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

    return segmentation2d.dice_score(result, gt_data)


def twentysix_neighbours_region_growing(point,image_copy):
    image_copy[point[0], point[1], point[2]] = 1
    #neighbours
    values = segmentation2d.twentysix_neighbourhood(image.shape[0], image.shape[1], image.shape[2], point[0], point[1], point[2])
    for item in values:
        n_x, n_y, n_z = item
        if image_copy[n_x][n_y][n_z] == -1 and abs(
                image[point[0], point[1], point[2]] - image[n_x, n_y,n_z]) / image[
            point[0], point[1], point[2]] < 0.085:
            image_copy[n_x, n_y, n_z] = 1
            twentysix_neighbours_region_growing(item,image_copy)


def six_neighbours_region_growing(point,image_copy):
    image_copy[point[0]][point[1]][point[2]] = 1
    #neighbours
    values = segmentation2d.six_neighbourhood(image.shape[0], image.shape[1], image.shape[2], point[0], point[1], point[2])
    for item in values:
        n_x, n_y, n_z = item
        if image_copy[n_x][n_y][n_z] == -1 and abs(
                image[point[0], point[1], point[2]] - image[n_x, n_y,n_z]) / image[point[0], point[1], point[2]] < 0.085:
            image_copy[n_x, n_y, n_z] = 1
            six_neighbours_region_growing(item,image_copy)



# load image
epi_img = nib.load('V.nii')
image = epi_img.get_fdata()

copy = np.full(image.shape, -1)
copy[:, :, 0:40] = 0
copy[:, :, 60:100] = 0

seeds = [[0, 20, 51], [130, 20, 49], [150, 0, 50], [50, 30, 50], [82, 25, 48]]
for seed in seeds:
    six_neighbours_region_growing(seed,copy)
copy[copy == -1] = 0 #restore
nib.save(nib.Nifti1Image(copy, affine=None), 'seg_6_3d.nii')
print("6N: ", segmentation(copy))

copy[:, :, 42:56] = -1
for seed in seeds:
    twentysix_neighbours_region_growing(seed,copy)
copy[copy == -1] = 0 #restore
nib.save(nib.Nifti1Image(copy, affine=None), 'seg_26_3d.nii')
print("26N: ", segmentation(copy))










