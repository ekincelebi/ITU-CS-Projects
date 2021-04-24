import cv2
import numpy as np
import landmarks
import landmarks_anim
import triangles
####shows the results of part 1 and 2

landmark_imgs = []
landmark_imgs.append(landmarks.circle_image("./images/deniro.jpg"))
landmark_imgs.append(landmarks.circle_image("./images/aydemirakbas.png"))
landmark_imgs.append(landmarks.circle_image("./images/kimbodnia.png"))

landmark_imgs.append(landmarks_anim.circle_image("./images/panda.jpg","./images/panda_landmarks.npy"))
landmark_imgs.append(landmarks_anim.circle_image("./images/cat.jpg","./images/cat_landmarks.npy"))
landmark_imgs.append(landmarks_anim.circle_image("./images/gorilla.jpg","./images/gorilla_landmarks.npy"))



humans = np.concatenate(landmark_imgs[:3], axis=1)
animals = np.concatenate(landmark_imgs[3:6], axis=1)

final_landmarks = cv2.vconcat([animals, humans])
cv2.imwrite('part1.jpg', final_landmarks)

triangle_imgs = []
triangles_deniro,tri_img_deniro,id_deniro = triangles.create_human_triangles("./images/deniro.jpg")
triangle_imgs.append(tri_img_deniro)
triangles_aydemir,tri_img_aydemir,id_aydemir = triangles.create_human_triangles("./images/aydemirakbas.png")
triangle_imgs.append(tri_img_aydemir)
triangles_kimbodnia,tri_img_kimbodnia,ids_kimbodnia = triangles.create_human_triangles("./images/kimbodnia.png")
triangle_imgs.append(tri_img_kimbodnia)

triangles_panda,tri_img_panda,id_panda = triangles.create_animal_triangles("./images/panda.jpg","./images/panda_landmarks.npy")
triangle_imgs.append(tri_img_panda)
triangles_cat,tri_img_cat,id_cat = triangles.create_animal_triangles("./images/cat.jpg","./images/cat_landmarks.npy")
triangle_imgs.append(tri_img_cat)
triangles_gorilla,tri_img_gorilla,ids_gorilla = triangles.create_animal_triangles("./images/gorilla.jpg","./images/gorilla_landmarks.npy")
triangle_imgs.append(tri_img_gorilla)

human_triangles = np.concatenate(triangle_imgs[:3], axis=1)
animal_triangles = np.concatenate(triangle_imgs[3:6], axis=1)

final_triangles = cv2.vconcat([human_triangles, animal_triangles])
cv2.imwrite('part2.jpg', final_triangles)



