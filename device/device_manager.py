# -*- coding: utf-8 -*-

# Title          : device_manager.py
# Description    : the role who manages the all I/O device
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

import logging
from re import compile
from masbot.config.global_settings import *
from masbot.device.motion.adlink_fake import ADLinkMotion as Motion
from masbot.device.piston import Piston
from masbot.device.motor import Motor

class DeviceManager(object):
    _instance = None
    # singleton: to guarantee there is only one instance
    def __new__(cls):
        if not DeviceManager._instance:
            DeviceManager._instance = object.__new__(cls)
            cls.__initial(cls)
        return DeviceManager._instance

    def __initial(self):
        self.__logger = logging.getLogger(__name__)
        self.__bulletin = {}
        self.__motion = Motion(io_card_info)
        di_count = self.__motion.di_card_count() * 32
        do_count = self.__motion.do_card_count() * 32
        axis_count = len(motor_info)
        self.__di_in_service = [0] * di_count
        self.__do_in_service = [0] * do_count
        self.__axis_in_service = [0] * axis_count
        #self.serial_in_service = [0] * serial_count

    def _device_proxy(self):
        return self.__motion

    def resource_status(self):
        resource = {}
        resource['DI'] = self.__di_in_service
        resource['DO'] = self.__do_in_service
        resource['AXIS'] = self.__axis_in_service
        return resource

    def request(self, actor_name, resource_type, module_info):
        if resource_type == 'piston':
            return self.__allocate_piston(module_info)
        elif resource_type == 'motor':
            return self.__allocate_axis(actor_name, module_info)

    def __allocate_piston(self, module_info):
        output_pattern = compile('.*_output$')
        input_pattern = compile('.*_input$')
        require = {'DO': [], 'DI': []}
        for key, val in module_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                require['DO'].append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                require['DI'].append(val)
        ret = self.__resource_check(require)
        if ret:
            self.__logger.error(ret)
            return ret
        else:
            return Piston(self.__motion, module_info, self.__bulletin)

    def __allocate_axis(self, actor_name, module_info):
        for axis in module_info:
            require = {'DO': [], 'DI': [], 'AXIS': []}
            if axis['motor_type'] == 'servo_type':             
                require['DO'].append(axis['ABSM'])
                require['DO'].append(axis['ABSR'])
                require['DI'].append(axis['TLC'])
                require['DI'].append(axis['DO1'])
                require['DI'].append(axis['ZSP'])
                require['AXIS'].append(axis['axis_id'])
            ret = self.__resource_check(require)
            if ret:
                self.__logger.error(ret)
                return ret
        return Motor(actor_name, self.__motion, module_info, self.__bulletin)
            
    def __resource_check(self, require):
        if 'DO' in require:
            for port in require['DO']:
                if self.__do_in_service[port]:
                    msg = 'DO port {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__do_in_service[port] = 1
        if 'DI' in require:
            for port in require['DI']:
                if self.__di_in_service[port]:
                    msg = 'DI port {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__di_in_service[port] = 1
        if 'AXIS' in require:
            for port in require['AXIS']:
                if self.__axis_in_service[port]:
                    msg = 'AXIS {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__axis_in_service[port] = 1
        return 0
    