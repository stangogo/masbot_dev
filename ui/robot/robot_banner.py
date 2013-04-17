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

from PySide import QtCore
from PySide.QtGui import *
from masbot.config.utils import Path

class RobotBanner(QWidget):

    def __init__(self):
        super(RobotBanner, self).__init__()        
        self.init_ui()
        
    def init_ui(self):
        robot_model_label = QLabel('機台種類')        
        product_type_label = QLabel('型號類別')
        machine_number_label = QLabel('機台編號')
        machine_info_label = QLabel('機台狀態')
            
        h_layout = QHBoxLayout()
        
        robot_info_layout = QVBoxLayout()    
        robot_info_layout.addWidget(robot_model_label, 1)
        robot_info_layout.addWidget(product_type_label, 1)
        robot_info_layout.addWidget(machine_number_label, 1)
        robot_info_layout.addWidget(machine_info_label, 3)

        table = QTableWidget()
        table.setColumnCount(6)
        table.setRowCount(5)
        
        h_layout.addLayout(robot_info_layout)
        h_layout.addWidget(QWidget())
        
        self.setLayout(h_layout)                
        self.setWindowTitle('Robot Banner')
        self.show()
            
def main():    
    app = QApplication(sys.argv)
    
    ex = RobotBanner()    
    app.exec_()

if __name__ == '__main__':
    main()        