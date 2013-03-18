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
        super(Piston, self).__init__()
        self.io_card = io_card
        self.piston_info = piston_info
        self.state = 'ready'
        
    def on_receive(self, message):
        # action on
        if message.get('msg') == 'down_action':
            self.state = 'downing'
            action_port = self.piston_info['action']
            ret = self.io_card.DO(action_port, 1)
            if ret:
                message['reply_to'].set('down_error')
                return ret
            on_port = self.piston_info['on_sensor']
            ret = self.io_card.check_sensor(on_port)
            if ret:
                message['reply_to'].set('ready')
            else:
                message['reply_to'].set('down_error')
        # action off
        elif message.get('msg') == 'up_action':
            self.state = 'upping'
            action_port = self.piston_info['action']
            ret = self.io_card.DO(action_port, 0)
            if ret:
                message['reply_to'].set('up_error')
                return ret
            on_port = self.piston_info['off_sensor']
            ret = self.io_card.check_sensor(on_port)
            if ret:
                message['reply_to'].set('ready')
            else:
                message['reply_to'].set('up_error')
