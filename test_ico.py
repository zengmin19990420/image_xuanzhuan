from PIL import Image

# 创建一个简单的 RGB 图像
image = Image.new('RGB', (64, 64), color='red')

# 打印 Pillow 支持的所有保存格式
print(Image.registered_extensions())

# 尝试保存为 ICO 文件
try:
    image.save('test.ico', format='ICO')
    print('ICO 文件保存成功！')
except Exception as e:
    print(f'保存 ICO 文件失败: {e}')