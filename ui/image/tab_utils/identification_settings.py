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
from masbot.config.utils import Path
from masbot.config.utils import UISignals, SigName
from masbot.ui.control.ui_utils import *

class Slider(QGroupBox):
    value_changed = Signal()
    def __init__(self, title):
        super(Slider, self).__init__(title)
        self.init_ui()
        
    def init_ui(self):
        (min_, max_) = [0, 100] 
            
        self.min_label = QLabel('')
        self.max_label = QLabel('')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.sliderChanged)
         
        self.cur_label = QLabel('{0}'.format(self.slider.value()))
        self.cur_label.setStyleSheet('QLabel{color : blue;}')# text-decoration: underline color blue}')
        self.cur_label.setContentsMargins(0,0,0,0)
        
        self.set_range(min_, max_)
        
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.min_label)
        hbox.addWidget(self.slider)          # 水平 Layout, 放置 slider, min and max label
        hbox.addWidget(self.max_label)        
        
        vbox = QVBoxLayout()            # 垂直 Layout, 放置 最大, 最小, 和 slider.
        vbox.addWidget(self.cur_label)
        vbox.addLayout(hbox)        
                
        vbox.setAlignment(hbox, Qt.AlignLeft)       # 置中
        vbox.setAlignment(self.cur_label, Qt.AlignCenter)        
        
        vbox.setContentsMargins(2,2,2,2)
        
        self.setLayout(vbox)        
        
    def set_range(self, min_, max_):
        self.slider.setRange(min_, max_)
        self.min_label.setText('{0}'.format(min_))
        self.max_label.setText('{0}'.format(max_))            
        
    def sliderChanged(self, val):        
        self.cur_label.setText('{0}'.format(val))
        self.value_changed.emit()    

    def value(self):
        return self.slider.value()
  
class IdentificationSettings(QWidget):
    def __init__(self):
        super(IdentificationSettings, self).__init__()
        self.init_ui()
        self.setCorrectionMode(False)
        
    def init_ui(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.init_info_bar())        
        vbox.addLayout(self.settings_layout())
                
        hbox = QHBoxLayout()
        
        hbox.addLayout(self.init_job_box(), 1)        
        hbox.addLayout(vbox, 3)
        
        self.setLayout(hbox)
        self.setMaximumWidth(700)        
        self.setWindowTitle('Identication Settings')
        self.show()

    def settings_layout(self):
        correction_box= QVBoxLayout()
        correction_box.addWidget(self.init_parameter_setting_box())
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.init_light_box())   # 光源選擇
        hbox.addLayout(correction_box)          # 參數調整
        hbox.addWidget(self.init_mgr_buttons()) # 儲存/載入/套用 按鈕
        
        hbox.setAlignment(self.mgr_buttons, Qt.AlignRight)
        return hbox

    def init_parameter_setting_box(self):
        
        hbox = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        # 左邊
        self.slider = Slider('1. 設定目標半徑')
        self.slider.set_range(50, 600)
        left_layout.addWidget(self.slider)
        
        # 右邊
        mode_combobox = QComboBox()
        mode_combobox.addItems(['顯示模式'])
        default_btn = create_button('', '預設值', '預設值')
        prev_btn =  create_button('up.png', '', '上一步')
        next_btn = create_button('down.png', '', '下一步')

        right_layout.addWidget(mode_combobox)
        right_layout.addWidget(default_btn)
        right_layout.addWidget(prev_btn)
        right_layout.addWidget(next_btn)
        right_layout.setSpacing(0)
        
        
        # 合起來
        
        hbox.addLayout(left_layout)
        hbox.addLayout(right_layout)
        hbox.addLayout(self.init_adjust_buttons())  # 確認/取消 按鈕
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.init_open_file_bar())
        vbox.addLayout(hbox)
        
        self.parameter_box = QGroupBox('參數設定')
        self.parameter_box.setLayout(vbox)    
        self.parameter_box.setStyleSheet('QGroupBox{background-color:lightblue}')
        #self.parameter_box.setFixedHeight(180)
        
        return self.parameter_box

    def init_slider(self, min_, max_, title):
        slider_groupbox = QGroupBox(title)
        layout = QHBoxLayout()
        layout.addWidget(Slider())

    def init_open_file_bar(self):
        # open file button
        open_file_btn = create_button('open_file.png', '', '開啟檔案')
        open_file_btn.setFixedSize(QSize(30, 30))
        open_file_btn.clicked.connect(self.open_file_dialog)
        
        # file path edit box
        self.file_path_edit = QLineEdit('D:\\Images\\LPCam2\\Image20120809_211044_396.bmp')
        
        # check box
        open_file_box = QHBoxLayout()
        preview_file_checkbox = QCheckBox('顯示檔案')
        preview_file_checkbox.clicked.connect(self.preview_file_checked)
        open_file_box.addWidget(preview_file_checkbox)
        open_file_box.addWidget(self.file_path_edit)
        open_file_box.addWidget(open_file_btn)
        open_file_box.setContentsMargins(0,0,0,0)
        
        self.open_file_bar = QWidget()
        self.open_file_bar.setContentsMargins(0,0,0,0)
        self.open_file_bar.setLayout(open_file_box)
                
        return self.open_file_bar
        
    def init_file_list(self):
        file_list = QComboBox()
        
        return file_list
        
    def init_light_box(self):
        self.lights = []    
        self.lights_layout = QVBoxLayout()
        self.lights_layout.setSpacing(0)
                
        self.lights_layout.setContentsMargins(1,1,1,1)        
        
        self.lights_box = QGroupBox('光源')
                
        self.lights_box.setLayout(self.lights_layout)
        self.lights_box.hide()

        #self.lights_box.setMinimumHeight(177)
        return self.lights_box
    
    def init_job_box(self):
        job_list = QListWidget()                
        job_list.clicked.connect(self.job_list_clicked)
        self.job_list = job_list
        
        self.adjust_btn = create_button('doc_edit.png', '校正', '校正(Adjust)')
        self.adjust_btn.setCheckable(True)
        self.adjust_btn.setFixedSize(QSize(70,30))   
        self.adjust_btn.clicked.connect(self.correction_click)
        
        vbox = QVBoxLayout()
        vbox.addWidget(job_list)
        vbox.addWidget(self.adjust_btn)
        
        vbox.setAlignment(self.adjust_btn, Qt.AlignCenter)    
        return vbox
    
    def init_mgr_buttons(self):        
        vbox = QVBoxLayout()

        save_btn = create_button('save.png', '', '儲存(Save)')
        load_btn = create_button('reload.png', '', '讀取(Load)')
        apply_btn = create_button('check.png', '', '變更(Apply)')
        
        save_btn.setFixedSize(48,30)
        load_btn.setFixedSize(48,30)
        apply_btn.setFixedSize(48,30)        
        
        #vbox.addWidget(adjust_btn, 1, Qt.AlignTop)
        vbox.addWidget(save_btn, 1, Qt.AlignBottom)
        vbox.addWidget(load_btn, 0, Qt.AlignBottom)
        vbox.addWidget(apply_btn, 0, Qt.AlignBottom)
        
        #save_btn.clicked.connect
        #load_btn.clicked.connect
        #apply_btn.clicked.connect
        #cancel_btn.clicked.connect
        
        apply_btn.clicked.connect(self.apply)
        
        self.mgr_buttons = QWidget()
        self.mgr_buttons.setLayout(vbox)
        return self.mgr_buttons
        
    def init_adjust_buttons(self):
        vbox = QVBoxLayout()

        confirmed_btn = create_button('check.png', '', '確認(Confirm)')
        cancel_btn = create_button('cancel.png', '', '取消(Cancel)')
        
        confirmed_btn.setFixedSize(48,30)
        cancel_btn.setFixedSize(48,30)
        
        vbox.addWidget(confirmed_btn, 1, Qt.AlignBottom)
        vbox.addWidget(cancel_btn, 0, Qt.AlignBottom)
        
        # confirmed_btn.clicked.connect
        # cancel_btn.clicked.connect            
        return vbox
                
    def init_info_bar(self):
        EDGE= 26
        
        light_icon = QLabel()
        light_icon.setPixmap(QPixmap('{0}/light.png'.format(Path.imgs_dir())).scaledToHeight(EDGE))
        light_icon.setFixedSize(EDGE,EDGE)
        
        self.light_label = QLabel(' ')
        #self.light_label.setWordWrap(True)
        
        camera_icon = QLabel()
        camera_icon.setPixmap(QPixmap('{0}/camera.png'.format(Path.imgs_dir())).scaledToHeight(EDGE))
        camera_icon.setFixedSize(EDGE, EDGE)
        self.camera_label = QLabel()
        
        file_icon = QLabel()
        file_icon.setPixmap(QPixmap('{0}/file.png'.format(Path.imgs_dir())).scaledToHeight(EDGE))
        file_icon.setFixedSize(EDGE,EDGE)
        self.file_list = self.init_file_list()
        
        hbox = QHBoxLayout()
        hbox.addWidget(light_icon)
        hbox.addWidget(self.light_label)    
        hbox.addWidget(camera_icon)        
        hbox.addWidget(self.camera_label)        
        hbox.addWidget(file_icon)
        hbox.addWidget(self.file_list)        
        
        hbox.setContentsMargins(0,0,0,0)        
        
        self.info_bar = QWidget()
        self.info_bar.setLayout(hbox)
        self.info_bar.setContentsMargins(0,0,0,2)
        return self.info_bar
    
    def set_lights(self, light_names):
        # 相減: 若大於零表示UI上的checkbox不夠多. 
        for k in range(len(light_names)-len(self.lights)):
            light_checkbox = QCheckBox()            
            self.lights_layout.addWidget(light_checkbox)
            self.lights.append(light_checkbox)
            light_checkbox.clicked.connect(self.light_checkbox_click)        
        
        # 更新所有checkbox上的文字
        for i in range(len(self.lights)):
            try:
                self.lights[i].setText(light_names[i])
                self.lights[i].show()
            except:
                self.lights[i].hide()   # UI上多的checkbox, 隱藏起來
    
    def apply(self):
        self.camera_lights = {}
        for name_light in get_specific_fields_camera_data(['name', 'light']):
            self.camera_lights[name_light[0]] = name_light[1]
        
        self.feed_data(identification_data)
        
    def feed_data(self, data):
        jobs = list( x['name'] for x in data)
        self.job_list.addItems(jobs)
        self.file_list.addItems(IPI_files)
        self.file_list.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

    def job_list_clicked(self):        
        self.load_job_data(self.job_list.currentItem().text())        
    
    def load_job_data(self, job_name):
        job_data_list = list(x for x in identification_data if x['name'] == job_name)
        if len(job_data_list):
            job_data = job_data_list[0]
            
            self.camera_label.setText(job_data['camera'])
            
            self.set_lights(job_data['light'])                        
            self.file_list.setCurrentIndex( self.file_list.findText(job_data['IPI_file']))
            self.light_label.setText('')
            
    def open_file_dialog(self):
        cur_path = os.path.abspath(self.file_path_edit.text())
        if os.path.exists(cur_path):
            home = cur_path
        else:
            home = '/home'
        
        file_name = QFileDialog.getOpenFileName(self, 'Open File', home,'Images (*.png *.bmp *.jpg)')
        try:
            if isinstance(file_name[0], str) and file_name[0]:
                self.file_path_edit.setText(file_name[0])                
        except:
            pass
        
    def light_checkbox_click(self):
        text = list(light.text() for light in self.lights if light.isChecked())
        self.light_label.setText('{0}'.format(text))            

    def preview_file_checked(self):
        sender = self.sender()
        path = self.file_path_edit.text()
        try:
            if sender.isChecked():
                UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit([path, None, ''])
            else:
                UISignals.GetSignal(SigName.IMG_THUMBNAIL).emit([path, 'rollback', ''])
        except:
            pass

    def correction_click(self):
        self.setCorrectionMode(self.sender().isChecked())
        
    def setCorrectionMode(self, correction_mode):
        self.info_bar.setEnabled(not correction_mode)
        #self.file_list.setEnabled(not correction_mode)
        self.mgr_buttons.setVisible(not correction_mode)
        
        self.lights_box.setVisible(not correction_mode)
        
        self.parameter_box.setVisible(correction_mode)
        self.job_list.setEnabled(not correction_mode)
        
        
def main():    
    app = QApplication(sys.argv)
    
    ex = IdentificationSettings()
    
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()        