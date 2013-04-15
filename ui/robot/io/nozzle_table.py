#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import sys

from datetime import datetime
from PySide import QtGui, QtCore, QtSql

#from masbot.config.sqldb import SqlDB
#from masbot.config.sqldb import sqldb
from masbot.config.utils import Path
from masbot.ui.control.dio_button import *
from masbot.ui import preaction

from masbot.ui.robot.io.IO_table_template import IOTableTemplate

class NozzleTable(IOTableTemplate):
    def __init__(self, data_table_name, ui_table_name, horizontal):
        super(NozzleTable, self).__init__(data_table_name, ui_table_name, horizontal)
        UISignals.GetSignal(SigName.DI_IN).connect(self.di_changed)
        UISignals.GetSignal(SigName.DO_IN).connect(self.do_changed)        
   
    def do_clicked(self, io_num, on_off, row, column, table):
        if not table == self.data_table_name:
            return        
                
        sig = UISignals.GetSignal(SigName.DO_OUT)
        sig.emit(io_num, on_off)
    
    def do_di_changed(self, new_status, dio_list, bOn):

        
        if new_status == None:
            return
        
        if len(new_status) > 1: 
            for i in range(0, len(new_status)): # i io number
                value = dio_list.get(i)         # å¾ždict –å io_num = i object
                if not value == None:           
                    value.on_off(new_status[i]) # å°‡On-Off è¨­é€²DIO object è£
                    
        elif len(new_status) == 1:
            value = dio_list.get(new_status[0])    # å¾ždict –å io_num = new_status object
            if not value == None:           
                value.on_off(bOn)               # å°‡bOn è¨­é€²DIO object è£

    def do_changed(self, do_list, on_off):
        self.do_di_changed(do_list, self.do_dict, on_off)        
            
    def di_changed(self, di_list, on_off):
        self.do_di_changed(di_list, self.di_dict, on_off)
        
    #def save(self):
        #pass


class Nozzle(QtGui.QWidget):
    """    
    Nozzle is a QDockWidget embeded nozzle_table and docked on io_dock
    
    """
    def __init__(self, title = 'Nozzle', parent = None):
        super(Nozzle, self).__init__(parent)        
        
        self.init_ui(title)
    
    def init_ui(self, title):
        
        self.nozzle_table = NozzleTable('nozzle', 'nozzle_ui', True)        
        
        v_layout = QtGui.QVBoxLayout()
        v_layout.addWidget(self.nozzle_table)
        
        self.setLayout(v_layout)
        self.setWindowTitle(title)
        self.show()
        
    @QtCore.Slot(str)
    def combobox_text_changed(self, text):
        print(self.combobox.currentText())
        
    def save(self):
        self.nozzle_table.save()
        
    def reload(self):
        self.nozzle_table.reload()

def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = Nozzle()
    app.exec_()


if __name__ == '__main__':
    main()          




#class NozzleTable(QtGui.QTableWidget):        
    
    #do_dict = {}
    #di_dict = {}
    
    #def __init__(self, data_table_name, ui_table_name):
        #super(NozzleTable, self).__init__()
        
        #self.data_table = SqlDB().get_table_model(data_table_name)        
        #self.UI_table = SqlDB().get_table_model(ui_table_name)
        
        #self.init_vertical_header('display_text', ui_table_name)
        #self.init_horizontal_header('display_text',data_table_name)

        #self.fill_cells(ui_table_name, data_table_name)
        
        #for i in range(0, self.columnCount()):
            #self.setColumnWidth(i, 50)
            
        #UISignals.GetSignal(SigName.DI_IN).connect(self.di_changed)
        #UISignals.GetSignal(SigName.DO_IN).connect(self.do_changed)
                
        #self.setStyleSheet("QHeaderView::section { background-color:rgb(204, 100, 204) }");    #è¨­åè¡¨æ ¼title„color
        
        #self.setWindowTitle('Nozzle Table')
        #self.show()

    #def make_cell(self, type_, on_str, off_str, key, action, value_set, cur_value):
        #if type_ == 'button':  #DO
            #do_cell = NozzleDoButton(cur_value)
            #do_cell.set_properties(on_str, off_str, key, action)
            #self.do_dict[do_cell.io_num] = do_cell
            
            #return do_cell
        #elif type_ == 'DI_label': #DI
            #di_cell =  DIOLabel('{0}'.format(cur_value),False)#DISensor()
            #di_cell.io_num = cur_value
            #self.di_dict[di_cell.io_num] = di_cell
            #di_cell.set_properties(key, action)
            
            #cell_layout = QtGui.QHBoxLayout()
            #cell_layout.setContentsMargins(0,0,0,0)
            #cell_layout.addWidget(di_cell)
            #cell_widget = QtGui.QWidget()                
            #cell_widget.setLayout(cell_layout)
            
            #return cell_widget
        #elif type_ == 'combobox': #ComboBox            
            #self.get_value_set(value_set)
            #selection_cell = QtGui.QComboBox()
            #selection_cell.setInsertPolicy(QtGui.QComboBox.InsertPolicy.InsertAlphabetically)
            #options = self.get_value_set(value_set)
            
            #try:
                #index = options.index('{0}'.format(cur_value))
            #except:
                #index = -1
            
            #selection_cell.addItems(options)            
            #selection_cell.setCurrentIndex(index)
            #return selection_cell

    #def get_value_set(self, value_set):
        #option_table = SqlDB().get_table_model('option_value')
        #option_table.select()
        
        #query= option_table.query()
        #query.exec_("select value from option_value where option = '{0}'".format(value_set))        

        #options = []        
        #while query.next():
            #options.append("{0}".format(query.value(0)))
        #return options
    
    #def get_property_value(self, table_name, property_name):
        #self.data_table.select()
        #query = self.data_table.query()
        #query.exec_("select {0} from {1} order by id".format(property_name, table_name) )
        
        #data = []        
        #while query.next():
            #data.append(int(query.value(0)))
        #return data
        
        
    #def fill_cells(self, ui_table_name, data_table_name):
        ##row 0
        #self.UI_table.select()
        #query = self.UI_table.query()
        #query.exec_("select btn_on_str,btn_off_str,reference_val,display_type,value_set from {0} order by col_order".format(ui_table_name) )
        #n_row = 0
        #while query.next():
            #on_str = query.value(0)
            #off_str = query.value(1)
            #action = query.value(2) #©ç”¨™å€‹å€ –å´å€‹row„è å¡«å…¥.
            #type_ = query.value(3)
            #value_set = query.value(4)
            #action_data = self.get_property_value(data_table_name, action)            
            #for i in range(0, self.columnCount()):
                ##–å€‰action„å€ order by id, è·Ÿèmake_cell å¡«å…¥cellè£
                #key = self.column_key[i]
                #cell = self.make_cell(type_, on_str, off_str, key, action, value_set, action_data[i]) 
                #self.setCellWidget(n_row,i, cell)
                    
            #if type_ == 0:
                #try:
                    #cell.signals.clicked.disconnect(self.do_clicked)
                #except:
                    #pass
                #cell.signals.clicked.connect(self.do_clicked)
            #n_row += 1
                
    #def init_horizontal_header(self, field, table_name):
        #"""
        ##Read the properties of Nozzle, and save the the data in self.column_key
        ##header saves the header name of Nozzle table in UI
        
        #"""
        #self.data_table.select()
        #self.setColumnCount(self.data_table.rowCount())
        
        #query = self.data_table.query()
        #self.column_key = []
        #headers = []
        
        ##TODO: get DI and DO port and set them in to DO button and DI label.
        #query.exec_("select {0}, key from {1} order by id".format(field, table_name) )
        #while query.next():             
            #headers.append(query.value(0))      #header„åç¨
            #self.column_key.append(query.value(1))            
        #self.setHorizontalHeaderLabels(headers)
        
    #def init_vertical_header(self, field, ui_table_name):
        #self.UI_table.select()
        #self.setRowCount(self.UI_table.rowCount())
        #row_query = self.UI_table.query()
        #row_query.exec_("select {0} from {1} order by col_order".format(field, ui_table_name) )        
        #row_headers = []
        #while row_query.next():
            #row_headers.append(row_query.value(0))
        #self.setVerticalHeaderLabels(row_headers)
        #row_query.finish()
        
    #def do_clicked(self, io_num, on_off):        
        ##print('do {0} clicked {1}'.format(io_num, on_off))
        #sig = UISignals.GetSignal(SigName.DO_OUT)
        #sig.emit(io_num, on_off)
    
    #def do_di_changed(self, new_status, dio_list, bOn):
        #if new_status == None:
            #return
        
        #if len(new_status) > 1: 
            #for i in range(0, len(new_status)): # i io number
                #value = dio_list.get(i)         # å¾ždict –å io_num = i object
                #if not value == None:           
                    #value.on_off(new_status[i]) # å°‡On-Off è¨­é€²DIO object è£
                    
        #elif len(new_status) == 1:
            #value = dio_list.get(new_status[0])    # å¾ždict –å io_num = new_status object
            #if not value == None:           
                #value.on_off(bOn)               # å°‡bOn è¨­é€²DIO object è£

    #def do_changed(self, do_list, on_off):
        #self.do_di_changed(do_list, self.do_dict, on_off)        
        
    
    #def di_changed(self, di_list, on_off):
        #self.do_di_changed(di_list, self.di_dict, on_off)
        
    #def save(self):
        #pass
        
    
#def main():
    
    #app = QtGui.QApplication(sys.argv)
    #ex = NozzleTable('Nozzle', 'nozzle_ui')
    #app.exec_()

#if __name__ == '__main__':
    #main()        

