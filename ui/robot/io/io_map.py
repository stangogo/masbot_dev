#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: Mar. 2013
"""

import sys
from PySide import QtGui, QtCore

from masbot.config.utils import Path, SigName, UISignals
from masbot.ui.control.dio_button import *
from masbot.ui import preaction

class IOMap(QtGui.QWidget):
    
    def __init__(self, card_num):
        super(IOMap, self).__init__()
        
        self.init_ui(card_num)
        
        UISignals.GetSignal(SigName.DI_IN).connect(self.di_changed)
        UISignals.GetSignal(SigName.DO_IN).connect(self.do_changed)
        
        
    def init_ui(self, card_num):
        do_grid = QtGui.QGridLayout()
        do_grid.setVerticalSpacing(0)   # row的間距
        do_grid.setHorizontalSpacing(0)  # column的間距
        
        di_grid = QtGui.QGridLayout()
        di_grid.setVerticalSpacing(0)   # row的間距
        di_grid.setHorizontalSpacing(0)  # column的間距                 
                
        col_len = 20    
        #card_num = 10        
        #io_num = col_len*card_num
        io_num = 32 * card_num

        self.do_list = []
        self.di_list = []
        
        for i in range(0, io_num):
            row = (int)(i/col_len)
            column = i % col_len
            
            a = int(column/5)*5 + int(column/5) -1
            
            if a == column:
                di_grid.setColumnMinimumWidth(i % col_len, 8)
                do_grid.setColumnMinimumWidth(i % col_len, 8)
            
            do_btn = DIOButton(i, True)
            do_btn.clicked.connect(self.do_clicked)
            self.do_list.append(do_btn)
            self.di_list.append(DIOButton(i, False))
            do_grid.addWidget(self.do_list[i], row + 1, column + int(column /5))
            di_grid.addWidget(self.di_list[i], row + 1, column + int(column /5))

        do_title = DIOLabel('DO', True)
        do_title.on_off(True)
        do_title.setToolTip('顯示目前DO狀況, 按DO可手動控制作動')
        do_title.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        do_title.setFixedWidth(30)
        do_title.setFixedHeight(30)
       
        do_underscore = QtGui.QLabel()
        do_underscore.setObjectName("DO_underscope");
                
        do_underscore.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        do_underscore.setFixedWidth(550)
        do_underscore.setFixedHeight(1)

        di_title = DIOLabel('DI', False)        
        di_title.setToolTip('顯示目前DI狀況')
        di_title.on_off(True)
        #di_title.setStyleSheet('QLabel{ font-size: 12pt;  font-family:Segoe UI; background-color: rgb(232, 113, 6)}')
        #di_title.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        di_title.setFixedWidth(30)
        di_title.setFixedHeight(30)
        
        di_underscore = QtGui.QLabel()
        di_underscore.setObjectName("DI_underscope");        
        di_underscore.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        di_underscore.setFixedWidth(550)
        di_underscore.setFixedHeight(1)
        
        self.v_layout = QtGui.QVBoxLayout()
        
        self.v_layout.addWidget(do_title, 0)
        self.v_layout.addWidget(do_underscore, 0)
        
        self.v_layout.addLayout(do_grid, 10)
        
        self.v_layout.addWidget(di_title, 0)
        self.v_layout.addWidget(di_underscore, 0)
        
        self.v_layout.addLayout(di_grid, 10)
        self.v_layout.setAlignment(QtCore.Qt.AlignVCenter)
        #self.v_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.setLayout(self.v_layout)
                
        self.setWindowTitle('IO Map')
        self.show()
    def do_clicked(self):
        sender = self.sender()
        UISignals.GetSignal(SigName.DO_OUT).emit(sender.io_num, sender.nOn)
            
    def do_di_changed(self, new_status, old_list, On):
        if new_status == None:
            return
        
        if len(new_status) > 1:
            for i in range(0, len(new_status)):
                old_list[i].on_off(new_status[i])
        elif len(new_status) == 1:
            if new_status[0] >= len(old_list):
                print("out of range: max - {0}".format(len(old_list)))
            else :
                old_list[new_status[0]].on_off(On)
            
    def do_changed(self, do_new, On):
        """
        do_new: list for setting DO status. if the length = 1, it means the index of DO, and "on" is status 
        if the lenght > 1, each element means the status and index of list is the nubmer of DO
        """
        self.do_di_changed(do_new, self.do_list, On)
    
    def di_changed(self, di_new, On):
        self.do_di_changed(di_new, self.di_list, On)
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = IOMap(8)
    app.exec_()


if __name__ == '__main__':
    main()        