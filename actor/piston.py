# -- coding: utf-8 --

# Title          : piston.py
# Description    : piston with some DO and DI
# Author         : Stan Liu
# Date           : 20130313
# Dependency     : pykka
# usage          : 
# notes          : 

import pykka

class Piston(pykka.ThreadingActor):
    def __init__(self, io_card, piston_info):
        self.io_card = io_card
        self.piston_info = piston_info
        
    def on_receive(self, message):
        if message.get('msg') == 'down_action':
            message['reply_to'].set('downing')
            action_port = self.piston_info['action']
            self.DO(action_port, 1)
            message['reply_to'].set('ready')
        elif message.get('msg') == 'up_action':
            message['reply_to'].set('downing')
            action_port = self.piston_info['action']
            self.DO(action_port, 0)
            message['reply_to'].set('ready')