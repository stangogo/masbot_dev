#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

author: Cigar Huang
last edited: August 2013
"""
import sys
from PySide.QtGui import *
from PySide.QtCore import *
from masbot.config.utils import Path
from collections import OrderedDict
from masbot.config.utils import UISignals, SigName


class Slider(QFrame):
    
    value_changed = Signal()
    
    def __init__(self, *args):
        super(Slider, self).__init__()    
        self.init_ui(*args)
        
    def init_ui(self, *args):
        if not len(args) == 2:  # 建構子傳入 min 和 max 參數, 預設為 0 ~ 100
            (min_, max_) = [0, 100] 
        else:
            (min_, max_) = args
            
        min_label = QLabel('{0}'.format(min_))
        max_label = QLabel('{0}'.format(max_))
        
        self.slider = QSlider(Qt.Vertical)
        self.slider.setRange(min_, max_)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.sliderChanged)
         
        self.cur_label = QLabel('{0}'.format(self.slider.value()))
        self.cur_label.setStyleSheet('QLabel{color : blue;}')# text-decoration: underline color blue}')
        self.cur_label.setContentsMargins(0,0,0,0)
        
        text_len = max(len(min_label.text()), len(max_label.text()))
        self.cur_label.setMinimumWidth(int(text_len * 6))     # 設定current value label的寬度, 以免數值變化時, layout 會變動
        
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.slider)          # 水平 Layout, 放置 slider 和 current value
        hbox.addWidget(self.cur_label)
        
        vbox = QVBoxLayout()            # 垂直 Layout, 放置 最大, 最小, 和 slider.
        vbox.addWidget(max_label)
        vbox.addLayout(hbox)
        vbox.addWidget(min_label)
                
        vbox.setAlignment(hbox, Qt.AlignLeft)       # 三個元件全部置中
        vbox.setAlignment(max_label, Qt.AlignCenter)
        vbox.setAlignment(min_label, Qt.AlignCenter)
        
        vbox.setContentsMargins(0,2,0,0)
        
        self.setLayout(vbox)
        self.setContentsMargins(0,0,0,0)
        
        self.setFrameShape(QFrame.StyledPanel)
        
    def sliderChanged(self, val):        
        self.cur_label.setText('{0}'.format(val))
        self.value_changed.emit()    

    def value(self):
        return self.slider.value()

class AdjusterSlider(QWidget):
    
    setting_changed = Signal()    
    
    def __init__(self, *args):
        super(AdjusterSlider, self).__init__()
        self.color_dict = OrderedDict([ ('yellow', ['#FFFF00', '黃']), 
                                        ('green', ['#00FF00', '綠']), 
                                        ('red', ['#FF0000','紅']), 
                                        ('blue', ['#1E90FF','藍']), 
                                        ('turn_off', ['#F0F8FF','關'])
                                    ])
        self.init_ui(*args)        
        
    def init_ui(self, *args):
        """args:
        min_
        max_
        min_angle
        max_angle
        text_
        colorful
        """
        # 可容納 4 或 6 個參數
        if len(args) == 4:
            (min_, max_, text_, colorful) = args
        elif len(args) == 6:
            (min_, max_, min_angle, max_angle, text_, colorful) = args

        self.btn = self.create_button(text_, colorful)

        if len(args) == 4:
            self.btn.setMaximumWidth(50)
            self.setFixedWidth(60)
        elif len(args) == 6:
            self.setFixedWidth(120)
            
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn)        
        
        slider_box = QHBoxLayout()        
        self.sliders = []
        
        slider = Slider(min_, max_)
        slider.value_changed.connect(self.value_changed)
        slider_box.addWidget(slider)    # 第一組 slider
        
        self.sliders.append(slider)
        
        if len(args) == 6:
            slider_angle = Slider(min_angle, max_angle)
            slider_angle.value_changed.connect(self.value_changed)
            slider_box.addWidget(slider_angle)  # 第二組 slider
            self.sliders.append(slider_angle)
            
        vbox.addLayout(slider_box)
        vbox.setAlignment(self.btn, Qt.AlignCenter)
        vbox.setAlignment(slider_box, Qt.AlignCenter)
        
        vbox.setContentsMargins(0,0,0,0)
        
        self.setLayout(vbox)
        self.setContentsMargins(0,0,0,5)
        
        self.show()
    def create_button(self, text_, colorful):
        btn = QPushButton(text_)
        
        if colorful:    # 有色彩需求, 加入button menu
            self.menu = QMenu()
            for color_key, value in self.color_dict.items():
                action = self.menu_add_action(color_key)
                if color_key == 'turn_off':
                    self.turnoff_action = action
            
            self.menu.triggered.connect(self.menutrigger)
            btn.setMenu(self.menu)
            self.menu.removeAction(self.turnoff_action)
        else:      
            btn.setFlat(True)
            
            #btn.setCheckable(True)
            btn.clicked.connect(self.value_changed)
        
        self.color_key = 'turn_off'
        self.change_button_bk_color(btn, 'turn_off') # turn_off 為原始顏色 key
        return btn
        
    def menutrigger(self, action):
        color_index = list(x[1] for x in self.color_dict.values()).index(action.text())
        color_key = list(y for y in self.color_dict.keys())[color_index]    # 由 顏色中文 value 找出 color_key 
        
        if color_key == 'turn_off': # "關"被clicked時, 移除 menu 上 turn_off 的action.
            self.menu.removeAction(self.turnoff_action)
        else:
            self.menu.addAction(self.turnoff_action)
        self.change_button_bk_color(self.btn, color_key)
                            
    def menu_add_action(self, color_key):
        # 產生action上所需icon
        if color_key == 'turn_off':
            pixmap = QPixmap('{0}/turn_off.ico'.format(Path.imgs_dir()))
        else:
            pixmap = QPixmap(50, 50)
            pixmap.fill(self.color_dict[color_key][0])
        
        action = QAction(QIcon(pixmap), self.color_dict[color_key][1], self.menu)
        self.menu.addAction(action)
        return action
        
    def change_button_bk_color(self, button, color_key):
        stylesheet = 'QPushButton{background-color: %s;} QPushButton:checked { background-color: #17B6FF;}' % self.color_dict[color_key][0]
        button.setStyleSheet(stylesheet)    # 先變更button 設定
        
        if not self.color_key == color_key:
            self.color_key = color_key  
            self.value_changed()    # 再發變化通知
            
        
    def value(self):
        return list( slider.value() for slider in self.sliders)

    def button_status(self):
        return self.color_key
    
    def value_changed(self):
        self.setting_changed.emit()
        

class AidedTool(QListWidget):
#class AidedTool(QWidget):

    def __init__(self):
        super(AidedTool, self).__init__()
        self.init_ui()
        
    def init_ui(self):
        hbox = QHBoxLayout()
        
        self.sliders = []
        self.sliders.append(AdjusterSlider( -1000, 1000, 'X位移', False))
        self.sliders.append(AdjusterSlider( -1000, 1000, 'Y位移', False))
        self.sliders.append(AdjusterSlider( 0, 1000, '圓形1', True))
        self.sliders.append(AdjusterSlider( 0, 1000, -180, 180, '正方形1', True))
        self.sliders.append(AdjusterSlider( 0, 1000, -180, 180, '十字1', True))
        
        self.sliders.append(AdjusterSlider( 0, 1000, '圓形2', True))
        self.sliders.append(AdjusterSlider( 0, 1000, -180, 180, '正方形2', True))
        self.sliders.append(AdjusterSlider( 0, 1000, -180, 180, '十字2', True))        
                
        for slider in self.sliders:
            slider.setting_changed.connect(self.btn_clicked)
            self.add_slider(slider)            
            
            #hbox.addWidget(slider)
        
        #self.setLayout(hbox)
        
        self.setMaximumWidth(700)
        self.setFlow(QListWidget.LeftToRight)
        self.setWindowTitle('AidedTool - 輔助工具')
        self.show()
        
    def add_slider(self, slider):
        item = QListWidgetItem()
        
        width = 14
        for frame in slider.sliders:
            width += frame.size().width()
    
        item.setSizeHint(QSize(width, slider.size().height()))
        
        self.addItem(item)
        self.setItemWidget(item, slider)
        
    def btn_clicked(self):
        slider_dict = {}
        for slider in self.sliders:
            data = []
            if slider.btn.isCheckable():
                data.append(slider.btn.btn.isFlat())
            else:
                data.append(slider.button_status())
            for value in slider.value():
                data.append(value)
            
            slider_dict[slider.btn.text()] = data
        try:    
            UISignals.GetSignal(SigName.AIDED_TOOL).emit(slider_dict)
        except:
            pass
        
def main():    
    app = QApplication(sys.argv)
    
    #with open("{0}/stylesheet.css".format(Path.mosbot_dir()), 'r') as cssFile:
        #styleSheet =cssFile.read()
 
    #Settings = { "tabcolor":"#17B6FF", "fontsize":"10px" , "tablecolor":"#17B6BB"}
    #styleSheet = styleSheet % Settings 
    #app.setStyleSheet(styleSheet)    
    
    ex = AidedTool()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()        