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
from time import sleep
import tkinter
from datetime import datetime

from PySide import QtGui
from PySide import QtCore
from masbot.ui.image_widget import ImageWidget
from masbot.ui.robot_widget import RobotWidget
from masbot.ui.robot.io.io_map import IOMap
from masbot.ui.control.ui_utils import *

from masbot.config.utils import Path, Constants, UISignals, SigName
from masbot.controller.major_widget_ctrl import MajorWidgetCtrl


# event filter install test: 不覆寫Widget時, 可用 installEventFilter 方式接收event
class VisibleStatus(QtCore.QObject):
    visibleChanged = QtCore.Signal(bool)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            print('size change')
        else:
            return QtCore.QObject.eventFilter(self, obj, event)
        
        
class MainUI(QtGui.QMainWindow):
        
    def __init__(self):
        super(MainUI, self).__init__()
        
        self.init_ui()
        self._init_controller()
        
    def __del__(self):
        UISignals.GetSignal(SigName.MAIN_CLOSE).emit()
        
        
        
    def init_ui(self):
        
        tk = tkinter.Tk()
        
        width = tk.winfo_screenwidth() - 20
        height = tk.winfo_screenheight() - 30
        tk.destroy()
        
        self.dio_image_sbox = QtGui.QStackedLayout()
        self.dio_image_sbox.addWidget(ImageWidget())
        self.dio_image_sbox.addWidget(IOMap(8))
        self.dio_image_sbox.setContentsMargins(0,0,0,0)
        
        right_vbox = QtGui.QVBoxLayout()
        right_vbox.addWidget(self.init_dio_button())
        right_vbox.addLayout(self.dio_image_sbox)
        right_vbox.setAlignment(self.dio_btn, QtCore.Qt.AlignCenter)        
        right_vbox.setSpacing(0)
        right_vbox.setContentsMargins(0,5,0,0)        
        
        self.right_widget = QtGui.QWidget()
        self.right_widget.setLayout(right_vbox)
        
        main_widget = RobotWidget()
        
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        main_splitter.addWidget(main_widget)
        main_splitter.addWidget(self.right_widget) 
        
        main_splitter.setSizes([width*4/7, width*3/7])
        #main_splitter.setSizes([width/2, width/2])
        self.main_splitter = main_splitter

        UISignals.GetSignal(SigName.REMOVE_IMG_SIDE).connect(self.switch_dio_image)
        
        self.setCentralWidget(main_splitter)
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.init_caption())
        imgs_dir = Path.imgs_dir()
        self.setWindowIcon(QtGui.QIcon("{0}//App.ico".format(imgs_dir)))
        self.show()
        

    def _init_controller(self):
        try:
            self._major_widget_instance = MajorWidgetCtrl()
        except:
            pass
        
    def switch_dio_image(self):        
        if self.right_widget.isHidden():
            self.right_widget.show()
            self.main_splitter.setSizes([self.width(), self.right_width])
            new_width = self.width() + self.right_width
        else:
            self.right_widget.hide()
            self.right_width = self.main_splitter.sizes()[1]    # 右邊寬度存下來, 回復時可用
            new_width = self.main_splitter.sizes()[0]           # 寬度剩左邊
            self.main_splitter.addWidget

        tk = tkinter.Tk()
        width = tk.winfo_screenwidth() - 20
        tk.destroy()
        if new_width > width:
            new_width = width
            
        geometry = self.geometry()
        geometry.setWidth(new_width)
        self.setGeometry(geometry)

    def init_caption(self):
        now_time = datetime.now()
        caption = "Masbot - {0} Ver.{1} - start time: {2}".format(Constants.MACHINE_NAME, 
                                                    Constants.VERSION,
                                                    now_time.strftime("%Y/%m/%d %H:%M:%S"))
        return caption

    def init_dio_button(self):        
        dio_btn = QtGui.QPushButton(get_rotate_qicon("push.ico", 90),"")  #"DIO\n顯示")
        dio_btn.setFixedSize(300, 12)                
        dio_btn.setStyleSheet('QPushButton{border:0px; }')
        dio_btn.clicked.connect(self.switch_dio_map)
        dio_btn.setToolTip("切換DIO map 和 影像")
        dio_btn.setContentsMargins(0,0,0,0)
        #di_do_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        #UISignals.RegisterSignal(di_do_btn.clicked, SigName.DI_DO_SHOW)
        
        self.dio_btn = dio_btn
        return self.dio_btn
    
    def switch_dio_map(self):
        self.dio_image_sbox.setCurrentIndex( (self.dio_image_sbox.currentIndex() + 1) %2)
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    with open("stylesheet.css", 'r') as cssFile:
        styleSheet =cssFile.read()

    Settings = { "tabcolor":"#17B6FF", "fontsize":"10px" , "tablecolor":"lightblue" , 'fontfamily':'Microsoft JhengHei'}
    styleSheet = styleSheet % Settings 
    app.setStyleSheet(styleSheet)
 
    #app.setStyle(QtGui.QStyleFactory.create("plastique"))

    ex = MainUI()
    app.exec_()
    
if __name__ == '__main__':
    main()


        
        
