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

from masttif_ui.robot.axis_table import AxisTable

class AxisBanner(QtGui.QWidget):

    def __init__(self):
        super(AxisBanner, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):
        
        style = "QLabel { color:green; font-family: sans-serif; font-size: 18px;}"
        title_label = QtGui.QLabel('單\n軸\n移\n動')
        title_label.setStyleSheet(style)
    
        self.axis_banner = QtGui.QHBoxLayout(self)
    
        self.axis_banner .addWidget(title_label, 0, QtCore.Qt.AlignLeft)
        self.axis_banner .addWidget(AxisTable(), QtCore.Qt.AlignLeft)

        self.setLayout(self.axis_banner )
                
        self.setWindowTitle('Axis Banner')
        self.show()
            
def main():    
    app = QtGui.QApplication(sys.argv)
    ex = AxisBanner()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        