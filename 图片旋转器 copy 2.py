import sys
import os
from pathlib import Path
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QSlider,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFrame, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QFont

class ImageRotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadImages()
        
    def initUI(self):
        # 定义按钮样式
        button_style = """
            QPushButton {
                padding: 8px 20px;
                font-size: 14px;
                border-radius: 4px;
                color: white;
                min-width: 80px;
            }
            QPushButton:disabled {
                background-color: #cccccc !important;
                cursor: not-allowed;
            }
        """

        self.setWindowTitle('图片旋转器')
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet('background-color: #f0f0f0;')
        
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建文件夹选择区域
        folder_panel = QFrame()
        folder_panel.setFrameStyle(QFrame.Panel | QFrame.Raised)
        folder_panel.setLineWidth(1)
        folder_panel.setStyleSheet('background-color: #e0e0e0; border-radius: 5px;')
        folder_layout = QHBoxLayout(folder_panel)
        folder_layout.setContentsMargins(15, 10, 15, 10)

        # 输入文件夹选择
        input_folder_layout = QHBoxLayout()
        input_folder_label = QLabel('输入文件夹：')
        input_folder_label.setFont(QFont('Arial', 10))
        self.input_folder_path = QLabel('未选择')
        self.input_folder_path.setFont(QFont('Arial', 10))
        self.input_folder_path.setStyleSheet('color: #666666;')
        input_folder_button = QPushButton('选择')
        input_folder_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2196F3;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        input_folder_button.clicked.connect(self.selectInputFolder)
        input_folder_layout.addWidget(input_folder_label)
        input_folder_layout.addWidget(self.input_folder_path)
        input_folder_layout.addWidget(input_folder_button)

        # 输出文件夹选择
        output_folder_layout = QHBoxLayout()
        output_folder_label = QLabel('输出文件夹：')
        output_folder_label.setFont(QFont('Arial', 10))
        self.output_folder_path = QLabel('未选择')
        self.output_folder_path.setFont(QFont('Arial', 10))
        self.output_folder_path.setStyleSheet('color: #666666;')
        output_folder_button = QPushButton('选择')
        output_folder_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2196F3;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        output_folder_button.clicked.connect(self.selectOutputFolder)
        output_folder_layout.addWidget(output_folder_label)
        output_folder_layout.addWidget(self.output_folder_path)
        output_folder_layout.addWidget(output_folder_button)

        folder_layout.addLayout(input_folder_layout)
        folder_layout.addLayout(output_folder_layout)
        layout.addWidget(folder_panel)

        # 创建图片名称显示标签
        self.filename_label = QLabel()
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.filename_label.setFont(QFont('Arial', 12))
        self.filename_label.setStyleSheet('color: #333333;')
        layout.addWidget(self.filename_label)
        
        # 创建图片显示区域（水平布局）
        images_container = QWidget()
        images_layout = QHBoxLayout(images_container)
        images_layout.setSpacing(20)

        # 左侧：当前图片
        image_frame = QFrame()
        image_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        image_frame.setLineWidth(2)
        image_frame.setStyleSheet('background-color: white;')
        image_layout = QVBoxLayout(image_frame)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 500)
        image_layout.addWidget(self.image_label)
        images_layout.addWidget(image_frame)

        # 右侧：已存在的图片
        existing_frame = QFrame()
        existing_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        existing_frame.setLineWidth(2)
        existing_frame.setStyleSheet('background-color: white;')
        existing_layout = QVBoxLayout(existing_frame)
        
        self.existing_label = QLabel()
        self.existing_label.setAlignment(Qt.AlignCenter)
        self.existing_label.setMinimumSize(400, 500)
        existing_layout.addWidget(self.existing_label)
        images_layout.addWidget(existing_frame)

        layout.addWidget(images_container)
        
        # 创建警告标签
        self.warning_label = QLabel()
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setFont(QFont('Arial', 12))
        self.warning_label.setStyleSheet('color: #f44336;')
        layout.addWidget(self.warning_label)
        
        # 创建控制面板
        control_panel = QFrame()
        control_panel.setFrameStyle(QFrame.Panel | QFrame.Raised)
        control_panel.setLineWidth(1)
        control_panel.setStyleSheet('background-color: #e0e0e0; border-radius: 5px;')
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(15, 10, 15, 10)
        
        # 创建旋转角度滑动条和角度显示标签
        slider_layout = QHBoxLayout()
        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(359)
        self.rotation_slider.setValue(0)
        self.rotation_slider.setMinimumWidth(400)
        self.rotation_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #cccccc;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
                background: #4a90e2;
            }
        """)
        self.rotation_slider.valueChanged.connect(self.rotateImage)
        
        self.angle_label = QLabel('0°')
        self.angle_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.angle_label.setMinimumWidth(50)
        self.angle_label.setStyleSheet('color: #333333;')
        
        slider_layout.addWidget(self.rotation_slider)
        slider_layout.addWidget(self.angle_label)
        control_layout.addLayout(slider_layout)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        button_style = """
            QPushButton {
                padding: 8px 20px;
                font-size: 14px;
                border-radius: 4px;
                color: white;
                min-width: 80px;
            }
            QPushButton:disabled {
                background-color: #cccccc !important;
                cursor: not-allowed;
            }
        """
        
        # 创建导航按钮
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)

        self.prev_button = QPushButton('上一张')
        self.prev_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.prev_button.clicked.connect(self.prevImage)

        self.next_button = QPushButton('下一张')
        self.next_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.next_button.clicked.connect(self.nextImage)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        control_layout.addLayout(nav_layout)

        # 创建保存和跳过按钮
        save_button = QPushButton('保存')
        save_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #4CAF50;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(self.saveImage)
        
        skip_button = QPushButton('跳过')
        skip_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        skip_button.clicked.connect(self.skipImage)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(skip_button)
        control_layout.addLayout(button_layout)
        
        layout.addWidget(control_panel)
        main_widget.setLayout(layout)
        
    def selectInputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输入文件夹')
        if folder:
            self.image_dir = Path(folder)
            self.input_folder_path.setText(str(self.image_dir))
            self.loadImages()

    def selectOutputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        if folder:
            self.images_1_dir = Path(folder)
            self.output_folder_path.setText(str(self.images_1_dir))

    def loadImages(self):
        if not hasattr(self, 'image_dir'):
            self.warning_label.setText('请先选择输入文件夹！')
            return

        if not hasattr(self, 'images_1_dir'):
            self.images_1_dir = Path(os.path.join(os.path.dirname(str(self.image_dir)), 'output'))
            self.output_folder_path.setText(str(self.images_1_dir))

        self.images_1_dir.mkdir(exist_ok=True)
        
        def natural_sort_key(path):
            import re
            numbers = re.findall(r'\d+', path.name)
            return [int(num) if num else 0 for num in numbers]

        self.image_files = sorted([f for f in self.image_dir.glob('*.png')], key=natural_sort_key)
        if not self.image_files:
            self.warning_label.setText('所选文件夹中没有找到PNG图片！')
            return

        self.warning_label.setText('')
            
        self.current_index = 0
        self.loadCurrentImage()
        
    def loadCurrentImage(self):
        if 0 <= self.current_index < len(self.image_files):
            image_path = self.image_files[self.current_index]
            self.current_image = cv2.imdecode(
                np.fromfile(str(image_path), dtype=np.uint8),
                cv2.IMREAD_COLOR
            )
            self.original_image = self.current_image.copy()
            self.current_image_path = image_path
            # 更新图片名称显示
            self.filename_label.setText(f'当前图片：{image_path.name}')
            
            # 检查文件是否已存在
            save_path = self.images_1_dir / image_path.name
            if save_path.exists():
                self.warning_label.setText(f'警告：文件 {image_path.name} 已存在于 images_1 文件夹中！')
                # 加载并显示已存在的图片
                existing_image = cv2.imdecode(
                    np.fromfile(str(save_path), dtype=np.uint8),
                    cv2.IMREAD_COLOR
                )
                height, width = existing_image.shape[:2]
                bytes_per_line = 3 * width
                rgb_image = cv2.cvtColor(existing_image, cv2.COLOR_BGR2RGB)
                q_img = QImage(
                    rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(q_img)
                scaled_pixmap = pixmap.scaled(
                    self.existing_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.existing_label.setPixmap(scaled_pixmap)
            else:
                self.warning_label.setText('')
                self.existing_label.clear()
                
            self.updateDisplay()
            
            # 更新导航按钮状态
            self.prev_button.setEnabled(self.current_index > 0)
            self.next_button.setEnabled(self.current_index < len(self.image_files) - 1)

    def prevImage(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.rotation_slider.setValue(0)
            self.loadCurrentImage()

    def nextImage(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.rotation_slider.setValue(0)
            self.loadCurrentImage()
    def rotateImage(self):
        if hasattr(self, 'original_image'):
            angle = self.rotation_slider.value()
            self.angle_label.setText(f'{angle}°')
            height, width = self.original_image.shape[:2]
            center = (width // 2, height // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.current_image = cv2.warpAffine(
                self.original_image, rotation_matrix, (width, height)
            )
            self.updateDisplay()

    def skipImage(self):
        # 移动到下一张图片
        self.current_index += 1
        if self.current_index >= len(self.image_files):
            print('所有图片处理完成')
            sys.exit()
        
        # 重置滑动条并加载下一张图片
        self.rotation_slider.setValue(0)
        self.loadCurrentImage()
            
    def updateDisplay(self):
        if hasattr(self, 'current_image'):
            height, width = self.current_image.shape[:2]
            bytes_per_line = 3 * width
            rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            
            q_img = QImage(
                rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(q_img)
            
            # 调整图片大小以适应窗口
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            
    def saveImage(self):
        if hasattr(self, 'current_image') and hasattr(self, 'current_image_path'):
            # 构建保存路径
            save_path = self.images_1_dir / self.current_image_path.name
            
            # 检查文件是否已存在
            if save_path.exists():
                self.warning_label.setText(f'警告：文件 {self.current_image_path.name} 已存在于 images_1 文件夹中！')
                return
            
            # 清除警告信息
            self.warning_label.setText('')
            
            # 保存图片
            cv2.imencode('.png', self.current_image)[1].tofile(str(save_path))
            
            # 移动到下一张图片
            self.current_index += 1
            if self.current_index >= len(self.image_files):
                print('所有图片处理完成')
                sys.exit()
            
            # 重置滑动条并加载下一张图片
            self.rotation_slider.setValue(0)
            self.loadCurrentImage()

def main():
    app = QApplication(sys.argv)
    window = ImageRotator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()