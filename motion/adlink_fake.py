# -- coding: utf-8 --

# Title          : adlink_fake.py
# Description    : simulate adlink.py functions
# Author         : Stan Liu
# Date           : 20130307
# Dependency     : 
# usage          : import adlink_fake
# notes          : 

from masbot.motion.motion_card import *
from time import sleep

class ADLinkMotion(Motion):
    def __init__(self, cards_config=[]):
        self.mode = 'pci8158'

        self.cards_config = cards_config
        self.do_cards_index = []
        self.di_cards_index = []
        self.do_card_status = []
        self.di_card_status = []
        self.axis_servo_status = 8 * [0]
        self.axis_position = 8 * [0.0]
        self.initial()

    def __exit__(self):
        self.close_io_cards()
        self.close()

    def initial(self, manual_id = 0):
        print('8158 initial')
        self.join_io_cards()
        return 0
        

    def close(self):
        print('8158 close')

    def join_io_cards(self):
        sleep(0.2)
        for num, type in self.cards_config:
            print('8158 card No.%d start' % num)
            empty_card = 32 * [0]
            if type == 'DO_CARD':
                self.do_card_status.append(empty_card)
                self.do_cards_index.append(num)
            elif type == 'DI_CARD':
                self.di_card_status.append(empty_card)
                self.di_cards_index.append(num)

    def close_io_cards(self):
        print('8158 db51 close')

    def DO(self, port, state):
        card_order = int(port/32)
        if card_order < len(self.do_cards_index):
            card_num = self.do_cards_index[card_order]
            port = port % 32
        else:
            return '[DO port is out of range]: port = %d, total cards = %d' % (port, len(self.do_cards_index))
        sleep(0.1)
        self.do_card_status[card_order][port] = state

        return 0

    def DO_read(self, port):
        card_order = int(port/32)
        if card_order < len(self.do_cards_index):
            #card_num = self.do_cards_index[card_order]
            port = port % 32
        else:
            return '[DO port is out of range]: port = %d, total cards = %d' % (port, len(self.do_cards_index))
        
        return self.do_card_status[card_order][port]

    def DI(self, port):
        card_order = int(port/32)
        if card_order < len(self.di_cards_index):
            #card_num = self.di_cards_index[card_order]
            port = port % 32
        else:
            return '[DI port is out of range]: port = %d, total cards = %d' % (port, len(self.di_cards_index))
        
        return self.di_card_status[card_order][port]

    def servo_on_off(self, axis_info, on_off):
        axis_id = axis_info['axis_id']
        self.axis_servo_status[axis_id] = on_off

    def get_io_status(self, axis):
        return 0

    def get_motion_status(self, axis):
        return 0

    def get_position(self, axis):
        return self.axis_position[axis]

    def set_position(self, axis, position):
        self.axis_position[axis] = position
        return 0

    def get_command(self, axis):
        return 0

    def set_command(self, axis, command):
        return 0

    def emg_stop(self, axis):
        return 0
        
    def relative_move(self, axis_list, speed, Tacc=0.2, Tdec=0.2, SVacc=0.75, SVdec=0.75):
        simulate_count = 10
        for count in range(simulate_count):
            for axis in axis_list:
                self.axis_position[axis.axis_id] += axis.position / simulate_count
                sleep(0.025)
        return 0

    def absolute_move(self, axis_list, speed, Tacc=0.2, Tdec=0.2, SVacc=0.75, SVdec=0.75):
        now_position = [0] * len(axis_list)
        for axis in axis_list:
            now_position[axis.axis_id] = self.axis_position[axis.axis_id]

        simulate_count = 10
        for count in range(simulate_count):
            for axis in axis_list:
                shift_position = axis.position - now_position[axis.axis_id]
                self.axis_position[axis.axis_id] += shift_position / simulate_count
                sleep(0.025)
        return 0

    def set_home_config(self, axis, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        return 0

    def home_search(self, axis, speed, acc_time, ORG_offset):
        return 0

    def sync_position(self, axis_info):
        axis_id = axis_info['axis_id']
        proportion = axis_info['proportion']
        ret = self.set_position(axis_id, proportion*100)
        
    def check_sensor(self, port, timeout=5000):
        """ check if sensor is on
        
        Example:
            _check_sensor(12, 200)
            
        Args:
            axis(integer): sensor port
            timeout(integer): timeout (ms)
        
        Returns:
            1: in place
            timeout message

        Raises:
            
        """
        return 1