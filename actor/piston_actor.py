# -- coding: utf-8 --

# Title          : piston_actor.py
# Description    : piston with some DO and DI
# Author         : Stan Liu
# Date           : 20130313
# Dependency     : pykka
# usage          : device_manager.py piston.py
# notes          : 

import pykka
from masbot.device.device_manager import DeviceManager

class PistonActor(pykka.ThreadingActor):
    def __init__(self, resource):
        super(PistonActor, self).__init__()
        DM = DeviceManager()
        self._state = 'ready'
        resource['device_type'] = 'piston'
        self.piston_obj = DM.request(resource)
        
    def on_receive(self, message):
        # react on
        if message.get('msg') == 'state':
            message['reply_to'].set(self._state)
        elif message.get('msg') == 'react_on':
            self._state = 'reacting'
            ret = self.piston_obj.react(1)
            if ret:
                message['reply_to'].set('react_on_error')
            else:
                message['reply_to'].set('ready')
        # react off
        elif message.get('msg') == 'react_off':
            self._state = 'reacting'
            ret = self.piston_obj.react(0)
            if ret:
                message['reply_to'].set('react_off_error')
            else:
                message['reply_to'].set('ready')
        # sensor status
        elif message.get('msg') == 'sensor_status':
            sensor_status = self.piston_obj.get_di_status()
            message['reply_to'].set(sensor_status)
        # react status
        elif message.get('msg') == 'react_status':
            react_status = self.piston_obj.get_do_status()
            message['reply_to'].set(react_status)
        else:
            print('undefine message')

