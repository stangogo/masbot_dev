# Title          : PixelmapLabel.py
# Description    : Present a pixel map. Default height is 400.
#                  Using signal-slot to change the image
# Author         : Cigar Huang
# Date           : 20130307
# usage          : 
# notes          : 

import sys
import os
import logging
from PySide import QtGui, QtCore


class PixelMapLabel(QtGui.QLabel):
        
    height = 500
    clicked = QtCore.Signal(str)                # can be other types (list, dict, object...)        
    __change_image = QtCore.Signal(str, int)    #內部訊號, 通知更新圖片和大小; str: 圖檔路徑, int: 顯示大小 (height)
    __change_qimage = QtCore.Signal(str, QtGui.QImage)    #內部訊號, 通知更新圖片和大小; str: 圖檔路徑, int: 顯示大小 (height)
    
    def __init__(self, id_):
        super(PixelMapLabel, self).__init__()
        self.logger = logging.getLogger('ui.log')
        self.id_= id_
        self.orig_image_path = None
        self.__change_image.connect(self.update_pixmap)
        self.__change_qimage.connect(self.update_qimage)

    def set_height(self, height):
        self.height = height
    
    def update_pixmap(self, image_path, height=0):
        if not os.path.exists(image_path):
            return
        
        if height != 0:
            self.set_height(height)
        
        pixmap = QtGui.QPixmap(image_path).scaledToHeight(self.height)
        self.setPixmap(pixmap)
        
        #if not self.orig_image_path == None and not self.orig_image_path == image_path:
            #try:
                #os.remove(self.orig_image_path)
            #except:
                #pass
            
        self.orig_image_path = image_path
        
    def update_qimage(self, qimage, height=0):
        if height != 0:
            self.set_height(height)       
            
        pixmap = QtGui.QPixmap.fromImage(qimage).scaledToHeight(self.height)
        self.setPixmap(pixmap)
        
    @QtCore.Slot(str)
    def change_image(self, image_path):
        self.__change_image.emit(image_path, 0)
    
    def change_qimage(self, qimage):
        self.__change_qimage.emit(qimage, 0)
        
    def mousePressEvent(self, event):    
        self.clicked.emit(self.id_)

#class PixelMapWidget(QtGui.QWidget):
    #def __init__(self, index, name):
        #super(PixelMapWidget, self).__init__()
        #self.init_ui(index, name)
    
    #def init_ui(self, index, name):
        #v_layout = QtGui.QVBoxLayout()
        #self.img_label = PixelMapLabel(index)
        #self.name_text = QtGui.QLabel(name)
        
        #v_layout.addWidget(self.img_label, QtCore.Qt.AlignCenter)
        #v_layout.addWidget(self.name_text, QtCore.Qt.AlignCenter)
        
        #self.setLayout(v_layout)

    #def set_height(self, height):
        #self.img_label.height = height
      
    #def update_pixmap(self, image_path, height=0):        
        #self.img_label.update_pixmap(image_path, height)
          
    #def change_image(self, image_path):        
        #self.img_label.change_image(image_path)