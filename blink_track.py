import cv2
import json
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
    blink_data = json.load(f)

# 遍历每一帧
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    try:
        blink = blink_data[frame_count]['blink_strength']
    except:
        break
    
    print(frame_count)
    # 添加文字
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'blink strength: {:.2f}'.format(blink), (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
    out.write(frame)
    
    frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()
os.remove('video.mp4')
os.rename('output_video.mp4', 'video.mp4')