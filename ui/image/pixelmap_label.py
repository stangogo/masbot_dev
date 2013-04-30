# Title          : PixelmapLabel.py
# Description    : Present a pixel map. Default height is 400.
#                  Using signal-slot to change the image
# Author         : Cigar Huang
# Date           : 20130307
# usage          : 
# notes          : 

import sys
import os
import copy
import logging
from PySide import QtGui, QtCore


class PixelMapLabel(QtGui.QLabel):
        
    height = 500
    clicked = QtCore.Signal(str)                # can be other types (list, dict, object...)        
    __change_image = QtCore.Signal(str, int)    #內部訊號, 通知更新圖片和大小; str: 圖檔路徑, int: 顯示大小 (height)
    __change_qimage = QtCore.Signal(QtGui.QImage, int)    #內部訊號, 通知更新圖片和大小; str: 圖檔路徑, int: 顯示大小 (height)
    
    def __init__(self, id_):
        super(PixelMapLabel, self).__init__()
        self.logger = logging.getLogger('ui.log')
        self.id_= id_
        self.orig_image_path = None
        self.__change_image.connect(self.update_pixmap)
        self.__change_qimage.connect(self.update_qimage)
        #self.image_reader = QtGui.QImageReader()
        #self.image_reader.setScaledSize(QtCore.QSize(666,500))

    def set_height(self, height):
        self.height = height
        #self.image_reader.setScaledSize(QtCore.QSize(int(height*4/3), height))
    
    def update_pixmap(self, image_path, height=0):
        if not os.path.exists(image_path):
            return
        
        if height != 0:
            self.set_height(height)
        
        pixmap = QtGui.QPixmap(image_path).scaledToHeight(self.height)
        self.setPixmap(pixmap)
        
        if not self.orig_image_path == None and not self.orig_image_path == image_path:
            try:
                os.remove(self.orig_image_path)
            except:
                pass
            
        self.orig_image_path = image_path
        
    def update_qimage(self, qimage, height=0):
        if height != 0:
            self.set_height(height) 
            
        self.setPixmap(QtGui.QPixmap.fromImage(qimage).scaledToHeight(self.height))        
        self.orig_image_path = qimage
        #print('before ui',sys.getrefcount(qimage))
        #del(qimage)
    @QtCore.Slot(str)
    def change_image(self, image_path):
        self.__change_image.emit(image_path, 0)
    
    def change_qimage(self, qimage):
        self.__change_qimage.emit(qimage, 0)
        
    def mousePressEvent(self, event):    
        self.clicked.emit(self.id_)
