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
        send_run_btn = QPushButton('執行')
        send_run_btn.setCheckable(True)
        
        send_img_btn.clicked.connect(self.img_btn_click)
        send_msg_btn.clicked.connect(self.img_msg_click)
        send_run_btn.clicked.connect(self.img_run_click)
        
        vbox.addWidget(send_img_btn, 0)
        vbox.addWidget(send_msg_btn, 0)
        vbox.addWidget(send_run_btn, 1)
        
        vbox.setAlignment(send_img_btn, QtCore.Qt.AlignTop)
        vbox.setAlignment(send_msg_btn, QtCore.Qt.AlignTop)
        vbox.setAlignment(send_run_btn, QtCore.Qt.AlignTop)
        
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
        
    
    def img_run_click(self):
        sender = self.sender()
        UISignals.GetSignal(SigName.MAIN_PLAY).emit(sender.isChecked())        
    
    def threadFunc(self):
        self.stop_thread = False
        index = 0
        imgs_dir = Path.imgs_dir()
        
        while self.stop_thread == False:
            index = (index + 1) % 10
            
            index = self.change_thumbnail_image(index, '{0}'.format(index), imgs_dir)

            time.sleep(0.15)
    
    def change_thumbnail_image(self, index, id_, imgs_dir):   # 測試用             
        image_path = "{0}\\{1}.tif".format( imgs_dir, index)
        img_receiver = UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit([image_path, id_, '{0}'.format(index), 3])
        
        return index     
    
    
if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    window = ImageWidgetTest()
    window.show()      
    
    app.exec_()
    