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

class SigName:
    #axis_banner
    DI_DO_SHOW = 'DI_DO_SHOW'   
        # DIOÅã¥Ü«ö¶s
    
    #Major widget
    FLOW_MSG = 'FLOW_MSG'       
        #show flow message, send into a string
    ALARM_MSG = 'ALARM_MSG'     
        #show alarm message, send into a string
    PRODUCT_INFO = 'PRODUCT_INOF' 
        #show product info,send into dictionary, ex.
            #{'CT': 4.25, 
            #'ProdName': '9552A1', 
            #'MatchAngle':3.11, 
            #'AssembleMode': 'manually', 
            #'ProdBarCode': 'A222dsd323', 
            #'ProdNum': '11op98733', 
            #'Total': 200}
        
    LOG_IN = 'LOG_IN'           
        #Servo On button
    SERVO_ON = 'SERVO_ON'       
        #Servo On button
    START_MAIN = 'START_MAIN'   
        #Start button
    PAUSE_MAIN = 'PAUSE_MAIN'   
        #Pause button
    
    #Axis table
    ENTER_AXIS_TABLE = 'ENTER_AXIS_TABLE'   
        #set data to axis table - row_name(str), axis_name(str), value (int)
    FROM_AXIS_TABLE = 'FROM_AXIS_TABLE'     
        #data from axis table - axis_name(str), value(int), action (1:add, -1 minus)
    
    #DIO map
    ENTER_IO_MAP_DI = 'ENTER_IO_MAP_DI'
        #set DI in io map - DI status (list), on/off (bool)
    ENTER_IO_MAP_DO = 'ENTER_IO_MAP_DO'
        #set DO in io map - DO status (list), on/off (bool)
    FROM_IO_MAP = 'FROM_IO_MAP'
        #send DO clicked - DO number (int), on/off (bool)
    
class UISignals():
    signal_dict = {}
    @staticmethod
    def RegisterSignal(signal, name):
        UISignals.signal_dict[name] = signal
        
    @staticmethod
    def GetSignal(name):
        try:
            return UISignals.signal_dict[name]
        except:
            return None    
    
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

