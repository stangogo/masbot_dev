# -*- coding: utf-8 -*-

# Title          : camera.py
# Description    : camera grabber in simulation
# Author         : Henry Chang
# Date           : 20130424
# Dependency     : Channel.py 
# usage          : 
# notes          : 

import logging
from re import compile
from ctypes import *
from random import *
from time import sleep, clock
from PIL import Image
from masbot.device.channel import Channel

class Camera(Channel):    
    def __init__(self, camera_info):
        self.__owner = camera_info.get('camera_name', 'No_camera')
        super(Camera, self).__init__()
        self.__logger = logging.getLogger(__name__)  
        self.__str_length = 1024
        self.__para_set = {}
        self.__logger.debug('camera device:{0} is beginnig to initial.'.format(camera_info.get('display_text', 'No Name')))
        if camera_info.get('camera_type','') in ['1394IIDC','Directshow']:
            if camera_info.get('camera_type','') == '1394IIDC':
                self.__grabber = 1  
            elif camera_info.get('camera_type','') == 'Directshow':
                self.__grabber = 2
            else:
                self.__grabber = 0
                
            self.__para_enum = {'width':0,'height':1,'channel':2,'frame_rate':3,'reverse_type':4,'gain_value':5,
                                'gain_min':6,'gain_max':7,'shutter_value':8,'shutter_min':9,'shutter_max':10}     
            if self.__grabber:            
                self.__initial(camera_info)
            else:
                self.__logger.debug('Undefined camera device initialled error.')
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
            self.__logger.debug('camera device:{0} initialled successful.'.format(camera_info.get('display_text', 'No Name')))
        self.__logger.debug('camera device:{0} initialled fail.'.format(camera_info.get('display_text', 'No Name')))
        
    def open_framegrabber(self): 
        if self.__grabber:
            return 0
        else:
            return 1
    
    def get_parameter_values(self, cam_info):
        if cam_info.get('camera_type','') == '1394IIDC':
            self.__para_set.update({'width':1624,'height':1224,'channel':1,'frame_rate':30,'reverse_type':0,'gain_value':100,
                            'gain_min':0,'gain_max':519,'shutter_value':800,'shutter_min':0,'shutter_max':1340})  
        elif cam_info.get('camera_type','') == 'Directshow':
            self.__para_set.update({'width':640,'height':480,'channel':3,'frame_rate':15,'reverse_type':0,'gain_value':100,
                            'gain_min':0,'gain_max':519,'shutter_value':800,'shutter_min':0,'shutter_max':1340})
        else:
            self.__para_set.update({'width':1624,'height':1224,'channel':1,'frame_rate':15,'reverse_type':0,'gain_value':100,
                            'gain_min':0,'gain_max':519,'shutter_value':800,'shutter_min':0,'shutter_max':1340})        
        
        #setting parameter in advance
        self.set_parameter('reverse_type', cam_info['reverse_type'])
        self.set_parameter('gain_value', cam_info['gain_value'])
        self.set_parameter('shutter_value', cam_info['shutter_value'])
        
    def get_parameter(self, para_name):
        return self.__para_set.get(para_name, None)
        
    def set_parameter(self, para_name, value):
        if para_name in self.__para_enum.keys():            
            self.__para_set[para_name] = value
            self.__logger.debug('Camera:{0} device setting {1} successful.'.format(self.__display_text, para_name))
        return None
    
    def grab_image(self):  
        width, height, channel = [self.get_parameter('width'),self.get_parameter('height'), self.get_parameter('channel')]
        if channel == 1:
            im = Image.new('L', [width,height], randint(0, 255))
        elif channel == 3:
            im = Image.new('RGB', [width,height], (randint(0, 255),randint(0, 255),randint(0, 255)))
        sleep(1/self.get_parameter('frame_rate'))
        image_path = 'R:\\{0}_{1:.6f}.bmp'.format(self.__owner,clock())
        im.save(image_path)
        return image_path
        
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
        pass
        #ret = self.run(self.__grabber.close_grabber)
        #if ret != 0:
        #    self.__logger.warning('Camera:{0} device close grabber occurred {1} error.'.format(self.__display_text, self.get_error_msg(ret)))   
            
#-------------------------------------------------------------------------------------------------
#-----------------------------------------test----------------------------------------------------
#-------------------------------------------------------------------------------------------------
#camera_info =  {
            #'display_text': '上光源模組',
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
#from time import clock
#from time import sleep
#from threading import Thread
#cam = Camera(camera_info)
#print(cam.get_parameter('gain_value'))
#print(cam.get_parameter('shutter_value'))
#print(cam.get_parameter('channel'))
#print(cam.get_parameter('shutter_max'))
#print(cam.set_parameter('shutter_value', 1000))
#print(cam.get_parameter('shutter_value'))
#print(cam.set_parameter('reverse_type',3))
#def run ():
    #while True:
    ##for i in range(10):
        #s1 = clock()
        #im = cam.grab_image()
        #s2 = clock()
        ##im.show()        
        ##print(s2-s1)
        ##sleep(0.1)
    #print(cam.close_camera())
#grab = Thread(target = run)
#grab.start()