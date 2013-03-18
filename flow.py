# -- coding: utf-8 --

from masbot.config.global_settings import *
from masbot.motion.adlink_fake import ADLinkMotion as Motion
from masbot.actor.piston import Piston
from masbot.actor.doubleaxis import DoubleAxis

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
        if axis['motor_type'] == 'servo_type':
            ret = motion.sync_position(axis)
    stat()
    return ret

def servo_off():
    for key, axis in axis_cfg.items():
        ret = motion.servo_on_off(axis, 0)
    return ret

motion = Motion(motion_cfg)
stat()

# initial actor
piston = {}
for key, val in piston_cfg.items():
    piston[key] = {}
    piston[key] = Piston.start(motion, val)
tbar = DoubleAxis.start(motion, axis_cfg, xy_cfg)

def test():
    tbar.ask({'msg': 'move_xy', 'x': 250, 'y': 250})
    piston['piston1'].ask({'msg': 'down_action'})
    piston['piston2'].ask({'msg': 'down_action'})
    piston['piston1'].ask({'msg': 'up_action'}, False)
    piston['piston2'].ask({'msg': 'up_action'})
    tbar.ask({'msg': 'move_xy', 'x': 300, 'y': 300})
    piston['piston1'].ask({'msg': 'down_action'}, False)
    piston['piston2'].ask({'msg': 'down_action'})
    piston['piston1'].ask({'msg': 'up_action'}, False)
    piston['piston2'].ask({'msg': 'up_action'})
    
if __name__ == "__main__":
    #motion.DO(0, 1)
    #servo_on()
    test()