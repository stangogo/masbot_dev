#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: Mar. 2013
"""
import sys
from PySide import QtGui, QtCore

from masbot.config.utils import Path, SigName, UISignals

class DIOColor():
    green = 'font: 11px; background-color:qradialgradient(cx:0, cy:0, radius: 1, fx:0.3, fy:0.3, stop:0 white, stop:1 green); border: 1px solid #C4C4C3; border-radius: $size$px;'
    orange = 'font: 11px; background-color:qradialgradient(cx:0, cy:0, radius: 1, fx:0.3, fy:0.3, stop:0 white, stop:1 orange); border: 1px solid #C4C4C3; border-radius: $size$px;'
    gray_green = 'font: 11px; background-color:qradialgradient(cx:0, cy:0, radius: 1, fx:0.3, fy:0.3, stop:0 white, stop:1 gray); border: 1px solid green; border-radius: $size$px;'
    gray_orange = 'font: 11px; background-color:qradialgradient(cx:0, cy:0, radius: 1, fx:0.3, fy:0.3, stop:0 white, stop:1 gray); border: 1px solid orange; border-radius: $size$px;'
    

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
        if io_num >= 0:
            self.setText("%d" % io_num)
                
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)                
        self.set_size(24)
        
        self.on_off(False)
        self.setAutoFillBackground(True)
                
    def set_size(self, edge):
        self.setFixedWidth(edge)
        self.setFixedHeight(edge)       
        
        # 強迫更新stylesheet
        self.nOn = not self.nOn 
        self.on_off(not self.nOn)
        
        
    def on_clicked(self):        
        self.on_off(not self.nOn)
    
    def on_off(self, on):
        if self.nOn == on:
            return    
        self.nOn = on
        if on:                  #light on
            self.setStyleSheet(self.on_style.replace('$size$', '{0}'.format(int(self.size().width()/2))) )
            if not self.isChecked() and self.isCheckable():
                self.setChecked(True)
        else:
            self.setStyleSheet(self.off_style.replace('$size$', '{0}'.format(int(self.size().width()/2))) )
            if self.isChecked() and self.isCheckable():
                self.setChecked(False)
            
    def set_style(self, do):
        """
        設定DO 或 DI 的背景和文字style.
        """
        #imgs_dir = Path.imgs_dir()
        #off_img = "font: 10px;background-color: transparent ; border-image: url({0}/Grey Ball.png);".format(imgs_dir)
        #off_img = off_img.replace('\\', '/' )
        
        if do :
            # do_on_img = "font: 10px;background-color: transparent ; border-image: url({0}/Green Ball.png);".format(imgs_dir)
            on_img = DIOColor.green #'background-color:qradialgradient(cx:0, cy:0, radius: 1, fx:0.3, fy:0.3, stop:0 white, stop:1 green); border: 1px solid #C4C4C3; border-radius: 13px;'
            off_img = DIOColor.gray_green
            # do_on_img = do_on_img.replace('\\', '/' )                    
            
            
            
        else :
            #di_on_img = " font: 10px; background-color: transparent ; border-image: url({0}/Red Ball.png);".format(imgs_dir)
            on_img = DIOColor.orange # 'background-color:qradialgradient(cx:0, cy:0, radius: 1, fx:0.3, fy:0.3, stop:0 white, stop:1 orange); border: 1px solid #C4C4C3; border-radius: 13px;'
            #di_on_img = di_on_img.replace('\\', '/' )            
            off_img = DIOColor.gray_orange
            #self.on_style = "QPushButton{%s}" % on_img
        
        self.on_style = "QPushButton{%s}" % on_img
        self.off_style = "QPushButton{%s}"% off_img 

class DIOLabel(QtGui.QLabel):
    nOn = 1
    io_num = -1
    # key = ""            #屬誰
    action =""          #動作; blow, suck, up/down ...etc.    
    
    def __init__(self, text, do):
        super(DIOLabel, self).__init__()
        
        self.set_style(do)
        self.setText(text)
        self.on_off(False)

        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.set_size(24)
        self.setAutoFillBackground(True)
        
        
    def set_size(self, edge):
        self.setFixedWidth(edge)
        self.setFixedHeight(edge)          
        
        # 強迫更新stylesheet
        self.nOn = not self.nOn
        self.on_off(not self.nOn)

    def set_style(self, do):
        self.setAlignment(QtCore.Qt.AlignCenter)
        
        imgs_dir = Path.imgs_dir()
        if do :
            on_img = DIOColor.green            
            off_img = DIOColor.gray_green
        else :
            on_img = DIOColor.orange
            off_img = DIOColor.gray_orange
            
            
        #off_img = "background-color: transparent ; border-image: url({0}/Grey Ball.png);".format(imgs_dir)
        #off_img = off_img.replace('\\', '/' )
        
        self.on_style = "QLabel{%s}" % on_img
        
        self.off_style = "QLabel{%s}"% off_img 
    
    def set_properties(self, key, action):
        # self.key = key
        self.action = action    
    
    def on_off(self, on):
        if on == self.nOn:
            return
        
        self.nOn = on
        if on:      #用邊長的一半做border的radius, 可做出圓形的效果
            self.setStyleSheet(self.on_style.replace('$size$', '{0}'.format(int(self.size().width()/2))) )
        else: 
            self.setStyleSheet(self.off_style.replace('$size$', '{0}'.format(int(self.size().width()/2))) )

    #def on_clicked(self):
        #self.nOn = not self.nOn
        #self.on_off(self.nOn)

    #def mousePressEvent(self, event):    
        #self.clicked.emit("emit the signal")
        #self.on_clicked()




class ButtonForTableSignal(QtCore.QObject):
    """ 建立這個Signal 和 ButtonForTable clicked 間的連結
        在原來的clicked被觸發時, 由此Signal送出更多參數
        
    """
    clicked = QtCore.Signal(int, bool, int, int, str)  #io_num, on or off, row, column, table_name

class ButtonForTable(QtGui.QPushButton):
    nOn = 1
    io_num = -1    
    __on_str = "On"
    __off_str ="Off"
    #key = ""            #屬誰
    action =""          #動作; blow, suck, up/down ...etc.
    row = -1
    column = -1
    table = ''
   
    signals = QtCore.Signal(int, bool, int, int, str) # ButtonForTableSignal()
    
    #def __new__(self, io_num=None):
        #if icon == None:
            #return QtGui.QPushButton.__new__(self, self.__on_str)
        #else:
            #return QtGui.QPushButton.__new__(self, icon, self.__on_str)
        
    def __init__(self, io_num, table):
        super(ButtonForTable, self).__init__()
        self.io_num = io_num
        self.clicked.connect(self.on_clicked)
        self.on_off(False)
        self.table = table
        self.setMaximumWidth(58)
        
    def set_properties(self, on_str, off_str, key, action):
        self.__on_str = on_str
        self.__off_str = off_str
        # self.key = key
        self.action = action
        self.nOn = not self.nOn 
        
        self.on_off(not self.nOn)
    
    def set_row_column(self, row, colum):
        self.row = row
        self.column = colum
        
    def on_clicked(self):        
        self.signals.emit(self.io_num, not self.nOn, self.row, self.column, self.table)
        #self.on_off(not self.nOn)
    
    def on_off(self, on):
        if self.nOn == on:
            return
        
        self.nOn = on
        if on:
            self.setText(self.__on_str)
            if not self.__on_str == self.__off_str: #當 on 和 off 字串都一樣時, 表示button 不需要顏色變化
                self.setStyleSheet('QPushButton{background-color:lightgreen}')
        else: 
            self.setText(self.__off_str)
            self.setStyleSheet('QPushButton{background-color:white}')
        
        #self.signals.emit(self.io_num, on, self.row, self.column, self.table)

