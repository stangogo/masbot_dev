
from PySide import QtGui, QtCore
from masbot.ui.robot.major.major_widget import MajorWidget
from masbot.ui.robot.io.io_widget import IOWidget
    
class RobotPageDock(QtGui.QMainWindow):
    
    index_changed = QtCore.Signal(bool)
    
    def __init__(self):  
        QtGui.QMainWindow.__init__(self)
        self.pages = {}
        self.createDockWindows()
        
        
    def createDockWindows(self):
        #Empty widget to set the DockWidget with empty title
        main_title_widget = QtGui.QWidget()
        test_title_widget = QtGui.QWidget()
        IO_title_widget = QtGui.QWidget()
        system_title_widget = QtGui.QWidget()
        message_title_widget = QtGui.QWidget()
        
        self.pages['main_page'] = MajorWidget('主頁', self)
        self.pages['test_mode'] = QtGui.QDockWidget('測試模式', self)
        self.pages['IO_settings'] = IOWidget('I/O設定', self)
        self.pages['system_setting'] = QtGui.QDockWidget('系統設定', self)
        self.pages['message'] = QtGui.QDockWidget('訊息', self)

        self.pages['main_page'].setTitleBarWidget(main_title_widget)
        self.pages['test_mode'].setTitleBarWidget( test_title_widget)
        self.pages['IO_settings'].setTitleBarWidget( IO_title_widget )
        self.pages['system_setting'].setTitleBarWidget( system_title_widget )
        self.pages['message'].setTitleBarWidget( message_title_widget )
        
        
        self.setDockOptions(self.AnimatedDocks | self.ForceTabbedDocks)

        # sets the tab position at the top of tabbed dockwidgets
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtGui.QTabWidget.West)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.pages['main_page'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.pages['test_mode'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.pages['IO_settings'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.pages['system_setting'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.pages['message'])

        self.tabifyDockWidget(self.pages['main_page'], self.pages['test_mode'])
        self.tabifyDockWidget(self.pages['test_mode'], self.pages['IO_settings'])
        self.tabifyDockWidget(self.pages['IO_settings'], self.pages['system_setting'])
        self.tabifyDockWidget(self.pages['system_setting'], self.pages['message'])

        self.pages['IO_settings'].raise_()
        #self.pages['main_page'].raise_()
        
        self.pages['main_page'].visibilityChanged.connect(self.visible_)
        

    def visible_(self, visible):
        self.index_changed.emit(visible)
        #self.main_page_visible_changed(visible)


    #@QtCore.Slot(bool)
    #def main_page_visible_changed(self, visible):        
        #print('visible')
        
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = RobotPageDock()  
    window.show()  
    sys.exit(app.exec_())  