# -*- coding: utf-8 -*-

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

if __name__ == "__main__":
    piston['noz1'].send('action_on')
    piston['noz1'].send('action_status')
    piston['noz1'].send('action_off')
    piston['noz1'].send('action_status')
    piston['noz1'].send('sensor_status')
    
    print("=================================\n")
    
    motor['axis_z'].send('servo_on')
    motor['axis_z'].send('get_position')
    motor['axis_z'].send('abs_move', position = 200 )
    motor['axis_z'].send('get_position')
    motor['axis_z'].send('pt_move', pt = 'z1' )
    motor['axis_z'].send('get_position')

    print("=================================\n")
    motor['tbar'].send('servo_on')
    motor['tbar'].send('get_position')
    motor['tbar'].send('abs_move', position = (123, 234))
    motor['tbar'].send('get_position')
    motor['tbar'].send('rel_move', position = (10, -54) )
    motor['tbar'].send('get_position')
    motor['tbar'].send('pt_move', pt = 'p1' )
    motor['tbar'].send('get_position')
