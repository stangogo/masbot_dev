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
from masbot.config.common_lib import *
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
        if para_name in self.__para_enum.keys():
            return self.__para_set.get(para_name, None)
        elif para_name == 'camera_mode':
            return self.__camera_mode
        elif para_name == 'color_type':
            return self.__color_type
        
    def set_parameter(self, para_name, value):
        if para_name in self.__para_enum.keys():
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
        #s1 = clock()
        ret = self.run(self.__grabber.grab_image, self.__port, pData) 
        #print('%.5f'%(clock()-s1))
        if ret:
            self.__logger.warning("Camera:{} device grab image occurred error ({})".format(self.__owner, self.get_error_msg(ret)))
            return None
        else:
            return [pData, width, height, channel]
            #if channel == 1:
            #    im = Image.frombuffer('L', [width,height], pData, 'raw', 'L', 0, 1)
            #elif channel == 3:
            #    im = Image.frombuffer('RGB', [width,height], pData, 'raw', 'RGB', 0, 1)  
            #image_path = 'R:\\{0}_{1:06d}.bmp'.format(self.__owner,(int(clock()*100000)%100000))
            #im.save(image_path)
            #return image_path
        
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
            
#-------------------------------------------------------------------------------------------------
#-----------------------------------------test----------------------------------------------------
#-------------------------------------------------------------------------------------------------
#camera_info1 =  {
            #'display_text': '12',
            #'shutter_value': 800,
            #'port': 0,
            #'camera_type': '1394IIDC',
            #'pixel_size': 0.00725,
            #'reverse_type': 0,
            #'camera_name': 'top_camera',
            #'color_type': 'gray',
            #'gain_value': 100,
            #'camera_mode': '7:0:0'
        #}
#camera_info2 =  {
            #'display_text': '12',
            #'shutter_value': 800,
            #'port': 1,
            #'camera_type': '1394IIDC',
            #'pixel_size': 0.00725,
            #'reverse_type': 0,
            #'camera_name': 'under_camera',
            #'color_type': 'gray',
            #'gain_value': 100,
            #'camera_mode': '7:0:0'
        #}
#from time import clock
#from time import sleep
#from threading import Thread
#cam1 = Camera(camera_info1)
#cam2 = Camera(camera_info2)
##print(cam.get_parameter('gain_value'))
##print(cam.get_parameter('shutter_value'))
##print(cam.get_parameter('channel'))
##print(cam.get_parameter('shutter_max'))
##print(cam.set_parameter('shutter_value', 1000))
##print(cam.get_parameter('shutter_value'))
##print(cam.set_parameter('reverse_type',3))
##def run ():
    ##while True:
    ##for i in range(10):
        ##s1 = clock()
        ##im = cam.grab_image()
        ##s2 = clock()
        ##print(s2-s1)
        ##sleep(0.1)
    ##print(cam.close_camera())
##grab = Thread(target = run)
##grab.start()
#im1 = cam1.grab_image()
#im2 = cam2.grab_image()
#im1.save('D:\\im1.tif')
#im2.save('D:\\im2.tif')
#cam1.close_camera()
#cam2.close_camera()