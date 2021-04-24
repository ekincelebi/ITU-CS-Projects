#Ekin Çelebi 150160152
#Part 1: Dancing alone
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
        new_frame = new_frame[:, :, [2, 1, 0]]  # reverse channels for moviepy
        listToAppend.append(new_frame)

#read images
background = cv2.imread('Malibu.jpg')

#resize background
background_height = background.shape[0]
background_width = background.shape[1]
ratio = 360/background_height
background = cv2.resize(background, (int(background_width*ratio), 360))

#load cat images from the folder
cat_images = load_images_from_folder("./cat")

images_list = []  #holds images left cat + background
loop_in_images(cat_images, background, images_list)



clip = mpy.ImageSequenceClip(images_list, fps = 10)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip=audio)
clip.write_videofile('first.mp4', codec='libx264')



'''item = cat_images[1]

image_g_channel = item[:, :, 1]
image_r_channel = item[:, :, 0]
foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)  # supress green parts
nonzero_x, nonzero_y = np.nonzero(foreground)
nonzero_cat_values = item[nonzero_x, nonzero_y, :]  # matrix containing the cat part

#acat = nonzero_cat_values.astype(np.uint8)
cv2.imshow("cat.jpg",nonzero_cat_values )
cv2.waitKey(0)'''

