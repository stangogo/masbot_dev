# -*- coding: utf-8 -*-

# Title          : main_flow.py
# Description    : main flow during the auto run process
# Author         : Stan Liu
# Date           : 20130327
# Dependency     : pykka
# usage          : 
# notes          : 

import logging
import pykka
from masbot.config.common_lib import *
from time import sleep

class MainFlow(pykka.ThreadingActor):
    def __init__(self,):
        super(MainFlow, self).__init__()
        self._logger = logging.getLogger(__name__)
        self._state = 'tray_in'
        self._continue = True
        self._max_object_count = 20
        self._nozzle_count = 10
        self._nozzle_status = [0] * self._nozzle_count
        self._object_count = 0
        
    def on_receive(self, message):
        if message.get('msg') == 'start':
            self._continue = True
            ret = self._state
        elif message.get('msg') == 'pause':
            self._continue = False
            ret = self._state
        elif message.get('msg') == 'tray_in':
            ret = self.tray_in()
        elif message.get('msg') == 'get_object':
            ret = self.get_object()
        elif message.get('msg') == 'put_object':
            ret = self.put_object()
        elif message.get('msg') == 'tray_out':
            ret = ret = self.tray_out()
        else:
            ret = 'undefine message format'
        # check if continue running to next state
        self.check_continue(ret)
        #message['reply_to'].set(ret)
        
    def check_continue(self, next_state):
        if self._continue:
            self.actor_ref.send(next_state, wait=False)

    def tray_in(self):
        self._state = 'tray_in'
        self._object_count = 0
        for i in range(3):
            print('tray_in process ', i)
            sleep(0.1)
        next_state = 'get_object'
        return next_state

    def tray_out(self):
        self._state = 'tray_out'
        self._object_count = 0
        for i in range(3):
            print('tray_out process ', i)
            sleep(0.1)
        next_state = 'tray_in'
        return next_state

    def get_object(self):
        self._state = 'get_object'
        for i in range(self._nozzle_count):
            if self._nozzle_status[i] == 0:
                cur_nozzle = i
                break
        self._nozzle_status[cur_nozzle] = 1
        print('nozzle {} get'.format(cur_nozzle))
        sleep(0.1)
        
        if 0 in self._nozzle_status:
            next_state = 'get_object'
        else:
            next_state = 'put_object'
        return next_state

    def put_object(self):
        self._state = 'put_object'
        for i in range(self._nozzle_count):
            if self._nozzle_status[i] == 1:
                cur_nozzle = i
                break
        self._nozzle_status[cur_nozzle] = 0
        print('nozzle {} put'.format(cur_nozzle))
        self._object_count += 1
        sleep(0.1)
        if self._object_count >= self._max_object_count:
            next_state = 'tray_out'
            return next_state
        if 1 in self._nozzle_status:
            next_state = 'put_object'
        else:
            next_state = 'get_object'
        return next_state
