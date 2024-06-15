# 创建config.py 文件，用于配置生成数据的参数
import bpy
import bpy_extras.object_utils
import numpy as np
import math as m
import random
import os
# from . import tools
import numpy as np
from typing import Tuple
import sys
import json
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
import time
import sys
import os
from HumGen3D import Human
current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 1、生成配置文件

# base config 基础静态预设参数

# 定义数据集的根目录

# 今日格式化时间
DATE = time.strftime('%Y%m%d', time.localtime())
ROOT_DIR = r'd:/Facial Database/SynHG-{}'.format(DATE)
FOLDER_NAME = "human-test"
DATA_SAVE_PATH = os.path.join(ROOT_DIR, FOLDER_NAME)

if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)

BLEND_FILE_PATH = os.path.join(DATA_SAVE_PATH, "scene.blend")

# 定义数据集的图像尺寸
IMG_HEIGHT = 720
IMG_WIDTH = 1280

FRAME_START = 1
FPS = 60
FRAME_END = FPS*9 # 10s

# 设置眨眼变化阈值和检测间隔
THRESHOLD = 3.0
INTERVAL = 10  

# 动作读取
DIRECTORY = "D:/Facial Database/bvh files/"

def delete_default_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_light():
    bpy.ops.object.light_add(type='SUN', location=(0, -3, 3))

scene = bpy.data.scenes['Scene']
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
delete_default_objects()
create_light()

# 3、人物设置
def create_human(gender):
    global human
    assert gender in ['male', 'female'], "Invalid gender"
    with open('human_options.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 去除每行的换行符
    lines = [line.strip() for line in lines]
    # 随机选择一行
    
    max_attempts = 10
    attempts = 0
    
    human = None
    
    while attempts < max_attempts:
        try:
            # 随机选择一行
            chosen_option = random.choice(lines)
            
            # 尝试创建 Human 实例
            human = Human.from_preset(chosen_option)
            
            # 如果成功则跳出循环
            break
        except Exception as e:
            # 打印错误信息（可选）
            print(f"尝试失败：{chosen_option}")
            
            lines.remove(chosen_option)
            
            # with open('human_options.txt', 'w', encoding='utf-8') as file:
            #     file.write('\n'.join(lines) + '\n')
            
            # 增加尝试次数
            attempts += 1
    if human is not None:
        print("成功创建 Human 实例：", chosen_option)
    else:
        print("在最大尝试次数内未能成功创建 Human 实例。")
    human.expression.load_facial_rig(context=bpy.context)
    return bpy.context.object.data.shape_keys

def randomize_settings():
    age = random.randint(20, 80)
    print("age is: " + str(age))
    human.age.set(age=age)
    human.eyes.randomize()
    human.skin.randomize()
    human.face.randomize()
    # human.hair.face_hair.set_random(context=bpy.context)
    # human.expression.set_random(context=bpy.context)
    human.hair.regular_hair.set_random(context=bpy.context)
    human.hair.regular_hair.randomize_color()
    human.clothing.outfit.set_random(context=bpy.context) #set ramdom cloth

shape_keys = create_human('male')

# 4、眼部设置
# 眼睛形状键
def setup_eye(shape_keys, strength=40):
    # 省略具体实现，与您提供的类中方法相同
    obj = bpy.context.object
    if obj.data.shape_keys and obj.data.shape_keys.animation_data:
        fcurves = obj.data.shape_keys.animation_data.drivers
        # 查找针对特定形状键的 F-Curve
        for fcurve in fcurves:
            if fcurve.data_path == 'key_blocks["eyeLookUpLeft"].value':
                # 获取驱动器
                driver = fcurve.driver
                # 设置新的驱动器表达式
                driver.expression = "var * {}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookUpRight"].value':
                driver = fcurve.driver
                driver.expression = "var * {}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookDownLeft"].value':
                driver = fcurve.driver
                driver.expression = "var * -{}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookDownRight"].value':
                driver = fcurve.driver
                driver.expression = "var * -{}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookInLeft"].value':
                driver = fcurve.driver
                driver.expression = "var * {}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookInRight"].value':
                driver = fcurve.driver
                driver.expression = "var * -{}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookOutLeft"].value':
                driver = fcurve.driver
                driver.expression = "var * -{}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeLookOutRight"].value':
                driver = fcurve.driver
                driver.expression = "var * {}".format(strength)
            elif fcurve.data_path == 'key_blocks["eyeBlink_L"].value':
                obj.data.shape_keys.animation_data.drivers.remove(fcurve)
            elif fcurve.data_path == 'key_blocks["eyeBlink_R"].value':
                obj.data.shape_keys.animation_data.drivers.remove(fcurve)
            else:
                pass

def smooth_fcurve(fcurve, iterations=1):
    # 平滑关键帧的简单算法
    keyframe_points = fcurve.keyframe_points
    for _ in range(iterations):
        new_values = [key.co[1] for key in keyframe_points]
        for i in range(1, len(keyframe_points) - 1):
            prev_value = keyframe_points[i-1].co[1]
            next_value = keyframe_points[i+1].co[1]
            new_values[i] = (prev_value + keyframe_points[i].co[1] + next_value) / 3.0
        for i in range(1, len(keyframe_points) - 1):
            keyframe_points[i].co[1] = new_values[i]

def smooth_all_fcurves(obj, iterations=1):
    if obj.animation_data is None:
        return
    action = obj.animation_data.action
    if action is None: 
        return
    for fcurve in action.fcurves:
        smooth_fcurve(fcurve, iterations)

def setup_movements():
    all_files = [f for f in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, f))]
    random_file = random.choice(all_files)
    random_file = '02_01.bvh'
    file_name_without_extension = os.path.splitext(random_file)[0]
    
    print(f"select movement: {file_name_without_extension}")
    
    file_name = os.path.basename(random_file)
    bvh_filepath = os.path.join(DIRECTORY, file_name)
    bpy.ops.import_anim.bvh(filepath=bvh_filepath, global_scale=0.01, use_fps_scale=False)
    
    action = bpy.data.actions[0]

    # 获取动画帧数
    frame_count = action.frame_range[1]

    # 裁剪动画
    # if frame_count > 500:
    #     print("start to cut animation...")

    #     fcurves = bpy.data.actions[0].fcurves

    #     for frame in range(500, int(frame_count) + 1):
    #         for fcu in fcurves:
    #             bpy.data.objects[file_name_without_extension].keyframe_delete(fcu.data_path, frame = frame)
                
    #     action.frame_range = (0, 500)
    #     print("finished")
        
    # 获取加载的动作
    action = bpy.data.actions[0]

    # 获取动画帧数
    frame_count = action.frame_range[1]
    
    scene.frame_end = round(frame_count)
    # FRAME_END = frame_count
    
    print(f"BVH contains : {frame_count} frames")
    
    imported_armature = bpy.data.objects.get(file_name_without_extension) # change me to the name of your bvh file
    # 获取名为"HumGen"的集合
    humgen_collection = bpy.data.collections.get("HumGen")
    global human_armature
    human_armature = None
    if humgen_collection:
        # 遍历集合中的所有对象
        if humgen_collection.objects:
        # 获取第一个物体
            human_armature = humgen_collection.objects[0]
        else:
            print("HumGen has no object")
    else:
        print("HumGen not exist")
    bpy.context.scene.rsl_retargeting_armature_source = imported_armature
    bpy.context.scene.rsl_retargeting_armature_target = human_armature
    bpy.ops.rsl.build_bone_list()

    bpy.ops.rsl.retarget_animation()

    bpy.data.objects.remove(imported_armature)

    bpy.ops.object.mode_set(mode='POSE')

    bone1 = human_armature.pose.bones["upper_arm.L"]
    
    if bpy.context.area:
        bpy.context.area.type = 'VIEW_3D'
        
    bpy.ops.pose.select_all(action='DESELECT')
    human_armature.select_set(True)

    bone1.bone.select = True

    bpy.ops.anim.aide_activate_anim_offset()

    bpy.ops.transform.rotate(value=-0.887392, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, release_confirm=True)
    bpy.ops.transform.rotate(value=0.416932, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, release_confirm=True)
    bone1.bone.select = False

    bone2 = human_armature.pose.bones["upper_arm.R"]

    bone2.bone.select = True

    bpy.ops.transform.rotate(value=0.91677, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, release_confirm=True)
    bpy.ops.transform.rotate(value=-0.260602, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, release_confirm=True)
    bone2.bone.select = False

    try:
        bpy.ops.anim.aide_deactivate_anim_offset()
    except:
        pass
    
    bpy.context.view_layer.objects.active = human_armature
    bpy.ops.object.mode_set(mode='POSE')
    smooth_all_fcurves(human_armature, iterations=30)  # 可以调整 iterations 以增加平滑次数
    bpy.ops.object.mode_set(mode='OBJECT')

def setup_environment():
    folder_path = "D:/Facial Database/HDRIs/"
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    random_file = random.choice(all_files)
    name = os.path.basename(random_file)
    bpy.ops.hdriw.set_image(name=name, filename=f"{folder_path}{name}")
    random_degree = random.uniform(0, 360)
    bpy.data.window_managers["WinMan"].hdriw_properties.rotate = random_degree

def render_face_image():
    
    bpy.context.scene.frame_set(FRAME_START)
    dg = bpy.context.evaluated_depsgraph_get()
    eyes = bpy.context.scene.objects["HG_Eyes"]
    bone1 = human_armature.pose.bones["eyeball_lookat_master"]
    
    # 创建新的摄像机
    camera_data = bpy.data.cameras.new(name='MyCamera')
    camera_object = bpy.data.objects.new('MyCamera', camera_data)
    bpy.context.scene.collection.objects.link(camera_object)
    
    bpy.context.scene.camera = camera_object
    
    # 设置摄像机位置和旋转
    camera_object.location = bone1.tail + Vector((0.0, -0.4, 0.0))# 设置摄像机的 X, Y, Z 坐标
    camera_object.rotation_euler[0] = 1.5708
    # 设置渲染设置
    bpy.context.scene.camera = camera_object
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = os.path.join(DATA_SAVE_PATH, 'face.png')  # 设置输出文件路径

    # 渲染图像
    bpy.ops.render.render(write_still=True)
    
    json_face = {
        "pupil_mark_left": [],
        "pupil_mark_right": [],
        "pupil_mark_large_left": [],
        "pupil_mark_large_right": [],
        "pupil_center_left": (0.0, 0.0),
        "pupil_center_right": (0.0, 0.0),
        "pupil_radis": 0.0
    }
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    pupil_vertices_left = [1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 2037, 2040, 2042, 2044, 2046, 2048, 2050, 2052, 2054, 2056, 2058, 2060, 2062, 2064, 2066, 2067]
    pupil_vertices_right = [3950, 3951, 3952, 3953, 3954, 3955, 3956, 3957, 3966, 3967, 3968, 3969, 3970, 3971, 3972, 3973, 4681, 4684, 4686, 4688, 4690, 4692, 4694, 4696, 4698, 4700, 4702, 4704, 4706, 4708, 4710, 4711]
    pupil_vertices_large_left = [2669, 2671, 2672, 2674, 2676, 2678, 2680, 2682, 2721, 2722, 2723, 2724, 2725, 2726, 2727, 2728, 3278, 3282, 3285, 3289, 3291, 3295, 3297, 3301, 3303, 3307, 3309, 3313, 3315, 3319, 3321, 3324]
    pupil_vertices_large_right = [25, 27, 28, 30, 32, 34, 36, 38, 77, 78, 79, 80, 81, 82, 83, 84, 634, 638, 641, 645, 647, 651, 653, 657, 659, 663, 665, 669, 671, 675, 677, 680]
    pupil_center = [1603, 4247]
    pupil_radis = [24, 313]
    
    evaled = eyes.evaluated_get(dg)
    mesh = evaled.to_mesh()
    
    for v in pupil_vertices_left:
        world_pos = eyes.matrix_world @ mesh.vertices[v].co
        video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera_object, world_pos)
        video_pos.x = video_pos.x * render_size[0]
        video_pos.y = video_pos.y * render_size[1]
        json_face['pupil_mark_left'].append((video_pos.x, video_pos.y))
        
    for v in pupil_vertices_right:
        world_pos = eyes.matrix_world @ mesh.vertices[v].co
        video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera_object, world_pos)
        video_pos.x = video_pos.x * render_size[0]
        video_pos.y = video_pos.y * render_size[1]
        json_face['pupil_mark_right'].append((video_pos.x, video_pos.y))
        
    for v in pupil_vertices_large_left:
        world_pos = eyes.matrix_world @ mesh.vertices[v].co
        video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera_object, world_pos)
        video_pos.x = video_pos.x * render_size[0]
        video_pos.y = video_pos.y * render_size[1]
        json_face['pupil_mark_large_left'].append((video_pos.x, video_pos.y))
    
    for v in pupil_vertices_large_right:
        world_pos = eyes.matrix_world @ mesh.vertices[v].co
        video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera_object, world_pos)
        video_pos.x = video_pos.x * render_size[0]
        video_pos.y = video_pos.y * render_size[1]
        json_face['pupil_mark_large_right'].append((video_pos.x, video_pos.y))
    
    pos_center_left, pos_center_right = eyes.matrix_world @ mesh.vertices[pupil_center[1]].co, eyes.matrix_world @ mesh.vertices[pupil_center[0]].co
    video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera_object, pos_center_left)
    video_pos.x = video_pos.x * render_size[0]
    video_pos.y = video_pos.y * render_size[1]
    json_face['pupil_center_left'] = (video_pos.x, video_pos.y)
    video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera_object, pos_center_right)
    video_pos.x = video_pos.x * render_size[0]
    video_pos.y = video_pos.y * render_size[1]
    json_face['pupil_center_right'] = (video_pos.x, video_pos.y)
    
    pos1, pos2 = eyes.matrix_world @ mesh.vertices[pupil_radis[0]].co, eyes.matrix_world @ mesh.vertices[pupil_radis[1]].co
    json_face['pupil_radis'] = (pos1 - pos2).length
    
    json_data = json.dumps(json_face, indent=4)
    # 将JSON字符串写入文件
    with open("face_data.json", "w") as file:
        file.write(json_data)

def generate_normal_random_within_range(lower_bound, upper_bound):
    while True:
        # 生成均值为0，标准差为1的正态分布随机数
        number = np.random.normal(0, 1)
        # 如果生成的数在指定范围内，则返回
        if lower_bound <= number <= upper_bound:
            return number

def generate_eyes_keyframe(frame_start, frame_end, fps):
    print(f"from {frame_start} to {frame_end}")
    cur_num1, cur_num2= 0.0, 0.0
    bone1 = human_armature.pose.bones["eyeball_lookat_master"]
    frames = frame_end - frame_start + 1
    cur_frame = frame_start
    while cur_frame < frames:
        is_move = random.randint(0, 1)
        if is_move: 
            duration = 15
            bone1.location = (cur_num1, 0.0, cur_num2)
            bone1.keyframe_insert("location", frame=cur_frame)
            num1 = generate_normal_random_within_range(-0.03, 0.03)
            num2 = generate_normal_random_within_range(-0.03, 0.03)
            cur_num1, cur_num2 = num1, num2
            bone1.location = (num1, 0.0, num2)
            bone1.keyframe_insert("location", frame=cur_frame + duration)
            cur_frame += duration + random.randint(2*fps, 5*fps) 
            
    print("finished")   

setup_eye(shape_keys)

randomize_settings() #random human apperance

setup_movements()
setup_environment()

print("start generating eyes movement")
generate_eyes_keyframe(FRAME_START, scene.frame_end, FPS)
# human.make_camera_look_at_human(obj_camera=bpy.context.scene.camera)
# 5、渲染设置

def setup_render():
    render = bpy.context.scene.render
    render.resolution_x = IMG_WIDTH
    render.resolution_y = IMG_HEIGHT
    render.fps = FPS
    render.filepath = os.path.join(DATA_SAVE_PATH, 'video.mp4')
    render.image_settings.file_format = 'FFMPEG'
    render.ffmpeg.format = 'MPEG4'

def get_bone_positions(armature_obj):
    positions = []
    for bone in armature_obj.pose.bones:
        head_world = armature_obj.matrix_world @ bone.head
        tail_world = armature_obj.matrix_world @ bone.tail
        positions.append(head_world)
        positions.append(tail_world)
    return positions

def setup_camera():
    print("start setting up camera")
    # 获取动画帧范围
    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end
    print(f"from {frame_start} to {frame_end}")
    # 初始化包围盒的最小和最大坐标
    min_coord = [float('inf'), float('inf'), float('inf')]
    max_coord = [-float('inf'), -float('inf'), -float('inf')]

    # 遍历所有帧，找到最小包围盒
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        positions = get_bone_positions(human_armature)
        for pos in positions:
            for i in range(3):
                min_coord[i] = min(min_coord[i], pos[i])
                max_coord[i] = max(max_coord[i], pos[i])

    # 计算包围盒的中心和大小
    bbox_center = [(min_coord[i] + max_coord[i]) / 2 for i in range(3)]
    bbox_size = [max_coord[i] - min_coord[i] for i in range(3)]
    
    cam_data = bpy.data.cameras.new("Camera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.scene.camera = cam_obj
    bpy.context.scene.collection.objects.link(cam_obj)
    camera = bpy.data.objects['Camera']
    # 计算摄像机的位置和朝向
    bbox_max_size = max(bbox_size) 
    # 适当调整这个系数来获得合理的摄像机距离
    distance_factor = 0.9 
    distance = bbox_max_size * distance_factor

    # 将摄像机放置在包围盒中心后方（Z 轴方向），并朝向包围盒中心
    camera.location = (bbox_center[0], bbox_center[1] - distance, bbox_center[2] + 0.5)
    camera.rotation_euler = (m.pi / 2, 0, 0)
    print("finished")

setup_camera()

def export_label():
    print("start export labels")
    body = bpy.context.scene.objects["HG_Body"]
    eyes = bpy.context.scene.objects["HG_Eyes"]
    camera = bpy.data.objects['Camera']
    global frames
    frames = []
    
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    for frame in range(FRAME_START, scene.frame_end):
        bpy.context.scene.frame_set(frame)
        dg = bpy.context.evaluated_depsgraph_get()
        evaled = body.evaluated_get(dg)
        mesh = evaled.to_mesh()
        vertices = [807, 1401, 2799, 2829, 3638, 3751, 4563, 6220, 7335, 7675, 7810, 9118]
        face_vertices = [764, 775, 782, 852, 896, 974, 1007, 1028, 1031, 1322, 1356, 1396, 1579, 1633, 1636, 1760, 1901, 1920, 2003, 2014, 2060, 2072, 2089, 2109, 2178, 2184, 2200, 2216, 2284, 2294, 2539, 2608, 2637, 2644, 2677, 2682, 2701, 2754, 2762, 2901, 2921, 3338, 3573, 3579, 3588, 3625, 3626, 3648, 3652, 3685, 3687, 3824, 3830, 3866, 3926, 3994, 4003, 4365, 4388, 4725, 4754, 4771, 4821, 4835, 4963, 4973, 4980, 5008, 5050, 5090, 5568, 5621, 5738, 5821, 5836, 5839, 7142, 7470, 7676, 7760, 7769, 7777, 7793, 7796, 7801, 7820, 8902, 8958, 9084, 9696, 9782, 9791, 9799, 9817, 9845, 9861]
        pupil_vertices_left = [1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 2037, 2040, 2042, 2044, 2046, 2048, 2050, 2052, 2054, 2056, 2058, 2060, 2062, 2064, 2066, 2067]
        pupil_vertices_right = [3950, 3951, 3952, 3953, 3954, 3955, 3956, 3957, 3966, 3967, 3968, 3969, 3970, 3971, 3972, 3973, 4681, 4684, 4686, 4688, 4690, 4692, 4694, 4696, 4698, 4700, 4702, 4704, 4706, 4708, 4710, 4711]
        body_mark =["head", "neck", "upper_arm.R",  "upper_arm.L", "forearm.R", "forearm.L", "thigh.R", "thigh.L", "shin.R", "shin.L"]
        body_li = []
        
        frame_json = {
            "frame_number": frame,
            "vertices": [],
            "face_vertices": [],
            "eye_pitch": 0.0,
            "eye_yaw": 0.0,
            "head_pitch": 0.0,
            "head_yaw": 0.0,
            "head_roll": 0.0,
            "eye_pos_left": (0.0, 0.0),
            "eye_pos_right": (0.0, 0.0),
            "blink_strength": 0.0,
            "body_mark": [],
            "pupil_mark_left": [],
            "pupil_mark_right": []
        }
        for v in vertices:
            world_pos = body.matrix_world @ mesh.vertices[v].co
            
            video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_pos)
            video_pos.x = video_pos.x * render_size[0]
            video_pos.y = video_pos.y * render_size[1]
            frame_json['vertices'].append((video_pos.x, video_pos.y)) # face range
        
        for v in face_vertices:
            world_pos = body.matrix_world @ mesh.vertices[v].co
            video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_pos)
            video_pos.x = video_pos.x * render_size[0]
            video_pos.y = video_pos.y * render_size[1]
            frame_json['face_vertices'].append((video_pos.x, video_pos.y)) # face key points
            
        for mark in body_mark: # body mark generate
            bone = human_armature.pose.bones[mark]
            world_pos = human_armature.matrix_world @ bone.head
            video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_pos)
            video_pos.x = video_pos.x * render_size[0]
            video_pos.y = video_pos.y * render_size[1]
            body_li.append((video_pos.x, video_pos.y))
            world_pos = human_armature.matrix_world @ bone.tail
            video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_pos)
            video_pos.x = video_pos.x * render_size[0]
            video_pos.y = video_pos.y * render_size[1]
            body_li.append((video_pos.x, video_pos.y))
        
        frame_json['body_mark'] = list(set(body_li))
        frame_json['body_mark'].sort(key=body_li.index)
        
        evaled = eyes.evaluated_get(dg)
        mesh = evaled.to_mesh()
        
        for v in pupil_vertices_left:
            world_pos = eyes.matrix_world @ mesh.vertices[v].co
            
            video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_pos)
            video_pos.x = video_pos.x * render_size[0]
            video_pos.y = video_pos.y * render_size[1]
            frame_json['pupil_mark_left'].append((video_pos.x, video_pos.y))
        
        for v in pupil_vertices_right:
            world_pos = eyes.matrix_world @ mesh.vertices[v].co
            
            video_pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_pos)
            video_pos.x = video_pos.x * render_size[0]
            video_pos.y = video_pos.y * render_size[1]
            frame_json['pupil_mark_right'].append((video_pos.x, video_pos.y))
        
        pos1 = eyes.matrix_world @ mesh.vertices[4182].co
        pos2 = eyes.matrix_world @ mesh.vertices[4247].co
        pos3 = eyes.matrix_world @ mesh.vertices[1538].co
        
        video_pos_left = bpy_extras.object_utils.world_to_camera_view(scene, camera, pos1)
        video_pos_right = bpy_extras.object_utils.world_to_camera_view(scene, camera, pos3)
        video_pos_left.x, video_pos_left.y = video_pos_left.x * render_size[0], video_pos_left.y * render_size[1]
        video_pos_right.x, video_pos_right.y = video_pos_right.x * render_size[0], video_pos_right.y * render_size[1]
        frame_json['eye_pos_left'] = (video_pos_left.x, video_pos_left.y)
        frame_json['eye_pos_right'] = (video_pos_right.x, video_pos_right.y)
        direction = (pos2 - pos1).normalized()
        # 从Vector对象提取x,y,z分量
        x, y, z = direction

        # 计算pitch角度
        if y == 0:
            if z > 0:
                pitch = m.pi / 2
            else:
                pitch = -m.pi / 2
        else:
            pitch = m.atan2(z, -y)

        # 计算yaw角度
        if y == 0:
            if x > 0:
                yaw = m.pi / 2
            else:
                yaw = -m.pi / 2
        else:
            yaw = m.atan2(x, -y)
        pitch = m.degrees(pitch)
        yaw = m.degrees(yaw)
        frame_json['eye_pitch'] = pitch
        frame_json['eye_yaw'] = yaw
        
        bone = human_armature.pose.bones["head"]
        bone1 = human_armature.pose.bones["eyeball_lookat_master"]
        direction1 = (bone.tail - bone.head).normalized()
        direction2 = (bone1.tail - bone1.head).normalized()
        x, y, z = direction1
        x1, y1, z1 = direction2

        if z == 0:
            if y > 0:
                pitch1 = m.pi / 2
            else:
                pitch1 = -m.pi / 2
        else:
            pitch1 = m.atan2(y, z)
            
        if z == 0:
            if x > 0:
                yaw1 = m.pi / 2
            else:
                yaw1 = -m.pi / 2
        else:
            yaw1 = m.atan2(x, z)
            
        if y1 == 0:
            if x1 > 0:
                roll = m.pi / 2
            else:
                roll = -m.pi / 2
        else:
            roll = m.atan2(x1, -y1)
            
        pitch1 = m.degrees(pitch1)
        yaw1 = m.degrees(yaw1)
        roll = m.degrees(roll)
        
        if roll > 180:
            roll -= 360
        elif roll < -180:
            roll += 360
        
        frame_json['head_pitch'] = pitch1
        frame_json['head_roll'] = yaw1
        frame_json['head_yaw'] = roll
        
        frames.append(frame_json) 
    
    json_data = json.dumps(frames, indent=4)
    # 将JSON字符串写入文件
    with open("frames.json", "w") as file:
        file.write(json_data)
    print("finished")

def render_animation():
    bpy.ops.render.render(animation=True, write_still=False)

setup_render()

export_label()

#眨眼控制
def lid_function(t, µ, a, b, c):
    if t <= µ:
        return a - (t / µ) ** 2
    else:
        return b - np.exp(-c * np.log(t - µ + 1))

def generate_blink_strengths(frame_start, frame_end, fps, change_blink):
    # generate blink sequence from frame_start to frame_end
    frames = frame_end - frame_start + 1
    # genetate blink time
    # max_blink_times = max(int((frames / fps) / 60 * random.randint(15, 20)), 1)
    cur_frame = frame_start
    # blink_count = 0
    blink_strengths = [1] * frames
    # 参数设置
    µ = random.randint(30, 40)
    a = 0.98 # random_decimal = round(random.uniform(0.8, 0.98), 2)
    b = 1.18
    c = µ / 100
    while cur_frame < frames:
        is_blink = random.randint(0, 1)
        if change_blink[cur_frame - 1]:
            is_blink = 1
        print(str(cur_frame) + " " + str(is_blink))
        if is_blink:
            #blink_duration = max(int(random.uniform(0.2, 0.7))*fps, 3)
            blink_duration = 30
            scale_factor =  blink_duration / 100
            blink_strengths[cur_frame:cur_frame+blink_duration] = [lid_function(t / scale_factor, µ, a, b, c) for t in range(blink_duration)]
            cur_frame += blink_duration + random.randint(fps, 2*fps)
            # cur_frame += blink_duration
        else:
            cur_frame += 1
    return blink_strengths

def set_eye_blink_keyframes(shape_keys, value, frame):
    shape_keys.key_blocks["eyeBlink_L"].value = value
    shape_keys.key_blocks["eyeBlink_L"].keyframe_insert(data_path="value", frame=frame)
    shape_keys.key_blocks["eyeBlink_R"].value = value
    shape_keys.key_blocks["eyeBlink_R"].keyframe_insert(data_path="value", frame=frame)

def setup_blinks(shape_keys, change_blink):
    global blink_strengths
    blink_strengths = generate_blink_strengths(FRAME_START, scene.frame_end, FPS, change_blink)
    for i, blink_strength in enumerate(blink_strengths):
        set_eye_blink_keyframes(shape_keys, 1-blink_strength, i+1)

def calculate_angle_change(pitch1, yaw1, pitch2, yaw2):
    return m.sqrt((pitch2 - pitch1) ** 2 + (yaw2 - yaw1) ** 2)

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

def generate_natural_blink():
    print("start generating natural blinks")
    json_file_path = 'frames.json'
    significant_changes = find_significant_changes(json_file_path, THRESHOLD, INTERVAL)
    # for i, blink in enumerate(significant_changes):
    #     if blink is True:
    #         print(f"he will blink at {i} frame")
    print(significant_changes)
    setup_blinks(shape_keys, significant_changes)
    print("finished")

generate_natural_blink()

    
def edit_json():
    with open('frames.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        if 'blink_strength' in item:
            item["blink_strength"] = 1.0 - blink_strengths[item["frame_number"]]
    with open('frames.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

edit_json()

render_animation()

render_face_image()
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE_PATH)

exit()