# -- coding: utf-8 --

# Title          : piston_actor.py
# Description    : piston actor with action and detecting status
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : pykka
# usage          : 
# notes          : 

import pykka
from masbot.device.device_manager import DeviceManager

class PistonActor(pykka.ThreadingActor):
    def __init__(self, module_info):
        super(PistonActor, self).__init__()
        self._state = 'ready'
        DM = DeviceManager()
        self._piston_obj = DM.request('piston', module_info)
        
    def on_receive(self, message):
        # action on
        if message.get('msg') == 'state':
            message['reply_to'].set(self._state)
        elif message.get('msg') == 'action_on':
            self._state = 'actioning'
            ret = self._piston_obj.action(1)
            if ret:
                message['reply_to'].set('action_on_error')
            else:
                message['reply_to'].set('ready')
        # action off
        elif message.get('msg') == 'action_off':
            self._state = 'actioning'
            ret = self._piston_obj.action(0)
            if ret:
                message['reply_to'].set('action_off_error')
            else:
                message['reply_to'].set('ready')
        # sensor status
        elif message.get('msg') == 'sensor_status':
            sensor_status = self._piston_obj.get_di_status()
            message['reply_to'].set(sensor_status)
        # action status
        elif message.get('msg') == 'action_status':
            action_status = self._piston_obj.get_do_status()
            message['reply_to'].set(action_status)
        else:
            msg = 'undefine message format'
            print(msg)
            message['reply_to'].set(msg)

