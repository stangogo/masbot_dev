# -- coding: utf-8 --
# Title          : TrayInfoTable.py
# Description    : 繼承自QTableView, bind到資料庫的TrayInfo的資料表, 資料表欄位定義在一個YAML格式的檔案裡
#                  程式會讀取該檔的設定, 產生資料表和設定table的header 
#                
#                LogTime:
#                    HeaderName: 退盤時間
#                    Type: varchar(20)
#                    order: 0
#                CT:
#                    HeaderName: 單顆組裝時間
#                    Type: float
#                    order: 1
#                ProdName:
#                    HeaderName: 產品名稱
#                    Type: varchar(20)
#                    order: 2
#
# Author         : Cigar Huang
# Date           : 20130313
# Dependency     : 
# Usage          : import from TrayInfoTable
# Notes          : 
# Example        :  tray_info_table = TrayInfoTable('YourName')

import os
import logging
import sys

from collections import OrderedDict
from datetime import datetime
from PySide import QtGui, QtCore, QtSql

from masbot.ui.sqldb import SqlDB
from masbot.ui.db_table_def import DBTableDefine



class TrayInfoTable(QtGui.QTableView):
    
    def __new__(self, table_name):        
        self.sqldb = SqlDB()
        self.table_model = self.sqldb.get_table_model(table_name)
         
        return QtGui.QTableView.__new__(self)            
    
    def __init__(self, table_name):
        super(TrayInfoTable, self).__init__()
        
        self.bind_to_table_model(table_name)
            
        #self.setStyleSheet("QTableView{selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5, stop: 0 #FF92BB, stop: 1 green)}")        
        self.setStyleSheet("QTableView{selection-background-color:yellow}")
        self.setWindowTitle('Tray Info Table')
        self.show()
    
    def __del__(self): 
        self.table_model.submitAll()

    def set_header_name(self, table_name):
        
        self.table_model.removeColumn(0)    #don't show the ID
        
        self.table_define_dict = DBTableDefine().get_table_def(table_name)
        index = 0
        for values in self.table_define_dict.values():
            self.table_model.setHeaderData(index , QtCore.Qt.Horizontal, values[1]) 
            index +=1
            
                                                 
    def bind_to_table_model(self, table_name):
        self.table_model.setTable(table_name)
        self.table_model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.table_model.select(); 
        
        self.set_header_name(table_name)
        self.setModel(self.table_model)
        self.resizeColumnsToContents()
        #self.setColumnWidth(0, 40)
        
            
    def get_all_data(table_name):
        """
        set QSqlQueryModel to QTableView and get all data from table of database.
        """
        model = QtSql.QSqlQueryModel()
        model.setQuery('select * from {0}', table_name)
        self.setModel(model)
               
    def add_message(self, new_data):
        record = self.table_model.record()
        now_time = datetime.now()        
                
        for key in self.table_define_dict.keys():
            record.setValue(key, new_data[key])
            
        self.table_model.insertRecord(-1,record)    # -1: append new record in last row.
        self.scrollToBottom()
                    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = TrayInfoTable('TrayInfo')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        