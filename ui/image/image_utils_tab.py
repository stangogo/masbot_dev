import os
from PySide import QtGui, QtCore
from masbot.ui.image.tab_utils.aided_tool import AidedTool
from masbot.ui.image.tab_utils.camera_settings import CameraSettings

from masbot.config.utils import UISignals, SigName

class ImageUtilsTab(QtGui.QTabWidget):    
    imgs_dir = ""
    
    def __init__(self):  
        
        QtGui.QTabWidget.__init__(self)                
        self.imgs_dir = os.path.abspath(__file__ + "//..//..//")+"//Imgs"
        
        self.dockbars = {}
        self.createDockWindows()
        
    def createDockWindows(self):
        self.dockbars['message'] = QtGui.QWidget()
        
        self.addTab(self.dockbars['message'], '辨識訊息')
        self.addTab(CameraSettings(), 'Camera設定')
        self.addTab(QtGui.QWidget(), '辨識設定')
        self.addTab(QtGui.QWidget(), '校正參數')
        
        self.addTab(AidedTool(), '輔助工具')
        
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
        IPI_result_table.resize(320, 200)
        
        try:
            UISignals.GetSignal(SigName.AIDED_TOOL).connect(self.aided_data)                
        except:
            pass
        
        #IPI result table (方法2)
        # IPI_result_table = QtGui.QTableView()
        # model = QtGui.QStandardItemModel(3, 4)
        # model.setHorizontalHeaderLabels(['Time', 'Checking', 'Result' ])
        # model.setHorizontalHeaderItem(3, QtGui.QStandardItem('Spend Time'))
        # IPI_result_table.setModel(model)
        # model.setItem(0,0,QtGui.QStandardItem('88'))
        
    def aided_data(self, data_dict):
        for key, value in data_dict.items():
            print(key, value)    

if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = ImageUtilsTab()  
    window.show()  
    app.exec_()