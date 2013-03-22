#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtGui, QtCore
from datetime import datetime
from masttif_ui.robot.io.io_dock import IODock


class IOWidget(QtGui.QDockWidget):
    """    
    RobotIOPage is including two columns.
    RobotIOPageDock is placed on left side, 
    and Axis movement table is on right side.
    """
    def __init__(self, title = 'IO Widget', parent = None):
        super(IOWidget, self).__init__(parent)        
        
        self.initUI(title)
    
    def initUI(self, title):
        widget_base = QtGui.QWidget()  
        
        whole_layout = QtGui.QVBoxLayout()      # 水平佈局, 左側: RobotIOPageDock, 右側 axis_v_layout
        buttons_layout = QtGui.QHBoxLayout() # Table 垂直佈局: axis_op_table, save, load, apply buttons
        io_dock = IODock()

        # Axis Operation Table                    
        buttons_layout.addWidget(QtGui.QPushButton('儲存(Save)'), 1, QtCore.Qt.AlignRight)
        buttons_layout.addWidget(QtGui.QPushButton('讀取(Load)'), 0, QtCore.Qt.AlignRight)
        #apply_button = QtGui.QPushButton('套用(Apply)')
        #apply_button.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        #apply_button.resize(100, 25)
        buttons_layout.addWidget(QtGui.QPushButton('套用(Apply)'), 0, QtCore.Qt.AlignRight)
                
        whole_layout.addWidget(io_dock, 3)
        whole_layout.addLayout(buttons_layout, 1)
                              
        widget_base.setLayout(whole_layout)
        
        self.setWidget(widget_base)       
        self.setWindowTitle(title)
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = IOWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()          