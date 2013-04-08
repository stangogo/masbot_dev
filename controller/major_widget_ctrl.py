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
        self.__proxy_switch = 1
        self.__servo_status = 0
        UISignals.GetSignal(SigName.SERVO_ON).connect(self.__servo_on)
        
        
        UISignals.GetSignal(SigName.DO_OUT).connect(self.__do_clicked)
        
        self.__device_proxy()
        timer = threading.Timer(1, self.__update_position)
        timer.daemon = True
        timer.start()

    def set_proxy_switch(self, on_off=0):
        self.__proxy_switch = on_off

    def __device_proxy(self):
        DM = DeviceManager()
        self.__motion = DM._device_proxy()
        
        self.__motor_proxy = {}
        for rec in motor_info:
            points_info = {}
            if not rec['composite']:
                points_info = single_axis_points[rec['key']]
            #self.__motor_proxy[rec['key']] = Motor(self.__motion, [rec], points_info)
        
    def __do_clicked(self, do_port, on_off):
        print("ctrl:  do : {0}, {1}".format(do_port, on_off))
        
    def __servo_on(self):
        if self.__servo_status == 0:
            ret = motor['tbar'].send('servo_on')
            if ret:
                return ret
            ret = motor['axis_z'].send('servo_on')
            if ret:
                return ret
            self.__servo_status = 1
            return 0
        else:
            ret = motor['tbar'].send('servo_off', wait=False)
            if ret:
                return ret
            ret = motor['axis_z'].send('servo_off')
            if ret:
                return ret
            self.__servo_status = 0
            return 0

    def __update_position(self):
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE) 

        while True:
            if self.__proxy_switch:
                for axis in motor_info:
                    key = axis['key']
                    #position = self.__motor_proxy[key].get_position()
                    #display = '{0:.3f}'.format(position)
                    #slot.emit('position', key, float(display))
            sleep(0.3)
        