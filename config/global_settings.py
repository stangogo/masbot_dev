# -- coding: utf-8 --

# Title          : global_settings.py
# Description    : calling functions in 8154.dll and 8158.dll of ADLink
# Author         : Stan Liu
# Date           : 20130307
# Dependency     : 
# usage          : import global_settings
# notes          : 

from collections import namedtuple
AxisInfo = namedtuple('AxisInfo', ['axis_id', 'position'])

motion_cfg = [ 
    (1, 'DI_CARD'),
    (3, 'DI_CARD'),
    (5, 'DI_CARD'),
    (7, 'DI_CARD'), 
    (11, 'DO_CARD'),
    (13, 'DO_CARD'),
    (15, 'DO_CARD'),
    (17, 'DO_CARD')
]

axis_cfg = [
    {
        'axis_name': 'X',
        'axis_id': 0,
        'proportion': 200,
        'accelerative_time': 0.3,
        'ABSM': 122,
        'ABSR': 123,
        'TLC': 124,
        'DO1': 122,
        'ZSP': 123,
        'scope_min': 5,
        'scope_max': 400
    }
]