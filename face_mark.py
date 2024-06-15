import cv2
import numpy as np
import json
import os

img = cv2.imread('face.png')

height, width, channels = img.shape

with open('face_data.json', 'r') as f:
    face_data = json.load(f)

pupil_mark_left = face_data["pupil_mark_left"]
pupil_mark_right = face_data["pupil_mark_right"]
pupil_mark_large_left = face_data["pupil_mark_large_left"]
pupil_mark_large_right = face_data["pupil_mark_large_right"]


for i in range (0, len(pupil_mark_left)):
    pupil_mark_left[i][0] = round(pupil_mark_left[i][0])
    pupil_mark_left[i][1] = height - round(pupil_mark_left[i][1])
    
for i in range (0, len(pupil_mark_right)):
    pupil_mark_right[i][0] = round(pupil_mark_right[i][0])
    pupil_mark_right[i][1] = height - round(pupil_mark_right[i][1])
    
for i in range (0, len(pupil_mark_large_left)):
    pupil_mark_large_left[i][0] = round(pupil_mark_large_left[i][0])
    pupil_mark_large_left[i][1] = height - round(pupil_mark_large_left[i][1])
    
for i in range (0, len(pupil_mark_large_right)):
    pupil_mark_large_right[i][0] = round(pupil_mark_large_right[i][0])
    pupil_mark_large_right[i][1] = height - round(pupil_mark_large_right[i][1])

points_np = np.array(pupil_mark_left, dtype=np.int32)
ellipse = cv2.fitEllipse(points_np)
cv2.ellipse(img, ellipse, (255, 0, 0), 2)

points_np = np.array(pupil_mark_right, dtype=np.int32)
ellipse = cv2.fitEllipse(points_np)
cv2.ellipse(img, ellipse, (255, 0, 0), 2)

points_np = np.array(pupil_mark_large_left, dtype=np.int32)
ellipse = cv2.fitEllipse(points_np)
cv2.ellipse(img, ellipse, (0, 255, 0), 2)

points_np = np.array(pupil_mark_large_right, dtype=np.int32)
ellipse = cv2.fitEllipse(points_np)
cv2.ellipse(img, ellipse, (0, 255, 0), 2)

cv2.circle(img, (round(face_data["pupil_center_left"][0]), height - round(face_data["pupil_center_left"][1])), 1, (0, 0, 255), -1)
cv2.circle(img, (round(face_data["pupil_center_right"][0]), height - round(face_data["pupil_center_right"][1])), 1, (0, 0, 255), -1)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, f'eyeball radius: {face_data["pupil_radis"] / 2 * 100} cm', (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('output.jpg', img)