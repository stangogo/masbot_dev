#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang

website: 
last edited: Mar. 2013
"""

import sys
import os
import logging

import tkinter
from datetime import datetime

from PySide import QtGui
from PySide import QtCore
from masbot.ui.image_widget import ImageWidget
from masbot.ui.robot_widget import RobotWidget
from masbot.ui.robot.io.io_map import IOMap

from masbot.config.utils import Path, Constants, UISignals, SigName
from masbot.controller.major_widget_ctrl import MajorWidgetCtrl

class MainUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainUI, self).__init__()
        
        self.init_ui()
        self._init_controller()
   
    def init_ui(self):
        
        root = tkinter.Tk()
        
        width = root.winfo_screenwidth() - 20
        height = root.winfo_screenheight() - 20
        
        #width = 1420
        #height = 880
        
        self.right_widget = QtGui.QWidget()        
        self.right_layout = QtGui.QStackedLayout()
        self.right_layout.addWidget(ImageWidget())
        self.right_layout.addWidget(IOMap(8))
        self.right_widget.setLayout(self.right_layout)
        
        main_widget = RobotWidget()
        
        btn = UISignals.GetSignal(SigName.DI_DO_SHOW)
        btn.connect(self.right_stack_changed)
        
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        main_splitter.addWidget(main_widget)
        main_splitter.addWidget(self.right_widget) 
        
        #main_splitter.setSizes([width*4/7, width*3/7])
        main_splitter.setSizes([width/2, width/2])

        UISignals.GetSignal(SigName.REMOVE_IMG_SIDE).connect(self.remove_img_side)
        
        self.setCentralWidget(main_splitter)
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.init_caption())
        imgs_dir = Path.imgs_dir()
        self.setWindowIcon(QtGui.QIcon("{0}//App.ico".format(imgs_dir)))
        self.show()

    def _init_controller(self):
        self._major_widget_instance = MajorWidgetCtrl()
        
    def remove_img_side(self):
        if self.right_widget.isHidden():
            self.right_widget.show()
        else:
            self.right_widget.hide()
        
    def right_stack_changed(self):
        self.right_layout.setCurrentIndex( (self.right_layout.currentIndex() + 1) %2)
        #start update         
        
    def init_caption(self):
        now_time = datetime.now()
        
        caption = "Masbot - {0} Ver.{1} - start time: {2}".format(Constants.MACHINE_NAME, 
                                                    Constants.VERSION,
                                                    now_time.strftime("%Y/%m/%d %H:%M:%S"))
        return caption
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    with open("stylesheet.css", 'r') as cssFile:
        styleSheet =cssFile.read()

    Settings = { "tabcolor":"#17B6FF", "fontsize":"10px" , "tablecolor":"lightblue"}
    styleSheet = styleSheet % Settings 
    app.setStyleSheet(styleSheet)
 
    #app.setStyle(QtGui.QStyleFactory.create("plastique"))

    ex = MainUI()
    app.exec_()
    
if __name__ == '__main__':
    main()


        
        
