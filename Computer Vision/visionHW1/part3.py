#Ekin Çelebi 150160152
#Part 3: Dancing with my friend
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

def get_histogram(image):
    histogram = []

    for ch in range(3):
        histogram.append([0] * 256)
        for i in range(256):
            histogram[ch][i] = (image[:, :, ch] == i).sum()
    return histogram

def foreground_histogram(image):
    image_g_channel = image[:, :, 1]
    image_r_channel = image[:, :, 0]
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)  # supress green parts
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image[nonzero_x, nonzero_y, :]  # matrix containing the cat part


    histogram = []

    for ch in range(3):
        histogram.append([0] * 256)
        for i in range(256):
            histogram[ch][i] = (nonzero_cat_values[:,ch] == i).sum()


    return histogram

def average_histogram(images):
    #finds average histograms of the foreground cats
    image_histograms = []
    for i in range(len(images)):
        hist = foreground_histogram(images[i])
        #hist = get_histogram(images[i])
        image_histograms.append(hist)
    histogram_average = np.average(image_histograms, axis=0)
    return histogram_average

def cdf(histogram):
    #create cdf for 3 channels
    cdf = []
    for channel_histogram in histogram:
        cumsum = np.cumsum(channel_histogram)
        cdf.append(cumsum / cumsum.max())
    return cdf

def lut(cdfImg, cdfTarget):
    luts = []
    for ch, cdf in enumerate(cdfImg):
        lut = [0] * 256
        for i, value in enumerate(cdf):
            lut[i] = np.argmax(cdfTarget[ch] >= value)
        luts.append(lut)
    return luts

def apply_lut(image, lut):
    image_copy = np.copy(image)
    b_copy = np.copy(image_copy[:, :, 0])
    g_copy = np.copy(image_copy[:, :, 1])
    r_copy = np.copy(image_copy[:, :, 2])
    for i in range(256):
        b_copy[image_copy[:, :, 0] == i] = lut[0][i]
        g_copy[image_copy[:, :, 1] == i] = lut[1][i]
        r_copy[image_copy[:, :, 2] == i] = lut[2][i]
    image_copy[:, :, 0] = b_copy
    image_copy[:, :, 1] = g_copy
    image_copy[:, :, 2] = r_copy

    return image_copy

def histogram_matching(histogramTarget,histogramSrc,image):
    '''source is the image to be changed
    target is the image that its properties are taken
    image is the source image'''
    cdfSrc = cdf(histogramSrc)
    cdfTarget = cdf(histogramTarget)
    luts = lut(cdfSrc, cdfTarget)
    copy = apply_lut(image, luts).astype(np.uint8)
    return copy

def append_image(image,background):
    image_g_channel = image[:, :, 1]
    image_r_channel = image[:, :, 0]
    foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)  # supress green parts
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = image[nonzero_x, nonzero_y, :]  # matrix containing the cat part
    new_frame = background.copy()
    new_frame[nonzero_x, nonzero_y, :] = nonzero_cat_values  # place cats
    return new_frame

def loop_in_images(images,backgroundImage,listToAppend):
    for item in images:
        image_g_channel = item[:, :, 1]
        image_r_channel = item[:, :, 0]
        foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)  # supress green parts
        nonzero_x, nonzero_y = np.nonzero(foreground)
        nonzero_cat_values = item[nonzero_x, nonzero_y, :]  # matrix containing the cat part
        new_frame = backgroundImage.copy()
        new_frame[nonzero_x, nonzero_y, :] = nonzero_cat_values  # place cats
        #new_frame = new_frame[:, :, [2, 1, 0]]  # reverse channels for moviepy
        listToAppend.append(new_frame)

def loop_in_images_video_background(images,backgroundList,listToAppend):
    for i in range(len(images)):
        image_g_channel = images[i][:, :, 1]
        image_r_channel = images[i][:, :, 0]
        foreground = np.logical_or(image_g_channel < 180, image_r_channel > 150)
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



avgHists = average_histogram(cat_images) #average histograms this is the histogram that its properties are taken and applied to right cat

disco_left = []
loop_in_images(cat_images,background,disco_left)

disco_cat_right = []
#make histogram matching for per cat frame for the right cat
for flip in flipped_cats:
    #calculate each cats histogram
    flipHistogram = get_histogram(flip)
    discoRight = histogram_matching(avgHists,flipHistogram,flip)
    #disco = disco[:, :, [2, 1, 0]]
    disco_cat_right.append(discoRight)

dancing_tohether = []
loop_in_images_video_background(disco_cat_right,disco_left,dancing_tohether)
clip = mpy.ImageSequenceClip(dancing_tohether, fps = 10)
audio = mpy.AudioFileClip('selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip=audio)
clip.write_videofile('fourth.mp4', codec='libx264')





