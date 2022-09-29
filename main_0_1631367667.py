#create the Easy Editor photo editor here!
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QListWidget, QFileDialog
import os
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap

#region setup

app = QApplication([])
window = QWidget()
window.resize(1000, 600)

file_list = QListWidget()
pic_label = QLabel("Image goes here")
folder_btn = QPushButton("Choose folder")
sharpness_btn = QPushButton("Sharpness")
mirror_btn = QPushButton("Mirror")
rotate_left_btn = QPushButton("Rotate left")
rotate_right_btn = QPushButton("Rotate right")
grayscale_btn = QPushButton("Grayscale")

main_box = QHBoxLayout()
left_column = QVBoxLayout()
right_column = QVBoxLayout()
buttons_box = QHBoxLayout()


window.setLayout(main_box)
main_box.addLayout(left_column, 20)
main_box.addLayout(right_column, 80)



left_column.addWidget(folder_btn)
left_column.addWidget(file_list)


right_column.addWidget(pic_label)
right_column.addLayout(buttons_box)


buttons_box.addWidget(sharpness_btn)
buttons_box.addWidget(mirror_btn)
buttons_box.addWidget(rotate_left_btn)
buttons_box.addWidget(rotate_right_btn)
buttons_box.addWidget(grayscale_btn)
#endregion setup

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.file_name = None
        self.dir = None
        self.save_dir = "modified/"
    def loadImage(self, directory, file_name):
        self.dir = directory
        self.file_name = file_name
        image_path = os.path.join(self.dir, self.file_name)
        self.image = Image.open(image_path)
    def showImage(self, path):
        pic_label.hide()
        p = QPixmap(path)
        p = p.scaled(pic_label.width(), pic_label.height(), True)
        pic_label.setPixmap(p)
        pic_label.show()
    def saveImage(self):
        folder_path = os.path.join(self.dir, self.save_dir)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        image_path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.image.save(image_path)
    def rotateLeft(self):
        self.image = self.image.rotate(-90)
        self.saveImage()
        new_image_path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(new_image_path)
    def rotateRight(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        new_image_path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(new_image_path)
    def grayscale(self):
        self.image = self.image.convert("L")
        self.saveImage()
        new_image_path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(new_image_path)
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        new_image_path = os.path.join(self.dir, self.save_dir, self.file_name)
        self.showImage(new_image_path)

proc = ImageProcessor()
folder = ''

def filter_filelist(filelist):
    filtered_list = []
    extensions = ['.png', '.jpeg', '.webp', '.jpg']
    for file in filelist:
        for ext in extensions:
            if file.endswith(ext):
                filtered_list.append(file)
    return filtered_list
def choose_folder():
    global folder
    folder = QFileDialog.getExistingDirectory()
    if folder != '':
        files = os.listdir(folder)
        file_list.clear()
        file_list.addItems(filter_filelist(files))

def displaySelectedImage():
    filename = file_list.currentItem().text()
    proc.loadImage(folder, filename)
    proc.showImage(os.path.join(folder, filename))

rotate_left_btn.clicked.connect(proc.rotateLeft)
rotate_right_btn.clicked.connect(proc.rotateRight)
grayscale_btn.clicked.connect(proc.grayscale)
mirror_btn.clicked.connect(proc.mirror)

folder_btn.clicked.connect(choose_folder)
file_list.currentRowChanged.connect(displaySelectedImage)










































window.show()
app.exec()