# -- coding: utf-8 --

from masbot.config.global_settings import *
from masbot.motion.adlink import ADLinkMotion as Motion
from time import sleep
from masbot.actor.piston import Piston

def move_xy(x, y, speed=50, acc_time=0.3):
    axis_list = []
    position = {}
    position['axis_x'] = x
    position['axis_y'] = y
    for key, axis in axis_cfg.items():
        axis_id = axis["axis_id"]
        proportion = axis["proportion"]
        pulse = position[key] * proportion
        axis_list.append(AxisInfo(axis_id, pulse))
    speed = speed * proportion
    ret = motion.absolute_move(axis_list, speed, acc_time, acc_time)
    stat()
    return ret

def single_rmove(axis_info, distance, speed=50, acc_time=0.3):
    axis_id = axis_info["axis_id"]
    proportion = axis_info["proportion"]
    relative_pulse = distance * proportion
    speed = speed * proportion
    ret = motion.single_rmove(axis_id, relative_pulse, speed, acc_time, acc_time)
    stat()
    return ret

def stat():
    for key, axis in axis_cfg.items():
        pulse = motion.get_position(axis['axis_id'])
        position = pulse / axis['proportion']
        print("axis {}: pulse = {}, position = {}".format(key, pulse, position))
        print("motion = {}".format(motion.get_motion_status(axis["axis_id"])))
    print("io status = {}".format(motion.get_io_status(0)))

def servo_on():
    for key, axis in axis_cfg.items():
        motion.servo_on_off(axis, 1)
        ret = motion.sync_position(axis)
    stat()
    return ret

def servo_off():
    for key, axis in axis_cfg.items():
        ret = motion.servo_on_off(axis, 0)
    return ret

motion = Motion(motion_cfg)
stat()

if __name__ == "__main__":
    #motion.DO(0, 1)
    #servo_on()
    piston1_cfg = {'action': 0, 'on_sensor': 0, 'off_sensor': 1}
    piston1 = Piston.start(motion, piston1_cfg)

    piston2_cfg = {'action': 3, 'on_sensor': 0, 'off_sensor': 1}
    piston2 = Piston.start(motion, piston2_cfg)

    print("ready to run 2 pistons down")
    sleep(0.5)
    piston1.tell({'command': 'down_no_wait'})
    piston2.tell({'command': 'down_no_wait'})
    print("ready to run 2 pistons down")
    sleep(0.5)
    piston1.tell({'command': 'up_no_wait'})
    piston2.tell({'command': 'up_no_wait'})
