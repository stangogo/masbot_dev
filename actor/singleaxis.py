# -- coding: utf-8 --

# Title          : singleaxis.py
# Description    : actor with 1 axis
# Author         : Stan Liu
# Date           : 20130318
# Dependency     : pykka
# usage          : 
# notes          : 

import pykka
from collections import namedtuple
AxisInfo = namedtuple('AxisInfo', ['axis_id', 'position'])

class SingleAxis(pykka.ThreadingActor):
    def __init__(self, motion, axis_info, axis_points={}):
        super(SingleAxis, self).__init__()
        self.motion = motion
        self.axis_info = axis_info
        self.axis_points = axis_points
        self.state = 0
        
    def on_receive(self, message):
        # 
        if message.get('msg') == 'check_state':
            message['reply_to'].set(self.state)
        elif message.get('msg') == 'move':
            position = message.get('position')
            ret = self._move(position)
            if ret:
                self.state = ret
                message['reply_to'].set(ret)
            else:
                self.state = 0
                message['reply_to'].set('ready')
        elif message.get('msg') == 'rmove':
            position = message.get('position')
            ret = self._rmove(position)
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
        position = self.axis_points[point_index]
        ret = self._move(position)
        return ret
        
    def _move(self, position, speed=50, acc_time=0.3):
        # check if position in safe scope
        ret = self._check_line_scope(position)
        if ret:
            return ret

        axis_list = []
        axis_id = self.axis_info['axis_id']
        proportion = self.axis_info['proportion']
        pulse = position * proportion
        axis_list.append(AxisInfo(axis_id, pulse))
        speed = speed * proportion
        self.state = 'moving'
        ret = self.motion.absolute_move(axis_list, speed, acc_time, acc_time)
        return ret

    def _rmove(self, position, speed=50, acc_time=0.3):
        # check if x,y in safe scope
        axis_id = self.axis_info['axis_id']
        proportion = self.axis_info['proportion']
        now_position = self.motion.get_position(axis_id) / proportion
        ret = self._check_line_scope(now_position + position)
        if ret:
            return ret

        axis_list = []
        axis_id = self.axis_info['axis_id']
        proportion = self.axis_info['proportion']
        pulse = position * proportion
        axis_list.append(AxisInfo(axis_id, pulse))
        speed = speed * proportion
        self.state = 'moving'
        ret = self.motion.relative_move(axis_list, speed, acc_time, acc_time)
        return ret
        
    def _check_line_scope(self, position):
        min = self.axis_info['scope_min']
        max = self.axis_info['scope_max']
        
        if position <= min:
            return '[out of scope]: target = {}, scope limit = {}'.format(position, min)
        elif position >= max:
            return '[out of scope]: target = {}, scope limit = {}'.format(position, max)
        else:
            return 0