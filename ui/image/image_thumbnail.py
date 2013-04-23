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
from masbot.config.utils import Path

class ImageThumbnail(QtGui.QListWidget):

    thumbnail_clicked = QtCore.Signal(str)
    add_item_signal = QtCore.Signal(str)    # 內部用 (非GUI thread 要新增item時用的)

    def __init__(self, thumbnail_id):
        super(ImageThumbnail, self).__init__()
        self.init_ui(thumbnail_id)
        
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        
        self.setMaximumHeight(109)
        self.setMaximumWidth(700)
        
        self.add_item_signal.connect(self.add_label)
        
        
    def init_ui(self, thumbnail_id):
        self.thumbnail = {}

        for id_ in thumbnail_id:
            self.add_label(id_)
        
        self.setFlow(QtGui.QListWidget.LeftToRight)
        self.setWindowTitle('Image thumbnail')
        self.show()

    def create_label_frame(self, id_, text):
        img_label = PixelMapLabel(id_)
        img_label.setContentsMargins(3, 0, 0, 0)    # 圖片偏左, 用margin往中間調
    
        img_label.clicked.connect(self.__thumbnail_clicked)                
        img_label.update_pixmap("{0}//Sunset.jpg".format(Path.imgs_dir()), 70)  # 預設圖片跟大小
        img_text = QtGui.QLabel(text)
        img_text.setContentsMargins(0,0,0,0)
        
        frame = QtGui.QFrame()        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(img_label)
        vbox.addWidget(img_text)
        vbox.setAlignment(img_text, QtCore.Qt.AlignCenter)
        vbox.setContentsMargins(0,2,0,0)
        frame.setLayout(vbox)
        frame.setFrameShape(QtGui.QFrame.StyledPanel)

        return [frame, img_label, img_text]        
    
    def add_label(self, id_):
        index = len(self.thumbnail)                 # 儲存 key = id_, value =[label,index]

        (frame, img_label, text_label) = self.create_label_frame(id_, 'Default')        
                
        item = QtGui.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(100,85))      # 每個item的大小
        self.addItem(item)
        self.setItemWidget(item, frame)
        
        if not self.thumbnail.get(id_):
            self.thumbnail[id_] = [img_label, index, text_label]    # 1. label, 2. index, 3.name
        
    def __thumbnail_clicked(self, thumbnail_id):
        index = self.thumbnail[thumbnail_id][1]     # 1 是index
        self.item(index).setSelected(True)          # 設定選擇的label (在listwidget上這個item會反白)
        self.thumbnail_clicked.emit(thumbnail_id)
    
    def change_image(self, image_data):        
        (image_path, id_, name) = image_data
        if not id_ :
            return
        
        if not self.thumbnail.get(id_):
            self.add_item_signal.emit(id_)  # 新增一個image label
        else:            
            self.thumbnail[id_][0].change_image(image_path) # 0 是 檔案路徑
            self.thumbnail[id_][2].setText(name)            # 2 是 名稱
        
    def change_qimage(self, qimage, id_):
        if not id_ :
            return
        
        if not self.thumbnail.get(id_):
            self.add_item_signal.emit(id_)            
        else:
            self.thumbnail[id_][0].change_qimage(qimage)    

def main():
    app = QtGui.QApplication(sys.argv)
    ex = ImageThumbnail(['1', '2', '3'])
    app.exec_()

if __name__ == '__main__':
    main()        