# -*- coding: utf-8 -*-

# Title          : piston.py
# Description    : piston feature with Operating On/Off
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

from re import compile

class Piston(object):
    def __init__(self, io_card, module_info):
        self._io_card = io_card
        self._module_info = module_info
        self._detect_type()

    def _detect_type(self):
        output_pattern = compile('.*_output$')
        input_pattern = compile('.*_input$')
        self._do_list = []
        self._di_list = []
        for key, val in self._module_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                self._do_list.append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                self._di_list.append(val)
        self._type = "{}_out_{}_in".format(len(self._do_list), len(self._di_list))

    def action(self, state):
        if self._type == '1_out_1_in':
            return self._action_1_out_1_in(state)
        elif self._type == '1_out_2_in':
            return self._action_1_out_2_in(state)
        elif self._type == '1_out_4_in':
            return self._action_1_out_4_in(state)
        elif self._type == '2_out_2_in':
            return self._action_2_out_2_in(state)
        else:
            exception_msg = "piston type is {}".format(self._type)
            raise TypeError(exception_msg)
       
    def get_do_status(self):
        do_status = []
        for port in self._do_list:
            stat = self._io_card.DO_read(port)
            do_status.append(stat)
        if self._type == '2_out_2_in':
            return do_status
        else:
            return do_status[0]

    def get_di_status(self):
        di_status = []
        for port in self._di_list:
            stat = self._io_card.DI(port)
            di_status.append(stat)
        return di_status
            
    def _action_1_out_1_in(self, state):
        pass
        
    def _action_1_out_2_in(self, state):
        if state:
            target_sensor = self._module_info['2nd_input']
        else:
            target_sensor = self._module_info['1st_input']

        if self._io_card.DI(target_sensor):
            return 0
        else:
            on_port = self._module_info['1st_output']
            ret = self._io_card.DO(on_port, state) 
            if ret:
                return ret
            if self._io_card.check_sensor(target_sensor):
                return 0
        
    def _action_1_out_4_in(self, state):
        pass

    def _action_2_out_2_in(self, state):
        pass
        