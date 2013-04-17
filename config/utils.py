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
    """axis_banner"""
    DI_DO_SHOW = 'DI_DO_SHOW'
        # DIO顯示按鈕
    
    TO_ROBOT_BANNER = 'TO_ROBOT_BANNER'
        # 顯示機台資訊
        
    REMOVE_IMG_SIDE = 'REMOVE_IMG_SIDE'
        # 移除影像側
    
    """Major widget"""
    FLOW_MSG = 'FLOW_MSG'
        # show flow message, send into a string
    ALARM_MSG = 'ALARM_MSG'
        # show alarm message, send into a string
    PRODUCT_INFO = 'PRODUCT_INOF'
        # show product info,send into dictionary, ex.
            #{'CT': 4.25, 
            # 'ProdName': '9552A1', 
            # 'MatchAngle':3.11, 
            # 'AssembleMode': 'manually', 
            # 'ProdBarCode': 'A222dsd323', 
            # 'ProdNum': '11op98733', 
            # 'Total': 200 }
        
    LOG_IN = 'LOG_IN'           
        # Servo On button
    SERVO_ON = 'SERVO_ON'       
        # Servo On button
    START_MAIN = 'START_MAIN'   
        # Start button
    PAUSE_MAIN = 'PAUSE_MAIN'   
        # Pause button
    
    """Axis table"""
    ENTER_AXIS_TABLE = 'ENTER_AXIS_TABLE'   
        # set data to axis table - 
        # @row_name(str), @axis_name(str), @value (int)
    FROM_AXIS_TABLE = 'FROM_AXIS_TABLE'     
        # data from axis table - 
        # @axis_name(str), @value(int)
    
    """ DIO agent"""
    DO_IN = 'DIO_AGENT_DO_IN'
        # Signals of DO from outside - 
        # @DO status (list), @on/off (int 1/0)
    DI_IN = 'DIO_AGENT_DI_IN'
        # Signals of DI from outside - 
        # @DI status (list), @on/off (int 1/0)
    DO_OUT = 'DIO_AGENT_DO_OUT'
        # Send DO signal out - 
        # @DO number (int), @on/off (int 1/0)
                
    IMG_THUMBNAIL = 'IMG_THUMBNAIL'
        # Receive the preview data of image, applied at image thumbnail and preview label
        # @file path(str), @id (str)
    
    AIDED_TOOL = 'AIDED_TOOL'
    
class UISignals():
    signal_dict = {}
    @staticmethod
    def RegisterSignal(signal, name):
        """
        registere signal object with a name in UISignal for used by others later.
        @ signal: the signal object
        @ name: the name for dictionary, defined in SigName class.
        
        """
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
        current_dir= os.path.abspath(__file__ +  "//..//..//")
        dir_ =  "{0}\\ui\\{1}".format(current_dir, Constants.IMGS_FOLDER)
        return dir_
    
    def mosbot_dir():
        return os.path.abspath(__file__ +  "//..//..//")
        