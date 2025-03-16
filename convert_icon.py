import cairosvg
import io
from PIL import Image

# 将SVG转换为PNG
png_data = cairosvg.svg2png(url='icon.svg', output_width=256, output_height=256)

# 将PNG数据转换为PIL Image对象
img = Image.open(io.BytesIO(png_data))

# 转换为 RGB 模式
img = img.convert('RGB')

# 创建不同尺寸的图标 (只保留第一个尺寸)
sizes = [(16,16)] # 只保留 16x16 尺寸
icon_images = []

for size in sizes:
    resized_img = img.resize(size, Image.LANCZOS)
    icon_images.append(resized_img)

# 保存为ICO文件 (只保存单帧)
icon_images[0].save(
    'icon.ico',
    # format='ICO',  # 移除 format='ICO' 参数
    # append_images=icon_images[1:], # 移除 append_images
    # save_all=True # 移除 save_all
)

print('Icon has been successfully converted! (single frame)')