# -*- coding: utf-8 -*-

# Title          : motor_actor.py
# Description    : motor features
#                  - absolute move
#                  - relative move
#                  - point move
#                  - get axis status
# Author         : Stan Liu
# Date           : 20130321
# Dependency     : pykka
# usage          : 
# notes          : 

import logging
import pykka
from masbot.device.device_manager import DeviceManager

class MotorActor(pykka.ThreadingActor):
    def __init__(self, motor_info):
        """ initial the Motor as an Actor
        
        Example:
            None
            
        Args:
            motor_info(dict): motor infomation
        
        Returns:
            None

        Raises:
        
        """
        super(MotorActor, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__points_info = motor_info['points_info']
        self.__state = 0
        DM = DeviceManager()
        self.__motor_obj = DM.request(motor_info, 'motor')
        
    def on_receive(self, message):
        # action on
        msg = message.get('msg')
        if msg == 'state':
            message['reply_to'].set(self.__state)
        elif msg == 'servo_on':
            ret = self.__motor_obj.servo_on()
        elif msg == 'servo_off':
            ret = self.__motor_obj.servo_off()
        elif msg == 'get_position':
            ret = self.__motor_obj.get_position()
        elif msg == 'get_status':
            ret = self.__motor_obj.get_motion_status()
        elif msg == 'get_speed':
            ret = self.__motor_obj.get_speed()
        elif msg == 'set_speed':
            new_speed = message.get('speed')
            ret = self.__motor_obj.set_speed(new_speed)
        elif msg == 'get_acc_time':
            ret = self.__motor_obj.get_acc_time()
        elif msg == 'set_acc_time':
            new_acc_time = message.get('acc_time')
            ret = self.__motor_obj.set_acc_time(new_acc_time)
        elif msg == 'abs_move':
            target_position = message.get('position')
            ret = self.__motor_obj.abs_move(target_position)
        elif msg == 'rel_move':
            rel_position = message.get('position')
            ret = self.__motor_obj.rel_move(rel_position)
        elif msg == 'pt_move':
            pt_name = message.get('pt')
            ret = self.pt_move(pt_name)
        elif msg == 'reset':
            ret = self.__motor_obj.reset_step()
        else:
            ret = 'undefine message format'
            self.__logger.error(ret)
        # message response
        self.__state = ret
        message['reply_to'].set(ret)

    def pt_move(self, pt_name):
        if pt_name not in self.__points_info:
            msg = 'undefine point name: {}'.format(pt_name)
            self.__logger.error(msg)
            return msg
        target_position = self.__points_info[pt_name]
        target_position = tuple(target_position)
        return self.__motor_obj.abs_move(target_position)
