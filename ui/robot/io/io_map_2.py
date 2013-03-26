#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
website: zetcode.com 
last edited: Mar. 2013
"""

import sys
from PySide import QtGui, QtCore

from masbot.ui.utils import Path, UISignals



class MyLabel(QtGui.QLabel):
    def __init__(self):
        super(MyLabel, self).__init__()
        UISignals.GetSignal('btn').connect(self.clicked)
        
    def clicked(self):
        print('MyLabel clicked')



class IOMap(QtGui.QWidget):
    
    def __init__(self):
        super(IOMap, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):        
  
        self.v_layout = QtGui.QVBoxLayout()
        
        btn = QtGui.QPushButton('a')
        self.v_layout.addWidget(btn)
        
        UISignals.RegisterSignal(btn.clicked, 'btn')
        lable = MyLabel()
        
        self.setLayout(self.v_layout)
                
        self.setWindowTitle('IO Map')
        self.show()
        
    def do_changed(self, index):
        pass
    def di_changed(self, index):        
        self.di_stacklayout.setCurrentIndex(index)
            
            
            
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = IOMap()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()        