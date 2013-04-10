# -*- coding: utf-8 -*-

# Title          : motor.py
# Description    : axis feature with moving, its status
# Author         : Stan Liu
# Date           : 20130321
# Dependency     : 
# usage          : 
# notes          : 

import logging
from masbot.device.bulletin import Bulletin

class Motor(Bulletin):
    def __init__(self, owner, motion, axis_list, board={}):
        self.__axis_count = len(axis_list)
        if self.__axis_count == 1:
            super(Motor, self).__init__(owner, board)
            self.__speed = axis_list[0]['speed']
            self.__acc_time = axis_list[0]['accelerative_time']
        else:
            super(Motor, self).__init__(owner, board)
            self.__speed = 50
            self.__acc_time = 0.2
        self.__logger = logging.getLogger(__name__)
        self.__axis_list = axis_list
        self.__motion = motion
        
    def get_speed(self):
        return self.__speed

    def set_speed(self, value):
        if isinstance(value, int):
            self.__speed = value
        else:
            self.__speed = 50
        
    def get_acc_time(self):
        return self.__acc_time
        
    def set_acc_time(self, value):
        if isinstance(value, (int, float)):
            self.__acc_time = value
        else:
            self.__acc_time = 0.2

    def servo_on(self):
        for axis_info in self.__axis_list:
            ret = self.__motion.servo_on_off(axis_info['axis_id'], 1)
            if ret:
                msg = "servo on error: {} {}".format(axis_info['key'], ret)
                self.__logger.critical(msg)
                return msg
            if axis_info['motor_type'] == 'servo_type':
                ret = self.__sync_pulse(axis_info)
            self.__logger.debug('%s servo on ret = %s', axis_info['key'], ret)
        return ret

    def servo_off(self):
        for axis_info in self.__axis_list:
            ret = self.__motion.servo_on_off(axis_info['axis_id'], 0)
            if ret:
                msg = "servo off error: {} {}".format(axis_info['key'], ret)
                self.__logger.critical(msg)
                return msg
            self.__logger.debug(ret)
        return ret
        
    def __sync_pulse(self, axis_info):
        ret = self.__motion.sync_pulse(axis_info)
        if ret:
            return ret
        return 0
        
    def abs_move(self, position_tuple):
        # check if parameter legal
        if len(position_tuple) != self.__axis_count:
            return 'axis count = {}'.format(self.__axis_count)
        # check if position under scope
        ret = self.__check_scope(position_tuple)
        if ret:
            return ret
        axis_list = self.__axis_list
        axis_map = []
        for index, position in enumerate(position_tuple):
            dic = {}
            dic['axis_id'] = axis_list[index]['axis_id']
            proportion = axis_list[index]['proportion']
            dic['pulse'] = proportion * position
            axis_map.append(dic)
        speed = self.__speed * proportion
        ret = self.__motion.absolute_move(
            axis_map, speed, self.__acc_time, self.__acc_time)
        if ret:
            msg = "abs move error: {}".format(ret)
            return msg
        return ret
            
    def rel_move(self, rel_position_tuple):
        # check if parameter legal
        if len(rel_position_tuple) != self.__axis_count:
            return "axis count = {}".format(self.__axis_count)
        # check if position under scope
        now_position_tuple = self.get_position()
        if len(rel_position_tuple) == 1:
            now_position_tuple = (now_position_tuple, )
        position_list = []
        for index in range(self.__axis_count):
            position_list.append(now_position_tuple[index] + rel_position_tuple[index])
        ret = self.__check_scope(position_list)
        if ret:
            return ret
        axis_list = self.__axis_list
        axis_map = []
        for index, position in enumerate(rel_position_tuple):
            dic = {}
            dic['axis_id'] = axis_list[index]['axis_id']
            proportion = axis_list[index]['proportion']
            dic['pulse'] = proportion * position
            axis_map.append(dic)
        speed = self.__speed * proportion
        ret = self.__motion.relative_move(
            axis_map, speed, self.__acc_time, self.__acc_time)
        if ret:
            msg = "rel move error: {}".format(ret)
            return msg
        return ret
        
    def __check_scope(self, position_tuple):
        # check if parameter legal
        if len(position_tuple) != self.__axis_count:
            return "axis count = {}".format(self.__axis_count)
        axis_list = self.__axis_list
        for index, position in enumerate(position_tuple):
            min = axis_list[index]['scope_min']
            max = axis_list[index]['scope_max']
            if position <= min or position >= max:
                msg = "out of scope: axis = {}, target = {}, scope between {} ~ {})".format(
                    axis_list[index]['key'], position, min, max)
                return msg
        return 0
        
    def get_pulse(self):
        pulse_list = []
        for axis_info in self.__axis_list:
            pulse = self.__motion.get_pulse(axis_info['axis_id'])
            pulse_list.append(pulse)
        if self.__axis_count == 1:
            return pulse
        else:
            return pulse_list
            
    def get_position(self):
        position_list = []
        for axis_info in self.__axis_list:
            pulse = self.__motion.get_pulse(axis_info['axis_id'])
            position = pulse / axis_info['proportion']
            position_list.append(position)
            #self.__logger.debug('%s position = %f', axis_info['key'], position)
        if self.__axis_count == 1:
            return position
        else:
            return position_list
            
    def get_motion_status(self):
        status_list = []
        for axis_info in self.__axis_list:
            stat = self.__motion.get_motion_status(axis_info['axis_id'])
            status_list.append(stat)
            self.__logger.debug('%s motion_status = %d', axis_info['key'], stat)
        if self.__axis_count == 1:
            return stat
        else:
            return status_list

    def get_io_status(self):
        status_list = []
        for axis_info in self.__axis_list:
            stat = self.__motion.get_io_status(axis_info['axis_id'])
            status_list.append(stat)
            self.__logger.debug('%s io_status = %d', axis_info['key'], stat)
        if self.__axis_count == 1:
            return stat
        else:
            return status_list
