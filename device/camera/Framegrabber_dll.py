# -*- coding: utf-8 -*-

# Title          : FrameGrabber_dll.py
# Description    : define functions format in the dll of image inspection
# Author         : Henry Chang
# Date           : 20130418
# Dependency     : all of FrameGrabber_dll 
# usage          : import FrameGrabber_dll
# notes          : 

from ctypes import *


# loaded shared libraries
Framegrabber_dll = CDLL(__file__+'/../Framegrabber.dll')

# define the argument and return type for the functions  

Framegrabber_dll.initial_dll.restype = None
Framegrabber_dll.initial_dll.argtypes = []

Framegrabber_dll.initial_grabber.restype = c_int
Framegrabber_dll.initial_grabber.argtypes = [c_int]

Framegrabber_dll.grab_image.restype = c_int
Framegrabber_dll.grab_image.argtypes = [c_int, POINTER(c_ubyte)]

Framegrabber_dll.set_camera_parameter.restype = c_int
Framegrabber_dll.set_camera_parameter.argtypes = [c_int, c_int, c_int]

Framegrabber_dll.get_camera_parameter.restype = c_int
Framegrabber_dll.get_camera_parameter.argtypes = [c_int, c_int, POINTER(c_int)]

Framegrabber_dll.set_camera_color_type.restype = c_int
Framegrabber_dll.set_camera_color_type.argtypes = [c_int, POINTER(c_char)]

Framegrabber_dll.get_camera_color_type.restype = c_int
Framegrabber_dll.get_camera_color_type.argtypes = [c_int, POINTER(c_char)]

Framegrabber_dll.set_camera_mode.restype = c_int
Framegrabber_dll.set_camera_mode.argtypes = [c_int, POINTER(c_char)]

Framegrabber_dll.get_camera_mode.restype = c_int
Framegrabber_dll.get_camera_mode.argtypes = [c_int, POINTER(c_char)]

Framegrabber_dll.set_camera_type.restype = c_int
Framegrabber_dll.set_camera_type.argtypes = [c_int, POINTER(c_char)]

Framegrabber_dll.get_camera_type.restype = c_int
Framegrabber_dll.get_camera_type.argtypes = [c_int, POINTER(c_char)]

Framegrabber_dll.get_camera_count.restype = c_int
Framegrabber_dll.get_camera_count.argtypes = []

Framegrabber_dll.close_grabber.restype = c_int
Framegrabber_dll.close_grabber.argtypes = [c_int]

Framegrabber_dll.get_version.restype = POINTER(c_char) 
Framegrabber_dll.get_version.argtypes = []

Framegrabber_dll.get_err_msg.restype = POINTER(c_char) 
Framegrabber_dll.get_err_msg.argtypes = [c_int]
