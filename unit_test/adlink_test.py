# -- coding: utf-8 --
import unittest
from masbot.motion.adlink import adlink_motion as motion

cards_config = [ 
    (1,'DI_CARD'),# (3,'DI_CARD'), (5,'DI_CARD'), (7,'DI_CARD'), 
    (9,'DO_CARD')#, (11,'DO_CARD'), (13,'DO_CARD'), (15,'DO_CARD')
]

motion = motion(cards_config)

class AdlinkTest(unittest.TestCase):

    def test_initial(self):
        ret = motion.initial()
        self.assertIn(ret, [0, -1])

if __name__ == '__main__':
    unittest.main(verbosity=2)