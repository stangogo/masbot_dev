#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from masbot.ui.utils import SigName, UISignals
from masbot.config.common_lib import *
import threading
from time import sleep
from random import *
from masbot.device.device_manager import DeviceManager
from masbot.device.piston import Piston
from masbot.device.motor import Motor

class MajorWidgetCtrl:

    def __init__(self):
        self._proxy_switch = 1
        self._servo_status = 0
        UISignals.GetSignal(SigName.SERVO_ON).connect(self._servo_on)
        self._device_proxy()
        timer = threading.Timer(1, self._update_position)
        timer.daemon = True
        timer.start()

    def set_proxy_switch(self, on_off=0):
        self._proxy_switch = on_off

    def _device_proxy(self):
        DM = DeviceManager()
        self.motion = DM._device_proxy()
        
        self.motor_proxy = {}
        for rec in motor_info:
            points_info = {}
            if not rec['composite']:
                points_info = single_axis_points[rec['key']]
            self.motor_proxy[rec['key']] = Motor(self.motion, [rec], points_info)
        
    def _servo_on(self):
        if self._servo_status == 0:
            ret = motor['tbar'].send('servo_on')
            if ret:
                return ret
            ret = motor['axis_z'].send('servo_on')
            if ret:
                return ret
            self._servo_status = 1
            return 0
        else:
            ret = motor['tbar'].send('servo_off', wait=False)
            if ret:
                return ret
            ret = motor['axis_z'].send('servo_off')
            if ret:
                return ret
            self._servo_status = 0
            return 0

    def _update_position(self):
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE) 

        while True:
            if self._proxy_switch:
                for axis in motor_info:
                    key = axis['key']
                    position = self.motor_proxy[key].get_position()
                    display = '{0:.3f}'.format(position)
                    slot.emit('position', key, float(display))
            sleep(0.3)
        