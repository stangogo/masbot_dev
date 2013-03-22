
import os
from PySide import QtCore



class Constants:
    MACHINE_NAME = 'LP_V01'
    DAT_FOLDER = 'data'
    IMGS_FOLDER = 'imgs'
    DB = 'db'
    LOG = 'Log'
    SQLITE_DB_NAME = 'Mastiff.db'
    VERSION = '1.0.0.0'
    
class Communicate(QtCore.QObject):
    """
    create two new signals on the fly: one will handle
    int type, the other will handle strings
    """
    speak_number = QtCore.Signal(int)
    speak_word = QtCore.Signal(str)

class Path():
    @staticmethod
    def data_dir():
        current_dir= os.path.abspath(__file__ +  "//..//..//")
        dir_ =  "{0}\\{1}".format(current_dir, Constants.DAT_FOLDER)
        return dir_
    
    @staticmethod
    def imgs_dir():
        current_dir= os.path.abspath(__file__ +  "//..//")
        dir_ =  "{0}\\{1}".format(current_dir, Constants.IMGS_FOLDER)
        return dir_