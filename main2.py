import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
# 导入模型
from ui.detect2 import Ui_MainWindow  # 导入detec_ui的界面
from detect_adjust import parse_opt, main

class UI_Logic_Window(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(UI_Logic_Window, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_slots()


    # 控件绑定相关操作
    def init_slots(self):
        self.ui.pushButton.clicked.connect(self.button_image_open)
        self.ui.pushButton_2.clicked.connect(self.button_image_detect_save)
        self.ui.pushButton_3.clicked.connect(self.detect)


    # 设置需要检测的图片
    def button_image_open(self):
        name_list = []
        try:
            self.img_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "打开图片", r"D:\AAAprogramfile\pycharm\yolov5-7.0\stft2\images\test",
                                                           "*.jpg;;*.png;;All Files(*)")
        except OSError as reason:
            print('文件打开出错啊！核对路径是否正确' + str(reason))
        else:
            # 判断图片是否为空
            if not self.img_name:
                QtWidgets.QMessageBox.warning(self, u"Warning", u"打开图片失败", buttons=QtWidgets.QMessageBox.Ok,
                                              defaultButton=QtWidgets.QMessageBox.Ok)
        # 打印检测图片，与label_3绑定起来
        jpg = QtGui.QPixmap(self.img_name).scaled(self.ui.label_3.width(), self.ui.label_3.height())
        self.ui.label_3.setPixmap(jpg)
        self.ui.label_3.setScaledContents(True)

    # 设置需要保存的地址
    def button_image_detect_save(self):
        print('button_image_save')
        self.save_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", "runs/detect")
        print("选择的文件夹路径：", self.save_dir)

    # 检测函数
    def detect(self):
        try:
            source = self.img_name.replace('/', '\\')
        except:
            QtWidgets.QMessageBox.warning(self, u"Warning", u"请先选择要检测的图片文件",
                                          buttons=QtWidgets.QMessageBox.Ok,
                                          defaultButton=QtWidgets.QMessageBox.Ok)
            pass

        try:
            save_dir = self.save_dir
        except:
            QtWidgets.QMessageBox.warning(self, u"Warning", u"请先选择要保存的图片文件夹",
                                          buttons=QtWidgets.QMessageBox.Ok,
                                          defaultButton=QtWidgets.QMessageBox.Ok)
            return
    # 构造参数，设置参数值

        opt = parse_opt()
        weights_path = "D:\AAAprogramfile\pycharm\yolov5-7.0\weights\exp12best.pt"
        opt.weights = weights_path
        opt.source = source
        opt.project = save_dir
        save_img = main(opt)
        print(save_img)
        jpg = QtGui.QPixmap(save_img).scaled(self.ui.label_2.width(), self.ui.label_2.height())
        self.ui.label_2.setPixmap(jpg)
        self.ui.label_2.setScaledContents(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    current_ui = UI_Logic_Window()
    current_ui.show()
    sys.exit(app.exec_())
