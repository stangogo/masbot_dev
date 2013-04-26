# -*- coding: utf-8 -*-

# Title          : camera1394IIDC_dll.py
# Description    : A camera connector between python and camera dll
# Author         : Henry Chang
# Date           : 20130424
# Dependency     : all kind of Camera device handler 
# usage          : 
# notes          : 

from ctypes import *

def initial_grabber(camera_type):        
    # loaded camera device library by different camera type    
    
    if camera_type == '1394IIDC':
        grabber = CDLL(__file__+'/../camera1394IIDC.dll')
        
    elif camera_type == 'Directshow':
        grabber = CDLL(__file__+'/../cameraDirectshow.dll')
    else:
        grabber = None
    # define the argument and return type for the functions  
    
    if grabber:
        grabber.initial_dll.restype = None
        grabber.initial_dll.argtypes = []    
        grabber.initial_dll()

        grabber.initial_grabber.restype = c_int
        grabber.initial_grabber.argtypes = [c_int]
        
        grabber.grab_image.restype = c_int
        grabber.grab_image.argtypes = [c_int, POINTER(c_ubyte)]
        
        grabber.set_camera_parameter.restype = c_int
        grabber.set_camera_parameter.argtypes = [c_int, c_int, c_int]
        
        grabber.get_camera_parameter.restype = c_int
        grabber.get_camera_parameter.argtypes = [c_int, c_int, POINTER(c_int)]
        
        grabber.set_color_type.restype = c_int
        grabber.set_color_type.argtypes = [c_int, POINTER(c_char)]
        
        grabber.get_color_type.restype = c_int
        grabber.get_color_type.argtypes = [c_int, POINTER(c_char)]
        
        grabber.set_camera_mode.restype = c_int
        grabber.set_camera_mode.argtypes = [c_int, POINTER(c_char)]
        
        grabber.get_camera_mode.restype = c_int
        grabber.get_camera_mode.argtypes = [c_int, POINTER(c_char)]
        
        grabber.get_available_camera.restype = c_int
        grabber.get_available_camera.argtypes = []            

        grabber.close_grabber.restype = c_int
        grabber.close_grabber.argtypes = [c_int]
        
        grabber.get_version.restype = POINTER(c_char) 
        grabber.get_version.argtypes = []
        
        grabber.get_err_msg.restype = POINTER(c_char) 
        grabber.get_err_msg.argtypes = [c_int]
        
        
        #para_enum = common_lib.enum('width','height','channel','frame_rate','reverse_type','gain_value',
                                             #'gain_min','gain_max','shutter_value','shutter_min','shutter_max')
        grabber.para_enum = {'width':0,'height':1,'channel':2,'frame_rate':3,'reverse_type':4,'gain_value':5,
                            'gain_min':6,'gain_max':7,'shutter_value':8,'shutter_min':9,'shutter_max':10}         
    
    return grabber