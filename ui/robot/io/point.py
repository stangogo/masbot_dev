#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtGui, QtCore
from datetime import datetime

from masbot.ui.robot.io.point_table import PointTable


class Point(QtGui.QWidget):
    """    
    Point is a QWidget embeded point_table and tab on io_tab
    
    """
    def __init__(self, title = 'Point', parent = None):
        super(Point, self).__init__(parent)
        
        self.init_ui(title)
    
    def init_ui(self, title):
        widget_base = QtGui.QWidget()  
                
        v_layout = QtGui.QVBoxLayout()        
        
        self.point_table = PointTable('point', 'point_ui', False)
        v_layout.addWidget(self.point_table)
        
        widget_base.setLayout(v_layout)
        
        self.setLayout(v_layout)        
        self.setWindowTitle(title)
        self.show()
        
    def save(self):
        print('point save')

def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = Point()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()          