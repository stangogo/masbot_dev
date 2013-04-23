#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 
import os
import yaml

import logging.config
import codecs

from PySide import QtGui, QtCore
from datetime import datetime
from masbot.ui.message_log import MessageAndLog
from masbot.ui.robot.major.tray_info_table import TrayInfoTable 
from masbot.config.utils import UISignals, SigName
from masbot.ui.control.ui_utils import *

class Signals(QtCore.QObject):
    """
    三個Signals, 分別做為 MajorWidget 的 flow message, 
    alarm message and product info (tray infomation) 
    的訊息傳入.
    """
    flow_speak = QtCore.Signal(str)
    alarm_speak = QtCore.Signal(str)
    product_info_speak = QtCore.Signal(dict)


class MajorWidget(QtGui.QWidget):
    def __init__(self, title = 'Major Widget', parent = None):
        super(MajorWidget, self).__init__(parent)

        self.init_ui(title)
    
    def init_ui(self, title):
        # widget_base = QtGui.QWidget()    
        v_layout = QtGui.QVBoxLayout()
        
        self.msg_in = Signals()
        self.msg_in.product_info_speak.connect(self.set_product_info)
        self.msg_in.alarm_speak.connect(self.set_alarm_msg)
        self.msg_in.flow_speak.connect(self.set_flow_msg)        
        
        UISignals.RegisterSignal(self.msg_in.flow_speak, SigName.FLOW_MSG)
        UISignals.RegisterSignal(self.msg_in.alarm_speak, SigName.ALARM_MSG)
        UISignals.RegisterSignal(self.msg_in.product_info_speak, SigName.PRODUCT_INFO)
        
        try:
            UISignals.GetSignal(SigName.MAIN_START).connect(self.start_button_on)
            UISignals.GetSignal(SigName.MAIN_PLAY).connect(self.play_button_on)
        except:
            pass
        
        btn_panel = QtGui.QHBoxLayout()
        button_grid_layout = QtGui.QGridLayout()
        
        login_btn = create_button('login.png', '', '登入(Log In)')    # QtGui.QPushButton('Log in')        
        login_btn .setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        login_btn.setIconSize(QtCore.QSize(32,32));
        UISignals.RegisterSignal(login_btn.clicked, SigName.MAIN_LOG_IN)
        
        #start_btn = create_button('on-off.png', '', '啟動 (Start)') # QtGui.QPushButton('Start')
        #start_btn .setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #start_btn.setIconSize(QtCore.QSize(32,32));
        #UISignals.RegisterSignal(start_btn.clicked, SigName.START_MAIN)
        
        start_btn = create_button('off.png','','啟動(Switch On)')
        start_btn.setCheckable(True)
        start_btn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        start_btn.setIconSize(QtCore.QSize(32,32))                
        start_btn.clicked.connect(self.start_clicked)
        self.start_btn = start_btn
        
        play_btn = create_button('play.png', '','執行(Play)')
        play_btn.setCheckable(True)
        play_btn.setIconSize(QtCore.QSize(32,32));
        play_btn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        play_btn.clicked.connect(self.play_clicked)
        self.play_btn = play_btn
        
        button_grid_layout.addWidget(login_btn, 0, 0, 0,1)
        #button_grid_layout.addWidget(start_btn, 0, 1)
        button_grid_layout.addWidget(start_btn, 0, 1)
        button_grid_layout.addWidget(play_btn, 1, 1)
        
        message_edit = QtGui.QTextEdit()
        message_edit.resize(200, 200)
        
        
        btn_panel.addLayout(button_grid_layout,1)
        btn_panel.addWidget(message_edit, 2)
                

        flow_box = QtGui.QGroupBox('流程訊息(Flow Message)')                
        self.flow_message = MessageAndLog('ui.flow_message')
        
        flow_layout = QtGui.QVBoxLayout()
        flow_layout.addWidget(self.flow_message)
        flow_box.setLayout(flow_layout)
        
        
        alarm_box = QtGui.QGroupBox('警報訊息(Alarm Message)')
        self.alarm_message = MessageAndLog('ui.alarm_message')
        
        alarm_layout = QtGui.QVBoxLayout()
        alarm_layout.addWidget(self.alarm_message)
        alarm_box.setLayout(alarm_layout)
        
        product_box = QtGui.QGroupBox('成品訊息(Product Message)')
        self.product_message = TrayInfoTable('TrayInfo')
        product_layout = QtGui.QVBoxLayout()
        product_layout.addWidget(self.product_message)
        product_box.setLayout(product_layout)        
        
        v_layout.addLayout(btn_panel)
        v_layout.addWidget(flow_box)
        v_layout.addWidget(alarm_box)
        v_layout.addWidget(product_box)

        self.setLayout(v_layout)
        
        #self.setWidget(widget_base)       
        self.setWindowTitle(title)
        self.show()


    def play_button_on(self, on):
        if on:
            self.play_btn.setIcon(QtGui.QPixmap('{0}/pause.png'.format(Path.imgs_dir())))
        else:
            self.play_btn.setIcon(QtGui.QPixmap('{0}/play.png'.format(Path.imgs_dir())))        
            
    def start_button_on(self, on):
        if on:
            self.start_btn.setIcon(QtGui.QPixmap('{0}/on.png'.format(Path.imgs_dir())))
        else:
            self.start_btn.setIcon(QtGui.QPixmap('{0}/off.png'.format(Path.imgs_dir())))        

    def play_clicked(self):
        play_button = self.sender()        
        try:
            UISignals.GetSignal(SigName.MAIN_PLAY).emit(play_button.isChecked())
        except:
            self.play_button_on(play_button.isChecked())

    def start_clicked(self):
        start_button = self.sender()
        try:
            UISignals.GetSignal(SigName.MAIN_START).emit(start_button.isChecked())
        except:
            self.start_button_on(start_button.isChecked())
            

            
    def login_clicked(self):
        self.msg_in.flow_speak.emit('login')
        
    def set_flow_msg(self, msg):
        self.flow_message.add_message(msg)
        
    def set_alarm_msg(self, msg):
        self.alarm_message.add_message(msg)
        
    def set_product_info(self, info):
        now_time = datetime.now()
        info['LogTime']= now_time.strftime("%Y/%m/%d %H:%M:%S")
        self.product_message.add_message(info)
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = MajorWidget()
    app.exec_()


if __name__ == '__main__':
    main()          