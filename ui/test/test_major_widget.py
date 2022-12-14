#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
import logging
import logging.config
import codecs

from PySide import QtCore, QtGui
import unittest
from masbot.config.utils import SigName, UISignals
from masbot.ui.robot.major.major_widget import MajorWidget


    
class RobotPageDock(QtGui.QMainWindow):
    """
    要移到masbot資料夾底下執行, 才會work
    """
    
    index_changed = QtCore.Signal(bool)
    
    def __init__(self):  
        QtGui.QMainWindow.__init__(self)
        self.pages = {}
        self.createDockWindows()
        
    def createDockWindows(self):
        main_title_widget = QtGui.QWidget()
        
        self.pages['main_page'] = MajorWidget('主頁', self)
        #self.pages['main_page'].setTitleBarWidget(main_title_widget)

        self.setDockOptions(self.AnimatedDocks | self.ForceTabbedDocks)

        # sets the tab position at the top of tabbed dockwidgets
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtGui.QTabWidget.West)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.pages['main_page'])  
        
        # UISignals.GetSignal(SigName.START_MAIN).connect(self.btn_click)
        
    def btn_click(self):
        UISignals.GetSignal(SigName.ALARM_MSG).emit("test alarm msg")
        UISignals.GetSignal(SigName.FLOW_MSG).emit("test flow message")
        
class CalculatorTest(unittest.TestCase):                 

    def test_alarm_msg(self):
        UISignals.GetSignal(SigName.ALARM_MSG).emit("alarm msg")
    
    def test_flow_msg(self):
        UISignals.GetSignal(SigName.FLOW_MSG).emit("flow message")
        
    def test_prod_info(self):
        UISignals.GetSignal(SigName.PRODUCT_INFO).emit(
                                { 'CT': 4.25, 
                                'ProdName': '9552A1', 
                                'MatchAngle':3.11, 
                                'AssembleMode': 'manually', 
                                'ProdBarCode': 'A222dsd323', 
                                'ProdNum': '11op98733', 
                                'Total': 200})
    
    def start_btn(self):
        print('start button is clicked')
        
    def pause_btn(self):
        print('pause button is clicked')

    def servo_on_btn(self):
        print('servo on button is clicked')
        
    def login_btn(self):
        print('login_btn button is clicked')
        
    #def test_star_btn(self):
        # btn = UISignals.GetSignal(SigName.START_MAIN)
        #btn.connect(self.start_btn)    
        #btn.emit()
        
    def test_pause_btn(self):
        btn = UISignals.GetSignal(SigName.PAUSE_MAIN)
        btn.connect(self.pause_btn)    
        btn.emit()
        
    def test_servo_on_btn(self):
        btn = UISignals.GetSignal(SigName.SERVO_ON)
        btn.connect(self.servo_on_btn)    
        btn.emit()
        
    def test_login_on_btn(self):
        btn = UISignals.GetSignal(SigName.LOG_IN)
        btn.connect(self.login_btn)
        btn.emit()        
    
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = RobotPageDock()    
    window.show()      
    #unittest.main()
    
    app.exec_()
    