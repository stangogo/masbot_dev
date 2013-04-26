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
from masbot.config.utils import Path
from masbot.config.utils import UISignals, SigName
from masbot.ui import preaction
from masbot.config.db_table_def import DBTableDefine


class ImageWidget(QtGui.QWidget):

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.init_ui()
        self.cur_preview_id = None
        self.previous_preview_id = None
        
        UISignals.GetSignal(SigName.IMG_THUMBNAIL).connect(self.img_thumbnail_income)
        
    def init_ui(self):
        imgs_dir = Path.imgs_dir()

        # Image thumbnail
        self.img_thumbnail = ImageThumbnail([])
        self.img_thumbnail.thumbnail_clicked.connect(self.thumbnail_clicked)
        self.img_thumbnail.setMinimumHeight(105)
        
        # preview image
        self.preview_label = PixelMapLabel(0) 
        self.preview_label.update_pixmap("{0}//zero.jpg".format(imgs_dir))
        self.preview_label.setMinimumHeight(400)
        
        # tool bar        
        #toolbar = ImageToolbar()
        #toolbar.file_selected.connect(self.file_selected)
        #toolbar.button_clicked.connect(self.toolbar_btn_clicked)
        
        image_utils_tab = ImageUtilsTab()
     
        v_layout = QtGui.QVBoxLayout(self)
        v_layout.addWidget(self.img_thumbnail)
        v_layout.addWidget(self.preview_label)
        #v_layout.addWidget(toolbar)
        
        v_layout.addWidget(image_utils_tab)

        v_layout.setAlignment(self.preview_label, QtCore.Qt.AlignCenter)
        
        self.setLayout(v_layout)
             
        self.setWindowTitle('Image Widget')
        self.show()
        
    def thumbnail_clicked(self, thumbnail_id):
        print("thumbnail {0} is clicked".format(thumbnail_id))
        self.cur_preview_id = thumbnail_id

    #def file_selected(self, file_path):        
        #UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit( [file_path, self.cur_preview_id, 'file selected'])
            
    #def toolbar_btn_clicked(self, button_id):
        #if button_id == 'zoom_in_id':
            #pass    # threading.Thread(target = self.threadFunc).start()
        #elif button_id == 'zoom_out_id':
            #self.stop_thread = True
        #elif button_id == 'previous_id':
            #self.img_thumbnail.change_image( ["r:\\temp\\9.bmp", '1', 'select by previous'])
        
 

    def img_thumbnail_income(self, image_data):
        (path, id_, name) = image_data
        
        if not id_:                             # id_ 為空或Nonoe - 顯示手動選擇的影像檔案
            self.preview_label.change_image(path)
            if self.cur_preview_id:
                self.previous_preview_id = self.cur_preview_id
                
            self.cur_preview_id = ''
        elif id_ == 'rollback':
            if self.previous_preview_id and not self.cur_preview_id:
                self.cur_preview_id = self.previous_preview_id
        else:
            if self.cur_preview_id == id_:
                self.preview_label.change_image(path)
            self.img_thumbnail.change_image(image_data)        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = ImageWidget()
    app.exec_()


if __name__ == '__main__':
    main()        