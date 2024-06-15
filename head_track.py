import cv2
import json
import os

# 打开视频文件
cap = cv2.VideoCapture('video.mp4')

# 获取视频属性
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(width, height, fps)

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

# 加载JSON文件
with open('frames.json', 'r') as f:
    coordinates_data = json.load(f)
    
# 遍历每一帧
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 获取当前帧的坐标信息
    try:
        coordinates = coordinates_data[frame_count]['vertices']
    except:
        break
    # 找到最小包围盒
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    
    x_min, x_max = round(min(x_coords)), round(max(x_coords))
    y_min, y_max = round(min(y_coords)), round(max(y_coords))

    print(x_min, y_min, x_max, y_max)
    
    # 在帧上绘制矩形
    cv2.rectangle(frame, (x_min, height - y_min), (x_max, height - y_max), (0, 255, 0), 2)

    # 写入输出视频
    out.write(frame)

    frame_count += 1

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
os.remove('video.mp4')
os.rename('output_video.mp4', 'video.mp4')