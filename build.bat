@echo off
setlocal enabledelayedexpansion

echo 正在清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo 正在运行PyInstaller打包...
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico --name="图片旋转器" 图片旋转器.py

if !errorlevel! neq 0 (
    echo 打包过程中出现错误！
    pause
    exit /b 1
)

echo 打包完成！
echo 可执行文件位于 dist 目录下。
pause