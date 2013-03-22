# -- coding: utf-8 --
# Title          : MessageAndLog.py
# Description    : 繼承自QListWidget, 另實作記錄儲存到檔案功能. 檔案路徑取自My.py LARGAN_FOLDER\\MACHINE_NAME\\Log
# Author         : Cigar Huang
# Date           : 20130312
# Dependency     : My.py
# Usage          : import from MessageAndLog.py
# Notes          : 
# Example        :  message_list = MessageAndLog('YourName')
#                   message_list.add_message('SampleMessage')                    


import os
import logging
import sys
from datetime import date
from PySide import QtGui, QtCore
from masttif_ui.utils import Constants, Communicate

class MessageAndLog(QtGui.QListWidget):
    
    def __init__(self, name):
        super(MessageAndLog, self).__init__()
                
        self.name = name                        # name is used in handle of logger and log file path
        self.time_str = ""                      # save the date str in log file, if the log opened over one day, time_str must be updated.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.talker = Communicate()             # asynchronous to update the message to list
        self.talker.speak_word.connect(self.__add_message)
        current_dir= os.path.abspath(__file__ +  "//..//..//")
        self.log_dir = "{0}\\{1}\\{2}\\{3}".format(current_dir,
                                               Constants.DAT_FOLDER,
                                               Constants.MACHINE_NAME, 
                                               Constants.LOG)         
        if not os.path.exists(self.log_dir):
                        os.makedirs(self.log_dir)
        
        #self.initUI()
        self.show()
        
    #def initUI(self): 
        #self.setSortingEnabled(True)
        #self.show()
        #self.add_message("lkdjf;laskdjf;lkjl4jk2;3l4kj2;3lrkj;wlekfl;sd")
           
    def add_message(self, new_message):
        self.talker.speak_word.emit(new_message)
                
    @QtCore.Slot(str)
    def __add_message(self, new_message):
        self.addItem(QtGui.QListWidgetItem(new_message))
        self.scrollToBottom()
        self.save_message(new_message)
    
    """
    ## 如何讓logger 把訊息寫到不同的檔案
    import logging
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('/var/tmp/myapp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    """
        
    def save_message(self, msg):
        self.set_save_info()
        self.logger.info(msg)
               
    def set_save_info(self):
        local_time = date.today()
        new_time_str = local_time.__str__()
        #new_time_str = local_time.strftime("%Y%m%d")

        if new_time_str != self.time_str:   #檢查是否已經跨天
            self.time_str = new_time_str
            
            #folder = "{0}\\{1}\\{2}".format(Constants.LARGAN_FOLDER, Constants.MACHINE_NAME, Constants.LOG)      #資料夾
            full_path = "{0}\\{1}_{2}.log".format(self.log_dir, self.name, self.time_str) #完整路徑

            formatter = logging.Formatter('%(asctime)s - %(message)s')
            file_handler = logging.FileHandler(full_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)            
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MessageAndLog('test')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        