# -- coding: utf-8 --

from masbot.config.global_settings import *
from masbot.motion.adlink import ADLinkMotion as Motion

motion = Motion(motion_cfg)

def single_amove(axis_info, position, speed=50, acc_time=0.3):
    axis_list = []
    axis_id = axis_info["axis_id"]
    proportion = axis_info["proportion"]
    pulse = position * proportion
    speed = speed * proportion
    axis_list.append(AxisInfo(axis_id, pulse))
    ret = motion.absolute_move(axis_list, speed)

def single_rmove(axis_info, distance, speed=50, acc_time=0.3):
    axis_id = axis_info["axis_id"]
    proportion = axis_info["proportion"]
    relative_pulse = distance * proportion
    speed = speed * proportion
    return motion.single_rmove(axis_id, relative_pulse, speed, acc_time, acc_time)
    

def show_position(axis_info):
    pulse = motion.get_position(axis_info['axis_id'])
    position = pulse / axis_info['proportion']
    print("axis {}: pulse = {}, position = {}".format(axis_info["axis_name"], pulse, position))

if __name__ == "__main__":
    #motion.DO(0, 1)
    axis_x = axis_cfg[0]
    ret = motion.sync_position(axis_x)
    print(ret)
    show_position(axis_x)
    
    #ret = single_rmove(axis_x, 0.1)
    #print(ret)
    #show_position(axis_x)
