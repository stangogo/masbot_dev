# -- coding: utf-8 --

from pprint import pprint
from masbot.config.global_settings import *
from masbot.actor.piston_actor import PistonActor

piston = {}
for key, piston_info in piston_cfg.items():
    piston[key] = PistonActor.start(piston_info)
    
def test():
    print(piston['piston1'].ask({'msg':'state'}))
    print(piston['piston1'].ask({'msg':'react_on'}))
    print(piston['piston1'].ask({'msg':'react_status'}))
    print(piston['piston1'].ask({'msg':'react_off'}))
    print(piston['piston1'].ask({'msg':'react_status'}))

if __name__ == "__main__":
    print('main start')
    #test()
