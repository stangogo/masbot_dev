# -*- coding: utf-8 -*-

# Title          : camera_module.py
# Description    : camera module for camera actor directly
# Author         : Henry Chang
# Date           : 20130424
# Dependency     : Bulletin.py
# usage          : 
# notes          : 

import logging
from re import compile
from masbot.config.global_settings import *
from masbot.device.bulletin import Bulletin
#if hardware_simulation:
    #from masbot.device.camera.camera_fake import Camera
#else:
from masbot.device.camera.camera import Camera
    
class CameraModule(Bulletin):    
    def __init__(self, camera_info, io_cards, board={}):
        self.__owner = camera_info['camera_set']['camera_name']
        super(CameraModule, self).__init__(self.__owner, board)
        self.__logger = logging.getLogger(__name__)
        try:
            self.__camset_info = camera_info.get('camera_set',None)
            self.__job_info = camera_info.get('camera_job',None)
            self.__light_info = camera_info.get('light',None)
            self.__io_cards = io_cards
            self.__initial()              
        except:
            self.__logger.error('Gather camera module infomation error')   
                
    def __initial(self):      
        self.__camera = Camera(self.__camset_info) 
        
    def lights_switch(self, light_change):
        if isinstance(light_change[1], str) and light_change[1] == 'on':
            state = 1
        else:
            state = 0
        light_name = light_change[0]
        if light_name in self.__light_info:
            asg_io_card = self.__io_cards.get(self.__light_info[light_name]['module_type'], None)
            if asg_io_card:             
                return asg_io_card.DO(self.__light_info[light_name]['port'], state)
            else:
                msg = "{} module do not have authority to access io card.".format(self.__owner)
                self.__logger.error(msg)
                return msg                
        else:
            msg = '{} is not in {} module.'.format(light_name,self.__owner)
            self.__logger.error(msg)
            return msg     
        
    def get_parameter(self, para_name):
        return self.__camera.get_parameter(para_name)
    
    def set_parameter(self, para_name, value):
        return self.__camera.set_parameter(para_name, value)
    
    def grab_image(self):
        return self.__camera.grab_image()
        
    def close_camera(self):
        return self.__camera.close_camera()
            
