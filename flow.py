# -- coding: utf-8 --

from masbot.config.global_settings import *
from masbot.motion.adlink_fake import adlink_motion as motion

if __name__ == "__main__":
    motion = motion(motion_config)
    motion.DO(0, 1)
    print(motion.DO_read(0))
    motion.DO(0, 0)
    print(motion.DO_read(0))
    motion.DO(32, 1)
    print(motion.DO_read(32))