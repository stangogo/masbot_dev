# -*- coding: utf-8 -*-

# Title          : piston_actor.py
# Description    : piston actor with action and detecting status
# Author         : Stan Liu
# Date           : 20130320
# Dependency     : pykka
# usage          : 
# notes          : 

from re import compile
from time import sleep
import logging
import pykka
from masbot.device.device_manager import DeviceManager

class PistonActor(pykka.ThreadingActor):
    def __init__(self, actor_info):
        """ initial the Piston as an Actor
        
        Example:
            None
            
        Args:
            actor_info(dict): resource infomation includes all DOs and DIs
        
        Returns:
            None

        Raises:
        
        """
        super(PistonActor, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__state = 'ready'
        DM = DeviceManager()
        self.__piston_obj = DM.request(actor_info['key'], actor_info, 'piston', 'ADLink')
        self.__actor_info = actor_info
        self.__detect_type()
        
    def on_receive(self, message):
        # action on
        msg = message.get('msg')
        if msg == 'state':
            message['reply_to'].set(self.__state)
        elif msg == 'action_on':
            self.__state = 'actioning'
            if 'timeout' in message:
                timeout = message.get('timeout')
                ret = self.action(1, timeout)
            else:
                ret = self.action(1)
            
        # action off
        elif msg == 'action_off':
            self.__state = 'actioning'
            if 'timeout' in message:
                timeout = message.get('timeout')
                ret = self.action(0, timeout)
            else:
                ret = self.action(0)
        # sensor status
        elif msg == 'sensor_status':
            ret = self.get_di_status()
        # action status
        elif msg == 'action_status':
            ret = self.get_do_status()
        else:
            ret = 'undefine message format'
            self.__logger.debug(ret)
        # message response
        message['reply_to'].set(ret)

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
        for key, val in self.__actor_info.items():
            if output_pattern.match(key) and isinstance(val, int):
                self.__do_list.append(val)
            elif input_pattern.match(key) and isinstance(val, int):
                self.__di_list.append(val)
        self.__type = "{}_out_{}_in".format(len(self.__do_list), len(self.__di_list))

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
            o_port = self.__actor_info['1st_output']
            i_port = self.__actor_info['1st_input']
            o_status = self.__piston_obj.DO_read(o_port)
            i_status = self.__piston_obj.DI(i_port)
            if i_status == 1 and o_status == 0:
                return 0
            elif i_status == 0 and o_status == 1:
                return 1
        elif self.__type == '1_out_2_in':
            o_port = self.__actor_info['1st_output']
            i_port1 = self.__actor_info['1st_input']
            i_port2 = self.__actor_info['2nd_input']
            o_status = self.__piston_obj.DO_read(o_port)
            i_status1 = self.__piston_obj.DI(i_port1)
            i_status2 = self.__piston_obj.DI(i_port2)
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
            stat = self.__piston_obj.DO_read(port)
            do_status.append(stat)
        if self.__type == '2_out_2_in':
            return do_status
        else:
            return do_status[0]

    def get_di_status(self):
        di_status = []
        for port in self.__di_list:
            stat = self.__piston_obj.DI(port)
            di_status.append(stat)
        return di_status
            
    def __action_1_out_1_in(self, state, timeout):
        action_port = self.__actor_info['1st_output']
        ret = self.__piston_obj.DO(action_port, state)
        if ret:
            return ret
        # check if sensor in position
        on_off = state & 1
        target_sensor = self.__actor_info['1st_input']
        ret = self.__check_sensor(target_sensor, timeout, on_off)
        if ret:
            return ret
        # check if piston state is matched
        if self.detect_state() == state:
            return 0
        else:
            return -1
        
    def __action_1_out_2_in(self, state, timeout):
        action_port = self.__actor_info['1st_output']
        ret = self.__piston_obj.DO(action_port, state) 
        if ret:
            return ret
        # check if sensor in position
        #sensor_text = '2nd_input' if state else '1st_input'
        #target_sensor = self.__actor_info[sensor_text]
        #ret = self.__check_sensor(target_sensor, timeout)
        #if ret:
        #    return ret
        # check if piston state is matched
        #if self.detect_state() == state:
        #    return 0
        #else:
        #    return -1
        
    def __action_1_out_4_in(self, state, timeout):
        pass

    def __action_2_out_2_in(self, state, timeout):
        pass
        
    def __check_sensor(self, port, timeout, on_off=1):
        """ check if sensor is on
        
        Example:
            __check_sensor(12, 200)
            __check_sensor(20, on_off=0)
            
        Args:
            axis(integer): sensor port
            timeout(integer): timeout (ms)
            on_off(0 or 1): expect the sensor is 0 or 1
        
        Returns:
            0: sensor in position
            timeout message

        Raises:
            
        """
        count = 0
        interval = 50
        interval_time = interval / 1000
        while True:
            ret = self.__piston_obj.DI(port)
            if ret == on_off:
                return 0
            else:
                count = count + interval
            if count >= timeout:
                msg = 'expect DI port {} become to {}, timeout = {}'.format(
                    port, on_off, timeout)
                self.__logger.error(msg)
                return msg
            sleep(interval_time)