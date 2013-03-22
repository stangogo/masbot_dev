#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from abc import ABCMeta, abstractmethod

from collections import OrderedDict
"""

"""
    
class Signals(QtCore.QObject):
    """    
    訊息傳入AxisTable.
    """
    speak = QtCore.Signal(str, str, int)
    """
    row     - string.    定義在 db_table_def.py 裡的 AxisOP 
    column  - string     定義在database 的 SingleAxis 資料表裡的 axis_key 欄
    value   - 填入的值
    """

class IAxisTable:
    """
    抽象類別. 定義 AxisTable 所需Signal
    and Slot, 用以和外界溝通
    """
    __metaclass__ = ABCMeta
    msg_in = Signals()

    #接收AxisTable傳出來的值
    #@axis: 單軸名稱, 字串, 定義在database 的 SingleAxis 資料表裡的 axis_key 欄
    #@value: 移動距離
    #@action: 動作, 1: add, -1: minus
    @abstractmethod 
    def from_axis_table(self, axis, value, action):
        pass
   
    #傳入AxisTable
    def enter_axis_table(self, row, axis, value): 
        self.msg_in.speak.emit(row, axis, value)
   
     
class IAxisTableObj(IAxisTable):
    """
    繼承 IAxisTable 的示範類別. 用來接收 AxisTable 傳出來的值
    """
    def from_axis_table(self, axis, value, action):
        print("column: {0}, value: {1}".format(axis, value))
        self.enter_axis_table('position', axis, value)
           