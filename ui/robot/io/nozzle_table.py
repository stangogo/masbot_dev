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
    def __init__(self, data_table_name, order_by, horizontal):
        super(NozzleTable, self).__init__(data_table_name, order_by, horizontal)
        UISignals.GetSignal(SigName.DI_IN).connect(self.di_changed)
        UISignals.GetSignal(SigName.DO_IN).connect(self.do_changed)        
        self.horizontalHeader().hide()   
   
    def do_clicked(self, io_num, on_off, row, column, table):
        if not table == self.table_name:
            return        
                
        sig = UISignals.GetSignal(SigName.DO_OUT)
        sig.emit(io_num, on_off)
        print(io_num)
    
    def do_di_changed(self, new_status, dio_list, bOn):

        
        if new_status == None:
            return
        
        if len(new_status) > 1: 
            for i in range(0, len(new_status)): # i io number
                value = dio_list.get(i)         # 從dict o_num = i object
                if not value == None:           
                    value.on_off(new_status[i]) # 將On-Off 設進DIO object
                    
        elif len(new_status) == 1:
            value = dio_list.get(new_status[0])    # 從dict io_num = new_status object
            if not value == None:           
                value.on_off(bOn)               # 將bOn 設進DIO object 

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
        
        self.nozzle_table = NozzleTable('nozzle', ['key'], QtCore.Qt.Orientation.Horizontal)
        
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

