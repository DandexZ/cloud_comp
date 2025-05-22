import os
import hashlib
import subprocess

def generate_collision_files():
    # 使用md5collgen生成碰撞文件
    if not os.path.exists("md5collgen"):
        print("请先下载md5collgen工具并放在当前目录")
        return
    
    # 生成两个MD5值相同但内容不同的文件
    subprocess.run(["./md5collgen", "-o", "file1.bin", "file2.bin"])
    
    # 验证MD5值
    with open("file1.bin", "rb") as f1, open("file2.bin", "rb") as f2:
        md5_1 = hashlib.md5(f1.read()).hexdigest()
        md5_2 = hashlib.md5(f2.read()).hexdigest()
        
    print(f"文件1 MD5: {md5_1}")
    print(f"文件2 MD5: {md5_2}")
    print(f"MD5是否相同: {md5_1 == md5_2}")

def create_different_executables():
    # 创建两个不同行为的可执行文件
    code1 = """
#include <stdio.h>
int main() {
    printf("Hello from Program 1\\n");
    return 0;
}
"""
    
    code2 = """
#include <stdio.h>
int main() {
    printf("Hello from Program 2\\n");
    return 0;
}
"""
    
    # 写入源文件
    with open("prog1.c", "w") as f1, open("prog2.c", "w") as f2:
        f1.write(code1)
        f2.write(code2)
    
    # 编译可执行文件
    subprocess.run(["gcc", "prog1.c", "-o", "prog1"])
    subprocess.run(["gcc", "prog2.c", "-o", "prog2"])
    
    # 验证MD5值
    with open("prog1", "rb") as f1, open("prog2", "rb") as f2:
        md5_1 = hashlib.md5(f1.read()).hexdigest()
        md5_2 = hashlib.md5(f2.read()).hexdigest()
        
    print(f"可执行文件1 MD5: {md5_1}")
    print(f"可执行文件2 MD5: {md5_2}")
    print(f"MD5是否相同: {md5_1 == md5_2}")

if __name__ == "__main__":
    print("MD5碰撞实验")
    print("1. 生成MD5值相同的两个文件")
    generate_collision_files()
    
    print("\n2. 生成MD5值相同但行为不同的可执行文件")
    create_different_executables()