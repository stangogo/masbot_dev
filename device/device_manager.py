# -- coding: utf-8 --

# Title          : device_manager.py
# Description    : the role who manages the all I/O device
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

from pprint import pprint
from masbot.config.global_settings import *
from masbot.motion.adlink_fake import ADLinkMotion as Motion

class DeviceManager(object):
    _instance = None
    # singleton: to guarantee there is only on instance
    def __new__(cls):
        if not DeviceManager._instance:
            DeviceManager._instance = object.__new__(cls)
            cls.initial(cls)
        return DeviceManager._instance

    def initial(self):
        self.motion = Motion(io_card_cfg)
        di_count = self.motion.di_card_count() * 32
        do_count = self.motion.do_card_count() * 32
        axis_count = len(axis_cfg)
        self.di_in_service = [0] * di_count
        self.do_in_service = [0] * do_count
        self.axis_in_service = [0] * axis_count
        #self.serial_in_service = [0] * serial_count
        
    def resource_status(self):
        resource = {}
        resource['DI'] = self.di_in_service
        resource['DO'] = self.do_in_service
        resource['AXIS'] = self.axis_in_service
        return resource

    def request(self, resource={}):
        for type, port_list in resource.items():
            if type == 'DI':
                self.allocate_di(port_list)
            elif type == 'DO':
                self.allocate_do(port_list)
            elif type == 'AXIS':
                self.allocate_axis(port_list)

    def allocate_di(self, port_list):
        for port in port_list:
            if self.di_in_service[port]:
                raise IOError('DI port {} is in use'.format(port))
            else:
               self.di_in_service[port] = 1
        
    def allocate_do(self, port_list):
        for port in port_list:
            if self.do_in_service[port]:
                raise IOError('DO port {} is in use'.format(port))
            else:
               self.do_in_service[port] = 1
    
    def allocate_axis(self, port_list):
        for port in port_list:
            if self.axis_in_service[port]:
                raise IOError('AXIS {} is in use'.format(port))
            else:
               self.axis_in_service[port] = 1

DM = DeviceManager()
resource = {'DI': [0,1,2], 'DO': [0,1], 'AXIS': [0]}
DM.request(resource)
resource = {'DI': [3,4,5], 'DO': [2,3], 'AXIS': [1]}
DM.request(resource)