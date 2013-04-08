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
import time 


from PySide import QtGui, QtCore
from masbot.ui.image.pixelmap_label import PixelMapLabel
from masbot.ui.utils import Path



   

class ImageThumbnail(QtGui.QListWidget):

    thumbnail_clicked = QtCore.Signal(int)

    def __init__(self):
        super(ImageThumbnail, self).__init__()        
        self.init_ui()
        
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.setFixedHeight(100)
        self.setMaximumWidth(700)
        
        
        
    def init_ui(self):

        #Image List
        h_layout = QtGui.QHBoxLayout()
        h_layout.addStretch(0)
        imgs_dir = Path.imgs_dir()
        
        self.thumbnail = []
        for i in range(6):
            label = PixelMapLabel(i)
            label.setContentsMargins(3, 0, 0, 0)    #圖片偏左, 用margin往中間調
            self.thumbnail.append(label)
        
        for i in range(len(self.thumbnail)):
            self.thumbnail[i].clicked.connect(self.__thumbnail_clicked)
            self.thumbnail[i].update_pixmap("{0}//Sunset.jpg".format(imgs_dir), 70)
        
            myWidget = self.thumbnail[i]
            item = QtGui.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(100,70))  # 每個item的大小
            self.addItem(item)
            self.setItemWidget(item, myWidget)
            #h_layout.addWidget(self.thumbnail[i], 0, QtCore.Qt.AlignLeft)
        
        
        #h_layout.addWidget(self.thumbnail[len(self.thumbnail) -1], 1, QtCore.Qt.AlignLeft)  #stretch of last is 1        
        
        #self.setLayout(h_layout)
        self.setFlow(QtGui.QListWidget.LeftToRight)
        self.setWindowTitle('Image thumbnail')
        self.show()
        
    def __thumbnail_clicked(self, thumbnail_index):
        self.item(thumbnail_index).setSelected(True)
        #self.setCurrentIndex(thumbnail_index)
        self.thumbnail_clicked.emit(thumbnail_index)
    
    def change_image(self, image_path, index):
        if index > len(self.thumbnail):
            return 
        
        self.thumbnail[index].change_image(image_path)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ImageThumbnail()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        