#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: Mar. 2013
"""

import sys
from PySide import QtGui, QtCore

from masbot.ui.utils import Path, SigName, UISignals

class Signals(QtCore.QObject):
    to_do = QtCore.Signal(list, bool)
    to_di = QtCore.Signal(list, bool)
    from_do = QtCore.Signal(int, bool)    

class DIOButton(QtGui.QPushButton):
    bOn = True
    io_num = -1
    
    def __init__(self, io_num, do):
        super(DIOButton, self).__init__()
        if do:  # di 不能按
            self.clicked.connect(self.on_clicked)
            self.setCheckable(True)
       
        self.io_num = io_num      
        self.set_style(do)
        self.on_off(False)
        self.setText("%d" % io_num)
        
        #button size  24x24
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)                
        self.setFixedWidth(24)
        self.setFixedHeight(24)
        
        self.setAutoFillBackground(True)
        
        #self.setToolTip('This is a <b>QPushButton</b> widget')
        #self.on_img = "{0}/Start.bmp".format(imgs_dir)
        #self.off_img = "{0}/Stop.bmp".format(imgs_dir)
        
    def on_clicked(self):        
        self.on_off(not self.bOn)
    
    def on_off(self, on):
        if self.bOn == on:
            return
        
        self.bOn = on
        if on:                  #ligh on 
            self.setStyleSheet(self.on_style)
            if not self.isChecked():
                self.setChecked(True)
        else: 
            self.setStyleSheet(self.off_style)
            if self.isChecked():
                self.setChecked(False)
            
    def set_style(self, do):
        """
        設定DO 或 DI 的背景和文字style.
        """
        if do :
            self.on_style = 'QPushButton { background-color: rgb(31, 232, 3); \
                                              border-radius: 12px; \
                                              font-weight:bold }'
            
            self.off_style = 'QPushButton { background-color: rgb(168, 168, 168); \
                                              border-radius: 12px;}'
        else :
            self.on_style = 'QPushButton { background-color: rgb(232, 113, 6); \
                                                          border-radius: 12px; \
                                                          font-weight:bold }'  
            
            self.off_style = 'QPushButton { background-color: rgb(168, 168, 168); \
                                              border-radius: 12px;}'
            
            #self.setStyleSheet("background-color: rgb(255, 255, 0); color: rgb(255, 255, 255)")
            #self.setStyleSheet("background-color: rgb(150, 201, 100)")
            #self.setIcon(QtGui.QIcon(self.off_img))               

#class DIOLabel(QtGui.QLabel):
    #bOn = False
    #io_num = -1    
    #clicked = QtCore.Signal(str) # can be other types (list, dict, object...)
    
    #def __init__(self, io_num):
        #super(DIOLabel, self).__init__()
        #imgs_dir = Path.imgs_dir()
        #self.on_img = "{0}/Start.bmp".format(imgs_dir)
        #self.off_img = "{0}/Stop.bmp".format(imgs_dir)
        
        #self.setAlignment(QtCore.Qt.AlignLeft)
        #self.setText("%d" % io_num)
        #self.on_off(self.bOn)
        
        ##self.setToolTip('This is a <b>QPushButton</b> widget')
        ##self.resize(self.sizeHint())
        #self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        #self.setAutoFillBackground(True)
        
    #def on_clicked(self):
        #self.bOn = not self.bOn
        #self.on_off(self.bOn)
    
    #def on_off(self, on):
        #if on:
            #self.setPixmap(self.on_img)
        #else: 
            #self.setPixmap(self.off_img)

    #def mousePressEvent(self, event):    
        #self.clicked.emit("emit the signal")
        #self.on_clicked()



class IOMap(QtGui.QWidget):
    
    def __init__(self, card_num):
        super(IOMap, self).__init__()
        
        self.init_ui(card_num)
        self.signals = Signals()
        UISignals.RegisterSignal(self.signals.to_di, SigName.ENTER_IO_MAP_DI)
        UISignals.RegisterSignal(self.signals.to_do, SigName.ENTER_IO_MAP_DO)
        UISignals.RegisterSignal(self.signals.from_do, SigName.FROM_IO_MAP)
        
        self.signals.to_di.connect(self.di_changed)
        self.signals.to_do.connect(self.do_changed)
        
        
    def init_ui(self, card_num):
        do_grid = QtGui.QGridLayout()        
        do_grid.setVerticalSpacing(5)   # row的間距
        do_grid.setHorizontalSpacing(2)  # column的間距
        
        di_grid = QtGui.QGridLayout()
        di_grid.setVerticalSpacing(5)   # row的間距
        di_grid.setHorizontalSpacing(2)  # column的間距                 
                
        col_len = 20    
        #card_num = 10        
        #io_num = col_len*card_num
        io_num = 32*card_num

        self.do_list = []
        self.di_list = []
        
        for i in range(0, io_num):
            row = (int)(i/col_len)
            column = i % col_len
            
            a = int(column/5)*5 + int(column/5) -1
            
            if a == column:
                di_grid.setColumnMinimumWidth(i % col_len, 10)
                do_grid.setColumnMinimumWidth(i % col_len, 10)                                
            
            do_btn = DIOButton(i, True)
            do_btn.clicked.connect(self.do_clicked)
            self.do_list.append(do_btn)
            self.di_list.append(DIOButton(i, False))
            do_grid.addWidget(self.do_list[i], row + 1, column + int(column /5))
            di_grid.addWidget(self.di_list[i], row + 1, column + int(column /5))

        do_title = QtGui.QLabel('DO')
        do_title.setToolTip('顯示目前DO狀況, 按DO可手動控制作動')
        do_title.setMargin(2)
        do_title.setStyleSheet('QLabel{ font-size:12pt; font-family:Segoe UI; background-color: rgb(31, 232, 3)}')
        do_title.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        do_title.setFixedWidth(28)
        #do_title.setFixedHeight(16)
       
        do_underscore = QtGui.QLabel()
        do_underscore.setStyleSheet('QFrame { background-color: rgb(31, 232, 3);}')
        do_underscore.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        do_underscore.setFixedWidth(550)
        do_underscore.setFixedHeight(1)

        di_title = QtGui.QLabel(' DI')
        di_title.setToolTip('顯示目前DI狀況')
        di_title.setStyleSheet('QLabel{ font-size: 12pt;  font-family:Segoe UI; background-color: rgb(232, 113, 6)}')
        di_title.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        di_title.setFixedWidth(23)
        #di_title.setFixedHeight(12)
        
        di_underscore = QtGui.QLabel()
        di_underscore.setStyleSheet('QFrame { background-color: rgb(232, 113, 6);}') 
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
        self.signals.from_do.emit(sender.io_num, sender.bOn)
            
    def do_di_changed(self, new_status, old_list, bOn):
        if len(new_status) > 1:
            for i in range(0, len(new_status)):
                if new_status[i] == 0:
                    old_list[i].on_off(False)
                else:
                    old_list[i].on_off(True)
        elif len(index) == 1:
            if new_status[0] >= len(self.old_list):
                print("out of range: max - {0}".format(len(self.old_list)))
            else :
                self.old_list[new_status[0]].on_off(bOn)
            
    def do_changed(self, do_new, bOn):
        """
        do_new: list for setting DO status. if the length = 1, it means the index of DO, and "on" is status 
        if the lenght > 1, each element means the status and index of list is the nubmer of DO
        """
        self.do_di_changed(do_new, self.do_list, bOn)
    
    def di_changed(self, di_new, bOn):
        self.do_di_changed(di_new, self.di_list, bOn)
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = IOMap(8)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        