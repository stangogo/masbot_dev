#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

author: Cigar Huang
last edited: August 2013
"""
import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from masbot.ui.image.tab_utils.data_manager import *
from masbot.config.utils import *

class ImageMessage(QWidget):
    def __init__(self):
        super(ImageMessage, self).__init__()
        self.init_ui()

        try:
            UISignals.GetSignal(SigName.IMG_MESSAGE).connect(self.message_in)
        except:
            self.feed_data(demo_image_message)
        
    def init_ui(self):
        hbox = QHBoxLayout()
        self.table = self.create_message_table()
        hbox.addWidget(self.table)
        
        self.setLayout(hbox)         
        self.setMaximumWidth(700)        
        self.setWindowTitle('影像辨識訊息')
        self.show()
        
    def create_message_table(self):
        self.h_headers = ['時間', '辨識工作', '結果', '辨識時間(s)', '檔案路徑']
        table = QTableWidget()        
        table.setColumnCount(len(self.h_headers) )
        table.setHorizontalHeaderLabels(self.h_headers)

        self.set_table_properties(table)
        return table
    
    def set_table_properties(self, table):    
        table.setSelectionBehavior(QAbstractItemView.SelectRows) #一次選一整欄 (row)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # 不可編輯
        table.resizeColumnsToContents()     #列寬符合內容S
        table.setToolTip('滑鼠雙擊開啟影像檔')
        table.cellDoubleClicked.connect(self.cellDclicked)
                
    def feed_data(self, data):
        self.table.clear()
        self.table.setRowCount(0)
        
        self.table.setHorizontalHeaderLabels(self.h_headers)
        
        for one in data:
            self.insert_one_data(self.table, one)
            
        self.table.resizeColumnsToContents()     #列寬符合內容
        self.table.resizeRowsToContents()        #欄高符合內容
    
    def insert_one_data(self, table, data):
        if table:
            row_index = table.rowCount()
            table.setRowCount(row_index + 1)
            try:
                (time, job, result, spend_time, file_path) = data
                table.setItem(row_index, 0, self.create_table_item(time))
                table.setItem(row_index, 1, self.create_table_item(job))
                table.setItem(row_index, 2, self.create_table_item(result))
                table.setItem(row_index, 3, self.create_table_item(spend_time))
                table.setItem(row_index, 4, self.create_table_item(file_path))
                
                self.table.resizeColumnsToContents()     #列寬符合內容
                self.table.resizeRowsToContents()        #欄高符合內容                
            except e: 
                print (e)
    
    def create_table_item(self, item_value, tooltip = None):
        item = QTableWidgetItem('{0}'.format(item_value))        
        
        if tooltip:
            item.setForeground(QBrush(Qt.GlobalColor.blue))
            item.setToolTip(tooltip)
        return item    
    
    def cellDclicked(self, row, column):
        cur_item = self.table.item(row, 4)
        
        self.show_file(cur_item.text())

    def show_file(self, file_path):
        if os.path.exists(file_path):
            UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit([file_path, None, '', ImagePreviewMode.RealTime])
            #print('open {0}'.format(file_path))
        else:
            print('not exist {0}'.format(file_path))
            
    def message_in(self, message):
        self.insert_one_data(self.table, message)
        
        
def main():    
    app = QApplication(sys.argv)
    ex = ImageMessage()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()        