# -*- coding: utf-8 -*-

# Title          : camera_module.py
# Description    : camera module for camera actor directly
# Author         : Henry Chang
# Date           : 20130424
# Dependency     : Bulletin.py
# usage          : 
# notes          : 

import logging
from ctypes import *
from masbot.config.global_settings import *
from masbot.device.bulletin import Bulletin
from masbot.device.image_dll_handler import ImgDLLHandler
if hardware_simulation.get('camera', True):
    from masbot.device.camera.camera_fake import Camera
else:
    from masbot.device.camera.camera import Camera
    
class CameraModule(Bulletin):    
    def __init__(self, camera_info, io_cards , display_ctr, board={}):
        self.__owner = camera_info['camera_set']['camera_name']
        self.__disp_text = camera_info['camera_set']['display_text']
        super(CameraModule, self).__init__(self.__owner, board)
        self.__logger = logging.getLogger(__name__)
        try:
            self.__camset_info = camera_info.get('camera_set',None)
            self.__job_info = camera_info.get('camera_job',None)
            self.__light_info = camera_info.get('light',None)
            self.__io_cards = io_cards
            self.__disp_ctr = display_ctr
            self.__imghandler = ImgDLLHandler()
            self.__initial()
        except:
            self.__logger.error('Gather camera module infomation error')
            
    def __initial(self):
        self.__camera = Camera(self.__camset_info)
        for job, value in self.__job_info.items():
            self.assign_dll(job, value.get('dll_name'))
        
    def assign_dll(self, job_name, dll_name):
        if not isinstance(job_name, str) or not isinstance(dll_name, str):
            msg = 'send wrong type to  assign dll function'
            self.__logger.warning(msg)
            return msg
        job = self.__job_info.get(job_name, None)
        if job:
            handler = job.get('handler', None)
            if handler:
                if dll_name == job.get('dll_name', None):
                    self.__logger.debug('assign the dame image dll')
                    return 0
                ret = self.render_back_dll(job_name, handler)
            handler = self.__imghandler.assign_dll(job_name, dll_name)
            if handler:
                job.update({'handler': handler})
                self.__job_info.update({job_name:job})
            else:
                msg = 'assign image dll {} to {} job fail'.format(dll_name, job_name)
                self.__logger.warning(msg)
                return msg
        else:
            msg = 'find no job:{}'.format(job_name)
            self.__logger.warning(msg)
            return msg
    
    def render_back_dll(self, job_name, handler):
        return self.__imghandler.render_back_dll(job_name, handler)
    
    def lights_switch(self, light_name, state):
        if self.__io_cards:
            if light_name in self.__light_info:
                asg_io_card = self.__io_cards.get(self.__light_info[light_name]['module_type'], None)
                if asg_io_card:
                    return asg_io_card.DO(self.__light_info[light_name]['port'], state)
                else:
                    msg = "{} module do not have authority to access io card.".format(self.__owner)
                    self.__logger.error(msg)
                    return msg
            else:
                msg = '{} is not in {} module.'.format(light_name,self.__owner)
                self.__logger.error(msg)
                return msg
    
    def get_parameter(self, para_name):
        return self.__camera.get_parameter(para_name)
    
    def set_parameter(self, para_name, value):
        return self.__camera.set_parameter(para_name, value)
    
    def grab_image(self):
        return self.__camera.grab_image()
        
    def release_resourse(self):
        for job, value in self.__job_info.items():
            self.render_back_dll(job, value.get('handler'))
        self.close_camera()
        
    def close_camera(self):
        return self.__camera.close_camera()
            
    def inspection(self, job_name, turn_light = 1):
        if job_name in self.__job_info:
            msg = None
            if turn_light:
                for light in self.__job_info[job_name]['light']:
                    ret = self.lights_switch(light, 1)
            rawimage = self.grab_image()
            if rawimage:
                dllhandler = self.__job_info[job_name]['handler']
                if dllhandler:
                    result = (c_char*1024)()
                    infoimage = (c_char*1024)()
                    ret = dllhandler.run_inspection(rawimage[0], rawimage[1], rawimage[2], result, infoimage)
                    if not ret:
                        self.__disp_ctr.display_image(self.__owner, self.__disp_text, infoimage.value.decode())
                        msg = result.value.decode()
                    else:
                        msg = '{}.dll returns error message. ({})'.format(get_dll_error_msg(ret))
                        self.__logger.warning(msg)
                else:
                    msg = 'Job {} got dll hander fail when inspecting.'.format(job_name)
                    self.__logger.warning(msg)
            else:
                msg = 'Job {} grabbed image fail when inspecting.'.format(job_name)
                self.__logger.warning(msg)
            if turn_light:
                for light in self.__job_info[job_name]['light']:
                    ret = self.lights_switch(light, 0)
        else:
            msg = 'Job ({}) is not in {} module.'.format(job_name,self.__owner)
            self.__logger.error(msg)
        return msg
    
    def get_dll_error_msg(self, job_name, error_type):
        cstrp = c_char_p(0)
        cstrp = self.__job_info[job_name]['handler'].get_err_msg
        cstr = cast(cstrp, c_char_p)
        pstr = cstr.value.decode()
        return pstr
'''
##################### Test ###################
'''
#cam_info = {
    #'light': {
        #'top_ball_light': {
            #'module_type': '8158',
            #'port': 91,
            #'display_text': 'Á©çÂÉÂÊ∫
        #},
        #'top_coaxial_light': {
            #'module_type': '8158',
            #'port': 92,
            #'display_text': 'åËª∏âÊ'
        #},
        #'top_ring_light': {
            #'module_type': '8158',
            #'port': 93,
            #'display_text': '∞ÂΩ¢âÊ'
        #}
    #},
    #'camera_set': {
        #'shutter_value': 800,
        #'color_type': 'gray',
        #'camera_name': 'top_camera',
        #'display_text': '‰∏äÂÊ∫êÊ®°Áµ,
        #'reverse_type': 3,
        #'pixel_size': 0.00725,
        #'camera_type': '1394IIDC',
        #'port': 0,
        #'camera_mode': '7:0:0',
        #'gain_value': 100
    #},
    #'camera_job': {
        #'CAMERA_CHECK': {
            #'light': ['top_ball_light'],
            #'display_text': 'êÂÊ™¢Êü•',
            #'dll_name': 'camera_check'
        #},
        #'BARREL': {
            #'light': ['top_ball_light'],
            #'display_text': '™ËëÂ‰Ω,
            #'dll_name': 'camera_check'
        #},
        #'IPQC': {
            #'light': ['top_ring_light'],
            #'display_text': 'êÂÊ™¢Êü•',
        #'dll_name': 'IPI_9552A1'
        #}
    #}
#}

#cam = CameraModule(cam_info,None)
#ret = cam.inspection('BARREL', 0)
#print(ret)