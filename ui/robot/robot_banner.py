#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
顯示單軸狀態, 控制表單
                        author: Cigar Huang
                        website: zetcode.com 
                        last edited: 18 Mar. 2013
"""

import sys
import os
import threading
import time 
from threading import Thread
from PySide import QtGui, QtCore

from masbot.ui.robot.axis_table import AxisTable
from masbot.config.utils import Path, UISignals, SigName
from masbot.ui.robot.robot_info import RobotInfo
from masbot.ui.control.ui_utils import *

class RobotBanner(QtGui.QWidget):

    def __init__(self):
        super(RobotBanner, self).__init__()
        
        self.init_ui()        
        
    def init_ui(self):        
        self.table = AxisTable()        
        
        self.stack_layout = QtGui.QStackedLayout()
        self.stack_layout.addWidget(self.table)        
        self.stack_layout.addWidget(RobotInfo())
        self.stack_layout.setCurrentIndex(0)        
        
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addLayout(self.init_switch_buttons(), 1)
        hbox.addLayout(self.stack_layout, 40)

        hbox.setSpacing(0)

        self.mode_button.setChecked(True)
        self.mode_changed()
        self.setLayout(hbox)
        self.setWindowTitle('Axis Banner')
        self.show()
    
    def init_switch_buttons(self):
        
        #self.switch_button = []
        axis_button = QtGui.QPushButton('單\n軸\n移\n動')        
        axis_button.setStyleSheet("QPushButton { font-family: Microsoft JhengHei; font-size: 14px;}")
        axis_button.setToolTip('切換"單軸移動"表單和"機台資訊"')
        axis_button.setMinimumHeight(100)
        axis_button.setMaximumWidth(30)
        axis_button.clicked.connect(self.switch_clicked)
        #self.switch_button.append(axis_button)
        
        #robot_info_button = QtGui.QPushButton('機台\n資訊')
        #robot_info_button.setStyleSheet("QPushButton { color:green; font-family: sans-serif; font-size: 12px;}")
        #robot_info_button.setMinimumHeight(50)
        #robot_info_button.setMaximumWidth(35)
        #robot_info_button.setCheckable(True)
        #robot_info_button.clicked.connect(self.switch_clicked)
        #self.switch_button.append(robot_info_button)
        
        self.mode_button = QtGui.QPushButton()
        self.mode_button.setToolTip('只顯示有勾選的欄位')
        self.mode_button.setCheckable(True)
        self.mode_button.clicked.connect(self.mode_changed)
        
        title_vbox = QtGui.QVBoxLayout()
        title_vbox.addWidget(axis_button,0)
        #title_vbox.addWidget(robot_info_button,0)
        title_vbox.addWidget(self.mode_button, 1)
        
        title_vbox.setAlignment(axis_button, QtCore.Qt.AlignTop)
        #title_vbox.setAlignment(robot_info_button, QtCore.Qt.AlignTop)
        title_vbox.setAlignment(self.mode_button, QtCore.Qt.AlignBottom)
        
        title_vbox.setSpacing(0)

        return title_vbox        
    
    
    def remove_image_btn_clicked(self):
        self.di_do_btn.setEnabled(self.remove_image_btn.isChecked()) 
       
    def mode_changed(self):
        self.table.change_diaplay_mode(self.mode_button.isChecked())
        if self.mode_button.isChecked():
            self.mode_button.setIcon( get_rotate_qicon('top_right_expand.png', 90) )
        else:
            self.mode_button.setIcon( get_rotate_qicon('top_right_expand.png', 270) )

    def switch_clicked(self):
        index = (self.stack_layout.currentIndex() + 1)%2
        self.stack_layout.setCurrentIndex(index)
        button = self.sender()
        QPushButton.setText
        if index == 0:
            button.setText('單\n軸\n移\n動')            
        else:
            button.setText('機\n台\n資\n訊')
        
        self.mode_button.setEnabled(not index)
    
def main():    
    app = QtGui.QApplication(sys.argv)
    ex = RobotBanner()
    app.exec_()

if __name__ == '__main__':
    main()        