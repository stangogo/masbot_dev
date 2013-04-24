#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from datetime import datetime
from PySide import QtGui, QtCore, QtSql

#from masbot.config.sqldb import SqlDB
from masbot.config.sqldb import sqldb
from masbot.config.utils import Path
from masbot.ui.control.dio_button import *
from masbot.ui import preaction
from masbot.ui.robot.io.IO_table_template import  IOTableTemplate

class PointTable(IOTableTemplate):
        
    def __init__(self, data_table_name, horizontal):
        super(PointTable, self).__init__(data_table_name, horizontal)
        
        
    def do_clicked(self, io_num, on_off, row, column, table):
        if not table == self.table_name:
            return    
        
        if row == -1 or column == -1:
            return
        
        if self.orientation == QtCore.Qt.Orientation.Horizontal:
            x_item = self.item(1, column)
            y_item = self.item(2, column)
        else:
            x_item = self.item(row, 1)
            y_item = self.item(row, 2)

        if io_num == 1: 
            print('go to {0}, {1}'.format(x_item.text(),y_item.text()))
        elif io_num == 2:
            print('replace {0}, {1}'.format(x_item.text(),y_item.text()))
                

class Point(QtGui.QSplitter):
    """    
    Point is a QWidget embeded point_table and tab on io_tab
    
    """
    def __init__(self, title = 'Point', parent = None):
        super(Point, self).__init__(parent)
        
        self.init_ui(title)
    
    def init_ui(self, title):
        
        self.point_table = PointTable('point', QtCore.Qt.Orientation.Vertical)        
        
        single_axis_point_table = sqldb.get_table_model('single_axis_points')
        
        table = QtGui.QTableView()
        table.setModel(single_axis_point_table)
        
        #table.setRowCount(3)
        #table.setColumnCount(4)
        
        
        double_axis_point_table = sqldb.get_table_model('double_axis_points')
        table2 = QtGui.QTableView()
        #table2 = QtGui.QTableWidget()        
        table2.setModel(double_axis_point_table)
        #table2.setRowCount(3)
        #table2.setColumnCount(4)        
        
        #v_layout = QtGui.QVBoxLayout()
        #v_layout.addWidget(single_point_box)
        #v_layout.addWidget(table)
        
        #a = QtGui.QWidget()
        #a.setLayout(v_layout)
            
        self.addWidget(self.point_table)
        self.addWidget(table)
        self.addWidget(table2)
        
        self.setOrientation(QtCore.Qt.Vertical)
        self.setSizes([300, 200, 200])
        self.setContentsMargins(1,5,1,1)
        #self.setStretchFactor(0,1);
                
        
        
        # self.setLayout(v_layout)        
        self.setWindowTitle(title)
        self.show()
        
    #def new_point(self):
        #self.point_table.add_one_data()
    
    #def delete_point(self):
        #pass
    
    def save(self):
        self.point_table.save()
    
    def reload(self):
        self.point_table.reload()

def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = Point()
    app.exec_()


if __name__ == '__main__':
    main()          
