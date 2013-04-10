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
#from masbot.ui.image.image_thumbnail import ImageThumbnail
from masbot.ui.image.image_toolbar import ImageToolbar
from masbot.ui.utils import Path
from masbot.ui.utils import UISignals, SigName
from masbot.ui import preaction
from masbot.ui.db_table_def import DBTableDefine
from masbot.ui.test.temp import ImageThumbnail

class ImageWidget(QtGui.QWidget):

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.init_ui()
        self.cur_preview_id = None
        UISignals.GetSignal(SigName.IMG_THUMBNAIL).connect(self.img_thumbnail_income)
        
    def init_ui(self):
        imgs_dir = Path.imgs_dir()

        # preview image
        self.preview_label = PixelMapLabel(0) 
        self.preview_label.update_pixmap("{0}//Water_lilies.jpg".format(imgs_dir))
        self.preview_label.setMinimumHeight(400)
        
        # tool bar        
        toolbar = ImageToolbar()
        toolbar.file_selected.connect(self.file_selected)
        toolbar.button_clicked.connect(self.toolbar_btn_clicked)
        
        # Image thumbnail
        #self.img_thumbnail = ImageThumbnail( DBTableDefine().get_table_def('ImageThumbnailID') )
        self.img_thumbnail = ImageThumbnail( ['1','2','3','4','5','6','7','8','9', '10'] )
        self.img_thumbnail.thumbnail_clicked.connect(self.thumbnail_clicked)
        
        #IPI result table (方法1)
        image_utils_tab = ImageUtilsTab()
     
        v_layout = QtGui.QVBoxLayout(self)
        v_layout.addWidget(self.preview_label)
        v_layout.addWidget(toolbar)
        v_layout.addWidget(self.img_thumbnail)
        v_layout.addWidget(image_utils_tab)

        self.setLayout(v_layout)
             
        self.setWindowTitle('Image Widget')
        self.show()
        
    def thumbnail_clicked(self, thumbnail_id):
        print("thumbnail {0} is clicked".format(thumbnail_id))
        self.cur_preview_id = thumbnail_id

    def file_selected(self, file_path):        
        UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit(file_path, self.cur_preview_id)        
            
    def toolbar_btn_clicked(self, button_id):
        if button_id == 'zoom_in_id':
            threading.Thread(target = self.threadFunc).start()
        elif button_id == 'zoom_out_id':
            self.stop_thread = True
        elif button_id == 'previous_id':
            self.img_thumbnail.change_image("r:\\temp\\9.bmp", '1')
            
        
        
    def threadFunc(self):
        self.stop_thread = False
        index = 0
        imgs_dir = 'R:\TEMP'#Path.imgs_dir()
        
        while self.stop_thread == False:
            index = (index + 1) % 15
            image_path = "{0}\\{1}.tif".format( imgs_dir, index + 1)
            
            self.preview_label.change_image(image_path)
            self.img_thumbnail.change_image(image_path, '1')
            
            index = self.change_thumbnail_image(index, '2')
            index = self.change_thumbnail_image(index, '3')
            index = self.change_thumbnail_image(index, '4')
            index = self.change_thumbnail_image(index, '5')
            index = self.change_thumbnail_image(index, '6')
            index = self.change_thumbnail_image(index, '7')
            index = self.change_thumbnail_image(index, '8')
            index = self.change_thumbnail_image(index, '9')
            index = self.change_thumbnail_image(index, '10')

            
            time.sleep(0.1)
    
    def change_thumbnail_image(self, index, id_):
        imgs_dir = 'R:\TEMP'
        index = (index + 1) % 15
        image_path = "{0}\\{1}.tif".format( imgs_dir, index + 1)
        self.img_thumbnail.change_image(image_path, id_)
        return index 
        
    def img_thumbnail_income(self, file_path, id_):
        self.img_thumbnail.change_image(file_path, id_)
        if self.cur_preview_id == id_:
            self.preview_label.change_image(file_path)
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = ImageWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        