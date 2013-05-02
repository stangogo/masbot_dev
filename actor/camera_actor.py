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
        self.__state = 0
        DM = DeviceManager()
        self.__camera_obj = DM.request(camera_info, 'camera_module')
        
    def on_stop(self):
        self.__camera_obj.close_camera()
        
    def on_receive(self, message):
        ret = None
        msg = message.get('msg')
        if isinstance(msg, str):
            if message.get('msg') == 'state':
                message['reply_to'].set(self.__state)
            elif message.get('msg') == 'snapshot':
                self.__state = 'grabbing'
                ret = self.__camera_obj.grab_image()
            else:
                ret = 'undefine message format'
                self.__logger.error(ret)
        elif isinstance(msg, list):
            self.__logger.debug('recieve msg:', msg)
            if msg != [] and len(msg) == 2:
                if msg[0] in self.__camera_info['light']:
                    self.__camera_obj.lights_switch(msg)
        elif isinstance(msg, dict):
            pass
        else:
            ret = 'undefine message format'
            self.__logger.error(ret)       
        self.__state = 'ready'
        message['reply_to'].set(ret)

