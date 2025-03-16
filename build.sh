#!/bin/bash

echo "正在清理旧的构建文件..."
rm -rf build

echo "正在运行PyInstaller打包..."
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico --name="图片旋转器" 图片旋转器.py

if [ $? -ne 0 ]; then
  echo "打包过程中出现错误！"
  read -n 1 -s -p "Press any key to continue..."
  exit 1
fi

echo "打包完成！"
echo "可执行文件位于 dist 目录下。"
read -n 1 -s -p "Press any key to continue..."