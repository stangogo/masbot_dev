#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtGui, QtCore
from datetime import datetime

from masttif_ui.robot.io.nozzle_tablewidget import NozzleTable


class Nozzle(QtGui.QDockWidget):
    """    
    Nozzle is including two columns.
    
    """
    def __init__(self, title = 'Nozzle', parent = None):
        super(Nozzle, self).__init__(parent)        
        
        self.init_ui(title)
    
    def init_ui(self, title):
        widget_base = QtGui.QWidget()  
                
        v_layout = QtGui.QVBoxLayout()        
        
        self.nozzle_table = NozzleTable('Nozzle', 'nozzle_ui')        
        v_layout.addWidget(self.nozzle_table)
        
        widget_base.setLayout(v_layout)
        
        self.setWidget(widget_base)       
        self.setWindowTitle(title)
        self.show()
        
    @QtCore.Slot(str)
    def combobox_text_changed(self, text):
        print(self.combobox.currentText())
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = Nozzle()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()          