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
    def __init__(self, require, points_info):
        super(MotorActor, self).__init__()
        self._state = 0
        DM = DeviceManager()
        self._motor_obj = DM.request('motor', require, points_info)
        
    def on_receive(self, message):
        # action on
        if message.get('msg') == 'state':
            message['reply_to'].set(self._state)
        elif message.get('msg') == 'servo_on':
            ret = self._motor_obj.servo_on_off(1)
        elif message.get('msg') == 'servo_off':
            ret = self._motor_obj.servo_on_off(0)        
        elif message.get('msg') == 'get_position':
            ret = self._motor_obj.get_position()
        elif message.get('msg') == 'set_speed':
            new_speed = message.get('speed')
            ret = self._motor_obj.set_speed(new_speed)
        elif message.get('msg') == 'set_acc_time':
            new_acc_time = message.get('acc_time')
            ret = self._motor_obj.set_acc_time(new_acc_time)
        elif message.get('msg') == 'abs_move':
            target_position = message.get('position')
            if isinstance(target_position, (int, float)):
                target_position = (target_position, )
            elif isinstance(target_position, list):
                target_position = tuple(target_position)
            ret = self._motor_obj.abs_move(target_position)
        elif message.get('msg') == 'rel_move':
            target_position = message.get('position')
            if isinstance(target_position, (int, float)):
                target_position = (target_position, )
            elif isinstance(target_position, list):
                target_position = tuple(target_position)
            ret = self._motor_obj.rel_move(target_position)
        elif message.get('msg') == 'pt_move':
            point_index = message.get('pt')
            ret = self._motor_obj.pt_move(point_index)
        else:
            ret = 'undefine message format'
            print(ret)
        # message response
        self._state = ret
        message['reply_to'].set(ret)
