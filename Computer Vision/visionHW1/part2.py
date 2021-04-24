#Ekin Çelebi 150160152
#Part 2: Dancing with myself
#Part 3: Dancing with my shadow
import numpy as np
from matplotlib import pyplot as plt
import os
import cv2
import moviepy.editor as mpy

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def loop_in_images(images,backgroundImage,listToAppend):
    for item in images:
        image_g_channel = item[:, :, 1]
        image_r_channel = item[:, :, 0]
        foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)  # supress green parts
        nonzero_x, nonzero_y = np.nonzero(foreground)
        nonzero_cat_values = item[nonzero_x, nonzero_y, :]  # matrix containing the cat part
        new_frame = backgroundImage.copy()
        new_frame[nonzero_x, nonzero_y, :] = nonzero_cat_values  # place cats
        listToAppend.append(new_frame)

def loop_in_images_video_background(images,backgroundList,listToAppend,offset):
    for i in range(len(images)):
        image_g_channel = images[i][:, :, 1]
        image_r_channel = images[i][:, :, 0]
        foreground = np.logical_or(image_g_channel < 180-offset, image_r_channel > 150-offset)
        nonzero_x, nonzero_y = np.nonzero(foreground)
        nonzero_cat_values = images[i][nonzero_x, nonzero_y, :]  # matrix containing the cat part
        new_frame = backgroundList[i].copy()
        new_frame[nonzero_x, nonzero_y, :] = nonzero_cat_values  # place cats
        new_frame = new_frame[:, :, [2, 1, 0]]  # reverse channels for moviepy
        listToAppend.append(new_frame)

#read images
background = cv2.imread('Malibu.jpg')
exampleCat = cv2.imread("./cat/cat_0.png")

#resize background
background_height = background.shape[0]
background_width = background.shape[1]
ratio = 360/background_height
background = cv2.resize(background, (int(background_width*ratio), 360))

#load cat images from the folder
cat_images = load_images_from_folder("./cat")

# create new image of desired size and color (green) for padding
ww = background.shape[1]-exampleCat.shape[1] #padding must be the size of empty parts
hh = exampleCat.shape[0]
color = (15, 235, 16) #exact green color matches with the cat
result = np.full((hh,ww,3), color, dtype=np.uint8)


flipped_cats = [] #cat images as their mirrored selves
for cat in cat_images:
    flipped = cv2.flip(cat, 1)
    padded_img = cv2.hconcat([result, flipped])
    flipped_cats.append(padded_img)
#flipping the cat images and padding them to meet the left border of thge background image

images_list = []  #holds images left cat + background
loop_in_images(cat_images, background, images_list)

double_images_list = [] #holds images of images_list+right cat
loop_in_images_video_background(flipped_cats,images_list,double_images_list,0)

clip = mpy.ImageSequenceClip(double_images_list, fps = 10)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip=audio)
clip.write_videofile('second.mp4', codec='libx264')


#third part implementation
dark_cats = []
dark_images_list = []


intensity = np.ones(flipped_cats[1].shape, dtype="uint8") * 150
for cat in flipped_cats:
    dark_cat = cv2.subtract(cat,intensity) #subtracts a constant value from each pixels of the color channels
    dark_cats.append(dark_cat)

loop_in_images_video_background(dark_cats,images_list,dark_images_list,150)

clip = mpy.ImageSequenceClip(dark_images_list, fps = 10)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip=audio)
clip.write_videofile('third.mp4', codec='libx264')