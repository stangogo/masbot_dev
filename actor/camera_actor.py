# -*- coding: utf-8 -*-

# Title          : camera_actor.py
# Description    : handle all activity of camera 
# Author         : Henry Chang
# Date           : 20130424
# Dependency     : pykka
# usage          : 
# notes          : 

import logging
import pykka
from masbot.device.device_manager import DeviceManager

class CameraActor(pykka.ThreadingActor):
    def __init__(self, camera_info):
        """ initial the Camera as an Actor
        
        Example:
            None
            
        Args:
            camera_info(dict): camera infomation
        
        Returns:
            None

        Raises:
        
        """
        super(CameraActor, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__camera_info = camera_info
        self.__actor_name = self.__camera_info['camera_set']['camera_name']
        self.__actor_disp = self.__camera_info['camera_set']['display_text']
        self.__state = 0
        DM = DeviceManager()
        self.__camera_obj = DM.request(camera_info, 'camera_module')
        self.__disp_ctr = None
        
    def on_stop(self):
        self.__camera_obj.release_resourse()
        
    def on_receive(self, message):
        ret = None
        #print(message)
        if message.get('msg') == 'state':
            message['reply_to'].set(self.__state)
        elif message.get('msg') == 'snapshot':
            ret = self.__camera_obj.grab_image()
        elif message.get('msg') == 'inspect':
            target_job = message.get('job_name')
            rets = self.__camera_obj.inspection(target_job)
        elif message.get('msg') == 'light_on':
            ret = self.__camera_obj.lights_switch(message.get('light_name'), 1)
        elif message.get('msg') == 'light_off':
            ret = self.__camera_obj.lights_switch(message.get('light_name'), 0)
        elif message.get('msg') == 'job_assign':
            target_job = message.get('job_name')
            if target_job:
                if message.get('dll_name'):
                    ret = self.__camera_obj.assign_dll(target_job, message.get('dll_name'))
                elif message.get('light'):
                    pass
            else:
                ret = 'target job is undefined'
                self.__logger.warning(ret)         
        else:
            ret = 'undefine message format'
            self.__logger.error(ret)
        self.__state = 'idle'
        message['reply_to'].set(ret)