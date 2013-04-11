#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtGui, QtCore
from datetime import datetime


class Motor(QtGui.QWidget):
    """    
    RobotIO_Motor is including two columns.
    
    """
    def __init__(self, title = 'Motor', parent = None):
        super(Motor, self).__init__(parent)        
        
        self.initUI(title)
    
    def initUI(self, title):
        #widget_base = QtGui.QWidget()  
        
        # Axis Status Table 
        v_layout = QtGui.QVBoxLayout()        
        
        self.motor_table = QtGui.QTableWidget()
        self.set_table_layout()
        v_layout.addWidget(self.motor_table)
        
        #widget_base.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #widget_base.setLayout(v_layout)
        
        #self.setWidget(widget_base)       
        self.setLayout(v_layout)
        self.setWindowTitle(title)
        self.show()
        
    def set_table_layout(self):
        self.motor_table.setColumnCount(4)
        self.motor_table.setRowCount(39)
        self.motor_table.setColumnWidth(0, 80)
        self.motor_table.setColumnWidth(1, 200)
        self.motor_table.setColumnWidth(2, 80)
        self.motor_table.setColumnWidth(3, 80)
        self.motor_table.setStyleSheet("QHeaderView::section { background-color:rgb(204, 204, 204) }");    #設定表格title的color
        
        self.motor_table.verticalHeader().hide()
        headers = ['Category', 'Name', 'Type', 'Value']
        self.motor_table.setHorizontalHeaderLabels(headers)
        self.set_table_content()
        
        self.motor_table.resizeColumnsToContents();  
        self.motor_table.resizeRowsToContents();
        
        
        
    def set_table_content(self):
        self.motor_table.setItem(0, 0, QtGui.QTableWidgetItem('AutoRun'))#.setTextAlignment(QtCore.Qt.AlignCenter))
        
        item_0_1 = QtGui.QTableWidgetItem('移動速度')
        item_0_1.setBackground(QtGui.QColor(255, 0, 0))
        self.motor_table.setItem(0, 1, item_0_1)
        
        item_0_2 = QtGui.QTableWidgetItem('Integer')
        item_0_2.setBackground(QtGui.QColor(255, 0, 0))        
        self.motor_table.setItem(0, 2, item_0_2)
        
        
        item_0_3 = QtGui.QTableWidgetItem('1200')
        item_0_3.setBackground(QtGui.QColor(255, 0, 0))   
        self.motor_table.setItem(0, 3, item_0_3)
        
        self.motor_table.setItem(1, 1, QtGui.QTableWidgetItem('mm'))        
        self.motor_table.setSpan(0, 0, 4, 1) 
        
        self.combobox = QtGui.QComboBox ()
        self.combobox.addItem('A59')
        self.combobox.addItem('Glue')
        self.combobox.addItem('MTF')
        self.combobox.addItem('A70')
        
        self.motor_table.setCellWidget(3, 2, self.combobox)
        
        self.combobox.currentIndexChanged.connect(self.combobox_text_changed)
        
    @QtCore.Slot(str)
    def combobox_text_changed(self, text):
        print(self.combobox.currentText())
    
    def save(self):
        print('Motor save')
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = Motor()
    app.exec_()


if __name__ == '__main__':
    main()          