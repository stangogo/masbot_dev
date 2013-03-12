# -- coding: utf-8 --

from masbot.config.global_settings import *
from masbot.motion.adlink import ADLinkMotion as Motion
from time import sleep

motion = Motion(motion_cfg)
axis_x = axis_cfg[0]

def single_amove(axis_info, position, speed=50, acc_time=0.3):
    axis_list = []
    axis_id = axis_info["axis_id"]
    proportion = axis_info["proportion"]
    pulse = position * proportion
    speed = speed * proportion
    axis_list.append(AxisInfo(axis_id, pulse))
    ret = motion.absolute_move(axis_list, speed)
    stat()
    return ret

def single_rmove(axis_info, distance, speed=50, acc_time=0.3):
    axis_id = axis_info["axis_id"]
    proportion = axis_info["proportion"]
    relative_pulse = distance * proportion
    speed = speed * proportion
    ret = motion.single_rmove(axis_id, relative_pulse, speed, acc_time, acc_time)
    for i in range(15):
        stat()
        sleep(0.05)
    
    return ret

def stat():
    pulse = motion.get_position(axis_x['axis_id'])
    position = pulse / axis_x['proportion']
    print("axis {}: pulse = {}, position = {}".format(axis_x["axis_name"], pulse, position))
    print("motion  = {}".format(motion.get_motion_status(0)))
    print("io  = {}".format(motion.get_io_status(0)))

def servo_on():
    motion.servo_on_off(axis_x, 1)
    ret = motion.sync_position(axis_x)
    stat()

def servo_off():
    motion.servo_on_off(axis_x, 0)

#servo_on()
if __name__ == "__main__":
    #motion.DO(0, 1)
    servo_on()
    #ret = single_rmove(axis_x, 10, 1)
    #print(ret)
    #stat()
