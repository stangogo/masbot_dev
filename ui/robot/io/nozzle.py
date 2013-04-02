#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time 

from PySide import QtGui, QtCore
from datetime import datetime

from masbot.ui.robot.io.nozzle_table import NozzleTable


class Nozzle(QtGui.QWidget):
    """    
    Nozzle is a QDockWidget embeded nozzle_table and docked on io_dock
    
    """
    def __init__(self, title = 'Nozzle', parent = None):
        super(Nozzle, self).__init__(parent)        
        
        self.init_ui(title)
    
    def init_ui(self, title):
        v_layout = QtGui.QVBoxLayout()        
        self.nozzle_table = NozzleTable('Nozzle', 'nozzle_ui', True)        
        v_layout.addWidget(self.nozzle_table)
        
        
        
        self.setLayout(v_layout)
        self.setWindowTitle(title)
        self.show()
        
    @QtCore.Slot(str)
    def combobox_text_changed(self, text):
        print(self.combobox.currentText())
        
        
    def save(self):
            print('Nozzle save')

def main():
    
    app = QtGui.QApplication(sys.argv)

    ex = Nozzle()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()          