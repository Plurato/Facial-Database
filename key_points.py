import cv2
import json
import os
import numpy as np

# 打开视频文件
cap = cv2.VideoCapture('video.mp4')

# 获取视频属性
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

body_list = [(1, 0), (0, 2), (2, 3), (3, 4), (4, 7), (2, 5), (5, 6), (6, 8), (2, 9), (2, 11)]

# 加载JSON文件
with open('frames.json', 'r') as f:
    blink_data = json.load(f)
    
# 遍历每一帧
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    try:
        coordinates = blink_data[frame_count]['face_vertices']
        coordinates_body = blink_data[frame_count]["body_mark"]
        coordinates_pupil_left = blink_data[frame_count]["pupil_mark_left"]
        coordinates_pupil_right = blink_data[frame_count]["pupil_mark_right"]
    except:
        break
    
    print(frame_count)
    # 添加文字
    for coord in coordinates:
        x, y = round(coord[0]), round(coord[1])
        cv2.circle(frame, (x, height - y), 1, (0, 0, 255), -1)
    for coord in coordinates_body:
        x, y = round(coord[0]), round(coord[1])
        cv2.circle(frame, (x, height - y), 5, (0, 255, 0), -1)
        
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # for i in range(0, len(coordinates_body)):
    #     x, y = round(coordinates_body[i][0]), round(coordinates_body[i][1])
    #     cv2.putText(frame, str(i), (x, height - y), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    # cv2.line(frame, (round(coordinates_body[3][0]), height - round(coordinates_body[3][1])), (round(coordinates_body[2][0]), height - round(coordinates_body[2][1])), (0, 255, 0), 5)
    
    for line in body_list:
        x1, y1 = round(coordinates_body[line[0]][0]), height - round(coordinates_body[line[0]][1])
        x2, y2 = round(coordinates_body[line[1]][0]), height - round(coordinates_body[line[1]][1])
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    for i in range (0, len(coordinates_pupil_left)):
        coordinates_pupil_left[i][0] = round(coordinates_pupil_left[i][0])
        coordinates_pupil_left[i][1] = height - round(coordinates_pupil_left[i][1])
    
    for i in range (0, len(coordinates_pupil_right)):
        coordinates_pupil_right[i][0] = round(coordinates_pupil_right[i][0])
        coordinates_pupil_right[i][1] = height - round(coordinates_pupil_right[i][1])
    
    points_np = np.array(coordinates_pupil_left, dtype=np.int32)
    ellipse = cv2.fitEllipse(points_np)
    cv2.ellipse(frame, ellipse, (255, 0, 0), 1)
    points_np = np.array(coordinates_pupil_right, dtype=np.int32)
    ellipse = cv2.fitEllipse(points_np)
    cv2.ellipse(frame, ellipse, (255, 0, 0), 1)
    out.write(frame)
    
    frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()
os.remove('video.mp4')
os.rename('output_video.mp4', 'video.mp4')