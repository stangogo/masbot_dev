# -*- coding: utf-8 -*-

from masbot.config.common_lib import *
from masbot.flow.main_flow import *
from time import sleep

def sample():
    actor['tbar'].send('servo_on', wait = False)
    actor['axis_z'].send('servo_on')
    actor['tbar'].send('get_position')
    actor['axis_z'].send('get_position')
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    #mf = MainFlow().start()
    #mf.send('start', wait=False)
    #sleep(5)
    #ret = mf.send('pause')
