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
        self.__logger = logging.getLogger(__name__)
        self.__state = 0
        self.__pause = 0
        
    def on_receive(self, message):
        if message.get('command') == 'tray_in':
            next_state = 'recognition'
        if message.get('msg') == 'recognition':
            next_state = 'get_object'
        elif message.get('msg') == 'get_object':
            next_state = 'get_object'
            pass
        elif message.get('msg') == 'emg':
            pass
        else:
            next_state = 'undefine message format'
            
        # message response
        #self.__state = ret
        print(next_state)
        message['reply_to'].set(next_state)

