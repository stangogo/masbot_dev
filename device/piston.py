# -*- coding: utf-8 -*-

# Title          : piston.py
# Description    : piston feature with Operating On/Off
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : 
# usage          : 
# notes          : 

from re import compile
import logging
from masbot.device.bulletin import Bulletin

class Piston(Bulletin):
    def __init__(self, io_card, module_info, board={}):
        super(Piston, self).__init__(module_info['key'], board)
        self.__logger = logging.getLogger(__name__)
        self.__module_info = module_info
        self.__io_card = io_card
        self.__restrain_IO()
    
    def __restrain_IO(self):
        output_pattern = compile('.*_output$')
        input_pattern = compile('.*_input$')
        self.__do_list = []
        self.__di_list = []
        for key, val in self.__module_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                self.__do_list.append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                self.__di_list.append(val)

    def DO(self, port, state):
        if port in self.__do_list:
            return self.__io_card.DO(port, state)
        else:
            msg = 'it is not allowed to access DO {}'.format(port)
            self.__logger.error(msg)
            return msg

    def DI(self, port):
        if port in self.__di_list:
            return self.__io_card.DI(port)
        else:
            msg = 'it is not allowed to access DI {}'.format(port)
            self.__logger.error(msg)
            return msg

    def DO_read(self, port):
        if port in self.__do_list:
            return self.__io_card.DO_read(port)
        else:
            msg = 'it is not allowed to access DO {}'.format(port)
            self.__logger.error(msg)
            return msg

        