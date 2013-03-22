# -- coding: utf-8 --

from pprint import pprint
from masbot.config.global_settings import *
from masbot.actor.piston_actor import PistonActor
from masbot.actor.motor_actor import MotorActor

piston = {}
for rec in piston_info:
    piston[rec['key']] = PistonActor.start(rec)

motor = {}
for rec in motor_info:
    if not rec['composite']:
        points_info = single_axis_points[rec['key']]
        motor[rec['key']] = MotorActor.start([rec], points_info)

for key, rec in double_axis_info.items():
    points_info = double_axis_points[key]
    motor[key] = MotorActor.start(rec, points_info)

def test():
    #print(piston['noz1'].ask({'msg':'state'}))
    print(piston['noz1'].ask({'msg':'action_on'}))
    print(piston['noz1'].ask({'msg':'action_status'}))
    print(piston['noz1'].ask({'msg':'action_off'}))
    print(piston['noz1'].ask({'msg':'action_status'}))
    print(piston['noz1'].ask({'msg':'sensor_status'}))
    print("=================================\n")
    print(motor['axis_z'].ask({'msg':'servo_on'}))
    print(motor['axis_z'].ask({'msg':'sync_pulse'}))
    print(motor['axis_z'].ask({'msg':'get_position'}))
    print(motor['axis_z'].ask({'msg':'abs_move', 'position': 200}))
    print(motor['axis_z'].ask({'msg':'get_position'}))
    print(motor['axis_z'].ask({'msg':'pt_move', 'pt': 'z1'}))
    print(motor['axis_z'].ask({'msg':'get_position'}))
    print("=================================\n")
    print(motor['tbar'].ask({'msg':'servo_on'}))
    print(motor['tbar'].ask({'msg':'sync_pulse'}))
    print(motor['tbar'].ask({'msg':'get_position'}))
    print(motor['tbar'].ask({'msg':'abs_move', 'position': (123, 456)}))
    print(motor['tbar'].ask({'msg':'get_position'}))
    print(motor['tbar'].ask({'msg':'pt_move', 'pt': 'p1'}))
    print(motor['tbar'].ask({'msg':'get_position'}))
    print(motor['tbar'].ask({'msg':'rel_move', 'position': (300, -400)}))
    print(motor['tbar'].ask({'msg':'get_position'}))
    #print(motor['tbar'].ask({'msg':'get_position'}))
    #print(motor['tbar'].ask({'msg':'rel_move', 'position': (50, 20)}))
    #print(motor['tbar'].ask({'msg':'get_position'}))

if __name__ == "__main__":
    print('main start')
    #test()
