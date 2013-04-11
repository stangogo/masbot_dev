# -*- coding: utf-8 -*-

# Title          : image_dll.py
# Description    : define functions format in the dll of image inspection
# Author         : Henry Chang
# Date           : 20130409
# Dependency     : all of image dll 
# usage          : import image_dll
# notes          : 

from ctypes import *


def image_dll_initial(name):
    try:
        image_dll = CDLL(__file__ + '/../dll_pool/{}.dll'.format(name))
        
        # define the argument and return type for the functions
        image_dll.initial_DLL.restype = c_int
        image_dll.initial_DLL.argtypes = []
        
        image_dll.run_inspection.restype = c_int
        image_dll.run_inspection.argtypes = [POINTER(c_ubyte), c_int, c_int, POINTER(c_char), POINTER(c_char)]
        
        image_dll.get_parameter_amount.restype = c_int
        image_dll.get_parameter_amount.argtypes = [POINTER(c_int)]
        
        image_dll.set_parameter.restype = c_int
        image_dll.set_parameter.argtypes = [c_int, c_double]
        
        image_dll.get_parameter.restype = c_int
        image_dll.get_parameter.argtypes = [c_int, POINTER(c_double)]
        
        image_dll.set_window_size.restype = c_int
        image_dll.set_window_size.argtypes = [c_int, c_int]
        
        image_dll.get_window_size.restype = c_int
        image_dll.get_window_size.argtypes = [POINTER(c_int), POINTER(c_int)]
        
        image_dll.reset_parameter.restype = c_int
        image_dll.reset_parameter.argtypes = [c_int]
        
        image_dll.reset_all_parameter.restype = c_int
        image_dll.reset_all_parameter.argtypes = []
        
        image_dll.close_DLL.restype = c_int
        image_dll.close_DLL.argtypes = []
        
        image_dll.get_version.restype = c_char_p 
        image_dll.get_version.argtypes = []
        
        image_dll.get_err_msg.restype = c_char_p 
        image_dll.get_err_msg.argtypes = [c_int]  
        
        return image_dll
    except:
        return None
