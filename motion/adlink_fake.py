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
        for num, type in self.cards_config:
            sleep(0.2)
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

    def servo_on_off(self, axis, on_off):
        self.axis_servo_status[axis] = on_off

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
        
    def single_rmove(self, axis, distance, speed, Tacc=0.3, Tdec=0.3, SVacc=0.75, SVdec=0.75):
        return 0

    def single_amove(self, axis, distance, speed, Tacc=0.3, Tdec=0.3, SVacc=0.75, SVdec=0.75):
        return 0

    def set_home_config(self, axis, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        return 0

    def home_search(self, axis, speed, acc_time, ORG_offset):
        return 0

    def sync_position(self, axis, ABSM, ABSR, TLC, DO1, ZSP):
        return 0