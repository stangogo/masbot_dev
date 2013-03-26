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
from datetime import datetime

from PySide import QtGui
from PySide import QtCore
from masbot.ui.image_widget import ImageWidget
from masbot.ui.robot_widget import RobotWidget
from masbot.ui.robot.io.io_map import IOMap

from masbot.ui.utils import Path, Constants, UISignals, SigName
from masbot.controller.major_widget_ctrl import MajorWidgetCtrl

class MainUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainUI, self).__init__()
        
        self.init_ui()
        self._init_controller()
   
    def init_ui(self):
        
        width = 1420
        height = 880
        
        right_widget = QtGui.QWidget()        
        self.right_layout = QtGui.QStackedLayout()
        self.right_layout.addWidget(ImageWidget())
        self.right_layout.addWidget(IOMap(8))
        right_widget.setLayout(self.right_layout)
        
        main_widget = RobotWidget()
        
        btn = UISignals.GetSignal(SigName.DI_DO_SHOW)
        btn.connect(self.right_stack_changed)
                        
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        main_splitter.addWidget(main_widget)
        main_splitter.addWidget(right_widget) 
        
        #main_splitter.setSizes([width*4/7, width*3/7])
        main_splitter.setSizes([width/2, width/2])
        
        self.setCentralWidget(main_splitter)
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.init_caption())
        imgs_dir = Path.imgs_dir()
        self.setWindowIcon(QtGui.QIcon("{0}//App.ico".format(imgs_dir)))
        self.show()

    def _init_controller(self):
        self._major_widget_instance = MajorWidgetCtrl()
        
    def right_stack_changed(self):
        self.right_layout.setCurrentIndex( (self.right_layout.currentIndex() + 1) %2)
        #start update 
        
        
    def init_caption(self):
        now_time = datetime.now()
        
        caption = "Masbot - {0} Ver.{1}: {2}".format(Constants.MACHINE_NAME, 
                                                    Constants.VERSION,
                                                    now_time.strftime("%Y/%m/%d %H:%M:%S"))
        return caption
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    #with open("stylesheet.css", 'r') as cssFile:
        #styleSheet =cssFile.read()

    #app.setStyleSheet(styleSheet)
        
    Settings = { "tabcolor":"#17B6FF", "fontsize":"10px" }
    
    stylesheet = """
    QToolBar{
        icon-size:16px;
        max-height:20px;
        min-height:20px;
        padding:1px;
    }
    
    QToolBar QToolButton{
        max-width:24px;
    }
    
    QToolBar::handle{
        width:0px;
    }
    
    QToolBar QComboBox{
        font-size:%(fontsize)s;
        height:12px;
    }
    
    QTabBar{
        text-align: left;
        font-size:12px;
        icon-size:0px;
    }
    
    QTabBar::tab {
        padding: 2px;
        font-size:12px;
        border-top-left-radius: 1px;
        border-top-right-radius: 1px;
        border: 1px solid #C4C4C3;
        margin:1px;
        spacing:0px;
        text-align: left;
        max-height:150px;
    }
    
    QTabBar::tab:top{
        padding-left:3px;
        padding-right:3px;
    }
    
    QTabBar::tab:selected {
         background: %(tabcolor)s;
         padding:1px;
    }
    
    QMenuBar{
        font-size:%(fontsize)s;
    }
    
    QStatusBar QLabel{
        font-size:%(fontsize)s;
    }
    
    QSplitter::handle {
        width:2px;
    }
    
    QTreeView{
        font-size:%(fontsize)s;
    }
    
    QToolTip{
        color:black;
    }
    
    QScrollBar:vertical {
         width: 6px;
         padding:0px;
         border:0px;
         background-color:gray;
     }
    
    QScrollBar::handle:vertical {
         background: %(tabcolor)s;
         min-height:30px;
    }
    
    QScrollBar:horizontal {
         height: 6px;
         padding:0px;
         border:0px;
         background-color:gray;
    }
    
    QScrollBar::handle:horizontal {
         background: %(tabcolor)s;
         min-width:30px;
    }
    
    .bbb { 
    background-color : red; 
    color: rgba(0, 255, 0, 90); 
    font-size:30pt ;
    }
    
    .title_lable { 
    background-color : lightblue; 
    color: rgb(0, 0, 0); 
    font-size:30pt ;
    font-family: ms pmincho;
    }    
    
    """ % Settings    
    
    
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    
    #app.setStyleSheet(stylesheet)

    ex = MainUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


        
        
