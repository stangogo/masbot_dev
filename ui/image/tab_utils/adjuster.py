#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial 

This example shows
how to use QtGui.QSplitter widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""
import sys
from PySide.QtGui import *
from PySide.QtCore import *
from masbot.config.utils import Path
from collections import OrderedDict

class AdjusterSlider(QWidget):
    
    menu_item = OrderedDict([ ('#FFFF00', '黃'), 
                              ('#00FF00', '綠'), 
                              ('#FF0000','紅'), 
                              ('#1E90FF','藍'),                               
                              ( 'turn_off','關')
                            ])
    
    def __init__(self, *args):
        super(AdjusterSlider, self).__init__()
        self.init_ui(*args)    

    def init_ui(self, *args):
        """args:
        min_value
        max_value
        btn_text
        combobox_values
        """
        (min_, max_, text_) = args

        slider = QSlider(Qt.Vertical)
        slider.setRange(min_, max_)
        slider.setMinimumHeight(150)
        slider.setValue(0)        
        
        self.btn = QPushButton(text_)
        
        self.menu = QMenu()
        self.menu.setStyleSheet('QMenu::item:selected {background-color:#17B6FF;} \
                                 QMenu{background-color:#F0F8FF;border: 1px solid black;}')
        
        for color in self.menu_item.keys():
            action = self.menu_add_action(color)            
            if color == 'turn_off':
                self.turnoff_action = action
        
        self.menu.triggered.connect(self.menutrigger)        
        self.btn.setMenu(self.menu)
        
        self.change_button_bk_color(self.btn, '#F0F8FF') 
        self.menu.removeAction(self.turnoff_action)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn)
        vbox.addWidget(slider)
        
        vbox.setAlignment(slider, Qt.AlignCenter)
        
        self.setMaximumWidth(80)
        self.setLayout(vbox)
        self.show()
        
    def menutrigger(self, action):
        color_index = list(x for x in self.menu_item.values()).index(action.text())
        color = list(y for y in self.menu_item.keys())[color_index]
        
        if color == 'turn_off':
            color = '#F0F8FF'            
            self.menu.removeAction(self.turnoff_action)
        else:
            self.menu.addAction(self.turnoff_action)
        self.change_button_bk_color(self.btn, color)
            
                
    def menu_add_action(self, color):
        if color == 'turn_off':
            pixmap = QPixmap('{0}/{1}.ico'.format(Path.imgs_dir(), color))
        else:
            pixmap = QPixmap(50, 50)
            pixmap.fill(color)
        
        action = QAction(QIcon(pixmap), self.menu_item[color], self.menu)
        self.menu.addAction(action)
        return action
        
    def change_button_bk_color(self, button, color):
        stylesheet = 'QPushButton{background-color: %s;}' % color       
        button.setStyleSheet(stylesheet ) 

class Adjuster(QWidget):

    def __init__(self):
        super(Adjuster, self).__init__()
        self.init_ui()
        
    def init_ui(self):
        vbox = QVBoxLayout()
        
           
        vbox.addWidget(AdjusterSlider( 0, 100, 'X位移2'))

 #       self.sone.valueChanged.connect(self.sliderChanged)

        self.setLayout(vbox)
        self.setWindowTitle('Adjuster')
        self.show()
        
    def sliderChanged(self, val):
        self.stwo.setValue(self.stwo.maximum() - val)
        
def main():
    
    app = QApplication(sys.argv)
    ex = Adjuster()
    app.exec_()


if __name__ == '__main__':
    main()        