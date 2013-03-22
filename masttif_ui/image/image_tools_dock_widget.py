import os
from PySide import QtGui, QtCore
  
class ImageToolsDockWidget(QtGui.QMainWindow):
    
    imgs_dir = ""
    
    def __init__(self):  
        
        QtGui.QMainWindow.__init__(self)                
        self.imgs_dir = os.path.abspath(__file__ + "//..//..//")+"//Imgs"
        
        self.dockbars = {}
        self.createDockWindows()
        
    def createDockWindows(self):
        self.dockbars['message'] = QtGui.QDockWidget('影像訊息', self)        
        self.dockbars['camera_settings'] = QtGui.QDockWidget('Camera設定', self)
        self.dockbars['IPI_settings'] = QtGui.QDockWidget('辨識設定', self)
        self.dockbars['verify_param'] = QtGui.QDockWidget('校正參數', self)
        self.dockbars['adjust_tools'] = QtGui.QDockWidget('調機工具', self)
        self.dockbars['other_tools'] = QtGui.QDockWidget('其他工具', self)

        
        self.dockbars['message'].setTitleBarWidget(QtGui.QWidget())
        self.dockbars['camera_settings'].setTitleBarWidget(QtGui.QWidget())        
        self.dockbars['IPI_settings'].setTitleBarWidget(QtGui.QWidget())
        self.dockbars['verify_param'].setTitleBarWidget(QtGui.QWidget())
        self.dockbars['adjust_tools'].setTitleBarWidget(QtGui.QWidget())
        self.dockbars['other_tools'].setTitleBarWidget(QtGui.QWidget())
        
        
        self.setDockOptions(self.AnimatedDocks | self.ForceTabbedDocks)

        # sets the tab position at the top of tabbed dockwidgets
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtGui.QTabWidget.North)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockbars['message'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockbars['camera_settings'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockbars['IPI_settings'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockbars['verify_param'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockbars['adjust_tools'])
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockbars['other_tools'])

        self.tabifyDockWidget(self.dockbars['message'], self.dockbars['camera_settings'])
        self.tabifyDockWidget(self.dockbars['camera_settings'], self.dockbars['IPI_settings'])
        self.tabifyDockWidget(self.dockbars['IPI_settings'], self.dockbars['verify_param'])
        self.tabifyDockWidget(self.dockbars['verify_param'], self.dockbars['adjust_tools'])
        self.tabifyDockWidget(self.dockbars['adjust_tools'], self.dockbars['other_tools'])

        self.dockbars['message'].raise_()


        IPI_result_table = QtGui.QTableWidget(self.dockbars['message'])
        IPI_result_table.setColumnCount(4)
        IPI_result_table.setRowCount(3)
        headers = ['時間', '辨識工作', '結果', '辨識時間(s)']
        IPI_result_table.setHorizontalHeaderLabels(headers)
        IPI_result_table.setItem(0,0, QtGui.QTableWidgetItem('A'))
        IPI_result_table.setItem(1, 0, QtGui.QTableWidgetItem('Time'))


        #icon_path = "{0}//Start.bmp".format(self.imgs_dir)
        IPI_result_table.setItem(2,0, QtGui.QTableWidgetItem(QtGui.QIcon("{0}//Start.bmp".format(self.imgs_dir)), "data"));
        IPI_result_table.setRowCount(4)
        IPI_result_table.setItem(3,0, QtGui.QTableWidgetItem(QtGui.QIcon("{0}//Stop.bmp".format(self.imgs_dir)), "data"));
        IPI_result_table.resize(420, 200)
        
        #IPI result table (方法2)
        # IPI_result_table = QtGui.QTableView()
        # model = QtGui.QStandardItemModel(3, 4)
        # model.setHorizontalHeaderLabels(['Time', 'Checking', 'Result' ])
        # model.setHorizontalHeaderItem(3, QtGui.QStandardItem('Spend Time'))
        # IPI_result_table.setModel(model)
        # model.setItem(0,0,QtGui.QStandardItem('88'))
        
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = ImageToolsDockWidget()  
    window.show()  
    sys.exit(app.exec_())  