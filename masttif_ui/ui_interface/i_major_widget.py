#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from abc import ABCMeta, abstractmethod

"""
i_major_widget 定義了 MajorWidget 與外界溝通界面的類別
有Signals, IRobotMajor 和 IRobotMajorObj 三個類別
"""
class Signals(QtCore.QObject):
    """
    三個Signals, 分別做為 MajorWidget 的 flow message, 
    alarm message and product info (tray infomation) 
    的訊息傳入.
    """
    flow_speak = QtCore.Signal(str)
    alarm_speak = QtCore.Signal(str)
    product_info_speak = QtCore.Signal(dict)

class IMajorWidget:
    """
    抽象類別. 定義 MajorWidget 所需Signal 
    and Slot, 用以和外界溝通
    """
    __metaclass__ = ABCMeta    
    msg_in = Signals()

    @abstractmethod
    def login_clicked(self):
        pass
    
    @abstractmethod
    def servo_on_clicked(self):
        pass
    
    @abstractmethod
    def pause_clicked(self):
        pass
    
    @abstractmethod
    def start_clicked(self):
        pass
        
    def flow_msg(self, str):
        self.msg_in.flow_speak.emit(str)
        
    def alarm_msg(self, str):
        self.msg_in.alarm_speak.emit(str)
    
    def product_info_msg(self, dict):
        self.msg_in.product_info_speak.emit(dict)    
    
     
class IRobotMajorObj(IMajorWidget):
    """
    繼承IRobotMajor的示範類別. 用來接收 MajorWidget 
    四個按鈕的click event.

    """
    def login_clicked(self):
        print('login is clicked')
        
    def servo_on_clicked(self):
        print('servo on clicked')
        self.flow_msg('flow message from interface')

    def pause_clicked(self):
        print('pause is clicked')
        self.alarm_msg('alarm message from interface')
        
    def start_clicked(self):     
        print('start is clicked')
        self.product_info_msg({ 'CT': 4.25, 
                                'ProdName': '9552A1', 
                                'MatchAngle':3.11, 
                                'AssembleMode': 'manually', 
                                'ProdBarCode': 'A222dsd323', 
                                'ProdNum': '11op98733', 
                                'Total': 200})
