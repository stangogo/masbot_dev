# -*- coding: utf-8 -*-

# Title          : main_flow.py
# Description    : main flow during the auto run process
# Author         : Stan Liu
# Date           : 20130327
# Dependency     : pykka
# usage          : 
# notes          : 

from time import sleep
import logging
import pykka
from masbot.config.common_lib import *

class MainFlow(pykka.ThreadingActor):
    def __init__(self,):
        super(MainFlow, self).__init__()
        self._logger = logging.getLogger(__name__)
        self._state = 'get_object'
        
    def check_continue(self, next_state):
        if self._continue:
            self.actor_ref.send(next_state, wait=False)
            
    def on_receive(self, message):
        # basic message format
        if message.get('msg') == 'start':
            self._continue = True
            ret = self._state
        elif message.get('msg') == 'pause':
            self._continue = False
            ret = self._state
        # ###################################################################
        # start to customize the state machine
        elif message.get('msg') == 'get_object':
            ret = self.get_object()
        elif message.get('msg') == 'put_object':
            ret = self.put_object()
        # end to customize the state machine
        # ###################################################################
        else:
            ret = 'undefine message format'
        # check if continue running to next state
        self.check_continue(ret)
        # message['reply_to'].set(ret)

    # #######################################################################
    # state machine process
    # #######################################################################
    def get_object(self):
        self._state = 'get_object'
        ret = actor['tbar'].send('pt_move', pt='get_pt')
        sleep(0.2)
        if ret:
            print(ret)
            return 'pause'

        return 'put_object'

    def put_object(self):
        self._state = 'put_object'
        ret = actor['tbar'].send('pt_move', pt='put_pt')
        sleep(0.2)
        if ret:
            print(ret)
            return 'pause'
            
        ret = actor['noz1'].send('action_on')
        sleep(0.2)
        if ret:
            print(ret)
            return 'pause'
            
        ret = actor['noz1'].send('action_off')
        sleep(0.2)
        if ret:
            print(ret)
            return 'pause'
        
        return 'get_object'
