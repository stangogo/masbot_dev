# -*- coding: utf-8 -*-

# Title          : image_module.py
# Description    : determining what camera and image dll with image module and calculating result(IPQC, fix position etc.) for masbot
# Author         : Henry Chang
# Date           : 20130410
# Dependency     : image_dll.py framegrabber_dll.py
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


    















#image_dll = image_dll_initial('CAMERA_CHECK')
#ret = c_int(0)
#ret = image_dll.initial_DLL()
#if ret!=0:
    #print('DLL initial fail')
    
#ret = FrameGrabber_dll.initial_grabber()
#if ret!=0:
    #print('Camera initial fail')   

#a = image_dll.get_version()
#print(a.decode())
#a = FrameGrabber_dll.get_version()
#print(a.decode())

#s1 = clock()
#pRawData = (c_ubyte*(FrameGrabber_dll.get_image_width()*FrameGrabber_dll.get_image_height()))()
#result = create_string_buffer(1024)
#infopath = create_string_buffer(1024)
#s2 = clock()
#print(s2-s1)
#start = clock()

#win_width = pointer(c_int(0))
#win_height = pointer(c_int(0))
#ret = image_dll.get_window_size(win_width, win_height)
#print(win_width[0])
#print(win_height[0])

#for i in range(1):    
    #s1 = clock()
    #ret = FrameGrabber_dll.grab_image(pRawData)
    #s2 = clock()
    #print(s2-s1)
    
    #s1 = clock()
    #im = Image.frombuffer('L', [FrameGrabber_dll.get_image_width(),FrameGrabber_dll.get_image_height()], pData, 'raw', 'L',0,1)
    #s2 = clock()
    #print(s2-s1)
    #im.save('R:\\python_saved.tif')
    
    #if ret!=0:
        #print('Grab fail')  
    #print(ret)
    
    #s1 = clock()
    #ret = image_dll.run_inspection(pRawData, FrameGrabber_dll.get_image_width(), FrameGrabber_dll.get_image_height(), result, infopath)
    #s2 = clock()
    #print(s2-s1)
    #end = clock()
    #print(end-start)
    #print(result.value.decode())
    #print(infopath.value.decode())
    #print(ret)

#if ret == 0:
    #infoimg = Image.open(infopath.value.decode())
    #infoimg.show()    
    
#del(infopath)
#del(pRawData)
#del(result)

