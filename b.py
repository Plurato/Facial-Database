import subprocess
import os
import time

# 切换到 UTF-8 编码以支持中文输出
os.system("chcp 65001")

# 定义命令
command = ['blender', '--python', 'a.py']

# 打印运行命令
print('Running command:', command)

# 批量运行脚本
num_runs = 50

for i in range(num_runs):
    print(f"Running script {i+1}/{num_runs}...")
    start_time = time.time()
    
    # 执行命令并等待其完成
    subprocess.run(command)
    
    end_time = time.time()
    print(f"Script {i+1} completed in {end_time - start_time:.2f} seconds.")
    
    # 如有需要，添加延迟
    # time.sleep(1)

print("All scripts have been run.")