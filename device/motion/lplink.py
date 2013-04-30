# -*- coding: utf-8 -*-

# Title          : lplink.py
# Description    : calling functions in LPLink.dll
# Author         : Stan Liu
# Date           : 20130410
# Dependency     : motion.py lplink_dll.py
# usage          : 
# notes          : 

import logging
from time import sleep
from masbot.device.motion.motion_card import Motion
from masbot.device.motion.lplink_dll import *
#from masbot.device.motion.adlink_table import *

class LPLink(Motion, Channel):
    def __init__(self, cards_config=[]):
        self.__logger = logging.getLogger(__name__)
        self.__initial()

    def __del__(self):
        #self.close_io_cards()
        #self.close()

    def __initial(self):
        """ 
        
        Example:
            
        Args:
                    
        Returns:
            
        Raises:
        
        """
        self.__logger.debug('LPLink card initial')

    def close(self):
        """ close the pci card
        """
        pass

    def do_count(self):
        return 0

    def di_count(self):
        return 0
        
    def close_io_cards(self):
        """ close all the I/O cards
        """
        pass

    def DO(self, port, state):
        """ write output
        """
        pass

    def DO_read(self, port):
        """ read DO signal
        """
        pass

    def DI(self, port):
        """ read DI signal
        """
        pass

    def servo_on_off(self, axis_id, on_off):
        """ motor servo on/off
        """
        pass
            
    def get_io_status(self, axis_id):
        """ get axis I/O status
        """
        pass

    def get_motion_status(self, axis):
        """ get axis status

        Example:
                        
        Args:
            axis(integer): axis id
        
        Returns:
            
        Raises:
            
        """
        pass

    def get_pulse(self, axis):
        """ Get the value of feedback position counter
        """
        pass

    def set_position(self, axis, position):
        """ Set the feedback position counter
        """
        pass

    def get_command(self, axis):
        """ Get the value of command position counter
        """
        pass

    def set_command(self, axis, command):
        """ Set the command position counter
        """
        pass

    def emg_stop(self, axis):
        """ emergency stop
        """
        pass
        
    def relative_move(self, axis_map, timeout, speed, Tacc=0.3, Tdec=0.3, SVacc=-1, SVdec=-1):
        """ single/multiple axis move relatively
        """
        pass

    def absolute_move(self, axis_map, timeout, speed, Tacc=0.3, Tdec=0.3, SVacc=-1, SVdec=-1):
        """ single/multiple axis move absolutely
        """
        pass

    def wait_motion_ready(self, axis_id, timeout=None, interval=20):
        """ check if motion status is ready
        
        Example:
                        
        Args:
            
        Returns:
            0: ready
            timeout message

        Raises:
            
        """
        pass

    def set_home_config(self, axis, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        """ Set the configuration for home return move motion
        """
        pass

    def home_search(self, axis, speed, acc_time, ORG_offset):
        """ Perform an auto search home

        Example:
            
        Args:
                
        Returns:
            An Integer, the return code

        Raises:
        
        """
        pass

    def sync_pulse(self, axis_info):
        """ update position
        """
        pass

    def __int32(self, x):
        """ to fit the 32 bits format
        """
        pass

    def set_inp(self, axis, inp_enable, inp_logic=0):
        pass

    def check_sensor(self, port, timeout, on_off=1):
        """ check if sensor is on
        
        Example:
                        
        Args:
            
        Returns:
            
        Raises:
            
        """
        pass
        