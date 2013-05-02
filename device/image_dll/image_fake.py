# -*- coding: utf-8 -*-

# Title          : image_fake.py
# Description    : simulation for defining functions format in the dll of image inspection
# Author         : Henry Chang
# Date           : 20130502
# Dependency     : 
# usage          : 
# notes          : 

class image_fake():
    def __init__(self, dll_name):
        self.__name = dll_name
    def initial_DLL(self, **arg):
        pass
    def run_inspection(self, **arg):
        pass
    def get_parameter_amount(self, **arg):
        pass
    def get_parameter(self, **arg):
        pass
    def get_window_size(self, **arg):
        pass
    def reset_parameter(self, **arg):
        pass
    def reset_all_parameter(self, **arg):
        pass
    def close_DLL(self, **arg):
        pass
    def get_version(self, **arg):
        pass
    def get_err_msg(self, **arg):
        pass
    
def image_dll_initial(name):
    try:
        image_dll = image_fake(name)       
        return image_dll
    except:
        return None
    
