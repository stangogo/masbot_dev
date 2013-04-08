# Title          : PixelmapLabel.py
# Description    : Present a pixel map. Default height is 400.
#                  Using signal-slot to change the image
# Author         : Cigar Huang
# Date           : 20130307
# usage          : 
# notes          : 

import sys
import logging
from PySide import QtGui, QtCore


class PixelMapLabel(QtGui.QLabel):
    
    image_index = 0
    height = 400
    clicked = QtCore.Signal(int)                # can be other types (list, dict, object...)        
    __change_image = QtCore.Signal(str, int)    #內部訊號, 通知更新圖片和大小; str: 圖檔路徑, int: 顯示大小 (height)
    
    def __init__(self, index):
        super(PixelMapLabel, self).__init__()
        self.logger = logging.getLogger('ui.log')
        self.index = index
        self.__change_image.connect(self.update_pixmap)

    def set_height(self, height):
        self.height = height
    
    def update_pixmap(self, image_path, height=0):
        if height != 0:
            self.set_height(height)            
        pixmap = QtGui.QPixmap(image_path).scaledToHeight(self.height)
        self.setPixmap(pixmap)
        
    @QtCore.Slot(str)
    def change_image(self, image_path):
        self.__change_image.emit(image_path, 0)
        
    def mousePressEvent(self, event):    
        self.clicked.emit(self.index)
           