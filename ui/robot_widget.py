#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
from masbot.ui.robot.robot_tab import RobotPageDock
from masbot.ui.robot.robot_banner import RobotBanner
from masbot.ui.robot.axis_banner import AxisBanner

class RobotWidget(QtGui.QWidget):
    
    def __init__(self):
        super(RobotWidget, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):

        v_layout = QtGui.QVBoxLayout()
        v_layout

        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0,0,0,0)

        robot_tab = RobotPageDock()
        robot_tab.currentChanged.connect(self.page_changed)
        self.stack_layout = QtGui.QStackedLayout()
        self.stack_layout.addWidget(RobotBanner())
        
        self.stack_layout.addWidget(AxisBanner())

        #di_do_btn = QtGui.QPushButton("Test")
        #di_do_btn.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        
        v_layout.addLayout(self.stack_layout, 2)
        #v_layout.addWidget(di_do_btn, 1, QtCore.Qt.AlignRight)
        v_layout.addWidget(robot_tab, 9)

        self.setLayout(v_layout)
        
        self.setWindowTitle('Robot')
        self.show()
    
    def page_changed(self, index):    # 改變stacklayout 的顯示頁面
        if index:
            self.stack_layout.setCurrentIndex(1)
        else: 
            self.stack_layout.setCurrentIndex(0)
            
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = RobotWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        