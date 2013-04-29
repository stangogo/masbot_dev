#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import threading
from time import sleep
from imp import reload
  
from masbot.config.utils import SigName, UISignals
from masbot.controller.wake_actor import *
from masbot.device.device_manager import DeviceManager
from masbot.flow.main_flow import MainFlow

class MajorWidgetCtrl:

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__proxy_switch = 1
        self.__servo_status = 0
        UISignals.GetSignal(SigName.MAIN_START).connect(self.__servo_on_off)
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).connect(self.__move_single_axis)
        UISignals.GetSignal(SigName.MAIN_PLAY).connect(self.__play_flow)
        UISignals.GetSignal(SigName.MAIN_LOG_IN).connect(self.__login_out)
        UISignals.GetSignal(SigName.DO_OUT).connect(self.__do_clicked)
        
        DM = DeviceManager()
        self.__device_proxy = DM._get_device_proxy()
        timer = threading.Timer(1, self.__update_ui)
        timer.daemon = True
        timer.start()
        # initail the flow actor
        self.__main_flow = MainFlow().start()
        self.__first_import = True
        
    def set_proxy_switch(self, on_off=0):
        self.__proxy_switch = on_off
        
    def __play_flow(self, play):
        if play:
            self.set_proxy_switch(0)
            self.__main_flow.send('start', wait=False)
        else:
            self.__main_flow.send('pause', wait=False)
            self.set_proxy_switch(1)
        
    def __do_clicked(self, do_port, on_off):
        self.__device_proxy['8158'].DO(do_port, on_off)
        
    def __servo_on_off(self, on):
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
                self.__refresh_dio_widget()
            sleep(0.2)
        
    def __refresh_axis_widget(self):
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE)
        for motor in motor_info:
            actor_name = motor['key']
            axis_info = motor['axis_info']
            axis_count = len(axis_info)
            position_list = actor[actor_name].send('get_position')
            status_list = actor[actor_name].send('get_status')
            if axis_count == 1:
                position_list = [position_list, ]
                status_list = [status_list, ]
            for i in range(axis_count):
                axis_name = axis_info[i]['key']
                slot.emit('position', axis_name, position_list[i])
                slot.emit('state', axis_name, status_list[i])
                
    def __refresh_axis_widget_by_actor(self):
        slot = UISignals.GetSignal(SigName.ENTER_AXIS_TABLE)
        for motor in motor_info:
            actor_name = motor['key']
            axis_info = motor['axis_info']
            axis_count = len(axis_info)
            position_list = actor[actor_name].send('get_position')
            status_list = actor[actor_name].send('get_status')
            if axis_count == 1:
                position_list = [position_list, ]
                status_list = [status_list, ]
            for i in range(axis_count):
                axis_name = axis_info[i]['key']
                slot.emit('position', axis_name, position_list[i])
                slot.emit('state', axis_name, status_list[i])

    def __refresh_dio_widget(self):
        do_slot = UISignals.GetSignal(SigName.DO_IN)
        di_slot = UISignals.GetSignal(SigName.DI_IN)
        
        do_status = []
        module_type = '8158'
        for i in range(self.__device_proxy[module_type].do_count()):
            status = self.__device_proxy[module_type].DO_read(i)
            do_status.append(status)
            
        di_status = []
        for i in range(self.__device_proxy[module_type].di_count()):
            status = self.__device_proxy[module_type].DI(i)
            di_status.append(status)
            
        do_slot.emit(do_status, 1)
        di_slot.emit(di_status, 1)
        
    def __move_single_axis(self, axis_name, offset):
        # check if the device proxy status
        if not self.__proxy_switch:
            msg = "it's not allowed to move axis when device proxy is closed"
            self.__logger.error(msg)
            return msg

        # check if the target scope is legal
        axis_info = axis_map[axis_name]
        module_type = axis_info['module_type']
        pulse = self.__device_proxy[module_type].get_pulse(axis_info['axis_id'])
        current_position = pulse / axis_info['proportion']
        target_position = current_position + offset
        min = axis_info['scope_min']
        max = axis_info['scope_max']
        if target_position <=  min or target_position >= max:
            msg = "out of scope: axis = {}, target = {}, scope between {} ~ {})".format(
                    axis_info['key'], target_position, min, max)
            self.__logger.error(msg)
            return msg
        
        # make up the dictionary for motion moving
        axis_dic = {
            'axis_id': axis_info['axis_id'],
            'pulse': axis_info['proportion'] * offset,
        }
        axis_list = [axis_dic, ]
        speed = axis_info['proportion'] * axis_info['speed']
        ret = self.__device_proxy[module_type].relative_move(axis_list, speed)
        return ret
        
    def __move_single_axis_by_actor(self, axis_name, offset):
        if not self.__proxy_switch:
            msg = "it's not allowed to move axis when device proxy is closed"
            self.__logger.error(msg)
            return msg

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