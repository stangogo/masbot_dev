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
from masbot.controller.wake_actor import *

# utility sample
# actor['tbar'].send('servo_on')
# actor['tbar'].send('servo_off')
# actor['tbar'].send('abs_move', position=(10,20))

# actor['axis_z'].send('set_speed', speed=100)
# actor['axis_z'].send('set_acc_time', acc_time=0.2)
# actor['axis_z'].send('get_position')
# actor['axis_z'].send('rel_move', position=5)
# actor['axis_z'].send('pt_move', pt='z1')

class MainFlow(pykka.ThreadingActor):
    def __init__(self,):
        super(MainFlow, self).__init__()
        self._logger = logging.getLogger(__name__)
        # ====================define initial value=======================
        self._state = 'stateA'
        # ===============================================================
        
    def check_continue(self, next_state):
        if self._continue:
            self.actor_ref.send(next_state, wait=False)
            
    def on_receive(self, message):
        # basic message format
        if message.get('msg') == 'start':
            self._continue = True
            next_state = self._state
        elif message.get('msg') == 'pause':
            self._continue = False
            next_state = self._state
        # =================customize the state machine===================
        elif message.get('msg') == 'stateA':
            next_state = self.stateA()
        elif message.get('msg') == 'stateB':
            next_state = self.stateB()
        # ===============================================================
        else:
            next_state = 'undefine state'
        self.check_continue(next_state)
        """message['reply_to'].set(next_state)"""

    # ====================state machine process==========================
    def stateA(self):
        self._state = 'stateA'
        position = actor['xy'].send('get_position')
        sleep(0.2)
        #actor['axis_z'].send('pt_move', pt='test1')
        if 0:
            return 'pause'
        return 'stateB'

    def stateB(self):
        self._state = 'stateB'
        position = actor['xy'].send('get_position')
        #actor['axis_z'].send('pt_move', pt='test2')
        sleep(0.2)
        return 'stateA'
