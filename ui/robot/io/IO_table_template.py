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

class IOTableTemplate(QtGui.QTableWidget):
    def __init__(self, data_table_name, ui_table_name, horizontal):
        super(IOTableTemplate, self).__init__()
        self.one_data_set = []   #one data sample for adding/updating data column/row
        self.do_dict = {}
        self.di_dict = {}        
        
        self.data_table = sqldb.get_table_model(data_table_name)
        self.ui_table = sqldb.get_table_model(ui_table_name)
        
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

        self.fill_cells(ui_table_name, data_table_name, self.ui_table, self.data_table, self.list_horizontal, False)
        
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, 50)
        
        self.resizeRowsToContents()
        self.logger = logging.getLogger('ui.log')
        
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
            widget_item = QtGui.QTableWidgetItem('{0}'.format(cur_value))
            return widget_item

    def get_value_set(self, value_set):
        option_table = sqldb.get_table_model('options')
        option_table.select()
        
        query= option_table.query()
        query.exec_("select value from options where id = '{0}'".format(value_set))        

        options = []        
        while query.next():
            options.append("{0}".format(query.value(0)))
        return options
    
    def get_property_value(self, table_name, property_name):
        self.data_table.select()
        query = self.data_table.query()
        query.exec_("select {0} from {1}".format(property_name, table_name) )
        
        data = []        
        while query.next():
            try:
                data.append(int(query.value(0)))
            except:
                data.append(query.value(0))
        return data
    
    def add_cell(self, row, column, cell, display_type):
        if display_type == 'button':
            cell.set_row_column(row, column)     # 在點位的table裡, 必須知道其所在的 row 跟 column
            
        if isinstance(cell, QtGui.QTableWidgetItem):
            self.setItem(row, column, cell)
        else:
            self.setCellWidget(row, column, cell)

    def fill_cells(self, ui_table_name, data_table_name, ui_table, data_table, list_horizontal, reload):        
        self.one_data_set.clear()
        self.keys = self.get_property_value(data_table_name, 'key')
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
            self.one_data_set.append([on_str, off_str, property_, display_type, value_set, action_data[0]])
            
            for i in range(0, len(action_data)):
                if list_horizontal:
                    row = data_count
                    column = i
                else:
                    row = i
                    column = data_count
                    
                if reload:
                    if display_type in ['button', 'DI_label']:  # button 跟 label 不用重新載入
                        continue
                    
                    if display_type == 'combobox':
                        combobox_cell = self.cellWidget(row, column)
                        cur_text = "{0}".format(action_data[i])
                        combobox_cell.setCurrentIndex(combobox_cell.findText(cur_text))
                    else:
                        item = self.item(row, column)
                        item.setText('{0}'.format(action_data[i]))
                else:
                    key = self.keys[i]
                    cell = self.make_cell(display_type, on_str, off_str, key, property_, value_set, action_data[i]) 
                  
                    self.add_cell(row, column, cell, display_type)
                        
            if not reload:
                if display_type == 'button':    # disconnect and then connect: 避免button重覆掛載do_clicked. 
                    try:
                        cell.signals.clicked.disconnect(self.do_clicked)
                    except:
                        pass
                    cell.signals.clicked.connect(self.do_clicked)
                    
            data_count += 1

    def init_horizontal_header(self, field, table, table_name, orderby):
        #table.select()
        self.setColumnCount(table.rowCount())
        query = table.query()
        
        if self.list_horizontal:
            self.horizontalHeader().hide()
            return
        
        headers = []
            
        query.exec_("select {0} from {1} order by {2}".format(field, table_name, orderby) )
        while query.next():             
            headers.append(query.value(0))      
        self.setHorizontalHeaderLabels(headers)
        
    def init_vertical_header(self, field, table, table_name, orderby):
        table.select()
        self.setRowCount(table.rowCount())
        
        if not self.list_horizontal:
            self.verticalHeader().hide()
            return        

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
    
    def reload(self):
        self.fill_cells(self.ui_table_name, self.data_table_name, self.ui_table, self.data_table, self.list_horizontal, True)
        
    def apply(self):        
        self.logger.debug('{0} apply changed'.format(self.data_table_name))
        pass
    def save(self):        
        for record_index in range(self.data_table.rowCount()):  # 由原始資料表依序處理
            record = self.data_table.record(record_index)       # 單筆原始資料
            if self.list_horizontal:            
                column = record_index 
            else:
                row = record_index
            
            for n_data_index in range(len(self.one_data_set)):  # 事先儲存的一筆資料, 為取得資料欄位屬性
                if self.list_horizontal:
                    row = n_data_index
                else:
                    column = n_data_index
                
                cell = self.cellWidget(row, column) # UI 表格上cell 有兩個type: QTableWidgetItem 和 QWidget (QCombox, QPushButton ...etc)
                if cell == None:                    # QTableWidgetItem
                    cell = self.item(row, column)
                    text = cell.text()              # 取得item上的字串
                else:
                    try:
                        text = cell.currentText()   # QCombox 才有currentText 函式. 其他QWidget會丟出exception.
                    except:
                        text = None
                        
                property_ = self.one_data_set[n_data_index][2]
                value = self.one_data_set[n_data_index][5]
                
                if not text == None:
                    record.setValue("{0}".format(property_), type(value)(text) )
                #else:
                    #record.setValue("{0}".format(property_), value)
            self.data_table.setRecord(record_index, record)
        self.data_table.submitAll()
        
        self.logger.debug('{0} save changed'.format(self.data_table_name))
        
    
        
    # 新增欄位由Sqlite的 utiltiy (Sqlite studio 或 導航貓) 操作
    #def add_one_data(self):
        #if self.list_horizontal:
            #self.insertColumn(self.columnCount())
        #else:
            #self.insertRow(self.rowCount())
            
        #record = self.data_table.record()
              
        #for n_data_index in range(len(self.one_data_set)):
            #on_str = self.one_data_set[n_data_index][0]
            #off_str = self.one_data_set[n_data_index][1]
            #property_ = self.one_data_set[n_data_index][2]
            #display_type = self.one_data_set[n_data_index][3]
            #value_set = self.one_data_set[n_data_index][4]
            #value = self.one_data_set[n_data_index][5]
            #if property_ == 'display_text':
                #value = '新增'
            
            #cell = self.make_cell(display_type, on_str, off_str, '', property_, value_set, value)
            #record.setValue(property_, value)
            
            #if self.list_horizontal:
                #self.add_cell(n_data_index, self.columnCount() -1, cell, display_type, value)
            #else:
                #self.add_cell(self.rowCount() -1, n_data_index, cell, display_type, value)
            #n_data_index +=1
            
            #if display_type == 'button':    # disconnect and then connect: 避免button重覆掛載do_clicked. 
                #try:
                    #cell.signals.clicked.disconnect(self.do_clicked)
                #except:
                    #pass
                #cell.signals.clicked.connect(self.do_clicked)
        #self.data_table.insertRecord(-1, record)
        #self.resizeRowsToContents()
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = IOTableTemplate('point', 'point_ui', False)
    app.exec_()

if __name__ == '__main__':
    main()        