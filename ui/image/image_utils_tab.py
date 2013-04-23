import os
from PySide import QtGui, QtCore
from masbot.ui.image.tab_utils.aided_tool import AidedTool
from masbot.ui.image.tab_utils.camera_settings import CameraSettings
from masbot.ui.image.tab_utils.identification_settings import IdentificationSettings
from masbot.ui.image.tab_utils.img_message_table import ImageMessage

from masbot.config.utils import UISignals, SigName

class ImageUtilsTab(QtGui.QTabWidget):    
    imgs_dir = ""
    
    def __init__(self):  
        
        QtGui.QTabWidget.__init__(self)                
        self.imgs_dir = os.path.abspath(__file__ + "//..//..//")+"//Imgs"
        
        self.createDockWindows()
        
        
    def createDockWindows(self):
        self.addTab(ImageMessage(), '辨識訊息')
        self.addTab(CameraSettings(), 'Camera設定')
        self.addTab(IdentificationSettings(), '工作設定')
        self.addTab(AidedTool(), '輔助工具')
        
        try:
            UISignals.GetSignal(SigName.IMG_AIDED_TOOL).connect(self.aided_data)                
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