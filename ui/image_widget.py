#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial 

This example shows
how to use QtGui.QSplitter widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""

import sys
import os
import threading
import time 
from threading import Thread

from PySide import QtGui, QtCore

from masbot.ui.image.pixelmap_label import PixelMapLabel
from masbot.ui.image.image_utils_tab import ImageUtilsTab
from masbot.ui.image.image_thumbnail import ImageThumbnail
from masbot.ui.image.image_toolbar import ImageToolbar
from masbot.config.utils import *

from masbot.ui import preaction
from masbot.config.db_table_def import DBTableDefine

    
class PreviewImage(PixelMapLabel):
    def __init__(self):
        super(PreviewImage, self).__init__(0)
        self.mode = ImagePreviewMode.RealTime
        self.id_ = None

        
    def set_image(self, file_path, id_, mode):
        self.set_mode(mode, id_)
                
        if self.mode == ImagePreviewMode.RealTime:
            bUpdate = True  
        elif self.mode == ImagePreviewMode.FixedId and self.id_ == id_: # 固定thunmbnail ID
            bUpdate = True
        elif self.mode == ImagePreviewMode.Locked and not id_:          # Locked 模式, 且沒有ID, 鎖定一張圖
            bUpdate = True
        else:
            bUpdate = False
                    
        if bUpdate:
            self.update_pixmap(file_path)
        
    def set_mode(self, mode, id_):
        if not mode:
            return

        # 鎖定和解鎖, 直接設定
        if not mode == ImagePreviewMode.RealTime:
            self.mode = mode
        
        if mode == ImagePreviewMode.FixedId and id_:
            self.id_ = id_
        elif mode == ImagePreviewMode.Unlocked:
            self.mode = ImagePreviewMode.RealTime
        print('current mode: ', self.mode)    


class ImageWidget(QtGui.QWidget):

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.init_ui()
        self.cur_preview_id = None
        self.previous_preview_id = None
        self.b_autorun = False
        
        UISignals.GetSignal(SigName.IMG_THUMBNAIL).connect(self.img_thumbnail_income)
        
        UISignals.GetSignal(SigName.MAIN_PLAY).connect(self.play_button_on)
        
        
    def init_ui(self):
        imgs_dir = Path.imgs_dir()

        # Image thumbnail
        self.img_thumbnail = ImageThumbnail([])
        self.img_thumbnail.thumbnail_clicked.connect(self.thumbnail_clicked)
        self.img_thumbnail.setMinimumHeight(105)
        
        # preview image
        self.preview_image = PreviewImage() 
        self.preview_image.update_pixmap("{0}//zero.jpg".format(imgs_dir))
        self.preview_image.setMinimumHeight(400)
        
        # image utility
        image_utils_tab = ImageUtilsTab()
     
        v_layout = QtGui.QVBoxLayout(self)
        v_layout.addWidget(self.img_thumbnail)
        v_layout.addWidget(self.preview_image)        
        v_layout.addWidget(image_utils_tab)        
        
        self.setLayout(v_layout)
             
        self.setWindowTitle('Image Widget')
        self.show()
        
    def thumbnail_clicked(self, thumbnail_id):
        print("thumbnail {0} is clicked".format(thumbnail_id))
        if self.b_autorun:
            self.preview_image.set_mode(ImagePreviewMode.FixedId, thumbnail_id)
        #self.cur_preview_id = thumbnail_id


    def img_thumbnail_income(self, image_data):
        if len(image_data) == 4:
            (path, id_, name, mode) = image_data
        else:
            (path, id_, name) = image_data
            mode = ImagePreviewMode.RealTime
        
        self.preview_image.set_image(path, id_, mode)
        
        if id_:                             # id_ 為空或Nonoe - 顯示手動選擇的影像檔案            
            self.img_thumbnail.change_image([path, id_, name])
       
    def play_button_on(self, play_btn_on):
        self.b_autorun = play_btn_on
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = ImageWidget()
    app.exec_()


if __name__ == '__main__':
    main()        