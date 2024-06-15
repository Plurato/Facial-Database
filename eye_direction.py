import cv2
import json
import numpy as np
import math
import os

# 弧度转换
def degrees_to_radians(degrees):
    return degrees * math.pi / 180.0

# 打开视频文件
cap = cv2.VideoCapture('video.mp4')

# 获取视频属性
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

# 加载JSON文件
with open('frames.json', 'r') as f:
    axis_data = json.load(f)

# 箭头长度和颜色
arrow_length = 70
arrow_red = (0, 0, 255)  # 红色
arrow_blue = (255, 0, 0)

# 遍历每一帧
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 获取当前帧的箭头信息
    try:
        arrow_info = axis_data[frame_count]
    except:
        break
    start_point_left = (round(arrow_info['eye_pos_left'][0]), height - round(arrow_info['eye_pos_left'][1]))
    start_point_right = (round(arrow_info['eye_pos_right'][0]), height - round(arrow_info['eye_pos_right'][1]))
    pitch = arrow_info['eye_pitch']
    roll = arrow_info['eye_yaw']

    # 转换为弧度制
    pitch_rad = degrees_to_radians(pitch)
    roll_rad = degrees_to_radians(roll)

    # 计算箭头方向向量
    direction_vector = np.array([
        np.sin(roll_rad),
        -np.sin(pitch_rad),
        np.sin(pitch_rad) * np.cos(roll_rad)
    ])

    # 计算箭头末端坐标
    end_point_left = (start_point_left[0] + int(direction_vector[0] * arrow_length),
             start_point_left[1] + int(direction_vector[1] * arrow_length))
    end_point_right = (start_point_right[0] + int(direction_vector[0] * arrow_length),
             start_point_right[1] + int(direction_vector[1] * arrow_length))
    
    # 绘制箭头
    cv2.arrowedLine(frame, start_point_left, end_point_left, arrow_red, 2)
    cv2.arrowedLine(frame, start_point_right, end_point_right, arrow_blue, 2)
    # 写入输出视频
    out.write(frame)
    print(f"frame {frame_count} finished!")
    frame_count += 1

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
os.remove('video.mp4')
os.rename('output_video.mp4', 'video.mp4')