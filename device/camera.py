# -*- coding: utf-8 -*-

# Title          : camera.py
# Description    : camera handler 
# Author         : Henry Chang
# Date           : 20130419
# Dependency     : 
# usage          : 
# notes          : 

import logging
from re import compile
from PIL import Image
from masbot.device.bulletin import Bulletin
from masbot.device.Framegrabber_dll import Framegrabber_dll

class Camera(Bulletin):
    def __init__(self, camera_info, board={}):
        #super(Piston, self).__init__(module_info['key'], board)
        self.__logger = logging.getLogger(__name__)
        self.__camera_info = camera_info
    
    def __initial_camera(self):
        output_pattern = compile('^output[0-9]$')
        input_pattern = compile('^input[0-9]$')
        self.__do_list = []
        self.__di_list = []
        for key, val in self.__module_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                self.__do_list.append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                self.__di_list.append(val)

    
        