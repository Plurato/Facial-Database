import subprocess
import os

os.system("chcp 65001") # 中文

command = ['blender', '--python', 'a.py']
print('Running command:', command)

# 执行命令
subprocess.run(command)