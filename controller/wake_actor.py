# -*- coding: utf-8 -*-

# Title          : wake_actor.py
# Description    : waking all the actors
# Author         : Stan Liu
# Date           : 20130424
# Dependency     : PistonActor, MotorActor
# usage          : 
# notes          : 

from masbot.config.gather_data import *
from masbot.actor.piston_actor import PistonActor
from masbot.actor.motor_actor import MotorActor
from masbot.actor.camera_actor import CameraActor

# initial all actors
actor = {}
for rec in piston_info:
    actor_name = rec['key']
    actor[actor_name] = PistonActor.start(rec)

for rec in motor_info:
    actor_name = rec['key']
    actor[actor_name] = MotorActor.start(rec)

for rec in camera_info:
    actor[rec['camera_set']['camera_name']] = CameraActor.start(rec)
