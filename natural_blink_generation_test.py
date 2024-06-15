import json
import math

def calculate_angle_change(pitch1, yaw1, pitch2, yaw2):
    return math.sqrt((pitch2 - pitch1) ** 2 + (yaw2 - yaw1) ** 2)

def find_significant_changes(json_file, threshold, interval):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    num_frames = len(data)
    significant_changes = [False] * num_frames
    
    for i in range(interval, num_frames, interval):
        previous_frame = data[i - interval]
        current_frame = data[i]
        
        angle_change = calculate_angle_change(
            previous_frame['eye_pitch'], previous_frame['eye_yaw'],
            current_frame['eye_pitch'], current_frame['eye_yaw']
        )
        
        if angle_change > threshold:
            significant_changes[i - interval] = True
    
    return significant_changes

# 设置变化阈值和检测间隔
THRESHOLD = 8.0
INTERVAL = 5  # 每隔5帧检测一次

# 替换为你的JSON文件路径
json_file_path = 'frames.json'
significant_changes = find_significant_changes(json_file_path, THRESHOLD, INTERVAL)

# 输出结果
for change in significant_changes:
    print(change)