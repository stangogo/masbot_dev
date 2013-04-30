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

class ADLink(Motion):
    def __init__(self, cards_config=[], manual_id=0):
        self.__logger = logging.getLogger(__name__)
        self.__mode = 'pci8158'
        self.__do_cards_index = []
        self.__di_cards_index = []
        self.__do_card_status = []
        self.__di_card_status = []
        self.__port_per_card = 32
        self.__motion_card_count = 10
        self.__axis_servo_status = [0] * self.__motion_card_count * 4
        self.__axis_pulse = [0.0] * self.__motion_card_count * 4
        self.__motion_status = [0] * self.__motion_card_count * 4
        self.__initial(cards_config, manual_id)

    def __del__(self):
        self.close()

    def __initial(self, cards_config, manual_id = 0):
        self.__logger.debug('adlink_fake card initial')
        sleep(0.2)
        for num, type in cards_config:
            self.__logger.debug('adlink_fake %s card %d initial', type, num)
            empty_card = self.__port_per_card * [0]
            if type == 'DO':
                self.__do_card_status.append(empty_card)
                self.__do_cards_index.append(num)
            elif type == 'DI':
                self.__di_card_status.append(empty_card)
                self.__di_cards_index.append(num)

    def close(self):
        self.__logger.debug('adlink_fake card close')

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
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__do_cards_index):
            card_num = self.__do_cards_index[card_order]
            port = port % port_per_card
        else:
            return '[DO port is out of range]: port = %d, total cards = %d' % (port, len(self.__do_cards_index))
        sleep(0.1)
        self.__do_card_status[card_order][port] = state

        return 0

    def DO_read(self, port):
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__do_cards_index):
            port = port % port_per_card
        else:
            return '[DO port is out of range]: port = %d, total cards = %d' % (port, len(self.__do_cards_index))
        
        return self.__do_card_status[card_order][port]

    def DI(self, port):
        port_per_card = self.__port_per_card
        card_order = int(port/port_per_card)
        if card_order < len(self.__di_cards_index):
            port = port % self.__port_per_card
        else:
            return '[DI port is out of range]: port = %d, total cards = %d' % (port, len(self.__di_cards_index))
        
        return self.__di_card_status[card_order][port]

    def servo_on_off(self, axis_id, on_off):
        self.__axis_servo_status[axis_id] = on_off
        return 0

    def get_io_status(self, axis):
        return 0

    def get_motion_status(self, axis_id):
        return self.__motion_status[axis_id]

    def get_pulse(self, axis_id):
        return self.__axis_pulse[axis_id]

    def set_position(self, axis_id, position):
        self.__axis_pulse[axis_id] = position
        return 0

    def get_command(self, axis_id):
        return 0

    def set_command(self, axis_id, command):
        return 0

    def emg_stop(self, axis):
        return 0
        
    def relative_move(self, axis_map, timeout, speed, Tacc=0.2, Tdec=0.2, SVacc=0.75, SVdec=0.75):
        simulate_count = 10
        for axis in axis_map:
            self.__motion_status[axis['axis_id']] = 14
            for count in range(simulate_count):
                self.__axis_pulse[axis['axis_id']] += axis['pulse'] / simulate_count
                sleep(0.02)
            self.__motion_status[axis['axis_id']] = 0
        return 0

    def absolute_move(self, axis_map, timeout, speed, Tacc=0.2, Tdec=0.2, SVacc=0.75, SVdec=0.75):
        now_position = [0] * 8
        for axis in axis_map:
            now_position[axis['axis_id']] = self.__axis_pulse[axis['axis_id']]

        simulate_count = 10
        for axis in axis_map:
            self.__motion_status[axis['axis_id']] = 14
            for count in range(simulate_count):
                shift_position = axis['pulse'] - now_position[axis['axis_id']]
                self.__axis_pulse[axis['axis_id']] += shift_position / simulate_count
                sleep(0.02)
            self.__motion_status[axis['axis_id']] = 0
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
        