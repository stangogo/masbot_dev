# -*- coding: utf-8 -*-

# Title          : piston_actor.py
# Description    : piston actor with action and detecting status
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : pykka
# usage          : 
# notes          : 

import logging
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
        self.__logger = logging.getLogger(__name__)
        self.__state = 'ready'
        DM = DeviceManager()
        self.__piston_obj = DM.request(module_info['key'], 'piston', module_info)
        
    def on_receive(self, message):
        # action on
        msg = message.get('msg')
        if msg == 'state':
            message['reply_to'].set(self.__state)
        elif msg == 'action_on':
            self.__state = 'actioning'
            ret = self.__piston_obj.action(1)
        # action off
        elif msg == 'action_off':
            self.__state = 'actioning'
            ret = self.__piston_obj.action(0)
        # sensor status
        elif msg == 'sensor_status':
            ret = self.__piston_obj.get_di_status()
        # action status
        elif msg == 'action_status':
            ret = self.__piston_obj.get_do_status()
        elif msg == 'declare':
            who = message.get('who')
            action = message.get('action')
            ret = self.__piston_obj.declare(who, action)
        elif msg == 'wipe':
            who = message.get('who')
            ret = self.__piston_obj.wipe(who)
        elif msg == 'board_info':
            ret = self.__piston_obj.board_info()
        else:
            ret = 'undefine message format'
            self.__logger.debug(ret)
        # message response
        message['reply_to'].set(ret)

