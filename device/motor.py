# -*- coding: utf-8 -*-

# Title          : motor.py
# Description    : axis feature with moving, its status
# Author         : Stan Liu
# Date           : 20130321
# Dependency     : 
# usage          : 
# notes          : 

import logging
from time import sleep
from masbot.device.bulletin import Bulletin

class Motor(Bulletin):
    def __init__(self, motor_info, motion, board={}):
        owner = motor_info['key']
        super(Motor, self).__init__(owner, board)
        self.__speed = motor_info['speed']
        self.__acc_time = motor_info['speed']
        self.__logger = logging.getLogger(__name__)
        self.__axis_list = motor_info['axis_info']
        self.__axis_count = len(motor_info['axis_info'])
        self.__motion = motion
        self.__timeout = 5000
        
    def get_speed(self):
        return self.__speed

    def set_speed(self, value):
        if isinstance(value, int):
            self.__speed = value
        else:
            self.__speed = 50
        
    def get_timeout(self):
        return self.__timeout

    def set_timeout(self, value):
        if isinstance(value, int):
            self.__timeout = value
        else:
            self.__timeout = 5000
            
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
            if axis_info['motor_type'] == 'servo':
                ret = self.__sync_pulse(axis_info)
                if ret:
                    msg = "sync pulse error: {} {}".format(axis_info['key'], ret)
                    self.__logger.error(msg)
            electric_brake = axis_info['electric_brake']
            if electric_brake and electric_brake >= 0:
                self.__motion.DO(axis_info['electric_brake'], 1)
            self.__logger.debug('%s servo on ret = %s', axis_info['key'], ret)
        return ret

    def servo_off(self):
        for axis_info in self.__axis_list:
            electric_brake = axis_info['electric_brake']
            if electric_brake and axis_info['electric_brake'] >= 0:
                self.__motion.DO(axis_info['electric_brake'], 0)
            ret = self.__motion.servo_on_off(axis_info['axis_id'], 0)
            if ret:
                msg = "servo off error: {} {}".format(axis_info['key'], ret)
                self.__logger.critical(msg)
                return msg
            self.__logger.debug("%s servo off sucessfully", axis_info['key'])
        return ret
        
    def __sync_pulse(self, axis_info):
        ret = self.__motion.sync_pulse(axis_info)
        if ret:
            return ret
        return 0
        
    def abs_move(self, position_tuple):
        # check if parameter format legal
        if isinstance(position_tuple, (int, float)):
            position_tuple = (position_tuple, )
        elif isinstance(position_tuple, list):
            position_tuple = tuple(position_tuple)
        if len(position_tuple) != self.__axis_count:
            return 'axis count = {}'.format(self.__axis_count)
        # check if position under scope
        ret = self.__check_scope(position_tuple)
        if ret:
            self.__logger.debug(ret)
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
            axis_map, speed, self.__timeout, self.__acc_time, self.__acc_time)
        if ret:
            msg = "abs move error: {}".format(ret)
            self.__logger.debug(msg)
            return msg
        return ret
            
    def rel_move(self, rel_position_tuple):
        # check if parameter format legal
        if isinstance(rel_position_tuple, (int, float)):
            rel_position_tuple = (rel_position_tuple, )
        elif isinstance(rel_position_tuple, list):
            rel_position_tuple = tuple(rel_position_tuple)
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
            self.__logger.debug(ret)
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
            axis_map, speed, self.__timeout, self.__acc_time, self.__acc_time)
        if ret:
            msg = "rel move error: {}".format(ret)
            self.__logger.debug(msg)
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
        if self.__axis_count == 1:
            return position
        else:
            return position_list
            
    def get_motion_status(self):
        status_list = []
        for axis_info in self.__axis_list:
            stat = self.__motion.get_motion_status(axis_info['axis_id'])
            status_list.append(stat)
        if self.__axis_count == 1:
            return stat
        else:
            return status_list

    def get_io_status(self):
        status_list = []
        for axis_info in self.__axis_list:
            stat = self.__motion.get_io_status(axis_info['axis_id'])
            status_list.append(stat)
        if self.__axis_count == 1:
            return stat
        else:
            return status_list

    def reset_step(self, timeout=5000, interval=20):
        axis_count = len(self.__axis_list)
        if axis_count != 1:
            msg = "axis count of motor is limited to 1, current = {}".format(axis_count)
            self.__logger.critical(msg)
            return msg
        motor_type = self.__axis_list[0]['motor_type']
        if  motor_type == 'servo':
            msg = "it can't reset in servo motor"
            self.__logger.critical(msg)
            return msg
        elif motor_type == 'step_line':
            pre_move_distance = 3
            ret = self.rel_move(pre_move_distance)
            if ret:
                msg = "error when the motor pre-move on reseting"
            axis_id = self.__axis_list[0]['axis_id']
            speed = -10 * self.__axis_list[0]['proportion']
            ret = self.__motion.home_search(axis_id, speed, 0.2, 0)
        elif motor_type == 'step_circle':
            pre_move_distance = 30
            ret = self.rel_move(pre_move_distance)
            if ret:
                msg = "error when the motor pre-move on reseting"
            axis_id = self.__axis_list[0]['axis_id']
            speed = -72 * self.__axis_list[0]['proportion']
            ret = self.__motion.home_search(axis_id, speed, 0.2, 0)
        
        sleep(0.1)
        # wait for motion done
        count = 0
        interval_time = interval / 1000
        while 1:
            stat = self.get_motion_status()
            if stat:
                count = count + interval
            else:
                break
            if count >= timeout:
                msg = 'timeout({}) when reseting step motor'.format(timeout)
                self.__logger.info(msg)
                return msg
            sleep(interval_time)
        self.__motion.set_position(axis_id, 0)
        self.__motion.set_command(axis_id, 0)
        