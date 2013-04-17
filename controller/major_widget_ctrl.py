#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from masbot.config.utils import SigName, UISignals
from masbot.config.common_lib import *
import threading
from time import sleep
from random import *
from masbot.device.device_manager import DeviceManager
from masbot.device.piston import Piston
from masbot.device.motor import Motor
from masbot.flow.main_flow import MainFlow
from imp import reload

class MajorWidgetCtrl:

    def __init__(self):
        self.__proxy_switch = 1
        self.__servo_status = 0
        UISignals.GetSignal(SigName.SERVO_ON).connect(self.__servo_on_off)
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).connect(self.__tuning_position)
        UISignals.GetSignal(SigName.START_MAIN).connect(self.__start_flow)
        UISignals.GetSignal(SigName.PAUSE_MAIN).connect(self.__pause_flow)
        UISignals.GetSignal(SigName.LOG_IN).connect(self.__login_out)
        UISignals.GetSignal(SigName.DO_OUT).connect(self.__do_clicked)
        
        self.__device_proxy()
        timer = threading.Timer(1, self.__update_ui)
        timer.daemon = True
        timer.start()
        # initail the flow actor
        self.__main_flow = MainFlow().start()
        self.__first_import = True
        
    def set_proxy_switch(self, on_off=0):
        self.__proxy_switch = on_off
        
    def __start_flow(self):
        #self.set_proxy_switch(0)
        self.__main_flow.send('start', wait=False)
        
    def __pause_flow(self):
        self.__main_flow.send('pause', wait=False)
        #self.set_proxy_switch(1)

    def __device_proxy(self):
        DM = DeviceManager()
        self.__adlink = DM._get_device_proxy('ADLink')
        
        self.__motor_proxy = {}
        for rec in motor_info:
        #    points_info = {}
        #    if not rec['individual']:
        #        points_info = single_axis_points[rec['key']]
            self.__motor_proxy[rec['key']] = Motor(rec['key'], self.__adlink, [rec])
        
    def __do_clicked(self, do_port, on_off):
        print("ctrl:  do : {0}, {1}".format(do_port, on_off))
        
    def __servo_on_off(self):
        if self.__servo_status == 0:
            # double axis servo on
            axis_list = []
            for actor_key, axis in double_axis_info.items():
                axis_list.append(actor_key)
                ret = actor[actor_key].send('servo_on')
                if ret:
                    for key in axis_list:
                        actor[key].send('servo_off')
                    return ret
            # single axis servo on
            for axis in motor_info:
                if axis['individual']:
                    key = axis['key']
                    ret = actor[actor_key].send('servo_on')
                    if ret:
                        for key in axis_list:
                            actor[key].send('servo_off')
                        return ret
            self.__servo_status = 1
            return 0
        else:
            # double axis servo on
            for actor_key, axis in double_axis_info.items():
                ret = actor[actor_key].send('servo_off')
                if ret:
                    return ret
            # single axis servo off
            for axis in motor_info:
                if axis['individual']:
                    actor_key = axis['key']
                    ret = actor[actor_key].send('servo_off')
                    if ret:
                        return ret
            self.__servo_status = 0
            return 0

    def __update_ui(self):
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE)

        while True:
            if self.__proxy_switch:        
                for axis in motor_info:
                    key = axis['key']
                    position = self.__motor_proxy[key].get_position()
                    status = self.__motor_proxy[key].get_motion_status()
                    slot.emit('position', key, position)
                    slot.emit('state', key, status)
            sleep(0.3)
        
    def __tuning_position(self, axis_name, offset):
        if self.__proxy_switch:
            offset = (offset, )
            return self.__motor_proxy[axis_name].rel_move(offset)

    def __login_out(self):
        import masbot.controller.test_flow
        if not self.__first_import:
            reload(masbot.controller.test_flow)
        self.__first_import = False