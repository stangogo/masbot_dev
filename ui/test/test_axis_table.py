#!/usr/bin/python
# -*- coding: utf-8 -*-


from PySide import QtCore, QtGui
import unittest
from masbot.config.utils import SigName, UISignals, Path
from masbot.ui.robot.axis_table import AxisTable
from masbot.ui.robot.major.major_widget import MajorWidget

 
class AxisBanner(QtGui.QWidget):

    def __init__(self):
        super(AxisBanner, self).__init__()
        
        self.init_ui()
        
    def init_ui(self):
        
        style = "QLabel { color:green; font-family: sans-serif; font-size: 18px;}"
        title_label = QtGui.QLabel('單\n軸\n移\n動')
        title_label.setStyleSheet(style)
        
    
    
        self.axis_banner = QtGui.QHBoxLayout(self)    
        self.axis_banner.addWidget(title_label, 1, QtCore.Qt.AlignLeft)
        self.axis_banner.addWidget(AxisTable(),40)
        
        btn = UISignals.GetSignal(SigName.FROM_AXIS_TABLE)
        btn.connect(self.start_btn)            

        self.setLayout(self.axis_banner )
                
        self.setWindowTitle('Axis Banner')
        self.show()
    
    def start_btn(self, axis, value):
        
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE)
        slot.emit('position', axis, value)

class CalculatorTest(unittest.TestCase):                 

    def start_btn(self, axis, value):
        
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE)
        slot.emit('position', axis, value)
        
    def test_star_btn(self):
        btn = UISignals.GetSignal(SigName.FROM_AXIS_TABLE)
        btn.connect(self.start_btn)
        btn.emit('axis_y', '10')
        btn.emit('axis_y', '10', -1)
        
def main():    
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = AxisBanner()
    ex.show()
    #unittest.main()
    app.exec_()

if __name__ == '__main__':
    main()        
                