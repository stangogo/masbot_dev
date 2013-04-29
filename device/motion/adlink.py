# -*- coding: utf-8 -*-

# Title          : adlink.py
# Description    : calling functions in 8154.dll and 8158.dll of ADLink
# Author         : Stan Liu
# Date           : 20130301
# Dependency     : motion.py adlink_dll.py adlink_table.py
# usage          : import adlink
# notes          : the library detects 8154 or 8158 card automatically

import logging
from time import sleep
from math import log

from masbot.device.channel import Channel
from masbot.device.motion.motion_card import Motion
from masbot.device.motion.adlink_dll import *
from masbot.device.motion.adlink_table import *

# common functions in 8154 and 8158
logger = logging.getLogger(__name__)
def int32(x):
    """ to fit the 32 bits format
    """
    if x > 0xFFFFFFFF:
        raise OverflowError
    # when x is negative
    if x > 0x7FFFFFFF:
        x = int(0x100000000 - x)
        if x < 0x80000000:
            return -x
        else:
            return -2147483648
    return x
        
#============================================================================
# ADLink 8154
#============================================================================
class ADLink8154(Channel, Motion):
    def __init__(self, cards_config=[], manual_id=0):
        super(ADLink8154, self).__init__()
        self.__port_per_card = 32
        self.__initial(cards_config, manual_id)

    def __del__(self):
        self.close()

    def __initial(self, cards_config, manual_id):
        """ detect cardtype automatically, and initial pci card
        
        Example:
            
        Args:
            manual_id(integer): Enable the On board dip switch(SW1) to decide
                the Card ID.
                0 is the sequence of PCI slot.
                1 is on board DIP switch(SW1).
        
        Returns:
            An Integer, the return code

        Raises:
        
        """
        self.__do_cards_index = []
        self.__di_cards_index = []
        self.__motion_card_count = 0

        cardid_inbit = pointer(c_ushort(0))
        ret = self.run(pci_8154._8154_initial, cardid_inbit, manual_id)
        # cardid_inbit:
        #    1 = 0001 means finding 1 card
        #    3 = 0011 means finding 2 cards
        #    7 = 0111 means finding 3 cards
        #    motion card count example:
        #    log(7+1, 2) = 3
        self.__motion_card_count = log(cardid_inbit[0]+1, 2)
        logger.info('ADLink8154 initial, motion card count = %d', self.__motion_card_count)
        ret = self.run(pci_8154._8154_config_from_file)
        logger.debug('8154 read config...ret = %d', ret)
        if len(cards_config) == 0:
            return
        
        # join all the I/O cards from configuration of cards
        live = pointer(c_short(0))
        self.run(pci_8154._8154_db51_HSL_initial, 0)
        self.run(pci_8154._8154_db51_HSL_auto_start, 0)
        self.run(pci_8154._8154_db51_HSL_set_scan_condition, 0, 0, 0)
        for num, type in cards_config:
            self.run(pci_8154._8154_db51_HSL_slave_live, 0, num, live)
            logger.debug('ADLink8154 DB8151 %s %d initial', type, num)
            if type == 'DO':
                self.__do_cards_index.append(num)
            elif type == 'DI':
                self.__di_cards_index.append(num)

    def close(self):
        """ close the pci card
        """
        # close the I/O cards
        self.run(pci_8154._8154_db51_HSL_stop, 0)
        self.run(pci_8154._8154_db51_HSL_close, 0)
        # close the motion cards
        self.run(pci_8154._8154_close)
        logger.debug('ADLink8154 close')

    def refresh(self, card_config, manual_id=0):
        self.close()
        self.__initial(card_config , manual_id)      

    def do_count(self):
        return len(self.__do_cards_index) * self.__port_per_card
        
    def di_count(self):
        return len(self.__di_cards_index) * self.__port_per_card

    def axis_count(self):
        return self.__motion_card_count * 4
        
    def DO(self, port, state):
        """ write output
        """
        port_per_card = self.__port_per_card
        # check DO status in advance
        if self.DO_read(port) == state:
            return 0
        card_order = int(port/port_per_card)
        if card_order < len(self.__do_cards_index):
            card_num = self.__do_cards_index[card_order]
            port = port % port_per_card
        else:
            msg = '[DO port is out of range]: port = {}, total cards = {}'.format(
                port, len(self.__do_cards_index))
            logger.error(msg)
            return msg
        ret = self.run(pci_8154._8154_db51_HSL_D_write_channel_output, 0, card_num, port, state)

        return error_table[ret]

    def DO_read(self, port):
        """ read DO signal
        """
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__do_cards_index):
            card_num = self.__do_cards_index[card_order]
            port = port % port_per_card
        else:
            msg = '[DO port is out of range]: port = {}, total cards = {}'.format(
                port, len(self.__do_cards_index))
            logger.error(msg)
            return msg
        state = pointer(c_ulong(0))
        self.run(pci_8154._8154_db51_HSL_D_read_output, 0, card_num, state)

        if state[0] & 1 << port:
            return 1
        else:
            return 0

    def DI(self, port):
        """ read DI signal
        """
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__di_cards_index):
            card_num = self.__di_cards_index[card_order]
            port = port % port_per_card
        else:
            msg = '[DI port is out of range]: port = {}, total cards = {}'.format(
                port, len(self.__di_cards_index))
            logger.error(msg)
            return msg
        state = pointer(c_ushort(0))
        self.run(pci_8154._8154_db51_HSL_D_read_channel_input, 0, card_num, port, state)

        return state[0]

    def servo_on_off(self, axis_id, on_off):
        """ motor servo on/off
        """
        ret = self.run(pci_8154._8154_set_servo, axis_id, on_off)

        return error_table[ret]
            
    def get_io_status(self, axis_id):
        """ get axis I/O status
        """
        status = pointer(c_ushort(0))
        ret = self.run(pci_8154._8154_get_io_status, axis_id, status)
        
        return status[0]

    def get_motion_status(self, axis_id):
        """ get axis status

        Example:
            get_motion_status(0)
            
        Args:
            axis_id(integer): axis id
        
        Returns:
            An Integer, the status code
            0	Normal stopped condition
            1	Waiting for DR
            2	Waiting for CSTA input
            3	Waiting for an internal synchronous signal
            4	Waiting for another axis to stop
            5	Waiting for a completion of ERC timer
            6	Waiting for a completion of direction change timer
            7	Correcting backlash
            8	Wait PA/PB
            9	At FA speed
            10	At FL Speed
            11	Accelerating
            12	At FH Speed
            13	Decelerating
            14	Wait INP
            15	Others(Controlling Start)
            16	SALM
            17	SPEL
            18	SMEL
            19	SEMG
            20	SSTP
            21	SERC

        Raises:
            
        """
        ret = self.run(pci_8154._8154_motion_done, axis_id)
        
        return ret

    def get_pulse(self, axis_id):
        """ Get the value of feedback position counter
        """
        position = pointer(c_double(0))
        ret = self.run(pci_8154._8154_get_position, axis_id, position)
        
        return position[0]

    def set_position(self, axis_id, position):
        """ Set the feedback position counter
        """
        ret = self.run(pci_8154._8154_set_position, axis_id, position)
        
        return error_table[ret]

    def get_command(self, axis_id):
        """ Get the value of command position counter
        """
        command = pointer(c_long(0))
        ret = self.run(pci_8154._8154_get_command, axis_id, command)
        
        return command[0]

    def set_command(self, axis_id, command):
        """ Set the command position counter
        """
        ret = self.run(pci_8154._8154_set_command, axis_id, command)
        
        return error_table[ret]

    def emg_stop(self, axis_id):
        """ emergency stop
        """
        ret = self.run(pci_8154._8154_emg_stop, axis_id)
        return error_table[ret]
        
    def relative_move(self, axis_list, speed, timeout=5000, Tacc=0.2, Tdec=0.2, SVacc=-1, SVdec=-1):
        """ single/multiple axis move relatively
        """
        start_vel = speed / 10
        if SVacc == -1:
            SVacc = speed / 4
        if SVdec == -1:
            SVdec = speed / 4
        axis_count = len(axis_list)
        axis_id_array = (c_short * axis_count)()
        position_array = (c_double * axis_count)()
        for index, axis in enumerate(axis_list):
            axis_id_array[index] = axis['axis_id']
            position_array[index] = axis['pulse']
        
        if axis_count == 1:
            argv_list = [axis_id_array[0], position_array[0], start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        else:
            argv_list = [axis_id_array, position_array, start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        
        if axis_count == 1:
            ret = self.run(pci_8154._8154_start_sr_move, *argv_list)
        elif axis_count == 2:
            ret = self.run(pci_8154._8154_start_sr_line2, *argv_list)
        elif axis_count == 3:
            ret = self.run(pci_8154._8154_start_sr_line3, *argv_list)
        elif axis_count == 4:
            ret = self.run(pci_8154._8154_start_sr_line4, *argv_list)
        else:
            msg = 'axis_count error because total axis = {}'.format(axis_count)
            logger.error(msg)
            return msg
        
        if ret:
            return error_table[ret]

        for axis_id in axis_id_array:
            ret = self.wait_motion_ready(axis_id, timeout)
            if ret:
                msg = 'move timeout ({} ms)'.format(timeout)
                logger.warning(msg)
                return msg
        
        return error_table[ret]

    def absolute_move(self, axis_list, speed, timeout=5000, Tacc=0.3, Tdec=0.3, SVacc=-1, SVdec=-1):
        """ single/multiple axis move absolutely
        """
        start_vel = speed / 10
        if SVacc == -1:
            SVacc = speed / 4
        if SVdec == -1:
            SVdec = speed / 4
        axis_count = len(axis_list)
        axis_id_array = (c_short * axis_count)()
        position_array = (c_double * axis_count)()
        for index, axis in enumerate(axis_list):
            axis_id_array[index] = axis['axis_id']
            position_array[index] = axis['pulse']
        
        if axis_count == 1:
            argv_list = [axis_id_array[0], position_array[0], start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        else:
            argv_list = [axis_id_array, position_array, start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        
        if axis_count == 1:
            ret = self.run(pci_8154._8154_start_sa_move, *argv_list)
        elif axis_count == 2:
            ret = self.run(pci_8154._8154_start_sa_line2, *argv_list)
        elif axis_count == 3:
            ret = self.run(pci_8154._8154_start_sa_line3, *argv_list)
        elif axis_count == 4:
            ret = self.run(pci_8154._8154_start_sa_line4, *argv_list)
        else:
            msg = 'axis_count error because total axis = {}'.format(axis_count)
            logger.error(msg)
            return msg
        
        if ret:
            return error_table[ret]

        for axis_id in axis_id_array:
            ret = self.wait_motion_ready(axis_id, timeout)
            if ret:
                msg = 'move timeout ({} ms)'.format(timeout)
                logger.warning(msg)
                return msg

        return error_table[ret]

    def wait_motion_ready(self, axis_id, timeout=None, interval=20):
        """ check if motion status is ready
        
        Example:
            wait_motion_ready(0, 2000, 10)
            
        Args:
            axis(integer): axis id
            timeout(integer): timeout (ms)
            interval(integer): sleep time (ms)
        
        Returns:
            0: ready
            timeout message

        Raises:
            
        """
        count = 0
        interval_time = interval / 1000
        while 1:
            ret = self.get_motion_status(axis_id)
            if ret:
                count = count + interval
            else:
                return ret
            if timeout and count >= timeout:
                return ret
            sleep(interval_time)

    def set_home_config(self, axis_id, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        """ Set the configuration for home return move motion
        """
        ret = self.run(pci_8154._8154_set_home_config, axis_id, home_mode, org_logic, ez_logic, ez_count, erc_out)
        
        return error_table[ret]

    def home_search(self, axis_id, speed, acc_time, ORG_offset):
        """ Perform an auto search home

        Example:
            
        Args:
            axis_id(integer): axis id
            speed(float): speed(pulse/sec)
            acc_time(float): acceleration time(sec)
            ORG_offset(integer): the escape pulse amounts when home search
                touches the ORG signal(pulse)
        
        Returns:
            An Integer, the return code

        Raises:
        
        """
        self.run(pci_8154._8154_set_home_config, axis_id, 9, 1, 0, 0, 0)
        start_vel = 100
        ret = self.run(pci_8154._8154_home_search, axis_id, start_vel, speed, acc_time, ORG_offset)
        
        return error_table[ret]

    def sync_pulse(self, axis_info):
        """ update position
        """
        ABSM = axis_info['ABSM']
        ABSR = axis_info['ABSR']
        TLC = axis_info['TLC']
        DO1 = axis_info['DO1']
        ZSP = axis_info['ZSP']
        
        if self.DO(ABSM, 1):
            self.DO(ABSM, 0)
            msg = '{} ABSM error: DO port = {}'.format(axis_info['key'], ABSM)
            logger.error(msg)
            return msg
        interval = 0.02
        sleep(interval)
        if self.DI(TLC) == 0:
            self.DO(ABSM, 0)
            msg = '{} TLC error: DI port = {}'.format(axis_info['key'], TLC)
            logger.error(msg)
            return msg
        sum = [0, 0, 0, 0]
        for i in range(0, 31, 2):
            self.DO(ABSR, 1)
            sleep(interval)
            if self.DI(TLC) == 0:
                DO1_buf = self.DI(DO1)
                ZSP_buf = self.DI(ZSP)
                sleep(interval)
                sum[0] = DO1_buf * (1<<i) + ZSP_buf * (1<<(i+1)) + sum[1]
                sum[1] = sum[0]
                self.DO(ABSR, 0)
                sleep(interval)
        for i in range(0, 5, 2):
            self.DO(ABSR, 1)
            sleep(interval)
            DO1_buf = self.DI(DO1)
            ZSP_buf = self.DI(ZSP)
            sleep(interval)
            sum[2] = DO1_buf * (1<<i) + ZSP_buf * (1<<(i+1)) + sum[3];
            sum[3] = sum[2]
            self.DO(ABSR, 0)
            sleep(interval)
        self.DO(ABSR, 0)
        sleep(interval)
        self.DO(ABSM, 0)
        sleep(interval)
        
        axis_id = axis_info['axis_id']
        now_pulse = int32(sum[0])
        ret = self.set_command(axis_id, now_pulse)
        if ret:
            logger.error(ret)
            return ret
        ret = self.set_position(axis_id, now_pulse)
        if ret:
            logger.error(ret)
            return ret
        return 0

    def set_inp(self, axis_id, inp_enable, inp_logic=0):
        ret = self.run(pci_8154._8154_set_inp, axis_id, inp_enable, inp_logic)
        
        return error_table[ret]

# ===========================================================================
# ADLink 8158
# ===========================================================================

class ADLink8158(Channel, Motion):
    def __init__(self, cards_config=[], manual_id=0):
        super(ADLink8158, self).__init__()
        self.__port_per_card = 32
        self.__initial(cards_config, manual_id)

    def __del__(self):
        self.close()

    def __initial(self, cards_config, manual_id):
        """ detect cardtype automatically, and initial pci card
        
        Example:
            
        Args:
            manual_id(integer): Enable the On board dip switch(SW1) to decide
                the Card ID.
                0 is the sequence of PCI slot.
                1 is on board DIP switch(SW1).
        
        Returns:
            An Integer, the return code

        Raises:
        
        """
        self.__do_cards_index = []
        self.__di_cards_index = []
        self.__motion_card_count = 0

        cardid_inbit = pointer(c_ushort(0))
        ret = self.run(pci_8158._8158_initial, cardid_inbit, manual_id)
        # cardid_inbit:
        #    1 = 0001 means finding 1 card
        #    3 = 0011 means finding 2 cards
        #    7 = 0111 means finding 3 cards
        #    motion card count example:
        #    log(7+1, 2) = 3
        self.__motion_card_count = log(cardid_inbit[0]+1, 2)
        logger.info('ADLink8158 initial, motion card count = %d', self.__motion_card_count)
        ret = self.run(pci_8158._8158_config_from_file)
        logger.debug('8158 read config...ret = %d', ret)
        if len(cards_config) == 0:
            return

        # join all the I/O cards from configuration of cards
        live = pointer(c_short(0))
        self.run(pci_8158._8158_db51_HSL_initial, 0)
        self.run(pci_8158._8158_db51_HSL_auto_start, 0)
        self.run(pci_8158._8158_db51_HSL_set_scan_condition, 0, 0, 0)
        for num, type in cards_config:
            self.run(pci_8158._8158_db51_HSL_slave_live, 0, num, live)
            logger.debug('ADLink8158 DB8151 %s %d initial', type, num)
            if type == 'DO':
                self.__do_cards_index.append(num)
            elif type == 'DI':
                self.__di_cards_index.append(num)

    def close(self):
        """ close the pci card
        """
        # close the I/O cards
        self.run(pci_8158._8158_db51_HSL_stop, 0)
        self.run(pci_8158._8158_db51_HSL_close, 0)
        # close the motion cards
        self.run(pci_8158._8158_close)
        logger.debug('ADLink8158 close')

    def refresh(self, card_config, manual_id=0):
        self.close()
        self.__initial(card_config , manual_id)      

    def do_count(self):
        return len(self.__do_cards_index) * self.__port_per_card
        
    def di_count(self):
        return len(self.__di_cards_index) * self.__port_per_card

    def axis_count(self):
        return self.__motion_card_count * 8
        
    def DO(self, port, state):
        """ write output
        """
        port_per_card = self.__port_per_card
        # check DO status in advance
        if self.DO_read(port) == state:
            return 0
        card_order = int(port/port_per_card)
        if card_order < len(self.__do_cards_index):
            card_num = self.__do_cards_index[card_order]
            port = port % port_per_card
        else:
            msg = '[DO port is out of range]: port = {}, total cards = {}'.format(
                port, len(self.__do_cards_index))
            logger.error(msg)
            return msg
        ret = self.run(pci_8158._8158_db51_HSL_D_write_channel_output, 0, card_num, port, state)

        return error_table[ret]

    def DO_read(self, port):
        """ read DO signal
        """
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__do_cards_index):
            card_num = self.__do_cards_index[card_order]
            port = port % port_per_card
        else:
            msg = '[DO port is out of range]: port = {}, total cards = {}'.format(
                port, len(self.__do_cards_index))
            logger.error(msg)
            return msg
        state = pointer(c_ulong(0))
        self.run(pci_8158._8158_db51_HSL_D_read_output, 0, card_num, state)

        if state[0] & 1 << port:
            return 1
        else:
            return 0

    def DI(self, port):
        """ read DI signal
        """
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__di_cards_index):
            card_num = self.__di_cards_index[card_order]
            port = port % port_per_card
        else:
            msg = '[DI port is out of range]: port = {}, total cards = {}'.format(
                port, len(self.__di_cards_index))
            logger.error(msg)
            return msg
        state = pointer(c_ushort(0))
        self.run(pci_8158._8158_db51_HSL_D_read_channel_input, 0, card_num, port, state)

        return state[0]

    def servo_on_off(self, axis_id, on_off):
        """ motor servo on/off
        """
        ret = self.run(pci_8158._8158_set_servo, axis_id, on_off)

        return error_table[ret]
            
    def get_io_status(self, axis_id):
        """ get axis I/O status
        """
        status = pointer(c_ushort(0))
        ret = self.run(pci_8158._8158_get_io_status, axis_id, status)
        
        return status[0]

    def get_motion_status(self, axis_id):
        """ get axis status

        Example:
            get_motion_status(0)
            
        Args:
            axis_id(integer): axis id
        
        Returns:
            An Integer, the status code
            0	Normal stopped condition
            1	Waiting for DR
            2	Waiting for CSTA input
            3	Waiting for an internal synchronous signal
            4	Waiting for another axis to stop
            5	Waiting for a completion of ERC timer
            6	Waiting for a completion of direction change timer
            7	Correcting backlash
            8	Wait PA/PB
            9	At FA speed
            10	At FL Speed
            11	Accelerating
            12	At FH Speed
            13	Decelerating
            14	Wait INP
            15	Others(Controlling Start)
            16	SALM
            17	SPEL
            18	SMEL
            19	SEMG
            20	SSTP
            21	SERC

        Raises:
            
        """
        ret = self.run(pci_8158._8158_motion_done, axis_id)
        
        return ret

    def get_pulse(self, axis_id):
        """ Get the value of feedback position counter
        """
        position = pointer(c_double(0))
        ret = self.run(pci_8158._8158_get_position, axis_id, position)
        
        return position[0]

    def set_position(self, axis_id, position):
        """ Set the feedback position counter
        """
        ret = self.run(pci_8158._8158_set_position, axis_id, position)
        
        return error_table[ret]

    def get_command(self, axis_id):
        """ Get the value of command position counter
        """
        command = pointer(c_long(0))
        ret = self.run(pci_8158._8158_get_command, axis_id, command)
        
        return command[0]

    def set_command(self, axis_id, command):
        """ Set the command position counter
        """
        ret = self.run(pci_8158._8158_set_command, axis_id, command)
        
        return error_table[ret]

    def emg_stop(self, axis_id):
        """ emergency stop
        """
        ret = self.run(pci_8158._8158_emg_stop, axis_id)
        return error_table[ret]
        
    def relative_move(self, axis_list, speed, timeout=5000, Tacc=0.2, Tdec=0.2, SVacc=-1, SVdec=-1):
        """ single/multiple axis move relatively
        """
        start_vel = speed / 10
        if SVacc == -1:
            SVacc = speed / 4
        if SVdec == -1:
            SVdec = speed / 4
        axis_count = len(axis_list)
        axis_id_array = (c_short * axis_count)()
        position_array = (c_double * axis_count)()
        for index, axis in enumerate(axis_list):
            axis_id_array[index] = axis['axis_id']
            position_array[index] = axis['pulse']
        
        if axis_count == 1:
            argv_list = [axis_id_array[0], position_array[0], start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        else:
            argv_list = [axis_id_array, position_array, start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        
        if axis_count == 1:
            ret = self.run(pci_8158._8158_start_sr_move, *argv_list)
        elif axis_count == 2:
            ret = self.run(pci_8158._8158_start_sr_line2, *argv_list)
        elif axis_count == 3:
            ret = self.run(pci_8158._8158_start_sr_line3, *argv_list)
        elif axis_count == 4:
            ret = self.run(pci_8158._8158_start_sr_line4, *argv_list)
        else:
            msg = 'axis_count error because total axis = {}'.format(axis_count)
            logger.error(msg)
            return msg
        
        if ret:
            return error_table[ret]

        for axis_id in axis_id_array:
            ret = self.wait_motion_ready(axis_id, timeout)
            if ret:
                msg = 'move timeout ({} ms)'.format(timeout)
                logger.warning(msg)
                return msg
        
        return error_table[ret]

    def absolute_move(self, axis_list, speed, timeout=5000, Tacc=0.3, Tdec=0.3, SVacc=-1, SVdec=-1):
        """ single/multiple axis move absolutely
        """
        start_vel = speed / 10
        if SVacc == -1:
            SVacc = speed / 4
        if SVdec == -1:
            SVdec = speed / 4
        axis_count = len(axis_list)
        axis_id_array = (c_short * axis_count)()
        position_array = (c_double * axis_count)()
        for index, axis in enumerate(axis_list):
            axis_id_array[index] = axis['axis_id']
            position_array[index] = axis['pulse']
        
        if axis_count == 1:
            argv_list = [axis_id_array[0], position_array[0], start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        else:
            argv_list = [axis_id_array, position_array, start_vel,
                        speed, Tacc, Tdec, SVacc, SVdec]
        
        if axis_count == 1:
            ret = self.run(pci_8158._8158_start_sa_move, *argv_list)
        elif axis_count == 2:
            ret = self.run(pci_8158._8158_start_sa_line2, *argv_list)
        elif axis_count == 3:
            ret = self.run(pci_8158._8158_start_sa_line3, *argv_list)
        elif axis_count == 4:
            ret = self.run(pci_8158._8158_start_sa_line4, *argv_list)
        else:
            msg = 'axis_count error because total axis = {}'.format(axis_count)
            logger.error(msg)
            return msg
        
        if ret:
            return error_table[ret]

        for axis_id in axis_id_array:
            ret = self.wait_motion_ready(axis_id, timeout)
            if ret:
                msg = 'move timeout ({} ms)'.format(timeout)
                logger.warning(msg)
                return msg

        return error_table[ret]

    def wait_motion_ready(self, axis_id, timeout=None, interval=20):
        """ check if motion status is ready
        
        Example:
            wait_motion_ready(0, 2000, 10)
            
        Args:
            axis(integer): axis id
            timeout(integer): timeout (ms)
            interval(integer): sleep time (ms)
        
        Returns:
            0: ready
            timeout message

        Raises:
            
        """
        count = 0
        interval_time = interval / 1000
        while 1:
            ret = self.get_motion_status(axis_id)
            if ret:
                count = count + interval
            else:
                return ret
            if timeout and count >= timeout:
                return ret
            sleep(interval_time)

    def set_home_config(self, axis_id, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        """ Set the configuration for home return move motion
        """
        ret = self.run(pci_8158._8158_set_home_config, axis_id, home_mode, org_logic, ez_logic, ez_count, erc_out)
        
        return error_table[ret]

    def home_search(self, axis_id, speed, acc_time, ORG_offset):
        """ Perform an auto search home

        Example:
            
        Args:
            axis_id(integer): axis id
            speed(float): speed(pulse/sec)
            acc_time(float): acceleration time(sec)
            ORG_offset(integer): the escape pulse amounts when home search
                touches the ORG signal(pulse)
        
        Returns:
            An Integer, the return code

        Raises:
        
        """
        self.run(pci_8158._8158_set_home_config, axis_id, 9, 1, 0, 0, 0)
        start_vel = 100
        ret = self.run(pci_8158._8158_home_search, axis_id, start_vel, speed, acc_time, ORG_offset)
        
        return error_table[ret]

    def sync_pulse(self, axis_info):
        """ update position
        """
        ABSM = axis_info['ABSM']
        ABSR = axis_info['ABSR']
        TLC = axis_info['TLC']
        DO1 = axis_info['DO1']
        ZSP = axis_info['ZSP']
        
        if self.DO(ABSM, 1):
            self.DO(ABSM, 0)
            msg = '{} ABSM error: DO port = {}'.format(axis_info['key'], ABSM)
            logger.error(msg)
            return msg
        interval = 0.02
        sleep(interval)
        if self.DI(TLC) == 0:
            self.DO(ABSM, 0)
            msg = '{} TLC error: DI port = {}'.format(axis_info['key'], TLC)
            logger.error(msg)
            return msg
        sum = [0, 0, 0, 0]
        for i in range(0, 31, 2):
            self.DO(ABSR, 1)
            sleep(interval)
            if self.DI(TLC) == 0:
                DO1_buf = self.DI(DO1)
                ZSP_buf = self.DI(ZSP)
                sleep(interval)
                sum[0] = DO1_buf * (1<<i) + ZSP_buf * (1<<(i+1)) + sum[1]
                sum[1] = sum[0]
                self.DO(ABSR, 0)
                sleep(interval)
        for i in range(0, 5, 2):
            self.DO(ABSR, 1)
            sleep(interval)
            DO1_buf = self.DI(DO1)
            ZSP_buf = self.DI(ZSP)
            sleep(interval)
            sum[2] = DO1_buf * (1<<i) + ZSP_buf * (1<<(i+1)) + sum[3];
            sum[3] = sum[2]
            self.DO(ABSR, 0)
            sleep(interval)
        self.DO(ABSR, 0)
        sleep(interval)
        self.DO(ABSM, 0)
        sleep(interval)
        
        axis_id = axis_info['axis_id']
        now_pulse = int32(sum[0])
        ret = self.set_command(axis_id, now_pulse)
        if ret:
            logger.error(ret)
            return ret
        ret = self.set_position(axis_id, now_pulse)
        if ret:
            logger.error(ret)
            return ret
        return 0

    def set_inp(self, axis_id, inp_enable, inp_logic=0):
        ret = self.run(pci_8158._8158_set_inp, axis_id, inp_enable, inp_logic)
        
        return error_table[ret]
