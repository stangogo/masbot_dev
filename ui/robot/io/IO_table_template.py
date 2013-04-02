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

class IOTableTemplate(QtGui.QTableWidget):
    do_dict = {}
    di_dict = {}
    
    def __init__(self, data_table_name, ui_table_name, horizontal):
        super(IOTableTemplate, self).__init__()
        
        self.data_table = SqlDB().get_table_model(data_table_name)        
        self.ui_table = SqlDB().get_table_model(ui_table_name)
        
        self.ui_table_name = ui_table_name
        self.data_table_name = data_table_name
        
        self.list_horizontal = horizontal
        
        header_key = 'display_text'
        if self.list_horizontal:
            self.init_vertical_header(header_key, self.ui_table, self.ui_table_name, 'col_order')
            self.init_horizontal_header(header_key, self.data_table, self.data_table_name, 'id')
        else:
            self.init_vertical_header(header_key, self.data_table, self.data_table_name, 'id')
            self.init_horizontal_header(header_key, self.ui_table, self.ui_table_name, 'col_order')

        self.fill_cells(ui_table_name, data_table_name, self.ui_table, self.data_table, self.list_horizontal)
        
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, 50)
            
        self.setStyleSheet("QHeaderView::section { background-color:rgb(204, 100, 204) }");    #設定表格title的color
        
        self.setWindowTitle('IO Table Template')
        self.show()

    def make_cell(self, type_, on_str, off_str, key, action, value_set, cur_value):
        if type_ == 'button':  #DO
            do_cell = NozzleDoButton(cur_value, self.data_table_name)
            do_cell.set_properties(on_str, off_str, key, action)
            self.do_dict[do_cell.io_num] = do_cell
            
            return do_cell
        elif type_ == 'DI_label': #DI
            di_cell =  DIOLabel('{0}'.format(cur_value),False)#DISensor()
            di_cell.io_num = cur_value
            self.di_dict[di_cell.io_num] = di_cell
            di_cell.set_properties(key, action)
            cell_layout = QtGui.QHBoxLayout()
            cell_layout.setContentsMargins(0,0,0,0)
            cell_layout.addWidget(di_cell)
            cell_widget = QtGui.QWidget()                
            cell_widget.setLayout(cell_layout)
                        
            return cell_widget
        elif type_ == 'combobox': #ComboBox            
            self.get_value_set(value_set)
            selection_cell = QtGui.QComboBox()
            selection_cell.setInsertPolicy(QtGui.QComboBox.InsertPolicy.InsertAlphabetically)
            options = self.get_value_set(value_set)
            
            try:
                index = options.index('{0}'.format(cur_value))
            except:
                index = -1
            
            selection_cell.addItems(options)            
            selection_cell.setCurrentIndex(index)
            return selection_cell
        else:
            return None

    def get_value_set(self, value_set):
        option_table = SqlDB().get_table_model('option_value')
        option_table.select()
        
        query= option_table.query()
        query.exec_("select value from option_value where option = '{0}'".format(value_set))        

        options = []        
        while query.next():
            options.append("{0}".format(query.value(0)))
        return options
    
    def get_property_value(self, table_name, property_name):
        self.data_table.select()
        query = self.data_table.query()
        query.exec_("select {0} from {1} order by id".format(property_name, table_name) )
        
        data = []        
        while query.next():
            try:
                data.append(int(query.value(0)))
            except:
                data.append(query.value(0))
        return data
    
        
        
    def fill_cells(self, ui_table_name, data_table_name, ui_table, data_table, list_horizontal):
        #row 0
        ui_table.select()
        query = ui_table.query()
        query.exec_("select btn_on_str,btn_off_str,reference_val,display_type,value_set from {0} order by col_order".format(ui_table_name) )
        data_count = 0
        while query.next():
            on_str = query.value(0)
            off_str = query.value(1)
            property_ = query.value(2) #利用這個值, 取得整個row的資料, 填入.
            display_type = query.value(3)
            value_set = query.value(4)
            
            action_data = self.get_property_value(data_table_name, property_)
            for i in range(0, len(action_data)):#self.columnCount()):
                key = ''
                cell = self.make_cell(display_type, on_str, off_str, key, property_, value_set, action_data[i]) 
                
                if list_horizontal:
                    row = data_count
                    column = i                    
                else:
                    row = i
                    column = data_count
                                    
                if not cell == None:
                    if display_type == 'button':
                        cell.set_row_column(row, column)
                    self.setCellWidget(row, column, cell)
                else:
                    item = QtGui.QTableWidgetItem('{0}'.format(action_data[i]))                    
                    self.setItem(row, column, item)
                                        
            if display_type == 'button':    # disconnect and then connect: 避免button重覆掛載do_clicked. 
                try:
                    cell.signals.clicked.disconnect(self.do_clicked)
                except:
                    pass
                cell.signals.clicked.connect(self.do_clicked)
            data_count += 1

    def init_horizontal_header(self, field, table, table_name, orderby):
        table.select()
        self.setColumnCount(table.rowCount())
        query = table.query()
        
        headers = []
        query.exec_("select {0} from {1} order by {2}".format(field, table_name, orderby) )
        while query.next():             
            headers.append(query.value(0))      
        self.setHorizontalHeaderLabels(headers)
        
    def init_vertical_header(self, field, table, table_name, orderby):
        table.select()
        self.setRowCount(table.rowCount())
        
        query = table.query()
        query.exec_("select {0} from {1} order by {2}".format(field, table_name, orderby))
        headers = []
        while query.next():
            headers.append(query.value(0))
            
        self.setVerticalHeaderLabels(headers)
        query.finish()
        
        #覆寫 do_clicked 時, 若有button type的cell, " if not table == self.data_table_name: " 判斷一定要寫
        #因button click 掛上後, 不管那個button被按, 會發給所有的button. 用table name 比對做判斷
    def do_clicked(self, io_num, on_off, row, column, table):   
        if not table == self.data_table_name:   
            return
        
        print('do {0} clicked {1}, row: {2}, column: {3}, table: {4}'.format(io_num, on_off, row, column, table))
        #sig = UISignals.GetSignal(SigName.DO_OUT)
        #sig.emit(io_num, on_off)
    
    def save(self):
        pass
    
    def reload(self):
        pass
    
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = IOTableTemplate('point', 'point_ui', False)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        