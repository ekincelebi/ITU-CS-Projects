import moviepy.video.io.VideoFileClip as mpy
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import cv2
import numpy as np
import math


def make_video(images, output="part2.mp4"):
    clip = ImageSequenceClip(images, 10)
    clip.write_videofile(output)

#get a suitable position for the hand
def get_hand_position(frame_no):
    biped_hand = mpy.VideoFileClip("biped_2.avi")
    handframe = biped_hand.get_frame(i * 1.0 / videofps)
    original = handframe.copy()
    hsv = cv2.cvtColor(handframe, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.fillPoly(mask, cnts, (255, 255, 255))
    handframe = mask[300:380, 0:handframe.shape[1]]
    handframe = (handframe != 0)
    seg_coords = np.argwhere(handframe == 1)
    mean_x = np.floor(seg_coords[:,0].mean()).astype(int)
    mean_y = np.floor(seg_coords[:,1].mean()).astype(int)
    point = (mean_y, mean_x+300)
    return point

def corner_points(frame_no):
    biped = mpy.VideoFileClip("biped_2.avi")
    frame_current = biped.get_frame(i * 1.0 / videofps)
    gray = cv2.cvtColor(frame_current, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 5, 3, 0.04)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
    #filename = str(i) + '.jpg'
    result = []
    for j in range(1, len(corners)):
        if corners[j][0] >= 218 and corners[j][0] < 283 and corners[j][1] > 188 and corners[j][1] < 308:
            tuple = (math.floor(corners[j][0]) , math.floor(corners[j][1]))
            result.append(tuple)
    return result

def motion_calculator(position, window_min, window_max, bipedframe_original,i):
    results = []
    kernel_window_size = (10, 10)

    # read current frame
    bipedframe_now = biped.get_frame(i * 1.0 / videofps)  # To get frames by ID
    bipedframe_now = bipedframe_now[window_min[1]:window_max[1], window_min[0]:window_max[0], :]
    bipedframe_now = cv2.GaussianBlur(bipedframe_now, (5, 5), 0)
    bipedframe_now = cv2.cvtColor(bipedframe_now, cv2.COLOR_BGR2GRAY)

    # read next frame
    bipedframe_next = biped.get_frame((i + 1) * 1.0 / videofps)  # To get frames by ID
    bipedframe_next = bipedframe_next[window_min[1]:window_max[1], window_min[0]:window_max[0], :]
    bipedframe_next = cv2.GaussianBlur(bipedframe_next, (5, 5), 0)
    bipedframe_next = cv2.cvtColor(bipedframe_next, cv2.COLOR_BGR2GRAY)

    kernel_for_x = np.array([[-1, 1], [-1, 1]]) / 4
    kernel_for_y = np.array([[-1, -1], [1, 1]]) / 4

    # apply derivative kernels
    Ix_now = cv2.filter2D(bipedframe_now, -1, kernel_for_x)
    Ix_now += cv2.filter2D(bipedframe_now, -1, -1 * kernel_for_x)
    Iy_now = cv2.filter2D(bipedframe_now, -1, kernel_for_y)
    Iy_now += cv2.filter2D(bipedframe_now, -1, -1 * kernel_for_y)

    Ix_next = cv2.filter2D(bipedframe_next, -1, kernel_for_x)
    Ix_next += cv2.filter2D(bipedframe_next, -1, -1 * kernel_for_x)
    Iy_next = cv2.filter2D(bipedframe_next, -1, kernel_for_y)
    Iy_next += cv2.filter2D(bipedframe_next, -1, -1 * kernel_for_y)

    # derivatives
    Ix = (Ix_now + Ix_next)
    Iy = (Iy_now + Iy_next)
    It = cv2.filter2D(bipedframe_next, -1, np.array([[1, 1], [1, 1]])) / 4 + cv2.filter2D(bipedframe_now, -1,
                                                                                           np.array([[-1, -1], [-1,
                                                                                                                -1]])) / 4

    # loop through a local window
    for x in range(math.floor(kernel_window_size[0] / 2),
                   bipedframe_now.shape[0] - math.floor(kernel_window_size[0] / 2)):
        for y in range(math.floor(kernel_window_size[1] / 2),
                       bipedframe_now.shape[1] - math.floor(kernel_window_size[1] / 2)):

            aTa = np.zeros((2, 2))
            aTb = np.zeros((2, 1))

            # loop in a smaller window
            for in_x in range(x - math.floor(kernel_window_size[0] / 2), x + math.floor(kernel_window_size[0] / 2)):
                for in_y in range(y - math.floor(kernel_window_size[1] / 2),
                                  y + math.floor(kernel_window_size[1] / 2)):
                    if in_y >= bipedframe_now.shape[0] or in_x >= bipedframe_now.shape[1]:
                        continue

                    IxIx = Ix[in_x, in_y] * Ix[in_x, in_y]
                    IxIy = Ix[in_x, in_y] * Iy[in_x, in_y]
                    IyIy = Iy[in_x, in_y] * Iy[in_x, in_y]

                    IxIt = Ix[in_x, in_y] * It[in_x, in_y]
                    IyIt = Iy[in_x, in_y] * It[in_x, in_y]

                    aTa[0, 0] += IxIx
                    aTa[0, 1] += IxIy
                    aTa[1, 0] += IxIy
                    aTa[1, 1] += IyIy

                    aTb[0, 0] += IxIt
                    aTb[1, 0] += IyIt

            # aTa . uv = aTb
            aTa_inv = np.linalg.pinv(aTa)
            uv = -1 * np.dot(aTa_inv, aTb)

            uv_vector = (uv[0, 0], uv[1, 0])

            dist = np.linalg.norm(uv_vector)
            results.append(uv)

    # find average motion vector
    results = np.array(results)
    avg = (np.average(results, axis=0)).astype(int)

    # draw vector on original frame
    bipedframe_original = cv2.arrowedLine(bipedframe_original, position, (position[0] - math.floor(avg[1, 0]),position[1] - math.floor(avg[0, 0])), (255, 0, 0), 4)

    return bipedframe_original

if __name__ == "__main__":

    biped = mpy.VideoFileClip("biped_2.avi")
    framecount = biped.reader.nframes
    videofps = biped.fps


    hand_min = (370, 310)  # hand loacl window
    hand_max = (420, 340)


    tl_min = (218, 188)  # top_left local window
    tl_max = (253, 250)

    tr_min = (253, 188)  # top right local window
    tr_max = (283, 250)


    bl_min = (218, 250)  # bottom left local window
    bl_max = (253, 308)

    br_min = (253, 259)  # bottom right local window
    br_max = (283, 308)

    #kernel_window_size = (10, 10)

    result_images = []

    for i in range(0, framecount - 1):
        results = []  # vector results of each pixel will be stored

        bipedframe_original = biped.get_frame(i * 1.0 / videofps)  # original frame for drawing arrow.

        hand_pos = get_hand_position(i)
        corn = corner_points(i)
        corn1 = corner_points(i)[0] #solüst
        corn2 = corner_points(i)[1] #sağüst
        corn3 = corner_points(i)[2] #solalt
        corn4 = corner_points(i)[3] #sağalt

        print("calculating motion")

        first = motion_calculator(corn1, tl_min, tl_max, bipedframe_original, i)
        second = motion_calculator(corn2, tr_min, tr_max, first,i)
        third = motion_calculator(corn3, bl_min, bl_max, second,i)
        fourth = motion_calculator(corn4, br_min, br_max, third,i)
        fifth = motion_calculator(hand_pos,hand_min, hand_max, fourth, i)
        result_images.append(fifth)

    make_video(result_images)
