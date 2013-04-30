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
#    from masbot.device.camera.camera_fake import Camera
#else:
from masbot.device.camera.camera import Camera
    
class CameraModule(Bulletin):    
    def __init__(self, camera_info, board={}):
        owner = camera_info['camera_set']['camera_name']
        super(CameraModule, self).__init__(owner, board)
        self.__logger = logging.getLogger(__name__)    
        self.__cam_info = camera_info
        #self.__io_card = io_card
        self.__initial()  
        
    #def __del__(self): 
        
    def __initial(self):      
        self.__camera = Camera(self.__cam_info.get('camera_set'))      
        
    def get_parameter(self, para_name):
        return self.__camera.get_parameter(para_name)
    
    def set_parameter(self, para_name, value):
        return self.__camera.set_parameter(para_name, value)
    
    def grab_image(self):
        return self.__camera.grab_image()
        
    def close_camera(self):
        return self.__camera.close_camera()
            
#-------------------------------------------------------------------------------------------------
#-----------------------------------------test----------------------------------------------------
#-------------------------------------------------------------------------------------------------
#camera_inf =  {
        #'camera_set': {
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
        #},
        #'camera_job': {
            #'CAMERA_CHECK': {
                #'display_text': '成品檢查',
                #'dll_name': 'camera_check',
                #'light': ['top_camera_ISL']
            #},
            #'IPQC': {
                #'display_text': '成品檢查',
                #'dll_name': 'IPI_9552A1',
                #'light': ['top_camera_ISL']
            #},
            #'BARREL': {
                #'display_text': '自裝鈑定位',
                #'dll_name': 'camera_check',
                #'light': ['top_camera_ISL', 'top_camera_RL']
            #}
        #},
        #'light': {
            #'top_camera_RL': ['ADLink', 102, '環形光源'],
            #'top_camera_ISL': ['ADLink', 100, '積分球光源'],
            #'top_camera_CL': ['ADLink', 101, '同軸光源']
        #}
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
