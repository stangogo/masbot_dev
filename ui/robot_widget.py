#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
from masbot.ui.robot.robot_dock import RobotPageDock
from masbot.ui.robot.robot_banner import RobotBanner
from masbot.ui.robot.axis_banner import AxisBanner

class RobotWidget(QtGui.QWidget):
    
    def __init__(self):
        super(RobotWidget, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):

        v_layout = QtGui.QVBoxLayout()

        robot_dock = RobotPageDock()
        robot_dock.index_changed.connect(self.page_changed)
        self.stack_layout = QtGui.QStackedLayout()
        self.stack_layout.addWidget(RobotBanner())
        
        self.stack_layout.addWidget(AxisBanner())

        v_layout.addLayout(self.stack_layout, 1)
        v_layout.addWidget(robot_dock, 5)

        self.setLayout(v_layout)
        self.setWindowTitle('Robot')
        self.show()
    
    def page_changed(self, visible):    # 改變stacklayout 的顯示頁面
        if visible:
            self.stack_layout.setCurrentIndex(0)
        else: 
            self.stack_layout.setCurrentIndex(1)
            
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = RobotWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        