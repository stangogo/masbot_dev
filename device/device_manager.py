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
from masbot.config.gather_data import *
# hardware detecttion
if hardware_simulation:
    from masbot.device.motion.adlink_fake import ADLink
    from masbot.device.motion.lplink_fake import LPLink
else:
    from masbot.device.motion.adlink import ADLink
    #from masbot.device.motion.lplink import LPLink
    from masbot.device.motion.lplink_fake import LPLink
from masbot.device.piston import Piston
from masbot.device.motor import Motor
from masbot.device import camera


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
        # ADLink Resource
        if 'ADLink' not in io_card_info:
            io_card_info['ADLink'] = []
        self.__adlink = ADLink(io_card_info['ADLink'])
        self.__adlink_di_count = self.__adlink.di_card_count() * 32
        self.__adlink_do_count = self.__adlink.do_card_count() * 32
        self.__adlink_axis_count = len(motor_info)
        self.__adlink_di_in_service = [0] * self.__adlink_di_count
        self.__adlink_do_in_service = [0] * self.__adlink_do_count
        self.__adlink_axis_in_service = [0] * self.__adlink_axis_count
        # LPLink Resource
        if 'LPLink' not in io_card_info:
            io_card_info['LPLink'] = []
        self.__lplink = LPLink(io_card_info['LPLink'])
        self.__lplink_di_count = self.__lplink.di_card_count() * 8
        self.__lplink_do_count = self.__lplink.do_card_count() * 8
        self.__lplink_axis_count = len(motor_info)
        self.__lplink_di_in_service = [0] * self.__lplink_di_count
        self.__lplink_do_in_service = [0] * self.__lplink_do_count
        self.__lplink_axis_in_service = [0] * self.__lplink_axis_count
        #self.serial_in_service = [0] * serial_count

    def _get_total_resource(self):
        resource = {}
        resource['ADLink'] = [self.__adlink_do_count,
                            self.__adlink_di_count,
                            self.__adlink_axis_count]
        resource['LPLink'] = [self.__lplink_do_count,
                            self.__lplink_di_count,
                            self.__lplink_axis_count]
        #resource['LPMax'] = [self.__lpmax_do_count,
        #                    self.__lpmax_di_count,
        #                    self.__lpmax_axis_count]
        return resource
            
    def _get_device_proxy(self, module):
        if module == 'ADLink':
            return self.__adlink
        elif module == 'LPLink':
            return self.__lplink
        else:
            return None

    def resource_status(self):
        resource = {'ADLink': {}, 'LPLink': {}}
        resource['ADLink']['DI'] = self.__adlink_di_in_service
        resource['ADLink']['DO'] = self.__adlink_do_in_service
        resource['ADLink']['AXIS'] = self.__adlink_axis_in_service
        resource['LPLink']['DI'] = self.__lplink_di_in_service
        resource['LPLink']['DO'] = self.__lplink_do_in_service
        resource['LPLink']['AXIS'] = self.__lplink_axis_in_service
        return resource

    def request(self, actor_info, actor_type):
        """ request DM for a modoule
        
        Example:
            piston
            
        Args:
            actor_info(dict): resource infomation
            actor_type(string): motor or piston...
        
        Returns:
            None

        Raises:
        
        """
        if actor_type == 'piston':
            return self.__allocate_piston(actor_info, actor_type)
        elif actor_type == 'motor':
            return self.__allocate_axis(actor_info, actor_type)

    def __allocate_piston(self, actor_info, actor_type):
        output_pattern = compile('^output[0-9]$')
        input_pattern = compile('^input[0-9]$')
        require = {'DO': [], 'DI': []}
        for key, val in actor_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                require['DO'].append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                require['DI'].append(val)
        ret = self.__resource_check(require)
        if ret:
            self.__logger.error(ret)
            return ret
        if actor_info['module_type'] == 'ADLink':
                motion_hardware = self.__adlink
        elif actor_info['module_type'] == 'LPLink':
            motion_hardware = self.__lplink
        else:
            msg = self.__logger.error("unknown module type %s", 
                actor_info['module_type'])
            return msg
        return Piston(self.__adlink, actor_info, self.__bulletin)

    def __allocate_axis(self, actor_info, actor_type):
        for axis in actor_info['axis_info']:
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
            if actor_info['module_type'] == 'ADLink':
                motion_hardware = self.__adlink
            elif actor_info['module_type'] == 'LPLink':
                motion_hardware = self.__lplink
            else:
                msg = self.__logger.error("unknown module type %s", 
                    actor_info['module_type'])
                return msg
        return Motor(actor_info, motion_hardware, self.__bulletin)
            
    def __resource_check(self, require):
        if 'DO' in require:
            for port in require['DO']:
                if port >= self.__adlink_do_count:
                    msg = 'DO port {} exceeds the max port ({})'.format(
                        port, self.__adlink_do_count)
                    self.__logger.error(msg)
                    return msg
                elif self.__adlink_do_in_service[port]:
                    msg = 'DO port {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__adlink_do_in_service[port] = 1
        if 'DI' in require:
            for port in require['DI']:
                if port >= self.__adlink_di_count:
                    msg = 'DI port {} exceeds the max port ({})'.format(
                        port, self.__adlink_di_count)
                    self.__logger.error(msg)
                    return msg
                elif self.__adlink_di_in_service[port]:
                    msg = 'DI port {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__adlink_di_in_service[port] = 1
        if 'AXIS' in require:
            for port in require['AXIS']:
                if port >= self.__adlink_axis_count:
                    msg = 'AXIS id {} exceeds the max port ({})'.format(
                        port, self.__adlink_axis_count)
                    self.__logger.error(msg)
                    return msg
                elif self.__adlink_axis_in_service[port]:
                    msg = 'AXIS {} was occupied'.format(port)
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__adlink_axis_in_service[port] = 1
        return 0
    
