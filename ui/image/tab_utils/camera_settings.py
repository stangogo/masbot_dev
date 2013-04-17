#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

author: Cigar Huang
last edited: August 2013
"""
import sys
from PySide.QtGui import *
from PySide.QtCore import *
from masbot.ui.image.tab_utils.aided_tool import AdjusterSlider
#from masbot.config.utils import Path

from masbot.config.utils import UISignals, SigName

class ParameterWidget(QFrame):
    def __init__(self, name):
        super(ParameterWidget, self).__init__()
        self.init_ui()
        
    def init_ui(self):
        self.sliders = []
        vbox_camera = QVBoxLayout()
        vbox_camera.addLayout(self.gain_shutter())                
        vbox_camera.addWidget(QPushButton('取得倍率'))
        
        hbox = QHBoxLayout()

        hbox.addLayout(vbox_camera)
        hbox.addWidget(self.light_buttons())

        hbox.setContentsMargins(1,1,1,1)
        self.setFrameShape(QFrame.StyledPanel)
        self.setLayout(hbox)
    
    def light_buttons(self):
        gbox = QGroupBox('光源')        
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        
        btn1 = QPushButton('光源1')
        btn1.setContentsMargins(1,1,1,1)
        
        btn2 = QPushButton('光源2')
        btn2.setContentsMargins(1,1,1,1)        
        
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(QPushButton('光源3'))
        vbox.addWidget(QPushButton('光源4'))
        vbox.addWidget(QPushButton('光源5'))
        vbox.addWidget(QPushButton('光源6'))
        
        vbox.setContentsMargins(1,1,1,1)
        
        gbox.setLayout(vbox)
        
        return gbox

    def gain_shutter(self):
        hbox = QHBoxLayout()
        
        hbox.addWidget(AdjusterSlider(0, 1394, 'Gain', False))
        hbox.addWidget(AdjusterSlider(0, 1394, 'Shutter', False))
        
        #hbox.addLayout(self.slider('Gain', 0, 1394))
        #hbox.addLayout(self.slider('Shutter', 0, 1394))
        return hbox        
    
    def slider(self, text, min_, max_):
        slider = QSlider(Qt.Vertical)
        slider.setRange(min_, max_)
        slider.valueChanged.connect(self.valueChanged)
        #slider.mousePressEvent.connect(self.
        
        self.sliders.append(slider)
        
        vbox = QVBoxLayout()
        name_label = QLabel(text)
        max_label = QLabel('{0}'.format(max_))
        min_label = QLabel('{0}~{1}'.format(min_, max_))
        
        vbox.addWidget(name_label)
        vbox.addWidget(max_label)
        vbox.addWidget(slider)
        vbox.addWidget(min_label)
        
        return vbox
    
    def valueChanged(self, value):        
        QToolTip.showText(QCursor.pos(), '{0}'.format(value))

class CameraSettings(QWidget):


    def __init__(self):
        super(CameraSettings, self).__init__()
        self.init_ui()
        
    def init_ui(self):

        vbox = QVBoxLayout()
        vbox.addWidget(ParameterWidget('攝影機參數設定'))
        vbox.addLayout(self.create_buttons())
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.create_camera_table(),2)        
        hbox.addLayout(vbox,1)
        
        self.setLayout(hbox)        
        
        self.setMaximumWidth(700)        
        self.setWindowTitle('Camera Settings')
        self.show()
        
    def create_buttons(self):
        
        vbox = QHBoxLayout()
        vbox.addWidget(QPushButton('儲存(Save)'), 1, Qt.AlignBottom)
        vbox.addWidget(QPushButton('讀取(Load)'), 0, Qt.AlignBottom)
        vbox.addWidget(QPushButton('套用(Apply)'), 0, Qt.AlignBottom)
                
        return vbox
    
    def create_camera_table(self):
        h_header = ['模組名稱', '倍率(mm)', 'Gain', 'Shutter', '上下翻轉', '左右翻轉' , '序號', '解析度', '(FPS)']
        table = QTableWidget()        
        table.setColumnCount(len(h_header) )
        table.setHorizontalHeaderLabels(h_header)
     
        table.setRowCount(6)
        
        table.verticalHeader().hide()    
        
        self.insert_camera_in_table(table, ['上攝影機模組', 0.00625, 100, 100, '5DW5F65E65EFE6', '1624*1224', 30], 0)
        self.insert_camera_in_table(table, ['下攝影機模組', 0.00703, 200, 300, '5DW5F6DFDSWD63', '1624*1224', 30], 1)
        self.insert_camera_in_table(table, ['監控模組', 0.00662, 233, 122,'5GRTESFD6W5555', '1624*1224', 30], 2)
        self.insert_camera_in_table(table, ['Tray盤定位模組', 0.00730, 443, 322, '5DW5DGDG6WEWC5', '1624*1224', 30], 3)
        self.insert_camera_in_table(table, ['USB影像裝置', 1, 11, 200, 'USB影像裝置', '640*480', 30], 4)

        table.setToolTip('彩色欄位可滑鼠雙擊')
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setCellWidget
        table.cellDoubleClicked.connect(self.celldclicked)
        return table
    
    def insert_camera_in_table(self, table, settings, row_index, ):
        if table:
            (name, rate, gain, shutter, serial, pixel, FPS) = settings
            table.setItem(row_index, 0, self.create_table_item(name))
            table.setItem(row_index, 1, self.create_table_item(rate, '滑鼠雙擊重新取得倍率'))
            table.setItem(row_index, 2, self.create_table_item(gain))
            table.setItem(row_index, 3, self.create_table_item(shutter))
            table.setItem(row_index, 4, self.create_table_item('翻轉', '雙擊滑鼠上下翻轉'))
            table.setItem(row_index, 5, self.create_table_item('翻轉', '雙擊滑鼠左右翻轉'))
            table.setItem(row_index, 6, self.create_table_item(serial))
            table.setItem(row_index, 7, self.create_table_item(pixel))
            table.setItem(row_index, 8, self.create_table_item(FPS))
    
    def create_table_item(self, item_value, tooltip = None):
        item = QTableWidgetItem('{0}'.format(item_value))        
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        
        if tooltip:
            item.setBackground(Qt.yellow)
            item.setToolTip(tooltip)
        return item
    
    def celldclicked(self, row, column):
        print('cell double click {0}, {1}'.format( row, column))
        
def main():    
    app = QApplication(sys.argv)
    
    #with open("{0}/stylesheet.css".format(Path.mosbot_dir()), 'r') as cssFile:
        #styleSheet =cssFile.read()
 
    #Settings = { "tabcolor":"#17B6FF", "fontsize":"10px" , "tablecolor":"#17B6BB"}
    #styleSheet = styleSheet % Settings 
    #app.setStyleSheet(styleSheet)    
    
    ex = CameraSettings()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()        