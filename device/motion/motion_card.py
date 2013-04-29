# -*- coding: utf-8 -*-

# Title          : motion_card.py
# Description    : motion abstract class
# Author         : Stan Liu
# Date           : 20130307
# Dependency     : 
# usage          : class SomeMotion(Motion):
#                    pass
# notes          : 

from abc import ABCMeta, abstractmethod

class Motion(metaclass=ABCMeta):
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def DO(self, port, state):
        pass

    @abstractmethod
    def DO_read(self, port):
        pass

    @abstractmethod
    def DI(self, port):
        pass

    @abstractmethod
    def servo_on_off(self, axis_id, on_off):
        pass

    @abstractmethod
    def get_motion_status(self, axis_id):
        pass

    @abstractmethod
    def get_pulse(self, axis_id):
        pass

    @abstractmethod
    def set_position(self, axis_id, position):
        pass

    @abstractmethod
    def emg_stop(self, axis_id):
        pass

    @abstractmethod
    def do_count(self):
        pass

    @abstractmethod
    def di_count(self):
        pass

    @abstractmethod
    def home_search(self, axis_id, speed, acc_time, ORG_offset):
        pass
        