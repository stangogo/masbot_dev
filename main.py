# -- coding: utf-8 --

from pprint import pprint
from masbot.config.global_settings import *
from masbot.actor.piston_actor import PistonActor

piston = {}
for rec in piston_info:
    piston[rec['key']] = PistonActor.start(rec)

#motor = {}
#for rec in motor_info:
#    if not rec['composite']:
#        motor[rec['key']] = AxisActor.start(rec)

#double_axis = {}
#for rec in motor_info:
#    double_axis[rec['key']] = AxisActor.start(rec)

def test():
    #print(piston['noz1'].ask({'msg':'state'}))
    print(piston['noz1'].ask({'msg':'action_on'}))
    print(piston['noz1'].ask({'msg':'action_status'}))
    print(piston['noz1'].ask({'msg':'action_off'}))
    print(piston['noz1'].ask({'msg':'action_status'}))
    print(piston['noz1'].ask({'msg':'sensor_status'}))

if __name__ == "__main__":
    print('main start')
    #test()
