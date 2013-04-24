
from PySide import QtGui, QtCore
from masbot.ui.robot.major.major_widget import MajorWidget
from masbot.ui.robot.io.io_widget import IOWidget
from masbot.config.utils import Path
from masbot.ui.control.ui_utils import *

    
class RobotPageDock(QtGui.QTabWidget):
    
    def __init__(self):  
        QtGui.QTabWidget.__init__(self)
        self.pages = {}
        self.init_tabs()
        
    def init_tabs(self):

        self.addTab(MajorWidget(), get_rotate_qicon('main.png', 90), '')
        self.addTab(IOWidget(), get_rotate_qicon('IO.png', 90), '')
        self.addTab(QtGui.QWidget(), get_rotate_qicon('system_settings.png', 90), '')
        self.addTab(QtGui.QWidget(), get_rotate_qicon('message.png', 90), '')
        self.addTab(QtGui.QWidget(), get_rotate_qicon('test.png', 90), '')
        
        self.sizeHint()
        
        #self.setStyleSheet('QTabBar::tab { min-width:60px ; min-height:30px ; font:12px ;}')   # 橫向 (West or East) 要設 width
        self.setTabPosition(QtGui.QTabWidget.West)
        
        #self.setStyleSheet('QTabBar::tab { height: 50px}') # 縱向 (North or South) 要設 height
        #self.setTabPosition(QtGui.QTabWidget.North)
        
        self.tab_tool_tip()
        self.setIconSize(QtCore.QSize(50, 50))
     
    def tab_tool_tip(self):
        self.setTabToolTip(0, '主頁')
        self.setTabToolTip(1, 'I/O設定')
        self.setTabToolTip(2, '系統設定')
        self.setTabToolTip(3, '訊息')
        self.setTabToolTip(4, '測試模式')

    #def get_rotate_icon(self, file_name, r_angle):
        #file_path = "{0}/{1}".format(Path.imgs_dir(), file_name)
        #qimage = QtGui.QImage(file_path)        
        #rotate = QtGui.QTransform()
        #rotate.rotate(r_angle)
        #r_qimage = qimage.transformed(rotate)
        
        #return QtGui.QIcon(QtGui.QPixmap.fromImage(r_qimage))
     
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = RobotPageDock()  
    window.show()  
    app.exec_()