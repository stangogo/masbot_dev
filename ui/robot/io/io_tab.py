
from PySide import QtGui, QtCore

from masbot.ui.utils import Path

from masbot.ui.robot.io.motor import Motor
from masbot.ui.robot.io.nozzle import Nozzle
from masbot.ui.robot.io.point import Point

class IOTab(QtGui.QTabWidget):
    def __init__(self):  
        QtGui.QTabWidget.__init__(self)
        self.pages = {}
        self.createTabWindows()
        
    def createTabWindows(self):
        #push_ico = QtGui.QIcon("{0}/zoom-in.png".format(Path.imgs_dir()))
        
        #self.addTab(Nozzle('吸嘴', self),  push_ico, '')
        self.addTab(Nozzle('吸嘴', self),  '吸嘴')
        self.addTab(Motor('馬達', self), '馬達')
        self.addTab(Point(), '點位')
        self.addTab(QtGui.QWidget(), 'Stock')
        self.addTab(QtGui.QWidget(), 'Lock')
        self.addTab(QtGui.QWidget(), '警示燈')

        #self.setTabPosition(QtGui.QTabWidget.North)
        self.setWindowTitle('IO Tab')

    def save(self):
        try:
            self.currentWidget().save()
        except:
            print('{0} no save function'.format(type(self.currentWidget())))
        

if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = IOTab()
    window.show()  
    sys.exit(app.exec_())  