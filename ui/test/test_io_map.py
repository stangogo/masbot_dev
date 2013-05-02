#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

author: Cigar Huang
website: 
last edited: Mar. 2013
"""

import sys
import os

from datetime import datetime
import threading
import time 
#from threading import Thread


from PySide import QtGui
from PySide import QtCore

from masbot.ui.robot.io.io_map import IOMap
from masbot.ui.robot.io.nozzle_table import NozzleTable

from masbot.config.utils import Path, Constants, UISignals, SigName

class MainUI(QtGui.QWidget):
    
    def __init__(self):
        super(MainUI, self).__init__()
        
        self.init_ui()
   
    def init_ui(self):        
        top_layout = QtGui.QHBoxLayout()
        start_btn = QtGui.QPushButton('Start')
        stop_btn = QtGui.QPushButton('Stop')
        start_btn.clicked.connect(self.start_change_img)
        stop_btn.clicked.connect(self.stop_change_img)
        top_layout.addWidget(start_btn)
        top_layout.addWidget(stop_btn)
        
        bottom_layout = QtGui.QHBoxLayout()
        bottom_layout.addWidget(IOMap(8))
        bottom_layout.addWidget(NozzleTable('nozzle', ['key'], QtCore.Qt.Orientation.Horizontal))
        #bottom_layout.addWidget(NozzleTable('', 'nozzle_ui', True))
        
        whole_layout = QtGui.QVBoxLayout()
        whole_layout.addLayout(top_layout)
        whole_layout.addLayout(bottom_layout)
        
                
        do_out = UISignals.GetSignal(SigName.DO_OUT)
        do_out.connect(self.do_changed)
        
                                
        self.setLayout(whole_layout)
        
        self.setWindowTitle(self.init_caption())
        imgs_dir = Path.imgs_dir()
        self.setWindowIcon(QtGui.QIcon("{0}//App.ico".format(imgs_dir)))
        self.show()

    def start_change_img(self):
        
        timer = threading.Timer(1, self.threadFunc) # 5秒后执行  
        timer.start()          
        
        
        #t = threading.Thread(target = self.threadFunc)
        #t.start()
          
    def stop_change_img(self):
        self.stop_thread = True
          
    def threadFunc(self):
        self.stop_thread = False
        index = 0
        
        set_dio = UISignals.GetSignal(SigName.DIO_STATUS)        
        
        do = [0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              1,0,0,1,0,1] 
        

        do1 = [1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,
               0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,
              1,0,0,1,0,1] 
        
        di = [[1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1]]
        
        do = [[1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,
                       1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,
                       1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1]]
        
        dio_8154 = {'type':'8154', 'di':[0,0,1,1,1,1,0,0,0,0], 'do':[0,0,0,0,0,1,0,1,1,1]}
        
        dio_8158 = {'type':'8158', 'di':[1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1], 'do':[1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0]}
        
        while self.stop_thread == False:
            dio_8154['di'] = di[index % 1]
            dio_8154['do'] = do[index % 1]
            dio_8158['di'] = di[index % 1]
            dio_8158['do'] = do[index % 1]
            
            set_dio.emit(dio_8154)
            set_dio.emit(dio_8158)

            index += 1
            time.sleep(1)            
            
    def do_changed(self, do_index, on):

        print("DO {0}, is {1}".format(do_index, on))
        
    
    def init_caption(self):
        now_time = datetime.now()
        
        caption = "Masbot - {0} Ver.{1} 啟動時間: {2}".format(Constants.MACHINE_NAME, 
                                                    Constants.VERSION,
                                                    now_time.strftime("%Y/%m/%d %H:%M:%S"))
        return caption
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    
    ex = MainUI()
    app.exec_()

if __name__ == '__main__':
    main()


        
        
