#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from datetime import datetime
from PySide import QtGui, QtCore, QtSql

from masttif_ui.sqldb import SqlDB
from masttif_ui.utils import Path


class DoButton(QtGui.QPushButton):
    __on_str = "On"
    __off_str ="Off"
    __bOn = False
    key = ""            #屬誰
    action =""          #動作; blow, suck, up/down ...etc.
   
    def __new__(self, icon=None):
        if icon == None:
            return QtGui.QPushButton.__new__(self, self.__on_str)
        else:
            return QtGui.QPushButton.__new__(self, icon, self.__on_str)
        
    def __init__(self, icon=None):
        super(DoButton, self).__init__()
        self.clicked.connect(self.on_clicked)        
        imgs_dir = Path.imgs_dir()
        self.on_img = "{0}/Start.bmp".format(imgs_dir)
        self.off_img = "{0}/Stop.bmp".format(imgs_dir)
        self.on_off(self.__bOn)
        
    def set_properties(self, on_str, off_str, key, action):
        self.__on_str = on_str
        self.__off_str = off_str
        self.key = key
        self.action = action
        self.on_off(self.__bOn)

    def on_clicked(self):        
        self.__bOn = not self.__bOn
        self.on_off(self.__bOn)
    
    def on_off(self, on):
        if on:
            self.setText(self.__on_str)
            #self.setIcon(QtGui.QIcon(self.on_img))
        else: 
            self.setText(self.__off_str)
            #self.setIcon(QtGui.QIcon(self.off_img))    
            
class DISensor(QtGui.QLabel):
    __bOn = False
    key = ""            #屬誰
    action =""          #動作; blow, suck, up/down ...etc.
   
    def __init__(self, icon=None):
        super(DISensor, self).__init__()
        
        imgs_dir = Path.imgs_dir()
        self.on_img = "{0}/Start.bmp".format(imgs_dir)
        self.off_img = "{0}/Stop.bmp".format(imgs_dir)
        self.on_off(self.__bOn)
        
    def set_properties(self, key, action):
        self.key = key
        self.action = action
    
    def on_off(self, on):
        if on:
            self.setPixmap(QtGui.QPixmap(self.on_img).scaledToHeight(15))
        else: 
            self.setPixmap(QtGui.QPixmap(self.off_img).scaledToHeight(15))
            
        self.setAlignment(QtCore.Qt.AlignCenter)
        

class NozzleTable(QtGui.QTableWidget):        
    
    #def __new__(self, data_table_name, ui_table_name):

        #self.table_model = SqlDB().get_table_model(table_name)

        #return QtGui.QTableWidget.__new__(self)
    
    def __init__(self, data_table_name, ui_table_name):
        super(NozzleTable, self).__init__()
        
        self.data_table = SqlDB().get_table_model(data_table_name)        
        self.UI_table = SqlDB().get_table_model(ui_table_name)
        
        self.init_vertical_header('header_name', ui_table_name)
        self.init_horizontal_header('header_name', data_table_name)

        self.fill_cells(ui_table_name)        
        
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, 50)
        
        self.setStyleSheet("QHeaderView::section { background-color:rgb(204, 100, 204) }");    #設定表格title的color
        
        self.setWindowTitle('Nozzle Table')
        self.show()

    def make_cell(self, type_, on_str, off_str, key, action, value_set):
        if type_ == 0:  #DO
            do_cell = DoButton()
            do_cell.set_properties(on_str, off_str, key, action)
            return do_cell
        elif type_ == 1: #DI
            di_cell = DISensor()
            di_cell.set_properties(key, action)
            return di_cell
        elif type_ == 2: #ComboBox
            self.get_value_set(value_set)
            selection_cell = QtGui.QComboBox()
            selection_cell.setInsertPolicy(QtGui.QComboBox.InsertPolicy.InsertAlphabetically)
            options = self.get_value_set(value_set)
            selection_cell.addItems(options)
            return selection_cell

    def get_value_set(self, value_set):
        option_table = SqlDB().get_table_model('option_value')
        option_table.select()
        
        query= option_table.query()
        query.exec_("select value from option_value where option_id = {0}".format(value_set))        

        options = []        
        while query.next():
            options.append("{0}".format(query.value(0)))
        return options
        
        
    def fill_cells(self, ui_table_name):
        #row 0
        self.UI_table.select()
        query = self.UI_table.query()
        query.exec_("select btn_on_str,btn_off_str,nozzle_property,display_type,value_set from {0} order by col_order".format(ui_table_name) )        
        n_row = 0
        while query.next():
            on_str = query.value(0)
            off_str = query.value(1)            
            action = query.value(2)
            type_ = query.value(3)
            value_set = query.value(4)
            for i in range(0, self.columnCount()):
                key = self.keys[i]
                self.setCellWidget(n_row,i, self.make_cell(type_, on_str, off_str, key, action, value_set) )
            n_row += 1
                
        
    def init_horizontal_header(self, field, table_name):
        self.data_table.select()
        self.setColumnCount(self.data_table.rowCount())        
        query = self.data_table.query()
        self.keys = []
        query.exec_("select {0},key from {1} order by id".format(field, table_name) )
        headers = []
        while query.next(): 
            headers.append(query.value(0))
            self.keys.append(query.value(1))
        self.setHorizontalHeaderLabels(headers)
    
        
        
    def init_vertical_header(self, field, ui_table_name):
        self.UI_table.select()
        self.setRowCount(self.UI_table.rowCount())
        row_query = self.UI_table.query()
        row_query.exec_("select {0} from {1} order by col_order".format(field, ui_table_name) )        
        row_headers = []
        while row_query.next():
            row_headers.append(row_query.value(0))
        self.setVerticalHeaderLabels(row_headers)
        row_query.finish()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = NozzleTable('Nozzle', 'nozzle_ui')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        