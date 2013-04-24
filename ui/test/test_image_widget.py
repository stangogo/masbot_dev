#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
import logging
import logging.config
import codecs
from datetime import datetime

import threading
from threading import Thread


from PySide import QtCore
from PySide.QtGui import *

from masbot.config.utils import SigName, UISignals
from masbot.ui.image_widget import ImageWidget
from masbot.ui.preaction import *
from masbot.config.utils import Path

    
class ImageWidgetTest(QWidget):
    def __init__(self):  
        super(ImageWidgetTest, self).__init__()
        self.init_ui()
        self.stop_thread = True

    def init_ui(self):
        layout = QHBoxLayout()
        layout.addLayout(self.init_buttons())
        layout.addWidget(ImageWidget())
        
        self.setLayout(layout)
        
    def init_buttons(self):
        vbox = QVBoxLayout()
        
        send_img_btn = QPushButton('送影像')
        send_msg_btn = QPushButton('送訊息')
        
        send_img_btn.clicked.connect(self.img_btn_click)
        send_msg_btn.clicked.connect(self.img_msg_click)
        
        vbox.addWidget(send_img_btn, 0)
        vbox.addWidget(send_msg_btn, 1)
        
        vbox.setAlignment(send_img_btn, QtCore.Qt.AlignTop)
        vbox.setAlignment(send_msg_btn, QtCore.Qt.AlignTop)
        
        return vbox
        
    def img_btn_click(self):        
        if self.stop_thread == False:
            self.stop_thread = True
        else:
            threading.Thread(target = self.threadFunc).start()
            
    def img_msg_click(self):
        # ['2013/03/04 AM 9:02.27', 'IPI', 'OK', 0.125, 'D:\\Images\\LPCam2\\Image20120809_211043_287.bmp']
        
        local_time = datetime.now()
        new_time_str = local_time.strftime("%Y/%m/%d %H:%M:%S")
        
        UISignals.GetSignal(SigName.IMG_MESSAGE).emit([new_time_str, 'IPI', 'OK', 0.125, 'D:\\Images\\LPCam2\\Image20120809_211043_287.bmp'])
        
    
    def threadFunc(self):
        self.stop_thread = False
        index = 0
        imgs_dir = Path.imgs_dir()
        
        while self.stop_thread == False:
            index = (index + 1) % 15
            
            index = self.change_thumbnail_image(index, '1', imgs_dir)
            index = self.change_thumbnail_image(index, '2', imgs_dir)
            index = self.change_thumbnail_image(index, '3', imgs_dir)
            index = self.change_thumbnail_image(index, '4', imgs_dir)
            index = self.change_thumbnail_image(index, '5', imgs_dir)
            index = self.change_thumbnail_image(index, '6', imgs_dir)
            index = self.change_thumbnail_image(index, '7', imgs_dir)
            index = self.change_thumbnail_image(index, '8', imgs_dir)
            index = self.change_thumbnail_image(index, '9', imgs_dir)
            index = self.change_thumbnail_image(index, '10', imgs_dir)

            time.sleep(0.15)
    
    def change_thumbnail_image(self, index, id_, imgs_dir):   # 測試用     
        index = (index + 1) % 15
        image_path = "{0}\\{1}.tif".format( imgs_dir, index + 1)
        img_receiver = UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit([image_path, id_, '{0}'.format(index)])
        
        return index     
    
    
if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    window = ImageWidgetTest()
    window.show()      
    
    app.exec_()
    