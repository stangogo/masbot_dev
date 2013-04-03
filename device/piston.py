# -*- coding: utf-8 -*-

# Title          : piston.py
# Description    : piston feature with Operating On/Off
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

import logging
from re import compile
from masbot.device.bulletin import Bulletin

class Piston(Bulletin):
    def __init__(self, io_card, module_info, board):
        super(Piston, self).__init__(module_info['key'], board)
        self.__logger = logging.getLogger(__name__)
        self.__io_card = io_card
        self.__module_info = module_info
        self.__detect_type()
        
    def __detect_type(self):
        """ detect which piston type (ex. 1 output and 2 input)
        
            [existing types]
            1 output 1 input
            1 output 2 input
            1 output 4 input
            2 output 2 input
        
        Example:
            it is a private member function
        Args:
            None
        Returns:
            None
        Raises:
            
        """
        output_pattern = compile('.*_output$')
        input_pattern = compile('.*_input$')
        self.__do_list = []
        self.__di_list = []
        for key, val in self.__module_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                self.__do_list.append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                self.__di_list.append(val)
        self.__type = "{}_out_{}_in".format(len(self.__do_list), len(self.__di_list))
        self.__state = self.detect_state()

    def detect_state(self):
        """ detect current state (0 means OFF, 1 means ON)
        
        Example:
            some_piston.detect_state()
        Args:
            None
        Returns:
            0: OFF
            1: ON
        Raises:
            
        """
        # correspond to the funtion by piston type
        if self.__type == '1_out_1_in':
            o_port = self.__module_info['1st_output']
            i_port = self.__module_info['1st_input']
            o_status = self.__io_card.DO_read(o_port)
            i_status = self.__io_card.DI(i_port)
            if i_status == 1 and o_status == 0:
                return 0
            elif i_status == 0 and o_status == 1:
                return 1
        elif self.__type == '1_out_2_in':
            o_port = self.__module_info['1st_output']
            i_port1 = self.__module_info['1st_input']
            i_port2 = self.__module_info['2nd_input']
            o_status = self.__io_card.DO_read(o_port)
            i_status1 = self.__io_card.DI(i_port1)
            i_status2 = self.__io_card.DI(i_port2)
            if i_status1 == 1 and i_status2 == 0 and o_status == 0:
                return 0
            elif i_status1 == 0 and i_status2 == 1 and o_status == 1:
                return 1
        elif self.__type == '1_out_4_in':
            pass
        elif self.__type == '2_out_2_in':
            pass
        else:
            exception_msg = "piston type is {}".format(self.__type)
            raise TypeError(exception_msg)
        # non-define state when running here
        #self.__logger.error('piston is on non-define state')
        return -1

    def action(self, state, timeout=5000):
        """ correspond to the funtion by piston type
        """
        if self.detect_state() == state:
            return 0
        if self.__type == '1_out_1_in':
            return self.__action_1_out_1_in(state, timeout)
        elif self.__type == '1_out_2_in':
            return self.__action_1_out_2_in(state, timeout)
        elif self.__type == '1_out_4_in':
            return self.__action_1_out_4_in(state, timeout)
        elif self.__type == '2_out_2_in':
            return self.__action_2_out_2_in(state, timeout)
        else:
            exception_msg = "piston type is {}".format(self.__type)
            raise TypeError(exception_msg)
       
    def get_do_status(self):
        do_status = []
        for port in self.__do_list:
            stat = self.__io_card.DO_read(port)
            do_status.append(stat)
        if self.__type == '2_out_2_in':
            return do_status
        else:
            return do_status[0]

    def get_di_status(self):
        di_status = []
        for port in self.__di_list:
            stat = self.__io_card.DI(port)
            di_status.append(stat)
        return di_status
            
    def __action_1_out_1_in(self, state, timeout):
        action_port = self.__module_info['1st_output']
        ret = self.__io_card.DO(action_port, state)
        if ret:
            return ret
        # check if sensor in position
        on_off = state & 1
        target_sensor = self.__module_info['1st_input']
        ret = self.__io_card.check_sensor(target_sensor, timeout, on_off)
        if ret:
            return ret
        # check if piston state is matched
        if self.detect_state() == state:
            return 0
        else:
            return -1
        
    def __action_1_out_2_in(self, state, timeout):
        action_port = self.__module_info['1st_output']
        ret = self.__io_card.DO(action_port, state) 
        if ret:
            return ret
        # check if sensor in position
        sensor_text = '2nd_input' if state else '1st_input'
        target_sensor = self.__module_info[sensor_text]
        ret = self.__io_card.check_sensor(target_sensor, timeout)
        if ret:
            return ret
        # check if piston state is matched
        if self.detect_state() == state:
            return 0
        else:
            return -1
        
    def __action_1_out_4_in(self, state, timeout):
        pass

    def __action_2_out_2_in(self, state, timeout):
        pass
        