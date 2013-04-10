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


#class ImageThumbnail(QtGui.QWidget):

    #thumbnail_clicked = QtCore.Signal(str)

    #def __init__(self, thumbnail_id):
        #super(ImageThumbnail, self).__init__()
        #self.init_ui(thumbnail_id)
        
        #self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        
        #self.setMaximumHeight(100)
        #self.setMaximumWidth(700)
        
        ##self.setMinimumHeight(80)
        
    #def init_ui(self, thumbnail_id):

        #h_layout = QtGui.QHBoxLayout()
        #h_layout.addStretch(0)
        
        
        #self.thumbnail = {}

        #for id_ in thumbnail_id:
            #self.add_label(id_, h_layout)
        
        ##self.setFlow(QtGui.QListWidget.LeftToRight)
        #self.setLayout(h_layout)
        #self.setWindowTitle('Image thumbnail')
        #self.show()
    
    #def add_label(self, id_, layout):
        #index = len(self.thumbnail)
        #img_label = PixelMapLabel(id_)
        #img_label.setContentsMargins(3, 0, 0, 0)    #圖片偏左, 用margin往中間調
    
        #img_label.clicked.connect(self.__thumbnail_clicked)
        
        #img_label.update_pixmap("{0}//Sunset.jpg".format(Path.imgs_dir()), 70)
                
        ##item = QtGui.QListWidgetItem()
        ##item.setSizeHint(QtCore.QSize(100,75))  # 每個item的大小
        ##self.addItem(item)
        ##self.setItemWidget(item, img_label)
        #layout.addWidget(img_label)
        #self.thumbnail[id_] = [img_label, index]    #第一欄是label, 這二欄是index        
        
    #def __thumbnail_clicked(self, thumbnail_id):
        #index = self.thumbnail[thumbnail_id][1]     #第二欄是index
        #self.item(index).setSelected(True)
        #self.thumbnail_clicked.emit(thumbnail_id)
    
    #def change_image(self, image_path, id_):
        #if not id_ :
            #return
        
        #if not self.thumbnail.get(id_):
            #self.add_label(id_)
        
        #self.thumbnail[id_][0].change_image(image_path)



class ImageThumbnail(QtGui.QListWidget):

    thumbnail_clicked = QtCore.Signal(str)

    def __init__(self, thumbnail_id):
        super(ImageThumbnail, self).__init__()
        self.init_ui(thumbnail_id)
        
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        
        self.setMaximumHeight(100)
        self.setMaximumWidth(700)
        
        #self.setMinimumHeight(80)
        
    def init_ui(self, thumbnail_id):

        h_layout = QtGui.QHBoxLayout()
        h_layout.addStretch(0)
        
        
        self.thumbnail = {}

        for id_ in thumbnail_id:
            self.add_label(id_)
        
        self.setFlow(QtGui.QListWidget.LeftToRight)
        self.setWindowTitle('Image thumbnail')
        self.show()
    
    def add_label(self, id_):
        index = len(self.thumbnail)
        img_label = PixelMapLabel(id_)
        img_label.setContentsMargins(3, 0, 0, 0)    #圖片偏左, 用margin往中間調
    
        img_label.clicked.connect(self.__thumbnail_clicked)
        
        img_label.update_pixmap("{0}//Sunset.jpg".format(Path.imgs_dir()), 70)
                
        item = QtGui.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(100,75))  # 每個item的大小
        self.addItem(item)
        self.setItemWidget(item, img_label)
        self.thumbnail[id_] = [img_label, index]    #第一欄是label, 這二欄是index        
        
    def __thumbnail_clicked(self, thumbnail_id):
        index = self.thumbnail[thumbnail_id][1]     #第二欄是index
        self.item(index).setSelected(True)
        self.thumbnail_clicked.emit(thumbnail_id)
    
    def change_image(self, image_path, id_):
        if not id_ :
            return
        
        if not self.thumbnail.get(id_):
            self.add_label(id_)
        
        self.thumbnail[id_][0].change_image(image_path)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ImageThumbnail(['1', '2', '3'])
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        