# -- coding: utf-8 --

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
    def initial(self, manual_id):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def join_io_cards(self):
        pass

    @abstractmethod
    def close_io_cards(self):
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
    def servo_on_off(self, axis, on_off):
        pass

    @abstractmethod
    def get_motion_status(self, axis):
        pass

    @abstractmethod
    def get_pulse(self, axis):
        pass

    @abstractmethod
    def set_position(self, axis, position):
        pass

    @abstractmethod
    def emg_stop(self, axis):
        pass
