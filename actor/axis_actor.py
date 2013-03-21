# -- coding: utf-8 --

# Title          : axis_actor.py
# Description    : axis features
#                  - absolute move
#                  - relative move
#                  - point move
#                  - get axis status
# Author         : Stan Liu
# Date           : 20130321
# Dependency     : pykka
# usage          : device_manager.py piston.py
# notes          : 

import pykka
from masbot.device.device_manager import DeviceManager

class AxisActor(pykka.ThreadingActor):
    def __init__(self, resource):
        super(AxisActor, self).__init__()
        self._state = 'ready'
        DM = DeviceManager()
        resource['device_type'] = 'axis'
        self._piston_obj = DM.request(resource)
        
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
        else:
            msg = 'undefine message format'
            print(msg)
            message['reply_to'].set(msg)

