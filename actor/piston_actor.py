# -*- coding: utf-8 -*-

# Title          : piston_actor.py
# Description    : piston actor with action and detecting status
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : pykka
# usage          : 
# notes          : 

import pykka
from masbot.device.device_manager import DeviceManager

class PistonActor(pykka.ThreadingActor):
    def __init__(self, module_info):
        """ initial the Piston as an Actor
        
        Example:
            None
            
        Args:
            module_info(dict): resource infomation includes all DOs and DIs
        
        Returns:
            None

        Raises:
        
        """
        super(PistonActor, self).__init__()
        self.__state = 'ready'
        DM = DeviceManager()
        self.__piston_obj = DM.request('piston', module_info)
        
    def on_receive(self, message):
        # action on
        if message.get('msg') == 'state':
            message['reply_to'].set(self.__state)
        elif message.get('msg') == 'action_on':
            self.__state = 'actioning'
            ret = self.__piston_obj.action(1)
        # action off
        elif message.get('msg') == 'action_off':
            self.__state = 'actioning'
            ret = self.__piston_obj.action(0)
        # sensor status
        elif message.get('msg') == 'sensor_status':
            ret = self.__piston_obj.get_di_status()
        # action status
        elif message.get('msg') == 'action_status':
            ret = self.__piston_obj.get_do_status()
        else:
            ret = 'undefine message format'
            print(msg)
        # message response
        message['reply_to'].set(ret)

