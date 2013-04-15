#!/usr/bin/python
# -*- coding: utf-8 -*-


import win32api
import win32con
import sys

from PySide import QtGui, QtCore

from masbot.config.db_table_def import DBTableDefine
from masbot.config.sqldb import sqldb
from masbot.config.utils import Path
from masbot.config.utils import UISignals, SigName
from masbot.ui import preaction

class AxisButton(QtGui.QPushButton):
    row = -1
    column = -1
    axis = ""
    scale = 1.0
   
    def __new__(self, icon, text=None):
        if text == None:
            if type(icon) == type(""):
                self.text = icon
            return QtGui.QPushButton.__new__(self, icon, "")
        else:
            self.text = text
            return QtGui.QPushButton.__new__(self, icon, text)
            
            
class AxisTable(QtGui.QTableWidget):
    
    scale_list = []
    row_dict = {}
    column_dict = {}
    
    def __init__(self):  
        super(AxisTable, self).__init__()
        self.init_ui()
        
        self.setStyleSheet("QTableView{selection-background-color:green}")
        UISignals.GetSignal(SigName.ENTER_AXIS_TABLE).connect(self.from_outside)
        #self.cellClicked.connect(self.new_cell)
        
        
    #def new_cell(self, row, column):
        #print("row: {0}, column: {1}, currentRow:{2}, currentColumn:{3}".format(row, column, self.currentRow(), self.currentColumn()))
        
    def init_ui(self):
        
        axis_table_model = sqldb.get_table_model('single_axis')
        
        self.setColumnCount(axis_table_model.rowCount())
        
        
        #欄寬 / ��        
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, 65)
        #self.setColumnWidth(self.columnCount()-1, 50)        
                
        #設��格title�color
        self.setStyleSheet("QHeaderView::section { background-color:rgb(184, 198, 137) }");    

        #橫軸 bar          
        H_headers = []
        query = axis_table_model.query()
        query.exec_("select display_text from SingleAxis")
        
        while query.next():
            H_headers.append(query.value(0))
                    
            
        self.setHorizontalHeaderLabels(H_headers)
        
        #縱軸 bar        
        V_Header = DBTableDefine().get_table_def('AxisOP')
        self.setRowCount(len(V_Header))
        self.setVerticalHeaderLabels(V_Header)
        #self.resizeRowsToContents()    #符�
        index = 0
        for op in V_Header:
            self.row_dict[op] = index
            index +=1
        
        self.fill_table(query)
        self.setWindowTitle('Axis Operation')
        
        #self.resizeRowsToContents()    #符�        
        #self.verticalHeader().hide()   #���側欄header
        
    def fill_table(self, query):
        query.exec_("select key from SingleAxis")
        index = 0
        for i in range(0, self.columnCount()):
            #btn_add = AxisButton(QtGui.QIcon("{0}/Start.bmp".format(Path.imgs_dir())),"+")
            #btn_add = AxisButton(QtGui.QIcon("C:\Python33\Lib\site-packages\masbot\ui/imgs/Start.bmp"),"+")
            btn_add = AxisButton("+")
            btn_minus = AxisButton('-')
            btn_scale = AxisButton('1')
            
            btn_add.column = btn_minus.column= btn_scale.column = i
            if query.next():
                btn_add.axis = btn_minus.axis = btn_scale.axis = query.value(0)
                self.column_dict[btn_add.axis] = index
                index += 1
            
            btn_add.clicked.connect(self.add_clicked)
            btn_minus.clicked.connect(self.minus_clicked)
            btn_scale.clicked.connect(self.scale_clicked)
            
            self.setCellWidget(2, i, btn_add)
            self.setCellWidget(3, i, btn_minus)
            self.setCellWidget(4, i, btn_scale)
            
            self.scale_list.append(btn_scale)
            
    def from_outside(self, row, axis, value):
        try:
            n_row = self.row_dict[row]
            n_col = self.column_dict[axis]
            item = QtGui.QTableWidgetItem("{0:.3f}".format(value))
            self.setItem(n_row, n_col, item)
        except:
            print("from_outside error: {0}".format(sys.exc_info()[1]))

    def minus_clicked(self):
        sender = self.sender()
        scale_value = self.scale_list[sender.column].scale    
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).emit(sender.axis, -scale_value  )
        
    def add_clicked(self):
        sender = self.sender()
        scale_value = self.scale_list[sender.column].scale
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).emit(sender.axis, scale_value)
        
    def scale_clicked(self):
        sender = self.sender()
        sender.scale = sender.scale *10
        if sender.scale > 10:
            sender.scale = 0.01
        sender.setText("{0}".format(sender.scale))
        
        print("scale_clicked - axis: {0}".format(sender.axis))
    
    def keyPressEvent(self, event):    
        _key = event.key()
        if  _key == QtCore.Qt.Key.Key_Plus or \
            _key == QtCore.Qt.Key.Key_Minus or \
            _key == QtCore.Qt.Key.Key_Up or \
            _key == QtCore.Qt.Key.Key_Down or \
            _key == QtCore.Qt.Key.Key_Left or \
            _key == QtCore.Qt.Key.Key_Right:
            
            # win32api and win32com �要��pywin32            
            #if win32api.GetAsyncKeyState(win32con.VK_SHIFT) < 0:
            
            if win32api.GetAsyncKeyState(win32con.VK_CONTROL) < 0:
                print("{0}".format(event.key()))
                if not self.currentRow == 0:
                    axis_name = self.get_axis_name(self.currentColumn())
                    scale_value = self.scale_list[self.currentColumn()].scale
                    dest = UISignals.GetSignal(SigName.FROM_AXIS_TABLE)
                    
                    if _key == QtCore.Qt.Key.Key_Up:
                        dest.emit(axis_name, scale_value)
                    elif _key == QtCore.Qt.Key.Key_Down: 
                        dest.emit(axis_name, scale_value * -1)
                        
    def get_axis_name(self, index):
        for key, value in self.column_dict.items():
            if value == index:
                return key
        
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = AxisTable()
    window.show()  
    app.exec_()