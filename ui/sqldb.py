#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from datetime import datetime
from collections import OrderedDict
from PySide import QtCore, QtSql

from masbot.ui.utils import Constants, Path
from masbot.ui.db_table_def import DBTableDefine

class SqlDB():
    
    db_opened = False
    def __init__(self):
        db_dir = "{0}\\{1}\\{2}".format(Path.data_dir(), 
                                        Constants.MACHINE_NAME, 
                                        Constants.DB)
        
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        
        db_path = "{0}\\{1}".format(db_dir, Constants.SQLITE_DB_NAME)
        
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        db.setDatabaseName(db_path)
        
        if not db.open():
            print("資料庫不能打開: {0}".format(db_path))
        else:
            self.db_opened = True

    def get_table_model(self, table_name):
        if self.db_opened:
            if not self.check_table_exist(table_name):
                self.create_table(self, table_name)
                
            table_model = QtSql.QSqlTableModel()
            table_model.setTable(table_name)
            table_model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
            table_model.select()
            return table_model
        else:
            return None
            
    def create_table(self, table_name):
        table_def = DBTableDefine().get_table_def(table_name)
        self.__create_table(table_name, table_def)
                            
    def __create_table(self, table_name, fields):
        query = QtSql.QSqlQuery()
        table_query = "create table {0}(id INTEGER PRIMARY KEY autoincrement".format(table_name)
    
        for key, value in fields.items():
            table_query = table_query + ", {0} {1}".format(key, value[0])
            
        table_query = table_query + ')'    
        exec_result = query.exec_(table_query)    
        if not exec_result:                
            print("create table, {0}: {1}".format(table_name, query.lastError().text()))                    
        
    def check_table_exist(self, table_name):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT * FROM sqlite_master WHERE name ='{0}' and type='table'".format(table_name))
        return query.first()