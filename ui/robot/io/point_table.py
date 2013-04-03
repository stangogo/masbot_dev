#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from datetime import datetime
from PySide import QtGui, QtCore, QtSql

from masbot.ui.sqldb import SqlDB
from masbot.ui.utils import Path
from masbot.ui.control.dio_button import *
from masbot.ui import signal_agent
from masbot.ui.robot.io.IO_table_template import  IOTableTemplate

class PointTable(IOTableTemplate):
        
    def __init__(self, data_table_name, ui_table_name, horizontal):
        super(PointTable, self).__init__(data_table_name, ui_table_name, horizontal)
        
    def do_clicked(self, io_num, on_off, row, column, table):
        if not table == self.data_table_name:
            return    
        
        if row == -1 or column == -1:
            return
        
        if self.list_horizontal:            
            x_item = self.item(0, column)
            y_item = self.item(1, column)
        else:
            x_item = self.item(row, 0)
            y_item = self.item(row, 1)

        if io_num == 1: 
            print('go to {0}, {1}'.format(x_item.text(),y_item.text()))
        elif io_num == 2:
            print('replace {0}, {1}'.format(x_item.text(),y_item.text()))
                
    def save(self):
        pass
    
    def reload(self):
        pass
    
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = PointTable('point', 'point_ui', True)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        