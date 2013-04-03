#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtCore, QtGui
from masbot.ui.utils import UISignals, SigName



class SigAgent(QtCore.QObject):
    di_in = QtCore.Signal(list, bool)
    """
    external DI signals - the index of list is the port number of DI, 
                          and the value means on or off. If the number
                          of list only one. The value presents the port
                          number of DI and bool is the status.
    @ list: DI port status
    @ on_off: on or off (True or False)
    
    #"""
    
    do_in = QtCore.Signal(list, bool)
    """
    external DO signal 
    @ list: DO port staus
    @ on_off: on or off (True or False)
    
    #"""
    
    do_out = QtCore.Signal(int, bool)
    
    
    into_single_axis = QtCore.Signal(str, str, float)
    """
    row     - string.    定義在 db_table_def.py 裡的 AxisOP 
    column  - string     定義在database 的 SingleAxis 資料表裡的 axis_key 欄
    value   - 填入的值
    """
    out_single_axis = QtCore.Signal(str, float, int)
    """axis name, value, action (1: add, -1: minus) """
    

def do_out_msg(io_num, on_off): # 測試用
    pass
    #print('{0} : {1} : {2}'.format(SigName.DO_OUT, io_num, on_off))
    #do_status = [io_num]
    #UISignals.GetSignal(SigName.DO_IN).emit(do_status, on_off)

def out_single_axis(axis_name, value, n_action):
    if n_action == 1:
        print('{0} 多 {1}'.format(axis_name, value))
    else:
        print('{0} 少 {1}'.format(axis_name, value))

sig_agent = SigAgent()

UISignals.RegisterSignal(sig_agent.di_in, SigName.DI_IN)
UISignals.RegisterSignal(sig_agent.do_in, SigName.DO_IN)
UISignals.RegisterSignal(sig_agent.do_out, SigName.DO_OUT)

UISignals.RegisterSignal(sig_agent.into_single_axis, SigName.ENTER_AXIS_TABLE)
UISignals.RegisterSignal(sig_agent.out_single_axis, SigName.FROM_AXIS_TABLE)

UISignals.GetSignal(SigName.FROM_AXIS_TABLE).connect(out_single_axis)
                                                     
UISignals.GetSignal(SigName.DO_OUT).connect(do_out_msg)







