#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
website: zetcode.com 
last edited: Mar. 2013
"""

import sys
from PySide import QtGui, QtCore

from masbot.ui.utils import Path

class DIOButton(QtGui.QPushButton):
    bOn = False
    io_number = -1    
    
    def __init__(self, io_num):
        super(DIOButton, self).__init__()
        self.clicked.connect(self.on_clicked)
        imgs_dir = Path.imgs_dir()
        self.on_img = "{0}/Start.bmp".format(imgs_dir)
        self.off_img = "{0}/Stop.bmp".format(imgs_dir)
        self.on_off(self.bOn)
        self.setText("%d" % io_num)
        
        self.setToolTip('This is a <b>QPushButton</b> widget')
        self.resize(self.sizeHint())
        
        self.resize(20,20)
        self.setCheckable(True)
        
        self.setAutoFillBackground(True)
        
        
    def on_clicked(self):
        self.bOn = not self.bOn
        self.on_off(self.bOn)
    
    def on_off(self, on):
        if on:
            self.setStyleSheet("background-color: rgb(255, 0, 0)")
            self.setIcon(QtGui.QIcon(self.on_img))
        else: 
            #self.setStyleSheet("background-color: rgb(255, 255, 0); color: rgb(255, 255, 255)")
            self.setStyleSheet("background-color: rgb(150, 201, 100)")
            self.setIcon(QtGui.QIcon(self.off_img))   
            

class DIOLabel(QtGui.QLabel):
    bOn = False
    io_number = -1    
    clicked = QtCore.Signal(str) # can be other types (list, dict, object...)
    
    def __init__(self, io_num):
        super(DIOLabel, self).__init__()
        imgs_dir = Path.imgs_dir()
        self.on_img = "{0}/Start.bmp".format(imgs_dir)
        self.off_img = "{0}/Stop.bmp".format(imgs_dir)
        
        self.setAlignment(QtCore.Qt.AlignLeft)
        #self.setText("%d" % io_num)
        self.on_off(self.bOn)
        
        #self.setToolTip('This is a <b>QPushButton</b> widget')
        #self.resize(self.sizeHint())
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        #self.setAutoFillBackground(True)
        
    def on_clicked(self):
        self.bOn = not self.bOn
        self.on_off(self.bOn)
    
    def on_off(self, on):
        if on:
            #self.setStyleSheet("background-color: rgb(150, 201, 100)")            
            #self.setPixmap(QtGui.QPixmap(self.on_img))
            self.setPixmap(self.on_img)
        else: 
            #self.setStyleSheet("background-color: rgb(255, 255, 0); color: rgb(255, 255, 255)")
            #self.setPixmap(QtGui.QPixmap(self.off_img))   
            self.setPixmap(self.off_img)

    def mousePressEvent(self, event):    
        self.clicked.emit("emit the signal")
        self.on_clicked()


class MsgIn():
    speak_number = QtCore.Signal(int, bool)

class IOMap(QtGui.QWidget):
    
    def __init__(self):
        super(IOMap, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):
        do_combobox = QtGui.QComboBox()
        di_combobox = QtGui.QComboBox()
        card_num = 5
        for i in range(0, card_num):
            do_combobox.addItem("DO_{0} Card".format(i+1))
            di_combobox.addItem("DI_{0} Card".format(i+1))            
        do_combobox.currentIndexChanged.connect(self.do_changed)
        di_combobox.currentIndexChanged.connect(self.di_changed)
                  
        self.di_stacklayout = QtGui.QStackedLayout()
        self.do_stacklayout = QtGui.QStackedLayout()
        
        for card_index in range(0, card_num):
            do_grid = QtGui.QGridLayout()
            do_grid.setVerticalSpacing(3)   # row的間距
            do_grid.setHorizontalSpacing(8)  # column的間距
            
            di_grid = QtGui.QGridLayout()
            di_grid.setVerticalSpacing(3)   # row的間距
            di_grid.setHorizontalSpacing(8)  # column的間距                
            
            col_len = 16
            io_num = 64
            for i in range(0, io_num):
                row = (int)(i/col_len) * 2
                number = io_num * card_index + i
                do_grid.addWidget(QtGui.QLabel("{0}".format(number)), row, i % col_len)
                do_grid.addWidget(DIOLabel(number), row + 1, i % col_len)
                
                di_grid.addWidget(QtGui.QLabel("{0}".format(number)), row, i % col_len)
                di_grid.addWidget(DIOLabel(number), row + 1, i % col_len)
            
            #self.do_stacklayout.addWidget(QtGui.QWidget().setLayout(do_grid))
            #self.di_stacklayout.addWidget(QtGui.QWidget().setLayout(di_grid))
     
        self.v_layout = QtGui.QVBoxLayout()
        
        self.v_layout.addWidget(do_combobox)
        self.v_layout.addLayout(self.do_stacklayout)
        self.v_layout.addWidget(di_combobox)
        self.v_layout.addLayout(self.di_stacklayout)

        self.v_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.setLayout(self.v_layout)
                
        self.setWindowTitle('IO Map')
        self.show()
        
    def do_changed(self, index):
        pass
    def di_changed(self, index):        
        self.di_stacklayout.setCurrentIndex(index)
        
            
            
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = IOMap()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        