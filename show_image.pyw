import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image

def show_image(image_path):
    app = QApplication(sys.argv)
    
    # 加载图片文件
    image = Image.open(image_path)
    
    # 将PIL图像转换为QPixmap
    image = image.convert("RGBA")  # 确保图像是RGBA格式
    data = image.tobytes("raw", "BGRA")
    qim = QImage(data, image.width, image.height, QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle('Image Viewer')
    window.setGeometry(100, 100, pixmap.width(), pixmap.height())  # 根据图片大小设置窗口大小
    window.setWindowFlags(Qt.WindowStaysOnTopHint)  # 设置窗口总在最前
    
    # 使用标签显示图片
    label = QLabel(window)
    label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignCenter)
    label.resize(pixmap.size())  # 调整标签大小以适应图片
    
    window.setCentralWidget(label)  # 将标签设置为窗口的中心部件
    
    # 显示窗口
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        show_image(image_path)
    else:
        print("Usage: python show_image.py <image_path>")
