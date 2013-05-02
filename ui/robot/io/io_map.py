#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: Mar. 2013
"""

import sys
from PySide import QtCore
from PySide.QtGui import *

from masbot.config.utils import Path, SigName, UISignals
from masbot.ui.control.dio_button import *
from masbot.ui import preaction

class IOMap(QWidget):
    
    def __init__(self, card_num):
        super(IOMap, self).__init__()        
        self.init_ui()
        UISignals.GetSignal(SigName.DIO_STATUS).connect(self.dio_changed)
        
        
        dio_8154 = {'type':'8154', 'di':[0 for x in range(0, 60)], 'do':[0 for x in range(0, 50)]}
        dio_8158 = {'type':'8158', 'di':[0 for x in range(0, 40)], 'do':[0 for x in range(0, 60)]}
        dio_LPLink = {'type':'LPLink', 'di':[0 for x in range(0, 64)], 'do':[0 for x in range(0, 32)]}
        dio_LPMax = {'type':'LPMax', 'di':[0 for x in range(0, 32)], 'do':[0 for x in range(0, 48)]}

        self.dio_status(dio_8154)
        self.dio_status(dio_8158)
        self.dio_status(dio_LPLink)
        self.dio_status(dio_LPMax)
        
        
        
    def init_ui(self):        
        self.card = {}              # 包含: 'type':     (str),              'do_layout':(Grid layout), 
                                    #       'di_layout':(Grid layout),      'do_list':(list of DO Button), 
                                    #       'di_list':  (list of DI Button)
        self.v_layout = QVBoxLayout()
        self.v_layout.setAlignment(QtCore.Qt.AlignVCenter)

        self.setLayout(self.v_layout)
        self.setWindowTitle('IO Map')
        self.show()
        
    def dio_status(self, dio_status):
        card_type = dio_status['type']
        
        if card_type in self.card:
            do_grid = self.card[card_type]['do_grid']
            di_grid = self.card[card_type]['di_grid']
            do_list = self.card[card_type]['do_list']
            di_list = self.card[card_type]['di_list']
        else:            
            card = {}
            do_grid = card['do_grid'] = QGridLayout()
            di_grid = card['di_grid'] = QGridLayout()
            do_grid.setVerticalSpacing(1)       # row的間距
            do_grid.setHorizontalSpacing(1)     # column的間距
            di_grid.setVerticalSpacing(1)       # row的間距
            di_grid.setHorizontalSpacing(1)     # column的間距
            
            do_list = card['do_list'] = []
            di_list = card['di_list'] = []
            self.card[card_type] = card
            
            groupbox = QGroupBox(card_type)
            hbox = QHBoxLayout()
            hbox.addLayout(do_grid)
            hbox.addLayout(di_grid)
            hbox.setAlignment(do_grid, QtCore.Qt.AlignTop)
            hbox.setAlignment(di_grid, QtCore.Qt.AlignTop)
            hbox.setContentsMargins(2,5,2,2)
            groupbox.setLayout(hbox)
            
            self.v_layout.addWidget(groupbox)
        
        do = dio_status['do']
        di = dio_status['di']
                
        col_len = 10 
        do_num = len(do)
        di_num = len(di)

        for i in range(0, max(do_num, di_num)):
            row = (int)(i/col_len)
            column = i % col_len
            
            #a = int(column/5)*5 + int(column/5) -1
            #if a == column: 
            if column > 0 and column % 5 == 0:                        
                di_grid.setColumnMinimumWidth(i % col_len, 5)
                do_grid.setColumnMinimumWidth(i % col_len, 5)
                
            if i < do_num:
                if i< len(do_list):
                    do_list[i].on_off(do[i])
                else:
                    do_btn = DIOButton(i, True)
                    do_btn.clicked.connect(self.do_clicked)
                    do_grid.addWidget(do_btn, row + 1, column + int(column /5))
                    do_list.append(do_btn)
            
            if i <di_num:
                if i < len(di_list):
                    di_list[i].on_off(di[i])
                else:
                    di_label = DIOButton(i, False)
                    di_grid.addWidget(di_label, row + 1, column + int(column /5))                
                    di_list.append(di_label)

    def do_clicked(self):
        sender = self.sender()
        UISignals.GetSignal(SigName.DO_OUT).emit(sender.io_num, sender.nOn)
            
    def dio_changed(self, dict_status):
        self.dio_status(dict_status)            

def main():
    
    app = QApplication(sys.argv)
    ex = IOMap(8)
    app.exec_()


if __name__ == '__main__':
    main()        