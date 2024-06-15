import cv2
import numpy as np

logo = cv2.imread('output.jpg', cv2.IMREAD_UNCHANGED)

scale_percent = 35  # 百分比
width = int(logo.shape[1] * scale_percent / 100)
height = int(logo.shape[0] * scale_percent / 100)
logo = cv2.resize(logo, (width, height))
logo_height, logo_width, _ = logo.shape

cap = cv2.VideoCapture('video.mp4')

video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('pictured_video.mp4', fourcc, 30, (video_width, video_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 计算图片应该被放置的位置
    x = 10  # 左下角的 x 坐标
    y = video_height - logo_height - 10  # 左下角的 y 坐标
    
    # 在视频帧上叠加图片
    roi = frame[y:y+logo_height, x:x+logo_width]
    roi_bg = roi.copy()
    roi[:] = logo[:roi.shape[0], :roi.shape[1]]
    
    # 合并背景和前景
    alpha = 1.0  # 透明度
    cv2.addWeighted(roi_bg, 1-alpha, roi, alpha, 0, roi)
    
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()