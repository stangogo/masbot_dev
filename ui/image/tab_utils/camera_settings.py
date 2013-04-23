#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

author: Cigar Huang
last edited: August 2013
"""
import sys
from PySide.QtGui import *
from PySide.QtCore import *
from masbot.ui.image.tab_utils.aided_tool import Slider, AdjusterSlider
from masbot.ui.image.tab_utils.data_manager import *
from masbot.ui.control.ui_utils import *
from masbot.config.utils import UISignals, SigName

class RotateComboBox(QComboBox):
    indexChange = Signal(int, int, int, str) #row, column, index, text
    
    def __init__(self, row, column):
        super(RotateComboBox, self).__init__()
        self.row = row
        self.column = column
        self.init()
        self.currentIndexChanged.connect(self.combobox_index_changed)

    def init(self):
        self.addItem('無')
        self.addItem('上下')
        self.addItem('左右')
        self.addItem('上下左右')
        
    def combobox_index_changed(self, index):
        text = self.itemText(index)
        self.indexChange.emit(self.row, self.column, index, text)        
                
class SliderDlg(QFrame):
    value_changed = Signal()      
    def __init__(self, *args):
        super(SliderDlg, self).__init__()    
        self.init_ui(*args)
        self.show()
        
    def init_ui(self, *args):
        if not len(args) == 2:  # 建構子傳入 min 和 max 參數, 預設為 0 ~ 100
            (min_, max_) = [0, 100] 
        else:
            (min_, max_) = args
            
        min_label = QLabel('{0}'.format(min_))
        max_label = QLabel('{0}'.format(max_))
        
        self.slider = self.create_slider(min_, max_)
        
        vbox = QVBoxLayout()            # 垂直 Layout, 依序: 最大, 最小, 和 slider.
        vbox.addWidget(max_label,0)
        vbox.addWidget(self.slider,1)
        vbox.addWidget(min_label,0)
                
        vbox.setAlignment(self.slider, Qt.AlignCenter)       # 三個元件全部置中
        vbox.setAlignment(max_label, Qt.AlignCenter)
        vbox.setAlignment(min_label, Qt.AlignCenter)

        self.setLayout(vbox)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(QSize(60, 180))        
        self.setWindowFlags(Qt.SubWindow)
        
    def create_slider(self, min_, max_):
        slider = QSlider(Qt.Vertical)
        slider.setRange(min_, max_)
        slider.setValue(0)        
        slider.setMinimumHeight(120)        
        slider.valueChanged.connect(self.sliderChanged)
        return slider
    
    def setValue(self, new_value):
        self.slider.setValue(new_value)

    def value(self):
        return self.slider.value()    
    
    def sliderChanged(self, val):
        self.value_changed.emit()        

    def event(self, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
                
        return Slider.event(self, event)
       
class ParameterWidget(QFrame):
    def __init__(self):
        super(ParameterWidget, self).__init__()
        self.init_ui()
        
    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.create_light_box())        
        hbox.setContentsMargins(1,1,1,1)
        self.setFrameShape(QFrame.StyledPanel)
        self.setLayout(hbox)
  
    def set_lights(self, light_names):
        for k in range(len(light_names)-len(self.lights)):
            button = QPushButton()
            button.setCheckable(True)
            self.light_box.addWidget(button)
            self.lights.append(button)
            
        for i in range(len(self.lights)):
            try:
                self.lights[i].setText(light_names[i])
                self.lights[i].show()
            except:
                self.lights[i].hide()
    
    def create_light_box(self):
        gbox = QGroupBox('光源')
        self.lights = []    
        self.light_box = QVBoxLayout()
        self.light_box.setSpacing(0)
                
        self.light_box.setContentsMargins(1,1,1,1)        
        gbox.setLayout(self.light_box)        
        return gbox

class CameraSettings(QWidget):
    def __init__(self):
        super(CameraSettings, self).__init__()
        self.init_ui()
        
    def init_ui(self):

        vbox = QHBoxLayout()
        self.lights = ParameterWidget()
        vbox.addWidget(self.lights)
        vbox.addLayout(self.create_buttons())
        
        hbox = QHBoxLayout()
        self.table = self.create_camera_table()
        hbox.addWidget(self.table,4)
        hbox.addLayout(vbox,1)
        
        self.setLayout(hbox)         
        self.setMaximumWidth(700)        
        self.setWindowTitle('Camera Settings')
        self.show()
        
    def create_buttons(self):        
        vbox = QVBoxLayout()
        save_btn = create_button('save.png', '', '儲存(Save)')
        load_btn = create_button('reload.png', '', '讀取(Load)')
        apply_btn = create_button('check.png', '', '套用(Apply)')
        
        save_btn.setFixedSize(48,30)
        load_btn.setFixedSize(48,30)
        apply_btn.setFixedSize(48,30)
        
        vbox.addWidget(save_btn, 1, Qt.AlignBottom)
        vbox.addWidget(load_btn, 0, Qt.AlignBottom)
        vbox.addWidget(apply_btn, 0, Qt.AlignBottom)

        apply_btn.clicked.connect(self.apply)        
        
        return vbox
    
    def apply(self):
        self.feed_data(camera_data)
    
    def create_camera_table(self):
        self.h_header = ['模組名稱', '倍率(mm)', 'Gain', 'Shutter', '翻轉','序號', '解析度', '(FPS)']
        table = QTableWidget()        
        table.setColumnCount(len(self.h_header) )
        table.setHorizontalHeaderLabels(self.h_header)

        self.set_table_properties(table)
        return table
    

    
    def set_table_properties(self, table):    
        table.verticalHeader().hide()           #隱藏 row header (垂直的)        
        table.setSelectionBehavior(QAbstractItemView.SelectRows) #一次選一整欄 (row)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # 不可編輯
        table.resizeColumnsToContents()     #列寬符合內容S
        table.setToolTip('藍色欄位可滑鼠雙擊')
        table.cellDoubleClicked.connect(self.cellDclicked)
        table.itemSelectionChanged.connect(self.selectionChange)
                
        
    def feed_data(self, data):
        self.table.clear()
        self.table.setRowCount(0)
        
        
        self.table.setHorizontalHeaderLabels(self.h_header)
        
        keys = ['name', 'rate','gain', 'shutter', 'module', 'resolution', 'FPS']
        
        for one in get_specific_fields_camera_data(keys):
            self.insert_camera_in_table(self.table, one)
            
        self.table.resizeColumnsToContents()     #列寬符合內容
        self.table.resizeRowsToContents()        #欄高符合內容
        self.rawdata = data
    
    def insert_camera_in_table(self, table, settings):
        if table:
            row_index = table.rowCount()
            table.setRowCount(row_index + 1)
            
            (name, rate, gain, shutter, serial, pixel, FPS) = settings
            table.setItem(row_index, 0, self.create_table_item(name))
            table.setItem(row_index, 1, self.create_table_item(rate, '滑鼠雙擊重新取得倍率'))
            table.setItem(row_index, 2, self.create_table_item(gain, '滑鼠雙擊顯示調整條'))
            table.setItem(row_index, 3, self.create_table_item(shutter, '滑鼠雙擊顯示調整條'))
            
            rotate_combobox = RotateComboBox(row_index, 4)
            rotate_combobox.indexChange.connect(self.combobox_index_changed)
            
            table.setCellWidget(row_index, 4, rotate_combobox)
            
            table.setItem(row_index, 5, self.create_table_item(serial))
            table.setItem(row_index, 6, self.create_table_item(pixel))
            table.setItem(row_index, 7, self.create_table_item(FPS))
    
    def combobox_index_changed(self, row, column, index, text):
        print('combobox select:', row, column, index, text)

    
    def create_table_item(self, item_value, tooltip = None):
        item = QTableWidgetItem('{0}'.format(item_value))        
        #item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        
        if tooltip:
            item.setForeground(QBrush(Qt.GlobalColor.blue))
            item.setToolTip(tooltip)
        return item
    
    def selectionChange(self):
        if self.rawdata:
            lights = self.rawdata[self.table.currentRow()]['light']
        
        self.lights.set_lights(lights)
    
    def cellDclicked(self, row, column):
        if column in [2 ,3] :
            self.show_slider(row, column)

    def show_slider(self, row, column):
        if self.rawdata:        
            min_ = self.rawdata[row]['gain_min']
            max_ = self.rawdata[row]['gain_max']
            self.item = self.table.item(row, column)
            
            self.sliderdlg = SliderDlg(min_, max_)
        
            self.sliderdlg.setValue(int(self.item.text()))
            pos = QCursor.pos()
            self.sliderdlg.setGeometry(QRect(pos.x()+25, pos.y()- 50, 0,0,))
            self.sliderdlg.value_changed.connect(self.value_changed)
            self.sliderdlg.setWindowTitle(self.h_header[column])        
            
            
    def value_changed(self):        
        self.item.setText('{0}'.format(self.sliderdlg.value()))
            
        
def main():    
   
    
    app = QApplication(sys.argv)
    
    ex = CameraSettings()
    
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()        