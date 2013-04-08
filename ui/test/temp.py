
import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):

        super(Form, self).__init__(parent)

        self.setWindowTitle("List Items")
        self.setGeometry(400, 300, 400, 300)

        # layput
        layout = QVBoxLayout()
        self.setLayout(layout)

        # list widget
        self.listWidget = QListWidget(self)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        layout.addWidget(self.listWidget)

        passes = 'lighting GI reflect specular refraction lighting GI reflect specular refraction '

        # list items
        for index, pass_name in enumerate(passes.split()):

            myWidget = MyWidget(pass_name)
            item = myQlistWidgetItem(myWidget, pass_name)
            item.setSizeHint(QSize(340,40))
            self.listWidget.addItem(item);
            self.listWidget.setItemWidget(item, myWidget);

        # add button
        self.button = QPushButton("List Items", self)
        self.button.clicked.connect(self.buttonClicked)
        layout.addWidget(self.button)

    def buttonClicked(self):

        item_num = self.listWidget.count()

        self.pass_list = []
        self.premult_list = []

        for i in range(item_num):
            item = self.listWidget.item(i)
            info_dict = item.get_info()

            if info_dict.get('pass_name') is not None:
                self.pass_list.append(info_dict.get('pass_name'))
                #print(info_dict.get('pass_name'))

            if info_dict.get('premult') is not None:
                self.premult_list.append(info_dict.get('premult'))
                #print(info_dict.get('premult'))

        print('passes: ' + str(self.pass_list))
        print('premult: ' + str(self.premult_list))

class myQlistWidgetItem(QListWidgetItem):

    def __init__(self, customWidget, name = 'No Name given' , parent=None):

        super(myQlistWidgetItem, self).__init__(parent)

        self.name = name
        self.custom_widget = customWidget

    def get_info(self):
        return self.custom_widget.get_info()

class MyWidget(QWidget):

    def __init__(self, name = 'No Name given', parent=None):

        super(MyWidget, self).__init__(parent)

        self.name = name

        # (x, y, w, h)
        self.setGeometry(QRect(500,300,300,50))

        self.gridLayout = QGridLayout(self)

        # PySide.QtGui.QGridLayout.addWidget(arg__1, row, column[, alignment=0])
        self.pass_checkbox = QCheckBox(name)
        self.pass_checkbox.setChecked(True)
        self.gridLayout.addWidget(self.pass_checkbox, 0, 0, 1, 1)

        self.premult_checkbox = QCheckBox('Premult')
        self.premult_checkbox.setChecked(True)
        self.gridLayout.addWidget(self.premult_checkbox, 0, 1, 1, 2)

        self.button = QPushButton(self.name+' button', self)
        self.button.clicked.connect(self.buttonClicked)
        self.gridLayout.addWidget(self.button, 0, 2, 1, 2)

    def get_pass(self):
        return self.name

    def get_info(self):

        info_dict = {}

        if self.pass_checkbox.isChecked(): info_dict.update({'pass_name':self.name})

        if self.premult_checkbox.isChecked(): info_dict.update({'premult':self.name})

        return info_dict

    def buttonClicked(self):

        sys.stdout.write('%s\n' %self.name)

        pass_list = []
        premult_list = []

        if self.pass_checkbox.isChecked():
            pass_list.append(self.name)

        else: return None

        if self.premult_checkbox.isChecked():
            premult_list.append(self.name)

        else: return None

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
