#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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

class RobotBanner(QtGui.QWidget):

    def __init__(self):
        super(RobotBanner, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):
        style = "QLabel { background-color : lightblue; font-size:28px}"
        robot_model_label = QtGui.QLabel('機台種類')
        robot_model_label.setStyleSheet(style)        
        product_type_label = QtGui.QLabel('型號類別')
        product_type_label.setStyleSheet(style)
        machine_number_label = QtGui.QLabel('機台編號')
        machine_number_label.setStyleSheet(style)
        machine_info_label = QtGui.QLabel('機台狀態')
        machine_info_label.setStyleSheet(style)
    
        self.robot_banner = QtGui.QHBoxLayout(self)
    
        self.robot_banner.addWidget(robot_model_label, 1)
        self.robot_banner.addWidget(product_type_label, 1)
        self.robot_banner.addWidget(machine_number_label, 1)
        self.robot_banner.addWidget(machine_info_label, 3)

        self.setLayout(self.robot_banner)
                
        self.setWindowTitle('Robot Banner')
        self.show()
            
def main():    
    app = QtGui.QApplication(sys.argv)
    ex = RobotBanner()
    app.exec_()

if __name__ == '__main__':
    main()        