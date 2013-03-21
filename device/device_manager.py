# -- coding: utf-8 --

# Title          : device_manager.py
# Description    : the role who manages the all I/O device
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

from pprint import pprint
from re import compile
from masbot.config.global_settings import *
from masbot.device.motion.adlink_fake import ADLinkMotion as Motion
from masbot.device.piston import Piston

class DeviceManager(object):
    _instance = None
    # singleton: to guarantee there is only one instance
    def __new__(cls):
        if not DeviceManager._instance:
            DeviceManager._instance = object.__new__(cls)
            cls._initial(cls)
        return DeviceManager._instance

    def _initial(self):
        self.motion = Motion(io_card_info)
        di_count = self.motion.di_card_count() * 32
        do_count = self.motion.do_card_count() * 32
        axis_count = len(motor_info)
        self._di_in_service = [0] * di_count
        self._do_in_service = [0] * do_count
        self._axis_in_service = [0] * axis_count
        #self.serial_in_service = [0] * serial_count
        
    def resource_status(self):
        resource = {}
        resource['DI'] = self._di_in_service
        resource['DO'] = self._do_in_service
        resource['AXIS'] = self._axis_in_service
        return resource

    def request(self, module_info={}):
        if module_info['device_type'] == 'piston':
            return self._allocate_piston(module_info)
            
    def _allocate_piston(self, module_info):
        output_pattern = compile('.*_output$')
        input_pattern = compile('.*_input$')
        require = {'DO': [], 'DI': []}
        for key, val in module_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                require['DO'].append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                require['DI'].append(val)
        ret = self._resource_check(require)
        print(require)
        if ret:
            print(ret)
            return ret
        else:
            return Piston(self.motion, module_info)
        
    def _resource_check(self, resource):
        if 'DO' in resource:
            for port in resource['DO']:
                if self._do_in_service[port]:
                    return 'DO port {} is occupied'.format(port)
                else:
                    self._do_in_service[port] = 1
        if 'DI' in resource:
            for port in resource['DI']:
                if self._di_in_service[port]:
                    return 'DI port {} is occupied'.format(port)
                else:
                    self._di_in_service[port] = 1
        if 'AXIS' in resource:
            for port in resource['AXIS']:
                if self._axis_in_service[port]:
                    return 'AXIS {} is occupied'.format(port)
                else:
                    self._axis_in_service[port] = 1
        return 0
    