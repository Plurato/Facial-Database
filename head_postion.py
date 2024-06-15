import cv2
import json
import numpy as np
from math import radians
import os

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

# 定义坐标轴长度和颜色
axis_length = 70
axis_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # RGB: X, Y, Z

# 遍历每一帧
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 获取当前帧的坐标轴信息
    axis_info = axis_data[frame_count]
    
    # if axis_info['head_yaw'] < -90 or axis_info['head_yaw'] > 90:
    #     out.write(frame)
    #     print(f"frame {frame_count} finished! with skip")
    #     frame_count += 1
    #     continue
    try:
        coordinates = axis_data[frame_count]['vertices']
    except:
        break
    # 找到最小包围盒
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    
    x_min, x_max = round(min(x_coords)), round(max(x_coords))
    y_min, y_max = round(min(y_coords)), round(max(y_coords))
    
    origin = (round(0.5 * (x_min + x_max)), round(0.5 * ((height - y_min) + (height - y_max))))
    pitch = radians(axis_info['head_pitch'])
    yaw = radians(axis_info['head_yaw'])
    roll = radians(axis_info['head_roll'])

    # 计算旋转向量
    rotation_vector = np.array([pitch, yaw, roll])
    
    # 计算旋转矩阵
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

    # 绘制坐标轴
    for i, color in enumerate(axis_colors):
        axis = np.zeros((3, 1), np.float64)
        axis[i] = axis_length
        axis_rotated = np.dot(rotation_matrix, axis)
        axis_2d = axis_rotated[:2].flatten()  # 投影到二维平面
        axis_end = origin + axis_2d
        cv2.arrowedLine(frame, tuple(origin), tuple(axis_end.astype(int)), color, 2)

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