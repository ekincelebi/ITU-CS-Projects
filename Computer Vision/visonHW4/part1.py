import moviepy.video.io.VideoFileClip as mpy
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import cv2
import numpy as np
import math


def make_video(images, output="part1.mp4"):
    clip = ImageSequenceClip(images, fps=10)
    clip.write_videofile(output)


def get_hand_position(frame_no):
    biped_hand = mpy.VideoFileClip("biped_1.avi")
    handframe = biped_hand.get_frame(i * 1.0 / videofps)
    original = handframe.copy()
    lower = np.array([0, 200, 0], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")
    mask = cv2.inRange(handframe, lower, upper)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.fillPoly(mask, cnts, (255, 255, 255))
    handframe = mask[0:380, 0:handframe.shape[1]]
    handframe = (handframe != 0)
    seg_coords = np.argwhere(handframe == 1)
    min_x = np.min(seg_coords[:, 0])
    min_y = np.min(seg_coords[:, 1])
    min_point = (min_y, min_x)
    max_x = np.max(seg_coords[:, 0])
    max_y = np.max(seg_coords[:, 1])
    max_point = (max_y, max_x)

    sum_point = (min_point[0] + max_point[0], min_point[1] + max_point[1])
    sum_point = (math.floor(sum_point[0] / 2), math.floor(sum_point[1] / 2))
    return sum_point

if __name__ == "__main__":

    biped = mpy.VideoFileClip("biped_1.avi")
    framecount = biped.reader.nframes
    videofps = biped.fps

    window_min = (370, 320)
    window_max = (420, 340)

    kernel_window_size = (5, 5)

    result_images = []

    for i in range(0, framecount - 1):
        results = []

        bipedframe_original = biped.get_frame(i * 1.0 / videofps)  # original to draw arrow.

        # read current frame
        bipedframe_now = biped.get_frame(i * 1.0 / videofps)
        bipedframe_now = bipedframe_now[window_min[1]:window_max[1], window_min[0]:window_max[0], :]
        bipedframe_now = cv2.GaussianBlur(bipedframe_now, (5, 5), 0)
        bipedframe_now = cv2.cvtColor(bipedframe_now, cv2.COLOR_BGR2GRAY)

        # read next frame
        bipedframe_next = biped.get_frame((i + 1) * 1.0 / videofps)
        bipedframe_next = bipedframe_next[window_min[1]:window_max[1], window_min[0]:window_max[0], :]
        bipedframe_next = cv2.GaussianBlur(bipedframe_next, (5, 5), 0)
        bipedframe_next = cv2.cvtColor(bipedframe_next, cv2.COLOR_BGR2GRAY)

        # create derivative kernels
        frame_current = biped.get_frame(i * 1.0 / videofps)
        frame_current = cv2.GaussianBlur(frame_current, (5, 5), 0)

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
        It = cv2.filter2D(bipedframe_next, -1, np.array([[1, 1], [1, 1]])) / 4 + cv2.filter2D(bipedframe_now, -1,np.array([[-1, -1], [-1, -1]])) / 4

        hand_pos = get_hand_position(i)  # get hand's position in my case its the middle pixel of the surrounding area

        # loop through hand area otherwise it takes ages to run the code
        for x in range(math.floor(kernel_window_size[0] / 2), bipedframe_now.shape[0] - math.floor(kernel_window_size[0] / 2)):
            for y in range(math.floor(kernel_window_size[1] / 2), bipedframe_now.shape[1] - math.floor(kernel_window_size[1] / 2)):

                aTa = np.zeros((2, 2))
                aTb = np.zeros((2, 1))

                # loop in a even smaller window
                for in_x in range(x - math.floor(kernel_window_size[0] / 2), x + math.floor(kernel_window_size[0] / 2)):
                    for in_y in range(y - math.floor(kernel_window_size[1] / 2), y + math.floor(kernel_window_size[1] / 2)):
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

                #aTa . uv = aTb
                aTa_inv = np.linalg.pinv(aTa)
                uv = -1 * np.dot(aTa_inv, aTb)


                uv_vector = (uv[0, 0], uv[1, 0])

                dist = np.linalg.norm(uv_vector)
                results.append(uv)

        #find average motion vector
        results = np.array(results)
        avg = (np.average(results, axis=0)*10).astype(int)

        # draw that vector onto the original image
        bipedframe_original = cv2.arrowedLine(bipedframe_original, hand_pos, (
        hand_pos[0] - math.floor(avg[1, 0]), hand_pos[1] - math.floor(avg[0, 0])), (255, 0, 0), 4)
        result_images.append(bipedframe_original)
    #make_video(result_images)
    clip = ImageSequenceClip(result_images, fps=10)
    clip.write_videofile("part1.mp4")
