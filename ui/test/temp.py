#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui
from PySide.QtGui import *


#everything from here down was created by Designer
#class Ui_Dialog(object):
    #def setupUi(self, Dialog):
        #Dialog.setObjectName("Dialog")
        #Dialog.resize(400, 300)
        #self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        #self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        #self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        #self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        #self.buttonBox.setObjectName("buttonBox")
        #self.graphicsView = QtGui.QGraphicsView(Dialog)
        #self.graphicsView.setGeometry(QtCore.QRect(50, 30, 256, 192))
        #self.graphicsView.setMouseTracking(False)
        #self.graphicsView.setFrameShadow(QtGui.QFrame.Sunken)
        #brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        #brush.setStyle(QtCore.Qt.SolidPattern)
        ##self.graphicsView.setForegroundBrush(brush)
        #self.graphicsView.setObjectName("graphicsView")

        #self.retranslateUi(Dialog)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    #def retranslateUi(self, Dialog):
        #Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))


#class MyDialog(QtGui.QGraphicsView):
    #def __init__(self):
        #super(MyDialog, self).__init__()
        
        #self.scene = QtGui.QGraphicsScene()
        #self.setScene(self.scene)
        #self.graph_item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap("R:\\TEMP\\1.tif").scaledToHeight(400))
        
        #self.scene.addItem(self.graph_item)
        #self.show()


class MyDialog(QtGui.QWidget):
    def __init__(self):
        super(MyDialog, self).__init__()
        
        self.view = GtGui.QGraphicsView()
        self.scene = QtGui.QGraphicsScene()
        self.view.setScene(self.scene)
        self.graph_item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap("R:\\TEMP\\1.tif").scaledToHeight(400))
        
        self.scene.addItem(self.graph_item)
        self.show()

        
        #self.ui = Ui_Dialog()
        #self.ui.setupUi(self)
        #self.scene = QGraphicsScene()
        #self.ui.graphicsView.setBackgroundBrush(QtGui.QImage("R:\\TEMP\\1.tif"))
        #self.ui.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)    
        #self.ui.graphicsView.setScene(self.scene)
        
   
        #self.scene.setSceneRect(0,0,100,100)
        #self.scene.addText('hello')




class ImageThumbnail(QtGui.QListWidget):

    thumbnail_clicked = QtCore.Signal(str)
    __change_image = QtCore.Signal(str, str) 
    __change_qimage = QtCore.Signal(QtGui.QPixmap, str) 
   
    def __init__(self, thumbnail_id):
        super(ImageThumbnail, self).__init__()
        self.init_ui(thumbnail_id)
        
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        
        self.setMaximumHeight(100)
        self.setMaximumWidth(700)
        
        self.__change_image.connect(self.change_image_)
        self.__change_qimage.connect(self.change_qimage_)
        
        #self.setMinimumHeight(80)
        
    def init_ui(self, thumbnail_id):

        h_layout = QtGui.QHBoxLayout()
        h_layout.addStretch(0)
        
        
        self.thumbnail = {}

        for id_ in thumbnail_id:
            self.add_label(id_)
            
        for id_ in thumbnail_id:
            self.change_image("R:\\TEMP\\1.bmp", id_)
        
        self.setFlow(QtGui.QListWidget.LeftToRight)
        self.setWindowTitle('Image thumbnail')
        self.show()
    
    def add_label(self, id_):
        index = len(self.thumbnail)
        
        img_label = QtGui.QGraphicsView()
        scene = QtGui.QGraphicsScene()
        img_label.setScene(scene)
        
        img_label.setContentsMargins(3, 0, 0, 0)    #圖片偏左, 用margin往中間調
        #img_label.clicked.connect(self.__thumbnail_clicked)
        #graph_item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap("R:\\TEMP\\1.bmp").scaledToHeight(70))
        graph_item = QtGui.QGraphicsPixmapItem()
        scene.addItem(graph_item)
        
        item = QtGui.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(100,75))  # 每個item的大小
        self.addItem(item)
        self.setItemWidget(item, img_label)
        self.thumbnail[id_] = [graph_item, index]    #第一欄是label, 這二欄是index        
        
    def __thumbnail_clicked(self, thumbnail_id):
        index = self.thumbnail[thumbnail_id][1]     #第二欄是index
        self.item(index).setSelected(True)
        self.thumbnail_clicked.emit(thumbnail_id)
    
    def change_image_(self, image_path, id_):
        self.thumbnail[id_][0].setPixmap( QtGui.QPixmap(image_path).scaledToHeight(70))
        
    def change_image(self, image_path, id_):
        if not id_ :
            return
        
        if not self.thumbnail.get(id_):
            self.add_label(id_)
        
        self.__change_image.emit(image_path, id_)
        
    def change_qimage_(self, qimage, id_):
        self.thumbnail[id_][0].setPixmap( qimage.scaledToHeight(70))
        #self.thumbnail[id_][0].setPixmap( QtGui.QPixmap.fromImage(qimage).scaledToHeight(70))
        
    def change_qimage(self, qimage, id_):
        if not id_ :
            return
        
        if not self.thumbnail.get(id_):
            self.add_label(id_)
        
        self.__change_qimage.emit(qimage, id_)    
        

def main(argv):
    app = QApplication(sys.argv)
    myapp = ImageThumbnail(['1','2','3'])
    myapp.show()
    app.exec_()    

if __name__ == "__main__":
    main(sys.argv)



""" Test Widget on listwidget

#class Form(QDialog):

    #def __init__(self, parent=None):

        #super(Form, self).__init__(parent)

        #self.setWindowTitle("List Items")
        #self.setGeometry(400, 300, 400, 300)

        ## layput
        #layout = QVBoxLayout()
        #self.setLayout(layout)

        ## list widget
        #self.listWidget = QListWidget(self)
        #self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        #layout.addWidget(self.listWidget)

        #passes = 'lighting GI reflect specular refraction lighting GI reflect specular refraction '

        ## list items
        #for index, pass_name in enumerate(passes.split()):

            #myWidget = MyWidget(pass_name)
            #item = myQlistWidgetItem(myWidget, pass_name)
            #item.setSizeHint(QSize(340,40))
            #self.listWidget.addItem(item);
            #self.listWidget.setItemWidget(item, myWidget);

        ## add button
        #self.button = QPushButton("List Items", self)
        #self.button.clicked.connect(self.buttonClicked)
        #layout.addWidget(self.button)

    #def buttonClicked(self):

        #item_num = self.listWidget.count()

        #self.pass_list = []
        #self.premult_list = []

        #for i in range(item_num):
            #item = self.listWidget.item(i)
            #info_dict = item.get_info()

            #if info_dict.get('pass_name') is not None:
                #self.pass_list.append(info_dict.get('pass_name'))
                ##print(info_dict.get('pass_name'))

            #if info_dict.get('premult') is not None:
                #self.premult_list.append(info_dict.get('premult'))
                ##print(info_dict.get('premult'))

        #print('passes: ' + str(self.pass_list))
        #print('premult: ' + str(self.premult_list))

#class myQlistWidgetItem(QListWidgetItem):

    #def __init__(self, customWidget, name = 'No Name given' , parent=None):

        #super(myQlistWidgetItem, self).__init__(parent)

        #self.name = name
        #self.custom_widget = customWidget

    #def get_info(self):
        #return self.custom_widget.get_info()

#class MyWidget(QWidget):

    #def __init__(self, name = 'No Name given', parent=None):

        #super(MyWidget, self).__init__(parent)

        #self.name = name

        ## (x, y, w, h)
        #self.setGeometry(QRect(500,300,300,50))

        #self.gridLayout = QGridLayout(self)

        ## PySide.QtGui.QGridLayout.addWidget(arg__1, row, column[, alignment=0])
        #self.pass_checkbox = QCheckBox(name)
        #self.pass_checkbox.setChecked(True)
        #self.gridLayout.addWidget(self.pass_checkbox, 0, 0, 1, 1)

        #self.premult_checkbox = QCheckBox('Premult')
        #self.premult_checkbox.setChecked(True)
        #self.gridLayout.addWidget(self.premult_checkbox, 0, 1, 1, 2)

        #self.button = QPushButton(self.name+' button', self)
        #self.button.clicked.connect(self.buttonClicked)
        #self.gridLayout.addWidget(self.button, 0, 2, 1, 2)

    #def get_pass(self):
        #return self.name

    #def get_info(self):

        #info_dict = {}

        #if self.pass_checkbox.isChecked(): info_dict.update({'pass_name':self.name})

        #if self.premult_checkbox.isChecked(): info_dict.update({'premult':self.name})

        #return info_dict

    #def buttonClicked(self):

        #sys.stdout.write('%s\n' %self.name)

        #pass_list = []
        #premult_list = []

        #if self.pass_checkbox.isChecked():
            #pass_list.append(self.name)

        #else: return None

        #if self.premult_checkbox.isChecked():
            #premult_list.append(self.name)

        #else: return None

#app = QApplication(sys.argv)
#form = Form()
#form.show()
#app.exec_()
"""
