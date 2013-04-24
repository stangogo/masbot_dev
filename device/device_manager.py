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
        self.__adlink = ADLink(io_card_info['ADLink'])
        # temp method to detect axis count
        self.__adlink_axis_count = len(axis_map)
        self.__adlink_di_in_service = [0] * self.__adlink.di_count()
        self.__adlink_do_in_service = [0] * self.__adlink.do_count()
        self.__adlink_axis_in_service = [0] * self.__adlink_axis_count

        self.__lplink = LPLink(io_card_info['LPLink'])
        # temp method to detect axis count
        self.__lplink_axis_count = len(axis_map)
        self.__lplink_di_in_service = [0] * self.__lplink.di_count()
        self.__lplink_do_in_service = [0] * self.__lplink.do_count()
        self.__lplink_axis_in_service = [0] * self.__lplink_axis_count
        #self.serial_in_service = [0] * serial_count

        self.__resource_map = {
            'ADLink_DO': {'count': self.__adlink.do_count()},
            'ADLink_DI': {'count': self.__adlink.di_count()},
            'ADLink_AXIS': {'count': 16},
            'LPLink_DO': {'count': self.__lplink.do_count()},
            'LPLink_DI': {'count': self.__lplink.di_count()},
            'LPLink_AXIS': {'count': 30},
            'LPMax_DO': {'count': 0},
            'LPMax_DI': {'count': 0},
            'LPMax_AXIS': {'count': 0},
            'RS232': {'count': 2},
            'Camera_1394': {'count': 10},
            'Camera_USB': {'count': 0},
        }
        
    def get_resource_map(self):
        return self.__resource_map
            
    def _get_device_proxy(self):
        proxy = {}
        proxy['ADLink'] = self.__adlink
        proxy['LPLink'] = self.__lplink
        #proxy['LPMax'] = self.__lpmax
        return proxy

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
        from pprint import pprint
        if actor_type == 'piston':
            return self.__allocate_piston(actor_info, actor_type)
        elif actor_type == 'motor':
            return self.__allocate_axis(actor_info, actor_type)

    def __allocate_piston(self, actor_info, actor_type):
        output_pattern = compile('^output[0-9]$')
        input_pattern = compile('^input[0-9]$')
        mod_type = actor_info['module_type']
        do_module = "{}_DO".format(mod_type)
        di_module = "{}_DI".format(mod_type)
        require = {do_module: [], di_module: []}
        for key, val in actor_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                require[do_module].append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                require[di_module].append(val)
        ret = self.__resource_check(actor_info['key'], require)
        if ret:
            return ret
        if mod_type == 'ADLink':
            io_card = self.__adlink
        elif mod_type == 'LPLink':
            io_card = self.__lplink
        elif mod_type == 'LPMax':
            io_card = None
            #io_card = self.__lpmax
        else:
            msg = "unknown module type: {}".format(mod_type)
            self.__logger.critical(msg)
            return msg
        return Piston(io_card, actor_info, self.__bulletin)

    def __allocate_axis(self, actor_info, actor_type):
        mod_type = actor_info['module_type']
        do_module = "{}_DO".format(mod_type)
        di_module = "{}_DI".format(mod_type)
        axis_module = "{}_AXIS".format(mod_type)
        require = {do_module: [], di_module: [], axis_module: []}
        if mod_type == 'ADLink':
            for axis in actor_info['axis_info']:
                if axis['motor_type'] == 'servo':             
                    require[do_module].append(axis['ABSM'])
                    require[do_module].append(axis['ABSR'])
                    require[di_module].append(axis['DO1'])
                    require[di_module].append(axis['ZSP'])
                    require[di_module].append(axis['TLC'])
                    require[axis_module].append(axis['axis_id'])
            ret = self.__resource_check(actor_info['key'], require)
            if ret:
                return ret
            else:
                io_card = self.__adlink
        elif mod_type == 'LPLink':
            for axis in actor_info['axis_info']:
                if axis['motor_type'] == 'servo':             
                    require[axis_module].append(axis['axis_id'])
            ret = self.__resource_check(actor_info['key'], require)
            if ret:
                return ret
            else:
                io_card = self.__lplink
        elif mod_type == 'LPMax':
            pass
        else:
            msg = "unknown module type {}".format(mod_type)
            self.__logger.critical(msg)
            return msg
        return Motor(actor_info, io_card, self.__bulletin)
            
    def __resource_check(self, actor_name, require):
        for resource_type, resource_list in require.items():
            for port in resource_list:
                # check max port
                max_port = self.__resource_map[resource_type]['count']
                if port >= max_port:
                    msg = "{} required {} {} that exceed max port {}".format(
                        actor_name,
                        resource_type,
                        port,
                        max_port
                    )
                    self.__logger.error(msg)
                    return msg
                # check if the port is occupied
                if port in self.__resource_map[resource_type]:
                    msg = "{} required {} {}, but it was occupied by {}".format(
                        actor_name,
                        resource_type,
                        port,
                        self.__resource_map[resource_type][port]
                    )
                    self.__logger.error(msg)
                    return msg
                else:
                    self.__resource_map[resource_type][port] = actor_name
