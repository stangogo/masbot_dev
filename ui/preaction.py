#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 
import os
import logging.config
import yaml
import codecs


from PySide import QtCore, QtGui
from masbot.config.utils import UISignals, SigName

class SigAgent(QtCore.QObject):
    """所有UI對外連接的串口的名稱和參數設定. 
    """
    main_close = QtCore.Signal()    
    
    main_start = QtCore.Signal(bool)
    """ signal for start button on major widget
    @ bool : button is clicked to trigger start / shutdown (true/false) system
    """
    
    main_play = QtCore.Signal(bool)
    """ signal for play button on major widget
    @ bool : button is clicked to trigger play / pause (true/false) system
    """    
    
    dio_status = QtCore.Signal(dict)
    """
    DIO status - 
    @ dict : there are there elements
            ex: 'type':'8154'               - 8154 card
                'di':[0,0,0,1,1,0]          - 6 DI port: off, off, off, on, on, off
                'd0':[1,0,0,0,1,0,1,0,0]    - 9 DO port: on, off, off, off, on, off, on, off, off
    
    """    
    
    do_out = QtCore.Signal(int, int)
    """ 提供 DIOButton, ButtonForTable clicked時, 輸出DO port 和 on-off的接口
    @ int: do port number
    @ int: on or off (1 or 0)
    """
    
    into_single_axis = QtCore.Signal(str, str, float)
    """ 提供單軸表格內容填入的接口
    @ str: row 定義在 db_table_def.py 裡的 AxisOP 
    @ str: 定義在database 的 SingleAxis 資料表裡的 axis_key 欄
    @ float: 填入的值
    """
    out_single_axis = QtCore.Signal(str, float)
    """ 提供單軸發出控制訊號
    @ str: axis name
    @ float: 單軸位置的 value
    """

    img_preview = QtCore.Signal(list)
    """影像預覽資料傳入
    @ list: image data - image path(str), id(str), name(str), mode(int)
    """
    
    qimage_preview = QtCore.Signal(list)
    """影像預覽資料傳入
    @ list: image data - iamge data(QImage), id(str), name(str), mode(int)
    """    
    
    img_aided_tool = QtCore.Signal(dict)
    """ 影像 - 輔助工具 設定值傳出口
    @ dict: 資料字典集
    """
    
    img_message = QtCore.Signal(list)
    """影像預覽資料傳入
    @ list: image data - image path(str), id(str), name(str)
    """    

"""初始化所有的接口, 並註冊到UISignals Dictionary
"""
sig_agent = SigAgent()
UISignals.RegisterSignal(sig_agent.main_close, SigName.MAIN_CLOSE)
UISignals.RegisterSignal(sig_agent.main_start, SigName.MAIN_START)
UISignals.RegisterSignal(sig_agent.main_play, SigName.MAIN_PLAY)
#UISignals.RegisterSignal(sig_agent.di_in, SigName.DI_IN)
#UISignals.RegisterSignal(sig_agent.do_in, SigName.DO_IN)
UISignals.RegisterSignal(sig_agent.dio_status, SigName.DIO_STATUS)
UISignals.RegisterSignal(sig_agent.do_out, SigName.DO_OUT)
UISignals.RegisterSignal(sig_agent.into_single_axis, SigName.ENTER_AXIS_TABLE)
UISignals.RegisterSignal(sig_agent.out_single_axis, SigName.FROM_AXIS_TABLE)
UISignals.RegisterSignal(sig_agent.img_preview, SigName.IMG_THUMBNAIL)
UISignals.RegisterSignal(sig_agent.qimage_preview, SigName.QIMAGE_THUMBNAIL)
UISignals.RegisterSignal(sig_agent.img_aided_tool, SigName.IMG_AIDED_TOOL)
UISignals.RegisterSignal(sig_agent.img_message, SigName.IMG_MESSAGE)


"""測試用
"""
#def do_out_msg(io_num, on_off):
    #pass
    #print('{0} : {1} : {2}'.format(SigName.DO_OUT, io_num, on_off))
    #do_status = [io_num]
    #UISignals.GetSignal(SigName.DO_IN).emit(do_status, on_off)

def out_single_axis(axis_name, value): 
    print('{0} 移動 {1}'.format(axis_name, value))
    
    

UISignals.GetSignal(SigName.FROM_AXIS_TABLE).connect(out_single_axis)                                                     
#UISignals.GetSignal(SigName.DO_OUT).connect(do_out_msg)


""" Initialization of Logger
"""
#change working directory.
masbot_dir = os.path.abspath(__file__ + "/../../")
os.chdir(masbot_dir)

# setup logging  
path = masbot_dir + "/config/logging.yaml"

if os.path.exists(path):
    logging.config.dictConfig(yaml.load(codecs.open(path,'r','utf-8')))            
else:
    logging.basicConfig(level=logging.INFO)   
