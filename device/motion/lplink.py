# -*- coding: utf-8 -*-

# Title          : lplink.py
# Description    : calling functions in ftd2xx.dll
# Author         : Stan Liu
# Date           : 20130430
# Dependency     : motion.py ftd2xx_dll.py
# usage          : 
# notes          : 

from masbot.config.common_lib import *
import logging
from time import sleep
from os.path import isfile, getsize
from os import stat

from masbot.device.channel import Channel
from masbot.device.motion.motion_card import Motion
from masbot.device.motion.ftd2xx_dll import *
from masbot.device.motion.ftd2xx_table import *

class LPLink(Channel, Motion):
    def __init__(self, cards_config=[]):
        super(LPLink, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__initial(cards_config)

    def __del__(self):
        self.close()

    def __initial(self, cards_config):
        """ 
        
        Example:
            
        Args:
                    
        Returns:
            
        Raises:
        
        """
        self.__logger.debug('LPLink card initial')
        # the format is byte
        self.SNA = b"FTWIQLXYA"
        self.SNB = b"FTWIQLXYB"
        self.__passive_serial_download()
        self.__logger.debug('LPLink rbf download ok')

    def __passive_serial_download(self):
        self.__ft_handle = c_void_p()
        ret = self.run(d2xx.FT_OpenEx, self.SNB, 1, self.__ft_handle)
        if ret:
            msg = "FT_OpenEx {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_ResetDevice, self.__ft_handle)
        if ret:
            msg = "FT_ResetDevice {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_SetUSBParameters, self.__ft_handle, 65536, 65536)
        if ret:
            msg = "FT_SetUSBParameters {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_SetChars, self.__ft_handle, 0, 0, 0, 0)
        if ret:
            msg = "FT_SetChars {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_SetTimeouts, self.__ft_handle, 500, 500)
        if ret:
            msg = "FT_SetTimeouts {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_SetLatencyTimer, self.__ft_handle, 2)
        if ret:
            msg = "FT_SetLatencyTimer {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_SetFlowControl, self.__ft_handle, FT_FLOW_RTS_CTS, 0, 0)
        if ret:
            msg = "FT_SetFlowControl {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        ret = self.run(d2xx.FT_SetBitMode, self.__ft_handle, 0, 0)
        if ret:
            msg = "FT_SetBitMode {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg

        send_size = pointer(c_ulong(0))
        buffer_size = 3
        TxBuffer = (c_ubyte * buffer_size)()
        
        # set up the hi-speed specific command for the ftx232h
        TxBuffer[0] = 0x8A
        TxBuffer[1] = 0x97
        TxBuffer[2] = 0x8D
        ret = self.run(d2xx.FT_Write, self.__ft_handle, TxBuffer, 3, send_size)
        if ret:
            msg = "FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg

        # set tck frequency
        TxBuffer[0] = 0x86
        TxBuffer[1] = 0x04
        TxBuffer[2] = 0x00
        ret = self.run(d2xx.FT_Write, self.__ft_handle, TxBuffer, buffer_size, send_size)
        if ret:
            msg = "FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg

        # set initial states of the mpsse interface
        # low byte
        TxBuffer[0] = 0x80
        TxBuffer[1] = 0xFA
        TxBuffer[2] = 0xD3
        ret = self.run(d2xx.FT_Write, self.__ft_handle, TxBuffer, buffer_size, send_size)
        if ret:
            msg = "FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg

        # high byte
        TxBuffer[0] = 0x82
        TxBuffer[1] = 0xFF
        TxBuffer[2] = 0xFF
        ret = self.run(d2xx.FT_Write, self.__ft_handle, TxBuffer, buffer_size, send_size)
        if ret:
            msg = "FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg

        # clear nConfig
        TxBuffer[0] = 0x80
        TxBuffer[1] = 0xEA
        TxBuffer[2] = 0xD3
        ret = self.run(d2xx.FT_Write, self.__ft_handle, TxBuffer, buffer_size, send_size)
        if ret:
            msg = "FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        sleep(0.01)

        # set nConfig
        TxBuffer[0] = 0x80
        TxBuffer[1] = 0xFA
        TxBuffer[2] = 0xD3
        ret = self.run(d2xx.FT_Write, self.__ft_handle, TxBuffer, buffer_size, send_size)
        if ret:
            msg = "FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        sleep(0.01)

        # read rbf file
        rbf_file_name = "LPLinkG2.rbf"
        abs_path = __file__ + "/../FPGA/{}".format(rbf_file_name)
        rbf_file = isfile(abs_path)
        if not rbf_file:
            msg = "not found {}".format(abs_path)
            self.__logger.critical(msg)
            return msg
        byte_count = getsize(abs_path)
        divide_count = int(byte_count / 65536)
        remainder = int(byte_count % 65536)
        
        rbf_raw = (c_ubyte * 500001)()
        rbf_buf = (c_ubyte * 65539)()
        #with open("myfile", "rb") as f:
        #    byte = f.read(1)
        #    while byte:
        #        rbf_raw    
        
        for i in range(divide_count+1):
            if i == divide_count:
                if remainder:
                    rbf_buf[0] = 0x19
                    rbf_buf[1] = (remainder - 1) % 256
                    rbf_buf[2] = (remainder - 1) >> 8
                    for j in range(remainder):
                        rbf_buf[j+3] = rbf_raw[i * 65536 + j]
                    ret = self.run(d2xx.FT_Write, self.__ft_handle, rbf_buf, remainder+3, send_size)
                    if ret:
                        msg = "Write rbf in divide count, FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
                        self.__logger.critical(msg)
                        return msg
            else:
                rbf_buf[0] = 0x19
                rbf_buf[1] = 255
                rbf_buf[0] = 255
                for j in range(65536):
                    rbf_buf[j+3] = rbf_raw[i * 65536 + j]
                ret = self.run(d2xx.FT_Write, self.__ft_handle, rbf_buf, 65536+3, send_size)
                if ret:
                    msg = "Write rbf others, FT_Write {}: {}".format(self.SNB, FT_STATUS[ret])
                    self.__logger.critical(msg)
                    return msg
        sleep(0.1)
        ret = self.run(d2xx.FT_SetBitMode, self.__ft_handle, 0, 0)
        if ret:
            msg = "FT_SetBitMode {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        
        ret = self.run(d2xx.FT_Close, self.__ft_handle)
        if ret:
            msg = "FT_Close {}: {}".format(self.SNB, FT_STATUS[ret])
            self.__logger.critical(msg)
            return msg
        sleep(0.2)

    def move(self):
        index = 3
        distance_pulse = 500
        verlocity_pps = 200
        
        opcode_motor_set = 42
        opcode_motor_run = 46
        max_pulse = 1000000000
        max_acc_step = 1023
        clock_rate = 48000000
        min_velocity = 0.1
        max_velocity = 1000000
        if index < 0 and index > 24:
            return "FUNCTION_PARAMETER_ERROR"
        if abs(distance_pulse):
            return "FUNCTION_PARAMETER_ERROR"
        if velocity_pps < min_velocity and velocity > max_velocity:
            return "FUNCTION_PARAMETER_ERROR"

        pulse = abs(distance_pulse)
        ccw = distance_pulse < 0
        #step_clock = 
        
    def close(self):
        """ close the pci card
        """
        pass

    def refresh(self, card_config):
        self.close()
        self.__initial(card_config)
        
    def do_count(self):
        return 0

    def di_count(self):
        return 0

    def axis_count(self):
        return 30
    
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
        
    def relative_move(self, axis_list, speed, timeout=5000, Tacc=0.2, Tdec=0.2, SVacc=-1, SVdec=-1):
        """ single/multiple axis move relatively
        """
        pass

    def absolute_move(self, axis_list, speed, timeout=5000, Tacc=0.3, Tdec=0.3, SVacc=-1, SVdec=-1):
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

    def set_inp(self, axis, inp_enable, inp_logic=0):
        pass

motion = LPLink()
