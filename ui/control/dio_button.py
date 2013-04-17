#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: Mar. 2013
"""
import sys
from PySide import QtGui, QtCore

from masbot.config.utils import Path, SigName, UISignals

class DIOButton(QtGui.QPushButton):
    """
    提供客製化DIO的按鈕, 自行變化背景圖按被按下的時候
    DO模式, 可按, 為checkable型態.
    DI模式, 僅能透過函式呼叫變化。
    """
    nOn = 1
    io_num = -1
    
    def __init__(self, io_num, do):
        super(DIOButton, self).__init__()
        if do:  # di 不能按
            self.clicked.connect(self.on_clicked)
            self.setCheckable(True)
            
        self.io_num = io_num
        
        self.set_style(do)
        self.on_off(False)
        if io_num >= 0:
            self.setText("%d" % io_num)
                
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)                
        self.set_size(26, 26)
        
        self.setAutoFillBackground(True)
                
    def set_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)       
        
    def on_clicked(self):        
        self.on_off(not self.nOn)
    
    def on_off(self, on):
        if self.nOn == on:
            return    
        self.nOn = on
        if on:                  #light on
            self.setStyleSheet(self.on_style)
            if not self.isChecked() and self.isCheckable():
                self.setChecked(True)
        else:
            self.setStyleSheet(self.off_style)
            if self.isChecked() and self.isCheckable():
                self.setChecked(False)
            
    def set_style(self, do):
        """
        設定DO 或 DI 的背景和文字style.
        """
        
        imgs_dir = Path.imgs_dir()
        
        off_img = "font: 10px;background-color: transparent ; border-image: url({0}/Grey Ball.png);".format(imgs_dir)
        off_img = off_img.replace('\\', '/' )
        
        if do :
            do_on_img = "font: 10px;background-color: transparent ; border-image: url({0}/Green Ball.png);".format(imgs_dir)
            do_on_img = do_on_img.replace('\\', '/' )                    
            self.on_style = "QPushButton{%s}" % do_on_img
        else :
            di_on_img = " font: 10px; background-color: transparent ; border-image: url({0}/Red Ball.png);".format(imgs_dir)
            di_on_img = di_on_img.replace('\\', '/' )            
            self.on_style = "QPushButton{%s}" % di_on_img
            
        self.off_style = "QPushButton{%s}"% off_img 



class NozzleDOButtonSignal(QtCore.QObject):
    """ 建立這個Signal 和 NozzleDoButton clicked 間的連結
        在原來的clicked被觸發時, 由此Signal送出更多參數
        
    """
    clicked = QtCore.Signal(int, bool, int, int, str)  #io_num, on or off, row, column, table_name

class NozzleDoButton(QtGui.QPushButton):
    nOn = 1
    io_num = -1
    
    __on_str = "On"
    __off_str ="Off"
    key = ""            #屬誰
    action =""          #動作; blow, suck, up/down ...etc.
    row = -1
    column = -1
    table = ''
   
    signals = NozzleDOButtonSignal()
    
    #def __new__(self, io_num=None):
        #if icon == None:
            #return QtGui.QPushButton.__new__(self, self.__on_str)
        #else:
            #return QtGui.QPushButton.__new__(self, icon, self.__on_str)
        
    def __init__(self, io_num, table):
        super(NozzleDoButton, self).__init__()
        self.io_num = io_num
        self.clicked.connect(self.on_clicked)
        self.on_off(False)
        self.table = table
        
    def set_properties(self, on_str, off_str, key, action):
        self.__on_str = on_str
        self.__off_str = off_str
        self.key = key
        self.action = action
        self.nOn = not self.nOn 
        
        self.on_off(not self.nOn)
    
    def set_row_column(self, row, colum):
        self.row = row
        self.column = colum
    
        
    def on_clicked(self):        
        self.on_off(not self.nOn)
    
    def on_off(self, on):
        if self.nOn == on:
            return
        
        self.nOn = on
        if on:
            self.setText(self.__on_str)
        else: 
            self.setText(self.__off_str)
        
        self.signals.clicked.emit(self.io_num, on, self.row, self.column, self.table)

class DIOLabel(QtGui.QLabel):
    nOn = 1
    io_num = -1
    key = ""            #屬誰
    action =""          #動作; blow, suck, up/down ...etc.    
    
    #clicked = QtCore.Signal(str) # can be other types (list, dict, object...)
    
    def __init__(self, text, do):
        super(DIOLabel, self).__init__()
        
        self.set_style(do)
        self.setText(text)
        self.on_off(False)

        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.set_size(26, 26)
        self.setAutoFillBackground(True)
        
    def set_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)          

    def set_style(self, do):
        self.setAlignment(QtCore.Qt.AlignCenter)
        
        imgs_dir = Path.imgs_dir()
        if do :
            do_on_img = "background-color: transparent ; border-image: url({0}/Green Ball.png);".format(imgs_dir)
            do_on_img = do_on_img.replace('\\', '/' )                    
            self.on_style = "QLabel{%s}" % do_on_img
            
        else :
            di_on_img = "background-color: transparent ; border-image: url({0}/Red Ball.png);".format(imgs_dir)
            di_on_img = di_on_img.replace('\\', '/' )            
            self.on_style = "QLabel{%s}" % di_on_img
            
            
        off_img = "background-color: transparent ; border-image: url({0}/Grey Ball.png);".format(imgs_dir)
        off_img = off_img.replace('\\', '/' )
        self.off_style = "QLabel{%s}"% off_img 
    
    def set_properties(self, key, action):
        self.key = key
        self.action = action    
    
    def on_off(self, on):
        if on == self.nOn:
            return
        
        self.nOn = on
        if on:
            self.setStyleSheet(self.on_style)
        else: 
            self.setStyleSheet(self.off_style)

    #def on_clicked(self):
        #self.nOn = not self.nOn
        #self.on_off(self.nOn)

    #def mousePressEvent(self, event):    
        #self.clicked.emit("emit the signal")
        #self.on_clicked()


