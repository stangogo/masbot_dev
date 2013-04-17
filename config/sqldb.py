#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import site
import logging

from datetime import datetime
from collections import OrderedDict
from PySide import QtCore, QtSql, QtGui

from masbot.config.utils import Constants, Path
from masbot.config.db_table_def import *

class SqlDB():  
    _instance = None
    # singleton: to guarantee there is only one instance
    def __new__(cls):
        if not SqlDB._instance:
            SqlDB._instance = object.__new__(cls)
            cls.__initial(cls)
        return SqlDB._instance
        
    def __initial(self):
        self.__logger = logging.getLogger(__name__)
        
        db_dir = "{0}/{1}/{2}".format(Path.data_dir(), 
                                        Constants.MACHINE_NAME, 
                                        Constants.DB)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.__db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db_path = "{0}/{1}".format(db_dir, Constants.SQLITE_DB_NAME)
        self.__db.setDatabaseName(db_path)
        
        if not self.__db.open():
            self.__logger.error("database can not be opened: %s", db_path)
        else:
            # initial all base tables
            self.__query = QtSql.QSqlQuery()
            for cmd in table_schemas:
                result = self.__query.exec_(cmd)
                if not result:
                    error_msg = 'error when creating tables, cmd = {}'.format(cmd)
                    self.__logger.critical(error_msg)

    def __del__(self):
        self.__db.close()
        
    def get_table_model(self, table_name):
        if not self.__check_table_exist(table_name):
            self.__create_table(table_name)
                
        table_model = QtSql.QSqlTableModel()
        table_model.setTable(table_name)
        table_model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        table_model.select()
        return table_model

    def __create_table(self, table_name):
        table_def = DBTableDefine().get_table_def(table_name)
        table_query = "create table {0}(id INTEGER PRIMARY KEY autoincrement".format(table_name)
        for key, value in table_def.items():
            table_query = table_query + ", {0} {1}".format(key, value[0])
            
        table_query = table_query + ')'    
        exec_result = self.__query.exec_(table_query)    
        if not exec_result:
            msg = "create table, {0}: {1}".format(table_name, self.__query.lastError().text())
            self.__logger.error(msg)

    def __check_table_exist(self, table_name):
        self.__query.exec_("SELECT * FROM sqlite_master WHERE name ='{0}' and type='table'".format(table_name))
        return self.__query.first()

    def execute(self, cmd):
        self.__query.exec_(cmd)
        return self.__query
        
site_pack_path = site.getsitepackages()[1]
QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))
sqldb = SqlDB()
