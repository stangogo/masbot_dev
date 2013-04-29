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
    from masbot.device.motion.adlink_fake import ADLink as ADLink8154
    from masbot.device.motion.adlink_fake import ADLink as ADLink8158
    from masbot.device.motion.lplink_fake import LPLink
    #from masbot.device.camera.camera_fake import Camera
else:
    from masbot.device.motion.adlink import ADLink8154
    from masbot.device.motion.adlink import ADLink8158
    #from masbot.device.motion.lplink import LPLink
    from masbot.device.motion.lplink_fake import LPLink
from masbot.device.piston import Piston
from masbot.device.motor import Motor
from masbot.device.camera_module import CameraModule

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
        self.__adlink8154 = ADLink8154(io_card_info['8154'])
        self.__adlink8158 = ADLink8158(io_card_info['8158'])
        self.__lplink = LPLink(io_card_info['LPLink'])
        #self.__lpmax = LPMax(io_card_info['LPMax'])

        self.__resource_map = {
            '8154_DO': {'count': self.__adlink8154.do_count()},
            '8154_DI': {'count': self.__adlink8154.di_count()},
            '8154_AXIS': {'count': self.__adlink8154.axis_count()},
            '8158_DO': {'count': self.__adlink8158.do_count()},
            '8158_DI': {'count': self.__adlink8158.di_count()},
            '8158_AXIS': {'count': self.__adlink8158.axis_count()},
            'LPLink_DO': {'count': self.__lplink.do_count()},
            'LPLink_DI': {'count': self.__lplink.di_count()},
            'LPLink_AXIS': {'count': 30},
            'LPMax_DO': {'count': 0},
            'LPMax_DI': {'count': 0},
            'LPMax_AXIS': {'count': 0},
            'RS232': {'count': 2},
            'Camera_1394': {'count': 10},
            'Camera_USB2': {'count': 10},
        }
        
    def get_resource_map(self):
        return self.__resource_map
            
    def _get_device_proxy(self):
        proxy = {
            '8154': self.__adlink8154,
            '8158': self.__adlink8158,
            'LPLink': self.__lplink,
            #'LPMax': self.__lpmax,
        }

        return proxy

    def request(self, actor_info, actor_type):
        """ request DM for a modoule
        
        Example:
            piston
            
        Args:
            actor_info(dict): resource infomation
            actor_type(string): motor, piston, camera, stock
        
        Returns:
            None

        Raises:
        
        """
        if actor_type == 'piston':
            return self.__allocate_piston(actor_info, actor_type)
        elif actor_type == 'motor':
            return self.__allocate_axis(actor_info, actor_type)
        elif actor_type == 'camera_module':
            return self.__allocate_camera_module(actor_info, actor_type)
        else:
            return None

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
        if mod_type == '8154':
            io_card = self.__adlink8154
        elif mod_type == '8158':
            io_card = self.__adlink8158
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
        ADLink_pattern = compile('^8[1-2]5[4,8]')
        mod_type = actor_info['module_type']
        do_module = "{}_DO".format(mod_type)
        di_module = "{}_DI".format(mod_type)
        axis_module = "{}_AXIS".format(mod_type)
        require = {do_module: [], di_module: [], axis_module: []}
        if ADLink_pattern.match(mod_type):
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
            elif mod_type == '8154':
                io_card = self.__adlink8154
            elif mod_type == '8158':
                io_card = self.__adlink8158
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
    
    def __allocate_camera_module(self, actor_info, actor_type):
        #output_pattern = compile('^output[0-9]$')
        #input_pattern = compile('^input[0-9]$')        
        try:
            mod_type = actor_info['camera_set']['camera_type']
        except:
            mod_type = None   
        if mod_type == '1394IIDC':
            camera_module = 'Camera_1394'
        elif mod_type == 'Directshow':
            camera_module = 'Camera_USB2'
        else:
            camera_module = None
        #do_module = "{}_DO".format(mod_type)
        #di_module = "{}_DI".format(mod_type)
        #require = {do_module: [], di_module: []}
        require = {camera_module:[actor_info['camera_set']['port']]}#do_module: [], di_module: []}
        #for key, val in actor_info.items():
        #    if output_pattern.match(key) and isinstance(val, int):
        #        require[do_module].append(val)
        #    elif input_pattern.match(key) and isinstance(val, int):
        #        require[di_module].append(val)
        ret = self.__resource_check(camera_module, require)
        if ret:
            return ret
        #if mod_type == 'ADLink':
            #io_card = self.__adlink
        #elif mod_type == 'LPLink':
            #io_card = self.__lplink
        #elif mod_type == 'LPMax':
            #io_card = None
            #io_card = self.__lpmax
        #else:
            #msg = "unknown module type: {}".format(mod_type)
            #self.__logger.critical(msg)
            #return msg
        return CameraModule(actor_info, self.__bulletin)        
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
