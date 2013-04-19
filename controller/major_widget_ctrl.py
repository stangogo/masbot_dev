#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from masbot.config.utils import SigName, UISignals
from masbot.config.common_lib import *
import threading
from time import sleep
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
        self.__lplink = DM._get_device_proxy('LPLink')
        
    def __do_clicked(self, do_port, on_off):
        print("ctrl:  do : {0}, {1}".format(do_port, on_off))
        
    def __servo_on_off(self):
        if self.__servo_status == 0:
            servo_on_ok_list = []
            for axis in motor_info:
                actor_key = axis['key']
                ret = actor[actor_key].send('servo_on')
                if ret:
                    for actor_key in servo_on_ok_list:
                        actor[actor_key].send('servo_off')
                    return ret
                servo_on_ok_list.append(actor_key)
            self.__servo_status = 1
            return 0
        else:
            self.__servo_status = 0
            for axis in motor_info:
                actor_key = axis['key']
                ret = actor[actor_key].send('servo_off')
                if ret:
                    return ret
            return 0

    def __update_ui(self):
        while True:
            if self.__proxy_switch:
                self.__refresh_axis_widget()
            sleep(0.3)
        
    def __refresh_axis_widget(self):
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE)
        for motor in motor_info:
            actor_name = motor['key']
            axis_info = motor['axis_info']
            axis_count = len(axis_info)
            position_list = actor[actor_name].send('get_position')
            status_list = actor[actor_name].send('get_status')
            if axis_count == 1:
                position_list = list(position_list)
                status_list = list(status_list)
            for i in range(axis_count):
                axis_name = axis_info[i]['key']
                slot.emit('position', axis_name, position_list[i])
                slot.emit('state', axis_name, status_list[i])
        
    def __tuning_position(self, axis_name, offset):
        if self.__proxy_switch:
            for motor in motor_info:
                #if axis_name in axis_map:
                if motor['key'] == axis_name:
                    return actor[axis_name].send('rel_move', position=(offset,))
                elif 'sub_axis' in motor and axis_name in motor['sub_axis']:
                    sub_axis = motor['sub_axis']
                    axis_count = len(sub_axis)
                    index = sub_axis.index(axis_name)
                    actor_name = motor['key']
                    rel_position_list = [0] * axis_count
                    rel_position_list[index] = offset
                    ret = actor[actor_name].send('rel_move', position=rel_position_list)
                    return ret

    def __login_out(self):
        import masbot.controller.test_flow
        if not self.__first_import:
            reload(masbot.controller.test_flow)
        self.__first_import = False