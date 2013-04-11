#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtGui, QtCore
from datetime import datetime
from masbot.ui.robot.io.io_tab import IOTab


class IOWidget(QtGui.QWidget):
    """    
    RobotIOPage is including two columns.
    RobotIOPageDock is placed on left side, 
    and Axis movement table is on right side.
    """
    def __init__(self, title = 'IO Widget', parent = None):
        super(IOWidget, self).__init__(parent)        
        
        self.initUI(title)
    
    def initUI(self, title):
        
        
        whole_layout = QtGui.QVBoxLayout()      # 水平佈局, 左側: RobotIOPageDock, 右側 axis_v_layout
        buttons_layout = QtGui.QHBoxLayout()    # Table 垂直佈局: axis_op_table, save, load, apply buttons
        self.io_tab = IOTab()

        # Axis Operation Table                    
        save_button = QtGui.QPushButton('儲存(Save)')
        load_button = QtGui.QPushButton('讀取(Load)')
        apply_button = QtGui.QPushButton('套用(Apply)')
        
        save_button.clicked.connect(self.save)
        load_button.clicked.connect(self.reload)
        apply_button.clicked.connect(self.apply)
        
        buttons_layout.addWidget(save_button, 1, QtCore.Qt.AlignRight)
        buttons_layout.addWidget(load_button, 0, QtCore.Qt.AlignRight)
        buttons_layout.addWidget(apply_button, 0, QtCore.Qt.AlignRight)
        
        #apply_button = QtGui.QPushButton('套用(Apply)')
        #apply_button.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        #apply_button.resize(100, 25)
                
        whole_layout.addWidget(self.io_tab, 3)
        #whole_layout.addWidget(QtGui.QTabWidget())
        whole_layout.addLayout(buttons_layout, 1)
                              
        self.setLayout(whole_layout)
                
        self.setWindowTitle(title)
        self.show()
    
    def save(self):
        self.io_tab.save()
    def reload(self):
        self.io_tab.reload()
    def apply(self):
        self.io_tab.apply()
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = IOWidget()
    app.exec_()


if __name__ == '__main__':
    main()          