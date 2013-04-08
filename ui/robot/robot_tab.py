
from PySide import QtGui, QtCore
from masbot.ui.robot.major.major_widget import MajorWidget
from masbot.ui.robot.io.io_widget import IOWidget
from masbot.ui.utils import Path
    
class RobotPageDock(QtGui.QTabWidget):
    
    def __init__(self):  
        QtGui.QTabWidget.__init__(self)
        self.pages = {}
        self.init_tabs()
        
    def init_tabs(self):
        push_ico = QtGui.QIcon("{0}/zoom-in.png".format(Path.imgs_dir()))
        
        self.addTab(MajorWidget(),  push_ico, '主頁')
        self.addTab(QtGui.QWidget(), '測試模式')
        self.addTab(IOWidget(), 'I/O設定')
        self.addTab(QtGui.QWidget(), '系統設定')
        self.addTab(QtGui.QWidget(), '訊息')
        
     
        self.sizeHint()
        
        self.setStyleSheet('QTabBar::tab { min-width:30px ; min-height:30px ; font:12px ;}')   # 橫向 (West or East) 要設 width
        self.setTabPosition(QtGui.QTabWidget.West)
        
        #self.setStyleSheet('QTabBar::tab { height: 50px}') # 縱向 (North or South) 要設 height
        #self.setTabPosition(QtGui.QTabWidget.North)
        
        self.tab_tool_tip()
     
    def tab_tool_tip(self):
        self.setTabToolTip(0, '主頁')
        self.setTabToolTip(1, '測試模式')
        self.setTabToolTip(2, 'I/O設定')
        self.setTabToolTip(3, '系統設定')
        self.setTabToolTip(4, '訊息')
            
     
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = RobotPageDock()  
    window.show()  
    sys.exit(app.exec_())  