# -- coding: utf-8 --
import unittest
from masbot.device.motion.adlink_fake import ADLinkMotion as Motion
from masbot.device.motion.adlink_table import *
from masbot.config.global_settings import *
from collections import namedtuple
AxisInfo = namedtuple('AxisInfo', ['axis_id', 'position'])

cards_config = [ 
    (1,'DI_CARD'),# (3,'DI_CARD'), (5,'DI_CARD'), (7,'DI_CARD'), 
    (9,'DO_CARD')#, (11,'DO_CARD'), (13,'DO_CARD'), (15,'DO_CARD')
]
motion = Motion(cards_config)

class ADLinkTest(unittest.TestCase):

    def test_initial(self):
        ret = motion.initial()
        self.assertIn(ret, [0, -1])

    def test_absolute_move(self):
        axis_list = []
        axis_list.append(AxisInfo(0, 55.66))
        axis_list.append(AxisInfo(1, 183.123))
        axis_list.append(AxisInfo(2, 77.88))
        
        speed = 200
        ret = motion.absolute_move(axis_list, speed)
        self.assertIn(ret, error_table.values())

if __name__ == '__main__':
    unittest.main(verbosity=2)
