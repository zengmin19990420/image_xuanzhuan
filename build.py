import os
import sys
import shutil
import subprocess

def clean_build_files():
    """清理旧的构建文件"""
    print("正在清理旧的构建文件...")
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

def get_platform_specific_args():
    """获取平台特定的参数"""
    platform = sys.platform
    args = ['--noconfirm', '--onefile', '--windowed', '--icon=icon.ico', '--name=图片旋转器', '图片旋转器.py']
    
    if platform == 'darwin':  # macOS
        args.append('--target-arch=x86_64')
    elif platform == 'linux':
        args.append('--hidden-import=PIL._tkinter_finder')
    
    return args

def run_pyinstaller():
    """运行PyInstaller打包"""
    print("正在运行PyInstaller打包...")
    args = ['pyinstaller'] + get_platform_specific_args()
    
    try:
        subprocess.run(args, check=True)
        print("打包完成！")
        print("可执行文件位于 dist 目录下。")
    except subprocess.CalledProcessError as e:
        print("打包过程中出现错误！")
        print(f"错误信息: {str(e)}")
        if sys.platform == 'win32':
            os.system('pause')
        else:
            input("按回车键继续...")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        if sys.platform == 'win32':
            os.system('pause')
        else:
            input("按回车键继续...")
        sys.exit(1)

def main():
    clean_build_files()
    run_pyinstaller()
    
    if sys.platform == 'win32':
        os.system('pause')
    else:
        input("按回车键继续...")

if __name__ == '__main__':
    main()