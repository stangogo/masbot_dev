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
from masbot.ui.utils import UISignals, SigName

class Signals(QtCore.QObject):
    """
    三個Signals, 分別做為 MajorWidget 的 flow message, 
    alarm message and product info (tray infomation) 
    的訊息傳入.
    """
    flow_speak = QtCore.Signal(str)
    alarm_speak = QtCore.Signal(str)
    product_info_speak = QtCore.Signal(dict)


class MajorWidget(QtGui.QDockWidget):
    def __init__(self, title = 'Major Widget', parent = None):
        super(MajorWidget, self).__init__(parent)

        self.init_ui(title)
    
    def init_ui(self, title):
        widget_base = QtGui.QWidget()    
        v_layout = QtGui.QVBoxLayout()
        
        self.msg_in = Signals()
        self.msg_in.product_info_speak.connect(self.set_product_info)
        self.msg_in.alarm_speak.connect(self.set_alarm_msg)
        self.msg_in.flow_speak.connect(self.set_flow_msg)        
        
        UISignals.RegisterSignal(self.msg_in.flow_speak, SigName.FLOW_MSG)
        UISignals.RegisterSignal(self.msg_in.alarm_speak, SigName.ALARM_MSG)
        UISignals.RegisterSignal(self.msg_in.product_info_speak, SigName.PRODUCT_INFO)
        
        btn_panel = QtGui.QHBoxLayout()
        button_grid_layout = QtGui.QGridLayout()
        
        login_btn = QtGui.QPushButton('Log in')        
        login_btn .setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)        
        UISignals.RegisterSignal(login_btn.clicked, SigName.LOG_IN)
        #login_btn.clicked.connect(self.login_clicked)
        
        start_btn = QtGui.QPushButton('Start')
        start_btn .setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        UISignals.RegisterSignal(start_btn.clicked, SigName.START_MAIN)
        
        servo_on_btn = QtGui.QPushButton('Servo On')        
        servo_on_btn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        UISignals.RegisterSignal(servo_on_btn.clicked, SigName.SERVO_ON)
        
        pause_btn = QtGui.QPushButton('Pause')
        pause_btn.setStyleSheet("QPushButton{color:red;font-size:17px;font-family:courier;font-style:italic}")
        pause_btn.setCheckable(True)
        pause_btn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        UISignals.RegisterSignal(pause_btn.clicked, SigName.PAUSE_MAIN)
        
        button_grid_layout.addWidget(login_btn, 0, 0)
        button_grid_layout.addWidget(start_btn, 0, 1)
        button_grid_layout.addWidget(servo_on_btn, 1, 0)
        button_grid_layout.addWidget(pause_btn, 1, 1)
        
        message_edit = QtGui.QTextEdit()
        message_edit.resize(500, 600)
        
        
        btn_panel.addLayout(button_grid_layout)
        btn_panel.addWidget(message_edit)
                

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

        widget_base.setLayout(v_layout)
        
        self.setWidget(widget_base)       
        self.setWindowTitle(title)
        self.show()

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
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()          