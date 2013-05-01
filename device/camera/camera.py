# -*- coding: utf-8 -*-

# Title          : camera.py
# Description    : camera grabber for all kind of camera device(eg. 1394IIDC, directshow)
# Author         : Henry Chang
# Date           : 20130424
# Dependency     : Channel.py   camera_dll.py
# usage          : 
# notes          : 

import logging
from re import compile
from ctypes import *
from time import clock
from PIL import Image
from masbot.device.channel import Channel
from masbot.device.camera import camera_dll

class Camera(Channel):
    def __init__(self, camera_info):
        self.__owner = camera_info.get('camera_name', 'No_camera')
        super(Camera, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__str_length = 1024
        self.__para_set = {}
        #self.__logger.debug('camera device:{} is beginnig to initial.'.format(self.__owner))
        self.__grabber = camera_dll.initial_grabber(camera_info.get('camera_type',''))
        if self.__grabber:
            self.__para_enum = self.__grabber.para_enum
            self.__initial(camera_info)
        else:
            self.__logger.debug('Undefined camera device initialled error.')
        
    def __del__(self):
        self.close_camera()
    
    def __initial(self, camera_info): 
        self.__port = camera_info.get('port', -1)
        self.__camera_mode = camera_info.get('camera_mode','')
        self.__color_type = camera_info.get('color_type', 'gray')
        self.__display_text = camera_info.get('display_text', '')
        if not self.open_framegrabber():
            self.get_parameter_values(camera_info)
            self.__logger.debug('camera:{} initialled successful.'.format(self.__owner))
        else:
            self.__logger.debug('camera:{} initialled fail.'.format(self.__owner))
    def open_framegrabber(self):
        cstr = (c_char*self.__str_length)(0)
        cstr.value = self.__color_type.encode()    #set camera type in advance
        ret = self.run(self.__grabber.set_color_type, self.__port, cstr)
        if ret:
            self.__logger.warning('Camera:{} device open framegrabber fail when setting {}.'.format(self.__owner,self.__camera_mode))
            return ret
        cstr.value = self.__camera_mode.encode()    #set camera mode in advance
        ret = self.run(self.__grabber.set_camera_mode, self.__port, cstr)
        if ret:
            self.__logger.warning('Camera:{} device open framegrabber fail when setting {}.'.format(self.__owner,self.__camera_mode))
            return ret
        ret = self.run(self.__grabber.initial_grabber, self.__port)
        if ret:
            self.__logger.error('Camera:{} device open framegrabber fail when initialling grabber.'.format(self.__owner))
            return ret
        self.__logger.debug('Camera:{} device open framegrabber successful.'.format(self.__owner))
        return ret;
    
    def get_parameter_values(self, cam_info):
        value = c_int(0)
        for i, index in enumerate(self.__para_enum):
            ret = self.run(self.__grabber.get_camera_parameter, self.__port, self.__para_enum[index], pointer(value))
            if ret:
                sself.__logger.warning('Camera:{} device setting {} fail.'.format(self.__owner, index))
                self.__para_set.update(i,0)
            else:
                self.__para_set.update({index:value.value})
        #setting parameter in advance
        self.set_parameter('reverse_type', cam_info['reverse_type'])
        self.set_parameter('gain_value', cam_info['gain_value'])
        self.set_parameter('shutter_value', cam_info['shutter_value'])
        
    def get_parameter(self, para_name):
        if isinstance(para_name, str):
            if para_name in self.__para_enum.keys():
                return self.__para_set.get(para_name, None)
            elif para_name == 'camera_mode':
                return self.__camera_mode
            elif para_name == 'color_type':
                return self.__color_type
        
    def set_parameter(self, para_name, value):
        if para_name in self.__para_enum.keys() and isinstance(para_name, str) and isinstance(value, int):
            if para_name in ['gain_value','shutter_value','reverse_type']:
                ret = self.run(self.__grabber.set_camera_parameter, self.__port, self.__para_enum[para_name], value)
                if ret:
                    self.__logger.warning('Camera:{} device setting {} fail.'.format(self.__owner, para_name))
                else:
                    self.__para_set[para_name] = value
                    self.__logger.debug('Camera:{} device setting {} successful.'.format(self.__owner, para_name))
                return ret
        return None
    
    def grab_image(self):
        width, height, channel = [self.get_parameter('width'),self.get_parameter('height'), self.get_parameter('channel')]
        if not width or not height or not channel:
            return None
        pData = (c_ubyte*(width*height*channel))()
        ret = self.run(self.__grabber.grab_image, self.__port, pData) 
        if ret:
            self.__logger.warning("Camera:{} device grab image occurred error ({})".format(self.__owner, self.get_error_msg(ret)))
            return None
        else:
            return [pData, width, height, channel]
        
    def get_error_msg(self, error_type):
        cstrp = c_char_p(0)
        cstrp = self.run(self.__grabber.get_err_msg, error_type)
        cstr = cast(cstrp, c_char_p)
        pstr = cstr.value.decode()
        return pstr
    
    def get_dll_version(self, error_type):
        cstrp = c_char_p(0)
        cstrp = self.run(self.__grabber.get_version)
        cstr = cast(cstrp, c_char_p)
        pstr = cstr.value.decode()
        return pstr
        
    def close_camera(self):
        ret = self.run(self.__grabber.close_grabber, self.__port)
        if ret != 0:
            self.__logger.warning('Camera:{} device close grabber occurred error ({})'.format(self.__owner, self.get_error_msg(ret)))