
from PySide import QtGui, QtCore

from masbot.ui.ui_interface.i_axis_table import IAxisTableObj as IAxisTableObj 
from masbot.ui.db_table_def import DBTableDefine
from masbot.ui.sqldb import SqlDB
from masbot.ui.utils import Path


class AxisButton(QtGui.QPushButton):
    row = -1
    column = -1
    axis = ""
    scale = 1
   
    def __new__(self, icon, text=None):
        if text == None:
            if type(icon) == type(""):
                self.text = icon
            return QtGui.QPushButton.__new__(self, icon, "")
        else:
            self.text = text
            return QtGui.QPushButton.__new__(self, icon, text)
            
            
class AxisTable(QtGui.QTableWidget):
    i_axis_table_obj = IAxisTableObj()
    scale_list = []
    row_dict = {}
    column_dict = {}
    
    def __init__(self):  
        super(AxisTable, self).__init__()
        self.init_ui()
        self.i_axis_table_obj.msg_in.speak.connect(self.from_outside)
        
    def from_outside(self, row, axis, value):
        try:
            n_row = self.row_dict[row]
            n_col = self.column_dict[axis]
            item = QtGui.QTableWidgetItem("{0}".format(value))            
            self.setItem(n_row, n_col, item)
        except:
            print("from_outside error: {0}".format(sys.exc_info()[1]))
            
    def init_ui(self):
        db = SqlDB()
        axis_table_model = db.get_table_model('SingleAxis')
        
        self.setColumnCount(axis_table_model.rowCount())
        
        
        #欄寬 / 列高
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, 40)
        self.setColumnWidth(self.columnCount()-1, 50)        
                
        #設定表格title的color                
        self.setStyleSheet("QHeaderView::section { background-color:rgb(184, 198, 137) }");    

        #橫軸 bar          
        H_headers = []
        query = axis_table_model.query()
        query.exec_("select axis_name from SingleAxis")
        
        while query.next():
            H_headers.append(query.value(0))
                    
            
        self.setHorizontalHeaderLabels(H_headers)
        
        #縱軸 bar        
        V_Header = DBTableDefine().get_table_def('AxisOP')
        self.setRowCount(len(V_Header))
        self.setVerticalHeaderLabels(V_Header)
        self.resizeRowsToContents()    #符合列高
        index = 0
        for op in V_Header:
            self.row_dict[op] = index
            index +=1
        
        index = 0
        query.exec_("select axis_key from SingleAxis")
        for i in range(0, self.columnCount()):
            
            btn_add = AxisButton(QtGui.QIcon("{0}/Start.bmp".format(Path.imgs_dir())),"+")
            #btn_add = AxisButton(QtGui.QIcon("C:\Python33\Lib\site-packages\masbot\ui/imgs/Start.bmp"),"+")
            btn_minus = AxisButton('-')
            btn_scale = AxisButton('1')
            
            btn_add.column = btn_minus.column= btn_scale.column = i
            if query.next():
                btn_add.axis = btn_minus.axis = btn_scale.axis = query.value(0)
                self.column_dict[btn_add.axis] = index
                index += 1
            
            btn_add.clicked.connect(self.add_clicked)
            btn_minus.clicked.connect(self.minus_clicked)
            btn_scale.clicked.connect(self.scale_clicked)
            
            self.setCellWidget(2, i, btn_add)
            self.setCellWidget(3, i, btn_minus)
            self.setCellWidget(4, i, btn_scale)
            
            self.scale_list.append(btn_scale)            
            
        
        self.setWindowTitle('Axis Operation')
        
        #self.resizeRowsToContents()    #符合列高        
        #self.verticalHeader().hide()   #隱藏左側欄header

    def minus_clicked(self):
        sender = self.sender()
        scale_value = self.scale_list[sender.column].scale    
        self.i_axis_table_obj.from_axis_table(sender.axis, scale_value, -1)
        
    def add_clicked(self):
        sender = self.sender()
        scale_value = self.scale_list[sender.column].scale    
        self.i_axis_table_obj.from_axis_table(sender.axis, scale_value, 1)
        
    def scale_clicked(self):
        sender = self.sender()
        sender.scale = sender.scale *10
        if sender.scale > 1000:
            sender.scale = 1
        sender.setText("{0}".format(sender.scale))
        
        print("scale_clicked - axis: {0}".format(sender.axis))

        
if __name__ == '__main__':  
    import sys  
    app = QtGui.QApplication(sys.argv)  
    window = AxisTable()
    window.show()  
    sys.exit(app.exec_())  