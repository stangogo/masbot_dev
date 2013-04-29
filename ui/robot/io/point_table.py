#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from datetime import datetime
from PySide import QtCore, QtSql
from PySide.QtGui import *


from masbot.config.sqldb import sqldb
from masbot.config.utils import Path
from masbot.ui.control.dio_button import *
from masbot.ui import preaction
from masbot.ui.robot.io.IO_table_template import  IOTableTemplate

class XAxisPointTable(IOTableTemplate):
        
    def __init__(self, data_table_name, order_by, horizontal):
        super(XAxisPointTable, self).__init__(data_table_name, order_by, horizontal)
        
        
    def do_clicked(self, go_replace, on_off, row, column, table):
        if not table == self.table_name:
            return    
        
        if row == -1 or column == -1:
            return
        
        if self.orientation == QtCore.Qt.Orientation.Horizontal:
            position = [self.item(x, column).text() for x in self.dclick]
            
        else:
            position = [self.item(row, x).text() for x in self.dclick]

        if go_replace == 1: 
            print('go to ', position)
        elif go_replace == 2:
            print('replace ', position)
                
#class SingleAxisPointTable(IOTableTemplate):
        
    #def __init__(self, data_table_name, order_by, horizontal):
        #super(SingleAxisPointTable, self).__init__(data_table_name, order_by, horizontal)
        
        
    #def do_clicked(self, io_num, on_off, row, column, table):
        #if not table == self.table_name:
            #return    
        
        #if row == -1 or column == -1:
            #return
        
        #if self.orientation == QtCore.Qt.Orientation.Horizontal:
            #x_item = self.item(1, column)
            #y_item = self.item(2, column)
        #else:
            #x_item = self.item(row, 1)
            #y_item = self.item(row, 2)

        #if io_num == 1: 
            #print('go to {0}, {1}'.format(x_item.text(),y_item.text()))
        #elif io_num == 2:
            #print('replace {0}, {1}'.format(x_item.text(),y_item.text()))
                
                
#class TripleAxisPointTable(IOTableTemplate):
        
    #def __init__(self, data_table_name, order_by, horizontal):
        #super(TripleAxisPointTable, self).__init__(data_table_name, order_by, horizontal)
        
        
    #def do_clicked(self, io_num, on_off, row, column, table):
        #if not table == self.table_name:
            #return    
        
        #if row == -1 or column == -1:
            #return
        
        #if self.orientation == QtCore.Qt.Orientation.Horizontal:
            #x_item = self.item(1, column)
            #y_item = self.item(2, column)
        #else:
            #x_item = self.item(row, 1)
            #y_item = self.item(row, 2)

        #if io_num == 1: 
            #print('go to {0}, {1}'.format(x_item.text(),y_item.text()))
        #elif io_num == 2:
            #print('replace {0}, {1}'.format(x_item.text(),y_item.text()))
            
            
            
class Point(QSplitter):
    """    
    Point is a QWidget embeded point_table and tab on io_tab
    
    """
    def __init__(self, title = 'Point', parent = None):
        super(Point, self).__init__(parent)
        self.point_table = []        
        self.init_ui(title)
    
    def init_ui(self, title):
        self.addWidget(self.init_d_axis_group())
        self.addWidget(self.init_s_axis_group())
        self.addWidget(self.init_t_axis_group())
        
        self.setOrientation(QtCore.Qt.Vertical)
        
        total = sum([table.data_count() for table in self.point_table])
        
        if total > 0:
            size_rate = [ int(700 * table.data_count() /total) for table in self.point_table ]
            self.setSizes(size_rate)
            
        self.setContentsMargins(1,5,1,1)
        #self.setStretchFactor(0,1);
        
        self.setChildrenCollapsible(False)  # Splitter 手動改變比例時, 不能把child折到不見
        self.setWindowTitle(title)
        self.show()
        
    #def new_point(self):
        #self.point_table.add_one_data()
    
    #def delete_point(self):
        #pass
    
    def init_d_axis_group(self):
        point_group = QGroupBox('雙軸點位')
        point_box = QHBoxLayout()
        point_box.setContentsMargins(0,1,0,0)
        table = XAxisPointTable('double_axis_point', ['KEY', 'point_index'], QtCore.Qt.Orientation.Vertical)
        point_box.addWidget(table)
        point_group.setLayout(point_box)
        
        self.point_table.append(table)
        return point_group
        
    def init_s_axis_group(self):
        point_group = QGroupBox('單軸點位')
        point_box = QHBoxLayout()
        point_box.setContentsMargins(0,1,0,0)
        table= XAxisPointTable('single_axis_point', ['KEY', 'point_index'], QtCore.Qt.Orientation.Vertical)
        point_box.addWidget(table)
        point_group.setLayout(point_box)
        
        self.point_table.append(table)
        return point_group
    
    def init_t_axis_group(self):
        point_group = QGroupBox('三軸點位')
        point_box = QHBoxLayout()
        point_box.setContentsMargins(0,1,0,0)
        table = XAxisPointTable('triple_axis_point', ['KEY', 'point_index'], QtCore.Qt.Orientation.Vertical)
        point_box.addWidget(table)
        point_group.setLayout(point_box)
        
        self.point_table.append(table)
        return point_group
    
    
    def save(self):
        for table in self.point_table:
            table.save()
    
    def reload(self):
        for table in self.point_table:
            table.reload()

def main():
    
    app = QApplication(sys.argv)

    ex = Point()
    app.exec_()


if __name__ == '__main__':
    main()          
