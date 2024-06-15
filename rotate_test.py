import numpy as np
from math import cos, sin, radians

def rotate_vectors(pitch, yaw, roll):
    # 将角度转换为弧度制
    pitch_rad = radians(pitch)
    yaw_rad = radians(yaw)
    roll_rad = radians(roll)

    # 构造旋转矩阵
    Rx = np.array([[1, 0, 0], 
                   [0, cos(pitch_rad), -sin(pitch_rad)],
                   [0, sin(pitch_rad), cos(pitch_rad)]])
    
    Ry = np.array([[cos(yaw_rad), 0, sin(yaw_rad)],
                   [0, 1, 0], 
                   [-sin(yaw_rad), 0, cos(yaw_rad)]])
    
    Rz = np.array([[cos(roll_rad), -sin(roll_rad), 0],
                   [sin(roll_rad), cos(roll_rad), 0],
                   [0, 0, 1]])
    
    # 综合旋转矩阵
    R = Rz @ Ry @ Rx
    
    # 原始单位向量
    vectors = np.array([[1, 0, 0], 
                        [0, 1, 0],
                        [0, 0, 1]])
    
    # 旋转后的向量
    rotated = R @ vectors.T
    
    return rotated.T

# 使用示例
pitch = 45  # 45度
yaw = 60    # 60度 
roll = 30   # 30度

vectors = rotate_vectors(pitch, yaw, roll)
print(vectors)