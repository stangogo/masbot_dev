# -*- coding: utf-8 -*-

# Title          : FrameGrabber_dll.py
# Description    : define functions format in the dll of image inspection
# Author         : Henry Chang
# Date           : 20130410
# Dependency     : all of FrameGrabber_dll 
# usage          : import FrameGrabber_dll
# notes          : 

from ctypes import *


# loaded shared libraries

FrameGrabber_dll = CDLL(__file__ + '/../FrameGrabber.dll')

# define the argument and return type for the functions
FrameGrabber_dll.initial_grabber.restype = c_int
FrameGrabber_dll.initial_grabber.argtypes = []

FrameGrabber_dll.grab_image.restype = c_int
FrameGrabber_dll.grab_image.argtypes = [POINTER(c_ubyte)]

FrameGrabber_dll.get_image_width.restype = c_int
FrameGrabber_dll.get_image_width.argtypes = []

FrameGrabber_dll.get_image_height.restype = c_int
FrameGrabber_dll.get_image_height.argtypes = []

FrameGrabber_dll.close_grabber.restype = c_int
FrameGrabber_dll.close_grabber.argtypes = []

FrameGrabber_dll.get_version.restype = c_char_p 
FrameGrabber_dll.get_version.argtypes = []

FrameGrabber_dll.get_err_msg.restype = c_char_p 
FrameGrabber_dll.get_err_msg.argtypes = [c_int]