# -- coding: utf-8 --

# Title          : doubleaxis.py
# Description    : actor with 2 axis
# Author         : Stan Liu
# Date           : 20130318
# Dependency     : pykka
# usage          : 
# notes          : 

import pykka
from collections import namedtuple
AxisInfo = namedtuple('AxisInfo', ['axis_id', 'position'])

class DoubleAxis(pykka.ThreadingActor):
    def __init__(self, motion, axis_info, axis_points):
        super(DoubleAxis, self).__init__()
        self.motion = motion
        self.axis_info = axis_info
        self.axis_points = axis_points
        self.state = 0
        
    def on_receive(self, message):
        # 
        if message.get('msg') == 'check_state':
            message['reply_to'].set(self.state)
        elif message.get('msg') == 'move_xy':
            x = message.get('x')
            y = message.get('y')
            ret = self._move_xy(x, y)
            if ret:
                self.state = ret
                message['reply_to'].set(ret)
            else:
                self.state = 0
                message['reply_to'].set('ready')
        elif message.get('msg') == 'rmove_xy':
            x = message.get('x')
            y = message.get('y')
            ret = self._rmove_xy(x, y)
            if ret:
                self.state = ret
                message['reply_to'].set(ret)
            else:
                self.state = 0
                message['reply_to'].set('ready')
        elif message.get('msg') == 'move_point':
            point_index = message.get('point_index')
            ret = self._move_to_point(point_index)
            if ret:
                self.state = ret
                message['reply_to'].set(ret)
            else:
                self.state = 0
                message['reply_to'].set('ready')

    def _move_to_point(self, point_index):
        x = self.axis_points[point_index]['x']
        y = self.axis_points[point_index]['y']
        ret = self._move_xy(x, y)
        return ret
        
    def _move_xy(self, x, y, speed=50, acc_time=0.3):
        # check if x,y in safe scope
        ret = self._check_area_scope(x, y)
        if ret:
            return ret

        axis_list = []
        position = {}
        position['axis_x'] = x
        position['axis_y'] = y
        for key, axis in self.axis_info.items():
            axis_id = axis["axis_id"]
            proportion = axis["proportion"]
            pulse = position[key] * proportion
            axis_list.append(AxisInfo(axis_id, pulse))
        speed = speed * proportion
        self.state = 'moving'
        ret = self.motion.absolute_move(axis_list, speed, acc_time, acc_time)
        return ret

    def _rmove_xy(self, x, y, speed=50, acc_time=0.3):
        # check if x,y in safe scope
        axis_x_id = self.axis_info['axis_x']['axis_id']
        axis_y_id = self.axis_info['axis_y']['axis_id']
        x_proportion = self.axis_info['axis_x']['proportion']
        y_proportion = self.axis_info['axis_y']['proportion']
        now_x = self.motion.get_position(axis_x_id) / x_proportion
        now_y = self.motion.get_position(axis_y_id) / y_proportion
        ret = self._check_area_scope(now_x+x, now_y+y)
        if ret:
            return ret

        axis_list = []
        position = {}
        position['axis_x'] = x
        position['axis_y'] = y
        for key, axis in self.axis_info.items():
            axis_id = axis["axis_id"]
            proportion = axis["proportion"]
            pulse = position[key] * proportion
            axis_list.append(AxisInfo(axis_id, pulse))
        speed = speed * proportion
        self.state = 'moving'
        ret = self.motion.relative_move(axis_list, speed, acc_time, acc_time)
        return ret
        
    def _check_area_scope(self, x, y):
        min_x = self.axis_info['axis_x']['scope_min']
        max_x = self.axis_info['axis_x']['scope_max']
        min_y = self.axis_info['axis_y']['scope_min']
        max_y = self.axis_info['axis_y']['scope_max']
        
        if x <= min_x:
            return '[out of scope]: target x = {}, scope limit = {}'.format(x, min_x)
        elif x >= max_x:
            return '[out of scope]: target x = {}, scope limit = {}'.format(x, max_x)
        elif y <= min_y:
            return '[out of scope]: target y = {}, scope limit = {}'.format(y, min_y)
        elif y >= max_y:
            return '[out of scope]: target y = {}, scope limit = {}'.format(y, max_y)
        else:
            return 0