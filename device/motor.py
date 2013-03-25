# -*- coding: utf-8 -*-

# Title          : motor.py
# Description    : axis feature with moving, its status
# Author         : Stan Liu
# Date           : 20130321
# Dependency     : 
# usage          : 
# notes          : 

class Motor(object):
    def __init__(self, motion, axis_list, points_info):
        self._motion = motion
        self._points_info = points_info
        self._axis_list = axis_list
        self._axis_count = len(axis_list)
        if self._axis_count == 1:
            self._speed = axis_list[0]['speed']
            self._acc_time = axis_list[0]['accelerative_time']
        else:
            self._speed = 50
            self._acc_time = 0.2
        
    def get_speed():
        return self._speed

    def set_speed(value):
        self._speed = value
        
    def get_acc_time():
        return self._acc_time
        
    def set_acc_time(value):
        self._acc_time = value
    
    def servo_on_off(self, on_off):
        for axis_info in self._axis_list:
            ret = self._motion.servo_on_off(axis_info['axis_id'], on_off)
            if ret:
                msg = "servo on error: {} {}".format(axis_info['name'], ret)
                return msg
            if axis_info['motor_type'] == 'servo_type':
                ret = self.sync_pulse()
        return ret
        
    def sync_pulse(self):
        for axis_info in self._axis_list:
            ret = self._motion.sync_pulse(axis_info)
            if ret:
                msg = "sync position error: {} {}".format(axis_info['name'], ret)
                return msg
        return ret
        
    def abs_move(self, position_tuple):
        # check if parameter legal
        if len(position_tuple) != self._axis_count:
            return 'axis count = {}'.format(self._axis_count)
        # check if position under scope
        ret = self.check_scope(position_tuple)
        if ret:
            return ret
        axis_list = self._axis_list
        axis_map = []
        for index, position in enumerate(position_tuple):
            dic = {}
            dic['axis_id'] = axis_list[index]['axis_id']
            proportion = axis_list[index]['proportion']
            dic['pulse'] = proportion * position
            axis_map.append(dic)
        ret = self._motion.absolute_move(
            axis_map, self._speed, self._acc_time, self._acc_time)
        if ret:
            msg = "abs move error: {}".format(ret)
            return msg
        return ret
            
    def rel_move(self, rel_position_tuple):
        # check if parameter legal
        if len(rel_position_tuple) != self._axis_count:
            return "axis count = {}".format(self._axis_count)
        # check if position under scope
        now_position_list = self.get_position()
        position_list = []
        for index in range(self._axis_count):
            position_list.append(now_position_list[index] + rel_position_tuple[index])
        ret = self.check_scope(position_list)
        if ret:
            return ret
        axis_list = self._axis_list
        axis_map = []
        for index, position in enumerate(rel_position_tuple):
            dic = {}
            dic['axis_id'] = axis_list[index]['axis_id']
            proportion = axis_list[index]['proportion']
            dic['pulse'] = proportion * position
            axis_map.append(dic)
        ret = self._motion.relative_move(
            axis_map, self._speed, self._acc_time, self._acc_time)
        if ret:
            msg = "rel move error: {}".format(ret)
            return msg
        return ret
        
    def pt_move(self, point_key):
        if point_key not in self._points_info:
            return 'undefine point key: {}'.format(point_key)
        target_point = self._points_info[point_key]
        target_point = tuple(target_point)
        return self.abs_move(target_point)
        
    def check_scope(self, position_tuple):
        # check if parameter legal
        if len(position_tuple) != self._axis_count:
            return "axis count = {}".format(self._axis_count)
        axis_list = self._axis_list
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
        for axis_info in self._axis_list:
            pulse = self._motion.get_pulse(axis_info['axis_id'])
            pulse_list.append(pulse)
        if self._axis_count == 1:
            return pulse
        else:
            return pulse_list
            
    def get_position(self):
        position_list = []
        for axis_info in self._axis_list:
            pulse = self._motion.get_pulse(axis_info['axis_id'])
            position = pulse / axis_info['proportion']
            position_list.append(position)
        if self._axis_count == 1:
            return position
        else:
            return position_list
            
    def get_motion_status(self):
        status_list = []
        for axis_info in self._axis_list:
            stat = self._motion.get_motion_status(axis_info['axis_id'])
            pulse_list.append(stat)
        if self._axis_count == 1:
            return stat
        else:
            return status_list

    def get_io_status(self):
        status_list = []
        for axis_info in self._axis_list:
            stat = self._motion.get_io_status(axis_info['axis_id'])
            pulse_list.append(stat)
        if self._axis_count == 1:
            return stat
        else:
            return status_list
