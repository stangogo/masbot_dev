
import logging

from PySide import QtGui, QtCore

from masbot.ui.utils import Path

from masbot.ui.robot.io.motor import Motor
from masbot.ui.robot.io.nozzle_table import Nozzle
from masbot.ui.robot.io.point_table import Point

class IOTab(QtGui.QTabWidget):
    def __init__(self):  
        QtGui.QTabWidget.__init__(self)
        # self.pages = {}
        self.init_tabs()
        self.logger = logging.getLogger('ui.log')
        
    def init_tabs(self):
        push_ico = QtGui.QIcon("{0}/zoom-in.png".format(Path.imgs_dir()))
        
        self.addTab(Nozzle('吸嘴', self),  push_ico, '吸嘴')        
        self.addTab(Motor('馬達', self), '馬達')
        self.addTab(Point(), '點位')
        self.addTab(QtGui.QWidget(), 'Stock')
        self.addTab(QtGui.QWidget(), 'Lock')
        self.addTab(QtGui.QWidget(), '警示燈')

        #self.setStyleSheet('QTabBar::tab { width: 30px}')   # 橫向 (West or East) 要設 width
        #self.setTabPosition(QtGui.QTabWidget.West)
        
        #self.setStyleSheet('QTabBar::tab { height: 30px; width: 100px; max-width: 250px}') # 縱向 (North or South) 要設 height        
        self.tab_tool_tip()
        #self.setTabPosition(QtGui.QTabWidget.North)
        self.setWindowTitle('IO Tab')


    def tab_tool_tip(self):
        self.setTabToolTip(0, '吸嘴')
        self.setTabToolTip(1, '馬達')
        self.setTabToolTip(2, '點位')
        self.setTabToolTip(3, 'Stock')
        self.setTabToolTip(4, 'Lock')
        self.setTabToolTip(5, '警示燈')
        
    def save(self):
        try:
            self.currentWidget().save()
        except:
            self.logger.debug('{0} no save function'.format(type(self.currentWidget())))

    def reload(self):
        try:
            self.currentWidget().reload()
        except:
            self.logger.debug('{0} no save function'.format(type(self.currentWidget())))
    
    def apply(self):
        try:
            self.currentWidget().aplly()
        except:
            self.logger.debug('{0} no save function'.format(type(self.currentWidget())))

if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = IOTab()
    window.show()  
    sys.exit(app.exec_())  