# -*- coding: utf-8 -*-

# Title          : camera_module.py
# Description    : camera grabber
# Author         : Henry Chang
# Date           : 20130423
# Dependency     : Bulletin.py channel.py Framegrabber_dll.py
# usage          : 
# notes          : 

import logging
from re import compile
from PIL import Image
from masbot.device.bulletin import Bulletin
from masbot.device.channel import Channel
from masbot.device.camera.Framegrabber_dll import *


class CameraModule(Bulletin, Channel):    
    def __init__(self, camera_info, board={}):
        owner = camera_info['camera_name']
        super(CameraModule, self).__init__(owner, board)
        #Due to multiple inheritance, it should active channel by hand.        
        self.init_channel()
        self.__logger = logging.getLogger(__name__)       
        # The string length is connected with the char length of framegrabber.dll, so can't change this variable.   
        self.__str_length = 1024           
        self.__para_set = {}
        #self.__para_enum = common_lib.enum('width','height','channel','frame_rate','reverse_type','gain_value',
                                 #'gain_min','gain_max','shutter_value','shutter_min','shutter_max')
        self.__para_enum = {'width':0,'height':1,'channel':2,'frame_rate':3,'reverse_type':4,'gain_value':5,
                                         'gain_min':6,'gain_max':7,'shutter_value':8,'shutter_min':9,'shutter_max':10}        
        self.__initial(camera_info)  
        
    def __del__(self):
        self.close_camera()   
        
    def __initial(self, camera_info):
        self.__logger.debug(' Camera device:{0} is beginnig to initial.'.format(camera_info.get('display_text', 'No camera')))        
        self.__port = camera_info.get('port', -1)
        self.__camera_type = camera_info.get('camera_type','')
        self.__camera_mode = camera_info.get('camera_mode','')       
        self.__color_type = camera_info.get('color_type', 'gray')
        self.__display_text = camera_info.get('display_text', '')
        self.run(Framegrabber_dll.initial_dll)  # initial dll handler
        ret = self.open_framegrabber()
        self.get_parameter_values(camera_info)
        
    def open_framegrabber(self): 
        cstr = (c_char*self.__str_length)(0)
        cstr.value = self.__camera_type.encode()    #set camera type in advance
        ret = self.run(Framegrabber_dll.set_camera_type, self.__port, cstr)
        if ret:
            self.__logger.warning('Camera:{0} device open framegrabber fail when setting {1}.'.format(self.__display_text,self.__camera_type))
            return ret
        cstr.value = self.__color_type.encode()    #set camera type in advance
        ret = self.run(Framegrabber_dll.set_camera_color_type, self.__port, cstr)
        if ret:
            self.__logger.warning('Camera:{0} device open framegrabber fail when setting {1}.'.format(self.__display_text,self.__camera_mode))  
            return ret
        cstr.value = self.__camera_mode.encode()    #set camera mode in advance
        ret = self.run(Framegrabber_dll.set_camera_mode, self.__port, cstr)
        if ret:
            self.__logger.warning('Camera:{0} device open framegrabber fail when setting {1}.'.format(self.__display_text,self.__camera_mode))
            return ret
        ret = self.run(Framegrabber_dll.initial_grabber, self.__port)
        if ret:
            self.__logger.error('Camera:{0} device open framegrabber fail when initialled camera grabber.'.format(self.__display_text))
            return ret 
        self.__logger.debug('Camera:{0} device open framegrabber successful.'.format(self.__display_text))
        return ret;
    
    def get_parameter_values(self, cam_info):
        value = c_int(0)
        for i, index in enumerate(self.__para_enum):
            ret = self.run(Framegrabber_dll.get_camera_parameter, self.__port, self.__para_enum[index], pointer(value))
            if ret:
                sself.__logger.warning('Camera:{0} device setting {1} fail.'.format(self.__display_text, index))
                self.__para_set.update(i,0)
            else:
                self.__para_set.update({index:value.value})
        #setting parameter in advance
        self.set_parameter('reverse_type', cam_info['reverse_type'])
        self.set_parameter('gain_value', cam_info['gain_value'])
        self.set_parameter('shutter_value', cam_info['shutter_value'])
        
    def get_parameter(self, para_name):
        if para_name in self.__para_enum.keys():
            return self.__para_set.get(para_name, None)
        elif para_name == 'camera_type':
            return self.__camera_type
        elif para_name == 'camera_mode':
            return self.__camera_mode
        elif para_name == 'color_type':
            return self.__color_type
        
    def set_parameter(self, para_name, value):
        if para_name in self.__para_enum.keys():
            if para_name in ['gain_value','shutter_value','reverse_type']:
                ret = self.run(Framegrabber_dll.set_camera_parameter, self.__port, self.__para_enum[para_name], value)
                if ret:
                    self.__logger.warning('Camera:{0} device setting {1} fail.'.format(self.__display_text, para_name))
                else:
                    self.__para_set[para_name] = value
                    self.__logger.debug('Camera:{0} device setting {1} successful.'.format(self.__display_text, para_name))
                return ret                
        return None
    
    def grab_image(self):
        pData = (c_ubyte*(self.get_parameter('width')*self.get_parameter('height')*self.get_parameter('channel')))()
        ret = self.run(Framegrabber_dll.grab_image, self.__port, pData) 
        if ret != 0:
            self.__logger.warning('Camera:{0} device grab image occurred {1} error.'.format(self.__display_text, self.get_error_msg(ret)))
            return None
        else:
            if cam.get_parameter('channel') == 1:
                im = Image.frombuffer('L', [self.get_parameter('width'),self.get_parameter('height')], pData, 'raw', 'L', 0, 1)
            elif cam.get_parameter('channel') == 3:
                im = Image.frombuffer('RGB', [imgwidth,imgheight], pData, 'raw', 'RGB', 0, 1)    
            return im
    def get_error_msg(self, error_type):
        cstrp = c_char_p(0)
        cstrp = self.run(Framegrabber_dll.get_err_msg, error_type)
        cstr = cast(cstrp, c_char_p)
        pstr = cstr.value.decode()
        return pstr   
    
    def get_dll_version(self, error_type):
        cstrp = c_char_p(0)
        cstrp = self.run(Framegrabber_dll.get_version)
        cstr = cast(cstrp, c_char_p)
        pstr = cstr.value.decode()
        return pstr         
        
    def close_camera(self):
        ret = self.run(Framegrabber_dll.close_grabber, self.__port)
        if ret != 0:
            self.__logger.warning('Camera:{0} device close grabber occurred {1} error.'.format(self.__display_text, self.get_error_msg(ret)))   
            
#-------------------------------------------------------------------------------------------------
#-----------------------------------------test----------------------------------------------------
#-------------------------------------------------------------------------------------------------
#camera_inf =  {
        #'pixel_size': 0.00725,
        #'shutter_value': 800,
        #'display_text': '上攝影機模組',
        #'light': {...
        #},
        #'IPQC': {
            #'light': ['top_camera_ISL', 'top_camera_RL'],
            #'dll_name': 'IPQC_9552A1',
            #'display_text': '成品檢查'
        #},
        #'gain_value': 100,
        #'camera_type': '1394IIDC',
        #'color_type': 'gray',
        #'port': 0,
        #'top_camera_RL': ['ADLink', 102, '環形光源'],
        #'CAMERA_CHECK': {
            #'light': ['top_camera_ISL'],
            #'dll_name': 'camera_check',
            #'display_text': 'CAMERA校正點確認'
        #},
        #'camera_job': {...
        #},
        #'top_camera_CL': ['ADLink', 101, '同軸光源'],
        #'camera_mode': '7:0:0',
        #'BARREL': {
            #'light': ['top_camera_ISL'],
            #'dll_name': 'circle_detection',
            #'display_text': '自裝鈑定位'
        #},
        #'top_camera_ISL': ['ADLink', 100, '積分球光源'],
        #'reverse_type': 0,
        #'camera_name': 'top_camera'
    #}
#from time import clock
#from time import sleep
#from threading import Thread
#cam = CameraModule(camera_inf)
#print(cam.get_parameter('gain_value'))
#print(cam.get_parameter('shutter_value'))
#print(cam.get_parameter('channel'))
#print(cam.get_parameter('shutter_max'))
#print(cam.set_parameter('shutter_value', 1000))
#print(cam.get_parameter('shutter_value'))
#print(cam.set_parameter('reverse_type',3))
#def run ():
    #for i in range(10):
        #s1 = clock()
        #im = cam.grab_image()
        #s2 = clock()
        #print(s2-s1)
        #sleep(0.1)
    #print(cam.close_camera())
#grab = Thread(target = run)
#grab.start()