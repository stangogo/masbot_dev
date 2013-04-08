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
from masbot.ui.image.image_tools_dock import ImageToolsDock
from masbot.ui.image.image_thumbnail import ImageThumbnail


class ImageWidget(QtGui.QWidget):

    imgs_dir = ""   # the dir placed the images for UI    
    
    def __init__(self):
        super(ImageWidget, self).__init__()
        
        self.init_ui()
        
    def open_file_dialog(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '/home','Images (*.png *.xpm *.jpg)')
        #self.file_path_edit.setText(file_name.)
        
    def start_change_img(self):
        threading.Thread(target = self.threadFunc).start()
        
    def stop_change_img(self):
        self.stop_thread = True
        
    def threadFunc(self):
        self.stop_thread = False
        index = 0
        
        while self.stop_thread == False:
            index = (index + 1) % 15        
            image_path = "{0}\\{1}.tif".format( self.imgs_dir, index + 1)
            
            self.preview_label.change_image(image_path)
            self.img_thumbnail.change_image(image_path, 0)
            self.img_thumbnail.change_image(image_path, 1)
            self.img_thumbnail.change_image(image_path, 2)
            self.img_thumbnail.change_image(image_path, 3)
            self.img_thumbnail.change_image(image_path, 4)
            self.img_thumbnail.change_image(image_path, 5)
            
            
            time.sleep(0.1)
        
    def init_ui(self):

        v_layout = QtGui.QVBoxLayout(self)
        
        self.imgs_dir = os.path.abspath(__file__ + "//..//")+"//Imgs"

        #preview image
        self.preview_label = PixelMapLabel(0) #QtGui.QLabel()
        self.preview_label.update_pixmap("{0}//Water_lilies.jpg".format(self.imgs_dir))
        
        #pixel_map = QtGui.QPixmap('Imgs\\Sunset.jpg').scaledToHeight(400)
        #preview_label.setPixmap(pixel_map)
        
        #tool bar
        tools_bar_layout = QtGui.QHBoxLayout()
        tools_bar_layout.addStretch()
        
        #camera button
        camera_btn = QtGui.QPushButton('Camera')
        
        #previous button 
        previous_btn = QtGui.QPushButton('Previous')
        
        #next button
        next_btn = QtGui.QPushButton('Next')
        
        #zoom-in button        
        zoom_in_btn = QtGui.QPushButton(QtGui.QIcon("{0}//zoom-in.png".format(self.imgs_dir)), "")
        zoom_in_btn.setFlat(True)
        zoom_in_btn.clicked.connect(self.start_change_img)
        
        #zoom-out button
        zoom_out_btn = QtGui.QPushButton(QtGui.QIcon("{0}//zoom-out.png".format(self.imgs_dir)), "")
        zoom_out_btn.setFlat(True)
        zoom_out_btn.clicked.connect(self.stop_change_img)
        
        #show open file dialog button
        open_file_btn = QtGui.QPushButton('Open File')
        open_file_btn.clicked.connect(self.open_file_dialog)
        
        #selected file path
        self.file_path_edit = QtGui.QLineEdit('d:\\Image\\IPI\\123.tif')

        
        tools_bar_layout.addWidget(camera_btn, 0, QtCore.Qt.AlignLeft)
        tools_bar_layout.addWidget(previous_btn, 0, QtCore.Qt.AlignLeft)
        tools_bar_layout.addWidget(next_btn, 0, QtCore.Qt.AlignLeft)
        tools_bar_layout.addWidget(zoom_in_btn, 0, QtCore.Qt.AlignLeft)
        tools_bar_layout.addWidget(zoom_out_btn, 0, QtCore.Qt.AlignLeft)
        tools_bar_layout.addWidget(open_file_btn, 0, QtCore.Qt.AlignLeft)
        tools_bar_layout.addWidget(self.file_path_edit, 1, QtCore.Qt.AlignLeft)

        #Image List
        self.img_thumbnail = ImageThumbnail()
        self.img_thumbnail.thumbnail_clicked.connect(self.thumbnail_clicked)
        
        #IPI result table (方法1)
        image_tools = ImageToolsDock()
     
        v_layout.addWidget(self.preview_label)
        v_layout.addLayout(tools_bar_layout)
        v_layout.addWidget(self.img_thumbnail)
        v_layout.addWidget(image_tools)

        self.setLayout(v_layout)
        
        #self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Image Vertical Layout')
        self.show()
        
    def thumbnail_clicked(self, thumbnail_index):
        print("thumbnail {0} is clicked".format(thumbnail_index))

            
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = ImageWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        