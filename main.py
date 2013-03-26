# -*- coding: utf-8 -*-

from masbot.config.common_lib import *

def sample():
    motor['tbar'].send('servo_on', wait = False)
    motor['axis_z'].send('servo_on')
    motor['tbar'].send('get_position')
    motor['axis_z'].send('get_position')
    
if __name__ == "__main__":
    logging.info('main start')
    pass
