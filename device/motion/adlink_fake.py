# -*- coding: utf-8 -*-

# Title          : adlink_fake.py
# Description    : simulate adlink.py functions
# Author         : Stan Liu
# Date           : 20130307
# Dependency     : 
# usage          : import adlink_fake
# notes          : 

import logging
from time import sleep
from random import *
from masbot.device.motion.motion_card import Motion

class ADLinkMotion(Motion):
    def __init__(self, cards_config=[]):
        self.logger = logging.getLogger(__name__)
        self.mode = 'pci8158'

        self.cards_config = cards_config
        self.do_cards_index = []
        self.di_cards_index = []
        self.do_card_status = []
        self.di_card_status = []
        self.axis_servo_status = 8 * [0]
        self.axis_pulse = 8 * [0.0]
        self.motion_status = 8 * [0]
        self.initial()

    def __exit__(self):
        self.close_io_cards()
        self.close()

    def initial(self, manual_id = 0):
        self.logger.debug('adlink_fake card initial')
        self.join_io_cards()
        return 0

    def close(self):
        self.logger.debug('adlink_fake card close')

    def join_io_cards(self):
        sleep(0.2)
        for num, type in self.cards_config:
            self.logger.debug('adlink_fake %s %d initial', type, num)
            empty_card = 32 * [0]
            if type == 'DO_CARD':
                self.do_card_status.append(empty_card)
                self.do_cards_index.append(num)
            elif type == 'DI_CARD':
                self.di_card_status.append(empty_card)
                self.di_cards_index.append(num)

    def do_card_count(self):
        return len(self.do_cards_index)

    def di_card_count(self):
        return len(self.di_cards_index)

    def close_io_cards(self):
        self.logger.debug('adlink_fake db51 close')

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

    def servo_on_off(self, axis_id, on_off):
        self.axis_servo_status[axis_id] = on_off

    def get_io_status(self, axis):
        return 0

    def get_motion_status(self, axis_id):
        return self.motion_status[axis_id]

    def get_pulse(self, axis_id):
        return self.axis_pulse[axis_id]

    def set_position(self, axis_id, position):
        self.axis_pulse[axis_id] = position
        return 0

    def get_command(self, axis_id):
        return 0

    def set_command(self, axis_id, command):
        return 0

    def emg_stop(self, axis):
        return 0
        
    def relative_move(self, axis_map, speed, Tacc=0.2, Tdec=0.2, SVacc=0.75, SVdec=0.75):
        simulate_count = 10
        for axis in axis_map:
            self.motion_status[axis['axis_id']] = 14
            for count in range(simulate_count):
                self.axis_pulse[axis['axis_id']] += axis['pulse'] / simulate_count
                sleep(0.01)
            self.motion_status[axis['axis_id']] = 0
        return 0

    def absolute_move(self, axis_map, speed, Tacc=0.2, Tdec=0.2, SVacc=0.75, SVdec=0.75):
        now_position = [0] * 8
        for axis in axis_map:
            now_position[axis['axis_id']] = self.axis_pulse[axis['axis_id']]

        simulate_count = 10
        for axis in axis_map:
            self.motion_status[axis['axis_id']] = 14
            for count in range(simulate_count):
                shift_position = axis['pulse'] - now_position[axis['axis_id']]
                self.axis_pulse[axis['axis_id']] += shift_position / simulate_count
                sleep(0.01)
            self.motion_status[axis['axis_id']] = 0
        return 0

    def set_home_config(self, axis_id, home_mode=1, org_logic=1, ez_logic=0, ez_count=0, erc_out=0):
        return 0

    def home_search(self, axis_id, speed, acc_time, ORG_offset):
        return 0

    def sync_pulse(self, axis_info):
        axis_id = axis_info['axis_id']
        proportion = axis_info['proportion']
        # random position
        current_position = uniform(0, 200)
        self.set_position(axis_id, proportion*current_position)
        return 0
        
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