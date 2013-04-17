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


class AxisBanner(QtGui.QWidget):

    def __init__(self):
        super(AxisBanner, self).__init__()
        
        self.init_ui()        
        
    def init_ui(self):
        
        style = "QLabel { color:green; font-family: sans-serif; font-size: 18px;}"
        title_label = QtGui.QLabel('單\n軸\n移\n動')
        title_label.setStyleSheet(style)
    
        push_ico = QtGui.QIcon("{0}/push.ico".format(Path.imgs_dir()))
        self.di_do_btn = QtGui.QPushButton(push_ico, "DIO\n顯示")
        self.di_do_btn.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.di_do_btn.setStyleSheet ("QPushButton{text-align:left}")
        self.di_do_btn.setFixedWidth(50)
        self.di_do_btn.setFixedHeight(50)
        self.di_do_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.di_do_btn.setCheckable(True)
        UISignals.RegisterSignal(self.di_do_btn.clicked, SigName.DI_DO_SHOW)
                
        to_robot_banner_btn = QtGui.QPushButton('至機台\n資訊')
        to_robot_banner_btn.setFixedWidth(50)
        to_robot_banner_btn.setFixedHeight(50)
        UISignals.RegisterSignal(to_robot_banner_btn.clicked, SigName.TO_ROBOT_BANNER)
        
        self.remove_image_btn = QtGui.QPushButton('右側\n開關')
        self.remove_image_btn.setCheckable(True)
        self.remove_image_btn.setChecked(True)
        self.remove_image_btn.setFixedWidth(50)
        self.remove_image_btn.setFixedHeight(50)
        self.remove_image_btn.clicked.connect(self.remove_image_btn_clicked)
        UISignals.RegisterSignal(self.remove_image_btn.clicked, SigName.REMOVE_IMG_SIDE)
        
        btn_v_layout = QtGui.QVBoxLayout()
        btn_v_layout.addWidget(self.remove_image_btn, 1)
        btn_v_layout.addWidget(to_robot_banner_btn, 0)
        btn_v_layout.addWidget(self.di_do_btn, 0)        
        
        self.axis_banner = QtGui.QHBoxLayout(self)    
        self.axis_banner.addWidget(title_label, 1, QtCore.Qt.AlignLeft)
        self.axis_banner.addWidget(AxisTable(),40)#, QtCore.Qt.AlignLeft)
        self.axis_banner.addLayout(btn_v_layout)
        #self.axis_banner.addWidget(self.di_do_btn, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)  
        #self.axis_banner.addWidget(push_label, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        

        
        self.setLayout(self.axis_banner )
                
        self.setWindowTitle('Axis Banner')
        self.show()
    
    def remove_image_btn_clicked(self):
        self.di_do_btn.setEnabled(self.remove_image_btn.isChecked()) 
def main():    
    app = QtGui.QApplication(sys.argv)
    ex = AxisBanner()
    app.exec_()

if __name__ == '__main__':
    main()        