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

class DisplayCheck(QtGui.QWidget):
#class DisplayCheck(QtGui.QLabel):
    row = -1
    column = -1
    axis = ""
    clicked = QtCore.Signal()
    
    def __init__(self, *args):
        super(DisplayCheck, self).__init__(*args)
        self.bChecked = False
        self.init_ui()
        self.setChecked(True)
        
    def init_ui(self):
        self.label = QtGui.QLabel()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label)
        layout.setAlignment(self.label, QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.setContentsMargins(0,0,0,0)
        
    def mousePressEvent(self, event):    
        self.setChecked(not self.bChecked)
        
    def setChecked(self, bChecked):
        if self.bChecked == bChecked:
            return
        
        if bChecked:            
            self.label.setPixmap(QtGui.QPixmap('{0}/checkbox_checked.png'.format(Path.imgs_dir())).scaledToHeight(18))
        else:
            self.label.setPixmap(QtGui.QPixmap('{0}/checkbox_unchecked.png'.format(Path.imgs_dir())).scaledToHeight(18))
            
        self.bChecked =bChecked

class AxisButton(QtGui.QPushButton):
    row = -1
    column = -1
    axis = ""
    scale = 1.0
   
    def __init__(self, *args):
        super(AxisButton, self).__init__(*args)

class ScaleComboBox(QtGui.QComboBox):
    def __init__(self):
        super(ScaleComboBox, self).__init__()

        self.row = -1
        self.column = -1
        self.axis= ''
        self.init()

    def init(self):
        self.addItem('0.01')
        self.addItem('0.05')
        self.addItem('0.1')
        self.addItem('0.5')
        self.addItem('1')
        self.addItem('5')
        self.addItem('10')
        
    def get_value(self):
        return float(self.currentText())
            
class AxisTable(QtGui.QTableWidget):
    
    scale_list = []
    row_dict = {}
    column_dict = {}
    
    def __init__(self):  
        super(AxisTable, self).__init__()
        self.init_ui()
        
        UISignals.GetSignal(SigName.ENTER_AXIS_TABLE).connect(self.from_outside)
        self.cellClicked.connect(self.new_cell)
        
        
    def new_cell(self, row, column):
        print("row: {0}, column: {1}, currentRow:{2}, currentColumn:{3}".format(row, column, self.currentRow(), self.currentColumn()))
        
    def init_ui(self):
        axis_table_model = sqldb.get_table_model('single_axis')
        self.setColumnCount(axis_table_model.rowCount())

        #horizontal header
        H_headers = []
        query = axis_table_model.query()
        query.exec_("select display_text from single_axis")
        
        while query.next():
            H_headers.append(query.value(0))                
            
        self.setHorizontalHeaderLabels(H_headers)
        
        #Vertical header
        v_name = DBTableDefine().get_table_def('AxisOP')    # 取回table縱向header的定義
        index = 0
        for op in list(name[0] for name in v_name):         # row 在對應資料庫欄位的名稱存進dict裡
            self.row_dict[op] = index
            index +=1

        V_Header = list(name[1] for name in v_name)         # index 1 是中文名稱
        self.setRowCount(len(V_Header))
        
        self.checkbox_widget_item = QtGui.QTableWidgetItem()    # 設定 check box 的圖到垂直 header
        self.checkbox_widget_item.setIcon(QtGui.QPixmap('{0}/checkbox_checked.png'.format(Path.imgs_dir())))        
        self.setVerticalHeaderItem(self.row_dict['display'], self.checkbox_widget_item)
        
        self.setVerticalHeaderLabels(V_Header)              # 設定header名稱
        
        self.fill_table(query)
        
        for i in range(self.columnCount()):
            self.setRowHeight(i, 26)
            
        self.resizeColumnsToContents()
        self.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  # 不可編輯
        
        self.verticalHeader().sectionClicked.connect(self.vertical_header_clicked)
        
        self.setWindowTitle('Axis Operation')
        
    def fill_table(self, query):
        query.exec_("select key from single_axis")
        index = 0
        for i in range(0, self.columnCount()):
            btn_add = AxisButton(QtGui.QIcon("{0}/up.png".format(Path.imgs_dir())), "")
            btn_minus = AxisButton(QtGui.QIcon("{0}/down.png".format(Path.imgs_dir())), "")
            btn_scale = ScaleComboBox()
            display_checkbox = DisplayCheck()
            
            btn_add.column = btn_minus.column= btn_scale.column = display_checkbox.column = i
            if query.next():
                btn_add.axis = btn_minus.axis = btn_scale.axis = display_checkbox.axis = query.value(0)
                self.column_dict[btn_add.axis] = index
                index += 1
            
            btn_add.clicked.connect(self.add_clicked)
            btn_minus.clicked.connect(self.minus_clicked)
            
            self.setCellWidget(2, i, btn_add)
            self.setCellWidget(3, i, btn_minus)
            self.setCellWidget(4, i, btn_scale)
            self.setCellWidget(5, i, display_checkbox)
            
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
        scale_value = self.scale_list[sender.column].get_value()
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).emit(sender.axis, -scale_value  )
        
    def add_clicked(self):
        sender = self.sender()
        scale_value = self.scale_list[sender.column].get_value()
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).emit(sender.axis, scale_value)
                
    def keyPressEvent(self, event):    
        _key = event.key()
        if  _key == QtCore.Qt.Key.Key_Plus or \
            _key == QtCore.Qt.Key.Key_Minus or \
            _key == QtCore.Qt.Key.Key_Up or \
            _key == QtCore.Qt.Key.Key_Down or \
            _key == QtCore.Qt.Key.Key_Left or \
            _key == QtCore.Qt.Key.Key_Right:
            
            # win32api and win32com: install pywin32
            #if win32api.GetAsyncKeyState(win32con.VK_SHIFT) < 0:
            
            if win32api.GetAsyncKeyState(win32con.VK_CONTROL) < 0:
                print("{0}".format(event.key()))
                if not self.currentRow == 0:
                    axis_name = self.get_axis_name(self.currentColumn())
                    scale_value = self.scale_list[self.currentColumn()].get_value()
                    dest = UISignals.GetSignal(SigName.FROM_AXIS_TABLE)
                    
                    if _key == QtCore.Qt.Key.Key_Up:
                        dest.emit(axis_name, scale_value)
                    elif _key == QtCore.Qt.Key.Key_Down: 
                        dest.emit(axis_name, scale_value * -1)
                        
    def get_axis_name(self, index):
        for key, value in self.column_dict.items():
            if value == index:
                return key
    
    
    def vertical_header_clicked(self, index):
        if index == self.row_dict['display']:
            if self.checkbox_widget_item.checkState() == QtCore.Qt.CheckState.Checked:
                self.checkbox_widget_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.checkbox_widget_item.setIcon(QtGui.QPixmap('{0}/checkbox_checked.png'.format(Path.imgs_dir())))
                bCheck = True
            else:
                self.checkbox_widget_item.setCheckState(QtCore.Qt.CheckState.Checked)
                self.checkbox_widget_item.setIcon(QtGui.QPixmap('{0}/checkbox_unchecked.png'.format(Path.imgs_dir())))
                bCheck = False
                
            for column in range(self.columnCount()):
                self.cellWidget(self.row_dict['display'], column).setChecked(bCheck)
    
    def change_diaplay_mode(self, editable):
        if editable:
            self.setRowHeight(self.row_dict['display'], 0)  # 隱藏"勾選"列
        else:
            self.setRowHeight(self.row_dict['display'], 27) # 顯示"勾選"列            

        for column in range(self.columnCount()):
            cell_widget = self.cellWidget(self.row_dict['display'], column)
            if (cell_widget.bChecked and self.columnWidth(column)== 0) or not editable:
                self.resizeColumnToContents(column)
            elif not cell_widget.bChecked:
                self.setColumnWidth(column, 0)
                
                
        
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = AxisTable()
    window.show()  
    app.exec_()