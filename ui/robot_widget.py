#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
from masbot.ui.robot.robot_tab import RobotPageDock
from masbot.ui.robot.robot_banner import RobotBanner
from masbot.config.utils import UISignals, SigName, Path


class RobotWidget(QtGui.QWidget):
    
    def __init__(self):
        super(RobotWidget, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):

        robot_tab = RobotPageDock()
        robot_tab.currentChanged.connect(self.page_changed)

        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(5,0,0,0)
        vbox.addWidget(RobotBanner(), 1)        
        vbox.addWidget(robot_tab, 3)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.init_shrink_button())
        hbox.setSpacing(0)

        self.setLayout(hbox)
        
        self.setWindowTitle('Robot')
        self.show()

    def init_shrink_button(self):
        shrink_button = QtGui.QPushButton(QtGui.QIcon("{0}/push.ico".format(Path.imgs_dir())), '')
        shrink_button.setCheckable(True)
        shrink_button.setChecked(True)
        shrink_button.setFixedWidth(10)
        shrink_button.setFixedHeight(400)        
        shrink_button.setStyleSheet('QPushButton{ border:0px;}')
        UISignals.RegisterSignal(shrink_button.clicked, SigName.REMOVE_IMG_SIDE)
        
        shrink_button.setToolTip('顯示/隱藏右側 (Show/Hide right side)')
        return shrink_button

    def page_changed(self, index):    # 改變stacklayout 的顯示頁面
        pass
        #if index:
            #self.stack_layout.setCurrentIndex(1)    # 單軸移動
        #else: 
            #self.stack_layout.setCurrentIndex(0)    # 機台資訊
    
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = RobotWidget()
    app.exec_()


if __name__ == '__main__':
    main()        