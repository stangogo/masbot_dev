# -- coding: utf-8 --

# Title          : piston.py
# Description    : piston feature with Operating On/Off
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

class Piston(object):
    def __init__(self, io_card, do_list, di_list):
        self._io_card = io_card
        self._do_list = do_list
        self._di_list = di_list
        self._detect_type()

    def _detect_type(self):
        do_count = len(self._do_list)
        di_count = len(self._di_list)
        self.type = "{}_out_{}_in".format(do_count, di_count)

    def react(self, state):
        if self.type == '1_out_1_in':
            return self._react_1_out_1_in(state)
        elif self.type == '1_out_2_in':
            return self._react_1_out_2_in(state)
        elif self.type == '1_out_4_in':
            return self._react_1_out_4_in(state)
        elif self.type == '2_out_2_in':
            return self._react_2_out_2_in(state)
        else:
            exception_msg = "piston type is {}".format(self.type)
            raise TypeError(exception_msg)
       
    def get_do_status(self):
        if self.type == '2_out_2_in':
            do_status = []
            for port in self._do_list:
                stat = self._io_card.DO_read(port)
                do_status.append(stat)
            return do_status
        else:
            on_port = self._do_list[0]
            return self._io_card.DO_read(on_port)
        
    def get_di_status(self):
        di_status = []
        for sensor in self._di_list:
            stat = self._io_card.DI(sensor)
            di_status.append(stat)
        return di_status
            
    def _react_1_out_1_in(self, state):
        pass
        
    def _react_1_out_2_in(self, state):
        target_sensor = self._di_list[state]
        if self._io_card.DI(target_sensor):
            return 0
        else:
            on_port = self._do_list[0]
            ret = self._io_card.DO(on_port, state) 
            if ret:
                return ret
            if self._io_card.check_sensor(target_sensor):
                return 0
        
    def _react_1_out_4_in(self, state):
        pass

    def _react_2_out_2_in(self, state):
        pass
        