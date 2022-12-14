#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import threading, sys, ctypes
from time import sleep, clock
from imp import reload
from masbot.config.utils import SigName, UISignals
from masbot.controller.wake_actor import *
from masbot.device.device_manager import DeviceManager
from masbot.controller.image_tools import *

import masbot.flow.main_flow

class MajorWidgetCtrl:

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__proxy_switch = 1
        self.__servo_status = 0
        UISignals.GetSignal(SigName.MAIN_CLOSE).connect(self.__ui_close)
        UISignals.GetSignal(SigName.MAIN_START).connect(self.__servo_on_off)
        UISignals.GetSignal(SigName.FROM_AXIS_TABLE).connect(self.__move_single_axis)
        UISignals.GetSignal(SigName.MAIN_PLAY).connect(self.__play_flow)
        UISignals.GetSignal(SigName.MAIN_LOG_IN).connect(self.__login_out)
        UISignals.GetSignal(SigName.DO_OUT).connect(self.__do_clicked)
        
        self.__b_ui_close = False
        
        DM = DeviceManager()
        self.__device_proxy = DM._get_device_proxy()
        self.__initial_image_control()        
        
        timer = threading.Timer(1, self.__update_ui)
        timer.daemon = True
        timer.start()       
        
        # initail the flow actor
        self.__main_flow = masbot.flow.main_flow.MainFlow().start()        
        
    def set_proxy_switch(self, on_off=0):
        self.__proxy_switch = on_off
        
    def __play_flow(self, play):
        if play:
            self.set_proxy_switch(0)
            self.__main_flow.send('start', wait=False)
            self.__realtime_display_image('off')
            self.__logger.debug('start_flow button is pressed by user')
        else:
            self.__main_flow.send('pause', wait=False)
            self.set_proxy_switch(1)
            self.__realtime_display_image('on')
            self.__logger.debug('pause_flow button is pressed by user')
            
    def __do_clicked(self, do_port, on_off):
        self.__device_proxy['8158'].DO(do_port, on_off)
        
        
    def __ui_close(self):
        """ terminate all running thread, actor, and flow.
        """
        self.__b_ui_close = True
        self.__logger.debug('main ui is closed by user')
        
        self.__main_flow.stop()
        for value in actor.values():
            value.stop()
        
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
            self.__logger.debug('servo_on button is pressed by user')
            return 0
        else:
            self.__servo_status = 0
            for axis in motor_info:
                actor_key = axis['key']
                ret = actor[actor_key].send('servo_off')
                if ret:
                    return ret
            self.__logger.debug('servo_off button is pressed by user')
            return 0

    def __update_ui(self):
        while True:
            if self.__b_ui_close:
                break
            
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
            
        #do_slot.emit(do_status, 1)
        #di_slot.emit(di_status, 1)
        
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
        #self.__main_flow.stop()
        self.__play_flow(0)
        del(self.__main_flow)
        reload(masbot.flow.main_flow)
        self.__main_flow = masbot.flow.main_flow.MainFlow().start()
    '''    
    ###############################################################
    #####################  image widget part ######################
    ###############################################################
    '''
    def __initial_image_control(self):
        slot = UISignals.GetSignal(SigName.QIMAGE_THUMBNAIL)
        self.__image_diplay_thread = []
        self.__display_on_off = False      
                
        for count in camera_info:
            actor_name = count['camera_set'].get('camera_name', None)
            actor_disp = count['camera_set'].get('display_text', 'No name')
            if actor_name:
                thd = threading.Thread(target=self.__update_image_thumbnail, args=[slot,actor_name,actor_disp])
                thd.daemon = True
                thd.start()                  
                self.__image_diplay_thread.append(thd)   
        test_thread = threading.Thread(target=self.test_inspection)
        test_thread.daemon = True
        test_thread.start()      
        
    def __realtime_display_image(self, switch):
        if switch == 'on':
            self.__display_on_off = True
        elif switch == 'off':
            self.__display_on_off = False
        else:
            pass
    
    def __update_image_thumbnail(self, slot, actor_name, display_text):
        sleep(1)
        while not self.__b_ui_close:
            if self.__display_on_off:
                data = actor[actor_name].send('snapshot')
                Qim = QImagefromData(data)
                if Qim:
                    msg = [Qim, actor_name, display_text]
                    slot.emit(msg)
            sleep(0.07)
            
    def test_inspection(self):
        sleep(3)
        for i in range(1000):
            sleep(1)
            actor['top_camera'].send('inspect',job_name='BARREL')