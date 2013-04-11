# -*- coding: utf-8 -*-

# Title          : camera_handler.py
# Description    : detect all camera device and service grabber
# Author         : Henry Chang
# Date           : 20130411
# Dependency     : image_module.py framegrabber_dll.py
# usage          : 
# notes          : 

import logging
from os import *
from time import sleep
from masbot.device.camera import *
from masbot.device.image_dll import image_dll_handler


class ImageHandler:
    def __init__(self, name):        
        self.__logger = logging.getLogger(__name__)
        self.name = name
        self.__dll_handler = None # store dll's name and handler
        self.__grab_handler = None # store camera's name and handler
        
    def _assign_dll(self, dll_name):
        #dllpath = __file__+ '/..\\image_dll\\dll_pool\\'
        #alldll = []
        #for filename in listdir(dllpath):
            #if filename.find('.dll') != -1:
                #name = filename.split('.')
                #alldll.insert(-1, name[0])     
        
        #self.__logger.info('found dll list:'+ str(alldll))
        #for filename in alldll:
        self.__dll_handler = image_dll_initial(dll_name)           
        if self.__dll_handler != None:
            ret = self.__dll_handler.initial_DLL()
            if ret == 0:
                self.__logger.info("image handler '{0}' assigned {1}.dll success".format(self.name, dll_name)) 
            else:
                self.__dll_handler.close_DLL()    
                self.__logger.info("image handler '{0}' assigned {1}.dll fail".format(self.name, dll_name)) 
        else: 
            self.__logger.info("image handler '{0}' assigned {1}.dll fail".format(self.name, dll_name)) 
                
    def _assign_camera(self):
        ret = FrameGrabber_dll.initial_grabber()
        if ret:
            self.__logger.warning('initial camera fail')    
            
    def __exit__(self):
        self.close()    
        
    def _insert_job(self, job):
        self.__job_table.update(job)
        
    def _print(self):
        print(self.__job_table)
