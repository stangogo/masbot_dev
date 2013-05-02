# -*- coding: utf-8 -*-

# Title          : image_dll_handler.py
# Description    : The image dll handler is the controller of all the camera job register
# Author         : Henry Chang
# Date           : 20130411
# Dependency     : image_dll.py
# usage          : 
# notes          : 

import logging
from os import listdir
from masbot.config.global_settings import *
if hardware_simulation.get('image_dll', True):
    from masbot.device.image_dll.image_fake import image_dll_initial
else:
    from masbot.device.image_dll.image_dll import image_dll_initial
    
class ImgDLLHandler(object):
    _instance = None
    _initialled = False
    # singleton: to guarantee there is only one instance
    def __new__(cls):
        if not ImgDLLHandler._instance:
            ImgDLLHandler._instance = object.__new__(cls)
        return ImgDLLHandler._instance
    
    def __init__(self):
        if not self._initialled:
            self.__initial()
            self._initialled = True
        
    def __initial(self):
        self.__logger = logging.getLogger(__name__)
        self.__dll_handler = {} # store dll's name and handler
        self.find_dlls()
        
    def find_dlls(self):
        dllpath = __file__+ '/../image_dll/dll_pool/'
        alldll = []
        for filename in listdir(dllpath):
            if filename.find('.dll') != -1:
                name = filename.split('.')
                alldll.insert(-1, name[0])
        self.__logger.debug('found dll list:'+ str(alldll))
        for filename in alldll:
            tmp_handler = self.connect_dll(filename)
            if tmp_handler:
                self.__dll_handler.update({filename:[]})
                tmp_handler.close_DLL()
                self.__logger.debug("Registered {0}.dll successful".format(filename))
            else:
                self.__logger.warning("Registered {0}.dll fail".format(filename))

    def __exit__(self):
        self.close()
        
    def get_dll_list(self):
        return list(self.__dll_handler.keys())
    
    def get_dll_connected(self, dllname):
        return self.__dll_handler.get(dllname)
    
    def connect_dll(self, dllname):
        ret_handler = image_dll_initial(dllname)
        if ret_handler:
            ret = ret_handler.initial_DLL()
            if ret:
                ret_handler.close_DLL()
                ret_handler = None
                self.__logger.warning("Connected {0}.dll fail".format(dllname))
        else: 
            elf.__logger.warning("Connected {0}.dll fail".format(dllname))
        return ret_handler
        
    def disconnect_dll(self, dllhandler, workname = None):
        ret = 0
        if workname:
            for dll, jobs in self.__dll_handler.items():
                if workname in jobs:
                    jobs.remove(workname)
                    self.__dll_handler.update({dll:jobs})
                    break
        try:
            ret = dllhandler.close_DLL()
        except:
            ret = 1
        return ret
    
    def assign_dll(self, workname, dllname):
        ret_handler = None
        Jobs_asg = self.__dll_handler.get(dllname, None)
        if Jobs_asg != None:
            ret_handler = self.connect_dll(dllname)
            Jobs_asg.append(workname)
            self.__dll_handler.update({dllname:Jobs_asg})
            self.__logger.debug("{0} job  got {1}.dll handler successful".format(workname,dllname)) 
        else:
            self.__logger.warning("{0}.dll was not found from image dll handler".format(dllname))
        return ret_handler
    
    def render_back_dll(self, workname, dllhandler):
        if dllhandler:
            return self.disconnect_dll(dllhandler, workname)
'''
########################  Test   ###########################
'''
#a = ImgDLLHandler()
#b = ImgDLLHandler()
#print(a, b)
#print(a.get_dll_list())
#handler = a.assign_dll('camera','camera_check')
#print(a.get_dll_connected('camera_check'))
#a.disconnect_dll(handler, 'camera')
#print(a.get_dll_connected('camera_check'))
