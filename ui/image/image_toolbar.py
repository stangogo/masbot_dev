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
from masbot.ui.utils import Path

class ButtonName:
    camera = 'camera_id'
    previous = 'previous_id'
    next_ = 'next_id'
    zoom_in = 'zoom_in_id'
    zoom_out = 'zoom_out_id'

class ToolBarButton(QtGui.QPushButton):
            
    def __init__(self, *args):
        if len(args)>0:
            self.id_ = args[-1] # 最後一個element
                
        super(ToolBarButton, self).__init__(*args[:-1])     # args[:-1] :全部項目, 除了最後一個

class ImageToolbar(QtGui.QWidget):

    file_selected = QtCore.Signal(str)
    button_clicked = QtCore.Signal(str)

    def __init__(self):
        super(ImageToolbar, self).__init__()        
        self.init_ui()
        #self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        
        self.setMaximumHeight(50)
        self.setMaximumWidth(700)
        
    def init_ui(self):
        tools_bar_layout = QtGui.QHBoxLayout()
        tools_bar_layout.addStretch()
        
        #camera_btn = QtGui.QPushButton('Camera')
        camera_btn = ToolBarButton('Camera', 'camera_id')
        camera_btn.clicked.connect(self.clicked)
        previous_btn = ToolBarButton('Previous', 'previous_id')
        previous_btn.clicked.connect(self.clicked)
        next_btn = ToolBarButton('Next', 'next_id')
        next_btn.clicked.connect(self.clicked)

        imgs_dir = Path.imgs_dir()                
        #zoom-in button        
        zoom_in_btn = ToolBarButton(QtGui.QIcon("{0}//zoom-in.png".format(imgs_dir)), "", 'zoom_in_id')
        zoom_in_btn.setFlat(True)
        zoom_in_btn.clicked.connect(self.clicked)
        
        #zoom-out button
        zoom_out_btn = ToolBarButton(QtGui.QIcon("{0}//zoom-out.png".format(imgs_dir)), "", 'zoom_out_id')
        zoom_out_btn.setFlat(True)
        zoom_out_btn.clicked.connect(self.clicked)
        
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

        self.setLayout(tools_bar_layout)
        self.setWindowTitle('Image toolbar')
        self.show()
        
    def clicked(self):
        sender = self.sender()
        self.button_clicked.emit(sender.id_)

    def open_file_dialog(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '/home','Images (*.png *.bmp *.jpg)')
        try:
            if isinstance(file_name[0], str) and file_name[0]:
                self.file_path_edit.setText(file_name[0])                
                self.file_selected.emit(file_name[0])
        except:
            pass
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = ImageToolbar()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        