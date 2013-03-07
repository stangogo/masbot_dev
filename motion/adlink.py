# -- coding: utf-8 --

# Title          : adlink.py
# Description    : calling functions in 8154.dll and 8158.dll of ADLink
# Author         : Stan Liu
# Date           : 20130301
# Dependency     : 8154.dll 8158.dll adlink_table.py
# usage          : import adlink
# notes          : the library detects 8154 or 8158 card automatically

from masbot.motion.motion_card import *
from masbot.motion.adlink_table import *
from ctypes import *
from time import sleep

# loaded shared libraries
pci_8154 = WinDLL(__file__ + '/../../dlls/8154.dll')
pci_8158 = WinDLL(__file__ + '/../../dlls/8158.dll')

# define the argument and return type for the functions
pci_8154._8154_initial.restype = c_short
pci_8154._8154_initial.argtypes = [POINTER(c_ushort), c_short]
pci_8158._8158_initial.restype = c_short
pci_8158._8158_initial.argtypes = [POINTER(c_ushort), c_short]

pci_8154._8154_close.restype = c_short
pci_8154._8154_close.argtypes = []
pci_8158._8158_close.restype = c_short
pci_8158._8158_close.argtypes = []

pci_8154._8154_config_from_file.restype = c_short
pci_8154._8154_config_from_file.argtypes = []
pci_8158._8158_config_from_file.restype = c_short
pci_8158._8158_config_from_file.argtypes = []

pci_8158._8158_config_from_file2.restype = c_short
pci_8158._8158_config_from_file2.argtypes = [c_char_p]

pci_8154._8154_db51_HSL_initial.restype = c_short
pci_8154._8154_db51_HSL_initial.argtypes = [c_short]
pci_8158._8158_db51_HSL_initial.restype = c_short
pci_8158._8158_db51_HSL_initial.argtypes = [c_short]

pci_8154._8154_db51_HSL_auto_start.restype = c_short
pci_8154._8154_db51_HSL_auto_start.argtypes = [c_short]
pci_8158._8158_db51_HSL_auto_start.restype = c_short
pci_8158._8158_db51_HSL_auto_start.argtypes = [c_short]

pci_8154._8154_db51_HSL_stop.restype = c_short
pci_8154._8154_db51_HSL_stop.argtypes = [c_short]
pci_8158._8158_db51_HSL_stop.restype = c_short
pci_8158._8158_db51_HSL_stop.argtypes = [c_short]

pci_8154._8154_db51_HSL_close.restype = c_short
pci_8154._8154_db51_HSL_close.argtypes = [c_short]
pci_8158._8158_db51_HSL_close.restype = c_short
pci_8158._8158_db51_HSL_close.argtypes = [c_short]

pci_8154._8154_db51_HSL_set_scan_condition.restype = c_short
pci_8154._8154_db51_HSL_set_scan_condition.argtypes = [c_short, c_short, c_short]
pci_8158._8158_db51_HSL_set_scan_condition.restype = c_short
pci_8158._8158_db51_HSL_set_scan_condition.argtypes = [c_short, c_short, c_short]

pci_8154._8154_db51_HSL_slave_live.restype = c_short
pci_8154._8154_db51_HSL_slave_live.argtypes = [c_short, c_short, POINTER(c_short)]
pci_8158._8158_db51_HSL_slave_live.restype = c_short
pci_8158._8158_db51_HSL_slave_live.argtypes = [c_short, c_short, POINTER(c_short)]

pci_8154._8154_db51_HSL_D_write_channel_output.restype = c_short
pci_8154._8154_db51_HSL_D_write_channel_output.argtypes = [c_short, c_short, c_short, c_short]
pci_8158._8158_db51_HSL_D_write_channel_output.restype = c_short
pci_8158._8158_db51_HSL_D_write_channel_output.argtypes = [c_short, c_short, c_short, c_short]

pci_8154._8154_db51_HSL_D_read_output.restype = c_short
pci_8154._8154_db51_HSL_D_read_output.argtypes = [c_short, c_short, POINTER(c_ulong)]
pci_8158._8158_db51_HSL_D_read_output.restype = c_short
pci_8158._8158_db51_HSL_D_read_output.argtypes = [c_short, c_short, POINTER(c_ulong)]

pci_8154._8154_set_servo.restype = c_short
pci_8154._8154_set_servo.argtypes = [c_short, c_short]
pci_8158._8158_set_servo.restype = c_short
pci_8158._8158_set_servo.argtypes = [c_short, c_short]

pci_8154._8154_get_io_status.restype = c_short
pci_8154._8154_get_io_status.argtypes = [c_short, POINTER(c_ushort)]
pci_8158._8158_get_io_status.restype = c_short
pci_8158._8158_get_io_status.argtypes = [c_short, POINTER(c_ushort)]

pci_8154._8154_emg_stop.restype = c_short
pci_8154._8154_emg_stop.argtypes = [c_short]
pci_8158._8158_emg_stop.restype = c_short
pci_8158._8158_emg_stop.argtypes = [c_short]

pci_8154._8154_motion_done.restype = c_short
pci_8154._8154_motion_done.argtypes = [c_short]
pci_8158._8158_motion_done.restype = c_short
pci_8158._8158_motion_done.argtypes = [c_short]

pci_8154._8154_get_command.restype = c_short
pci_8154._8154_get_command.argtypes = [c_short, POINTER(c_long)]
pci_8158._8158_get_command.restype = c_short
pci_8158._8158_get_command.argtypes = [c_short, POINTER(c_long)]

pci_8154._8154_set_command.restype = c_short
pci_8154._8154_set_command.argtypes = [c_short, c_long]
pci_8158._8158_set_command.restype = c_short
pci_8158._8158_set_command.argtypes = [c_short, c_long]

pci_8154._8154_get_position.restype = c_short
pci_8154._8154_get_position.argtypes = [c_short, POINTER(c_double)]
pci_8158._8158_get_position.restype = c_short
pci_8158._8158_get_position.argtypes = [c_short, POINTER(c_double)]

pci_8154._8154_set_position.restype = c_short
pci_8154._8154_set_position.argtypes = [c_short, c_double]
pci_8158._8158_set_position.restype = c_short
pci_8158._8158_set_position.argtypes = [c_short, c_double]

pci_8154._8154_start_sr_move.restype = c_short
pci_8154._8154_start_sr_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sr_move.restype = c_short
pci_8158._8158_start_sr_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sa_move.restype = c_short
pci_8154._8154_start_sa_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sa_move.restype = c_short
pci_8158._8158_start_sa_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_home_search.restype = c_short
pci_8154._8154_home_search.argtypes = [c_short, c_double, c_double, c_double, c_double]
pci_8158._8158_home_search.restype = c_short
pci_8158._8158_home_search.argtypes = [c_short, c_double, c_double, c_double, c_double]

pci_8154._8154_set_home_config.restype = c_short
pci_8154._8154_set_home_config.argtypes = [c_short, c_short, c_short, c_short, c_short, c_short]
pci_8158._8158_set_home_config.restype = c_short
pci_8158._8158_set_home_config.argtypes = [c_short, c_short, c_short, c_short, c_short, c_short]

class ADLinkMotion(Motion):
    def __init__(self, cards_config=[]):
        self.mode = 'pci8154'
        #self.mode = 'default'

        self.cards_config = cards_config
        self.do_cards_index = []
        self.di_cards_index = []
        self.initial()

    def __exit__(self):
        self.close_io_cards()
        self.close()

    def initial(self, manual_id = 0):
        """ detect cardtype automatically, and inital pci card
        
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
        cardid_inbit = pointer(c_ushort(0))
        ret_8154 = pci_8154._8154_initial(cardid_inbit, manual_id)
        ret_8158 = pci_8158._8158_initial(cardid_inbit, manual_id)
        
        if ret_8154 and ret_8158:
            return -1
            
        if ret_8154 == 0:
            pci_8154._8154_config_from_file()
            self.mode == 'pci8154'
            print('8154 initial')
            self.join_io_cards()
            return 0
        elif ret_8158 == 0:
            pci_8158._8158_config_from_file()
            self.mode == 'pci8158'
            print('8158 initial')
            self.join_io_cards()
            return 0
        else:
            return -1

    def close(self):
        """ close the pci card
        """
        if self.mode == 'pci8154' or self.mode == 'pci8158':
            pci_8154._8154_close()
            pci_8158._8158_close()
        else:
            pass

    def join_io_cards(self):
        """ join all the I/O cards from configuration of cards
        """  
        live = pointer(c_short(0))
        
        if self.mode == 'pci8154':
            for num, type in self.cards_config:
                pci_8154._8154_db51_HSL_initial(0)
                pci_8154._8154_db51_HSL_auto_start(0)
                pci_8154._8154_db51_HSL_set_scan_condition(0, 0, 0)
                pci_8154._8154_db51_HSL_slave_live(0, num, live)
                print('8154 card No.%d start' % num)
                if type == 'DO_CARD':
                    self.do_cards_index.append(num)
                elif type == 'DI_CARD':
                    self.di_cards_index.append(num)
        elif self.mode == 'pci8158':
            for num, type in self.cards_config:
                pci_8158._8158_db51_HSL_initial(0)
                pci_8158._8158_db51_HSL_auto_start(0)
                pci_8158._8158_db51_HSL_set_scan_condition(0, 0, 0)
                pci_8158._8158_db51_HSL_slave_live(0, num, live)
                print('8158 card No.%d start' % num)
                if type == 'DO_CARD':
                    self.do_cards_index.append(num)
                elif type == 'DI_CARD':
                    self.di_cards_index.append(num)
        else:
            pass

    def close_io_cards(self):
        """ close all the I/O cards
        """
        if self.mode == 'pci8154':
            pci_8154._8154_db51_HSL_stop(0)
            pci_8154._8154_db51_HSL_close(0)
        elif self.mode == 'pci8158':
            pci_8158._8154_db51_HSL_stop(0)
            pci_8158._8158_db51_HSL_close(0)
        else:
            pass

    def DO(self, port, state):
        """ write output
        """
        # check DO status in advance
        if self.DO_read(port) == state:
            return 0
        card_order = int(port/32)
        if card_order < len(self.do_cards_index):
            card_num = self.do_cards_index[card_order]
            port = port % 32
        else:
            return '[DO port is out of range]: port = %d, total cards = %d' % (port, len(self.do_cards_index))
        if self.mode == 'pci8154':
            ret = pci_8154._8154_db51_HSL_D_write_channel_output(0, card_num, port, state)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_db51_HSL_D_write_channel_output(0, card_num, port, state)
        else:
            return -1

        return get_msg(ret)

    def DO_read(self, port):
        """ read DO signal
        """
        card_order = int(port/32)
        if card_order < len(self.do_cards_index):
            card_num = self.do_cards_index[card_order]
            port = port % 32
        else:
            return '[DO port is out of range]: port = %d, total cards = %d' % (port, len(self.do_cards_index))
        state = pointer(c_ulong(0))
        if self.mode == 'pci8154':
            pci_8154._8154_db51_HSL_D_read_output(0, card_num, state)
        elif self.mode == 'pci8158':
            pci_8158._8158_db51_HSL_D_read_output(0, card_num, state)
        else:
            return -1

        if state[0] & 1 << port:
            return 1
        else:
            return 0

    def DI(self, port):
        """ read DI signal
        """
        card_order = int(port/32)
        if card_order < len(self.di_cards_index):
            card_num = self.di_cards_index[card_order]
            port = port % 32
        else:
            return '[DI port is out of range]: port = %d, total cards = %d' % (port, len(self.di_cards_index))
        state = pointer(c_ushort(0))
        if self.mode == 'pci8154':
            pci_8154._8154_db51_HSL_D_read_channel_input(0, card_num, port, state)
        elif self.mode == 'pci8158':
            pci_8158._8158_db51_HSL_D_read_channel_input(0, card_num, port, state)
        else:
            return -1

        return state[0]

    def servo_on_off(self, axis, on_off):
        """ motor servo on/off
        """
        if self.mode == 'pci8154':
            ret = pci_8154._8154_set_servo(axist, on_off)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_set_servo(axis, on_off)
        else:
            return -1
            
    def get_io_status(self, axis):
        """ get axis I/O status
        """
        status = pointer(c_ushort(0))
        if self.mode == 'pci8154':
            ret = pci_8154._8154_get_io_status(axis, status)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_get_io_status(axis, status)
        else:
            return -1

        return status[0]

    def get_motion_status(self, axis):
        """ get axis status

        Example:
            get_motion_status(0)
            
        Args:
            axis(integer): axis id
        
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
        if self.mode == 'pci8154':
            ret = pci_8154._8154_motion_done(axis, status)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_motion_done(axis, status)
        else:
            return -1

        return get_msg(ret)

    def get_position(self, axis):
        """ Get the value of feedback position counter
        """
        position = pointer(c_double(0))
        if self.mode == 'pci8154':
            ret = pci_8154._8154_get_position(axis, position)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_get_position(axis, position)
        else:
            return -1

        return position[0]

    def set_position(self, axis, position):
        """ Set the feedback position counter
        """
        if self.mode == 'pci8154':
            ret = pci_8154._8154_set_position(axis, position)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_set_position(axis, position)
        else:
            return -1

        return get_msg(ret)

    def get_command(self, axis):
        """ Get the value of command position counter
        """
        command = pointer(c_long(0))
        if self.mode == 'pci8154':
            ret = pci_8154._8154_get_command(axis, command)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_get_command(axis, command)
        else:
            return -1

        return position[0]

    def set_command(self, axis, command):
        """ Set the command position counter
        """
        if self.mode == 'pci8154':
            ret = pci_8154._8154_set_command(axis, command)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_set_command(axis, command)
        else:
            return -1

        return get_msg(ret)

    def emg_stop(self, axis):
        """ emergency stop
        """
        if self.mode == 'pci8154':
            ret = pci_8154._8154_emg_stop(axis, status)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_emg_stop(axis, status)
        else:
            return -1

        return get_msg(ret)
        
    def single_rmove(self, axis, distance, speed, Tacc=0.3, Tdec=0.3, SVacc=0.75, SVdec=0.75):
        """ single axis move relatively
        """
        start_vel = speed / 10
        if self.mode == 'pci8154':
            ret = pci_8154._8158_start_sr_move(axis, distance, start_vel, speed, Tacc, Tdec, SVacc, SVdec)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_start_sr_move(axis, distance, start_vel, speed, Tacc, Tdec, SVacc, SVdec)
        else:
            return -1

        return get_msg(ret)

    def single_amove(self, axis, distance, speed, Tacc=0.3, Tdec=0.3, SVacc=0.75, SVdec=0.75):
        """ single axis move absolutely
        """
        start_vel = speed / 10
        if self.mode == 'pci8154':
            ret = pci_8154._8158_start_sa_move(axis, distance, start_vel, speed, Tacc, Tdec, SVacc, SVdec)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_start_sa_move(axis, distance, start_vel, speed, Tacc, Tdec, SVacc, SVdec)
        else:
            return -1

        return get_msg(ret)

    def set_home_config(self, axis, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        """ Set the configuration for home return move motion
        """
        if self.mode == 'pci8154':
            ret = pci_8154._8154_set_home_config(axis, home_mode, org_logic, ez_logic, ez_count, erc_out)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_set_home_config(axis, home_mode, org_logic, ez_logic, ez_count, erc_out)
        else:
            return -1

        return get_msg(ret)

    def home_search(self, axis, speed, acc_time, ORG_offset):
        """ Perform an auto search home

        Example:
            
        Args:
            axis(integer): axis id
            speed(float): speed(pulse/sec)
            acc_time(float): acceleration time(sec)
            ORG_offset(integer): the escape pulse amounts when home search
                touches the ORG signal(pulse)
        
        Returns:
            An Integer, the return code

        Raises:
        
        """
        start_vel = speed / 10
        if self.mode == 'pci8154':
            ret = pci_8154._8154_home_search(axis, start_vel, speed, acc_time, ORG_offset)
        elif self.mode == 'pci8158':
            ret = pci_8158._8158_home_search(axis, start_vel, speed, acc_time, ORG_offset)
        else:
            return -1

        return get_msg(ret)

    def sync_position(self, axis, ABSM, ABSR, TLC, DO1, ZSP):
        """ update position
        """
        if self.DO(ABSM, 1):
            self.DO(ABSM, 0)
            return 'ABSM error: DO port = %d' % ABSM
        sleep(0.05)
        if self.DI(TLC):
            self.DO(ABSM, 0)
            return 'TLC error: DI port = %d' % TLC
        sum = [0, 0]
        for i in range(0, 31, 2):
            self.DO(ABSR, 1)
            sleep(0.02)
            DO1_buf = self.DI(DO1)
            ZSP_buf = self.DI(ZSP)
            sleep(0.02)
            sum[0] = DO1_buf * (1<<i) + ZSP_buf * (1<<(i+1)) + sum[1]
            sum[1] = sum[0]
            self.DO(ABSR, 0)
            sleep(0.02)
        sleep(0.02)
        
        self.set_command(sum[0])
        self.set_position(sum[0])