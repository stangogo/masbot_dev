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
# hardware detecttion
if hardware_simulation:
    from masbot.device.motion.adlink_fake import ADLinkMotion
else:
    from masbot.device.motion.adlink import ADLinkMotion
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
        self.__adlink = ADLinkMotion(io_card_info)
        self.__di_count = self.__adlink.di_card_count() * 32
        self.__do_count = self.__adlink.do_card_count() * 32
        self.__axis_count = len(motor_info)
        self.__di_in_service = [0] * self.__di_count
        self.__do_in_service = [0] * self.__do_count
        self.__axis_in_service = [0] * self.__axis_count
        #self.serial_in_service = [0] * serial_count

    def _device_proxy(self):
        return self.__adlink

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
            return Piston(self.__adlink, module_info, self.__bulletin)

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
        return Motor(actor_name, self.__adlink, module_info, self.__bulletin)
            
    def __resource_check(self, require):
        if 'DO' in require:
            for port in require['DO']:
                if port >= self.__do_count:
                    msg = 'DO port {} exceeds the max port ({})'.format(
                        port, self.__do_count)
                    self.__logger.error(msg)
                    return msg
                elif self.__do_in_service[port]:
                    msg = 'DO port {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__do_in_service[port] = 1
        if 'DI' in require:
            for port in require['DI']:
                if port >= self.__di_count:
                    msg = 'DI port {} exceeds the max port ({})'.format(
                        port, self.__di_count)
                    self.__logger.error(msg)
                    return msg
                elif self.__di_in_service[port]:
                    msg = 'DI port {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__di_in_service[port] = 1
        if 'AXIS' in require:
            for port in require['AXIS']:
                if port >= self.__axis_count:
                    msg = 'AXIS id {} exceeds the max port ({})'.format(
                        port, self.__axis_count)
                    self.__logger.error(msg)
                    return msg
                elif self.__axis_in_service[port]:
                    msg = 'AXIS {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__axis_in_service[port] = 1
        return 0
    
