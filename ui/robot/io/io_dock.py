
from PySide import QtGui, QtCore

from masbot.ui.robot.io.motor import Motor
from masbot.ui.robot.io.nozzle import Nozzle

class IODock(QtGui.QMainWindow):
    def __init__(self):  
        QtGui.QMainWindow.__init__(self)
        self.pages = {}
        self.createDockWindows()
        
        
    def createDockWindows(self):
        self.pages['taker'] = Nozzle('吸嘴', self)
        self.pages['motor'] = Motor('馬達', self)
        self.pages['point'] = QtGui.QDockWidget('點位', self)
        self.pages['stock'] = QtGui.QDockWidget('Stock', self)
        self.pages['lock'] = QtGui.QDockWidget('Lock', self)
        self.pages['alarm'] = QtGui.QDockWidget('警示燈', self)

        self.setDockOptions(self.AnimatedDocks | self.ForceTabbedDocks)
        
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtGui.QTabWidget.North)
        for page in self.pages.values():
            page.setTitleBarWidget(QtGui.QWidget())
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, page)
            
        self.tabifyDockWidget(self.pages['taker'], self.pages['motor'])
        self.tabifyDockWidget(self.pages['motor'], self.pages['point'])
        self.tabifyDockWidget(self.pages['point'], self.pages['stock'])
        self.tabifyDockWidget(self.pages['stock'], self.pages['alarm'])
        self.tabifyDockWidget(self.pages['alarm'], self.pages['lock'])        

        self.pages['taker'].raise_()
        self.setWindowTitle('IO dock')

if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = IODock()
    window.show()  
    sys.exit(app.exec_())  