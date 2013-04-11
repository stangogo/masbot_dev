# -*- coding: utf-8 -*-

# Title          : common_lib.py
# Description    : framework common library
# Author         : Stan Liu
# Date           : 20130326
# Dependency     : 
# usage          : 
# notes          : 

import os
import logging.config
import yaml
#import codecs
from masbot.config.global_settings import *
from masbot.actor.piston_actor import PistonActor
from masbot.actor.motor_actor import MotorActor

# setup logging
masbot_dir = os.path.abspath(__file__ + "/../../")
os.chdir(masbot_dir)
path = masbot_dir + "/config/logging.yaml"
if os.path.exists(path):
    #logging.config.dictConfig(yaml.load(codecs.open(path,'r','utf-8')))
    logging.config.dictConfig(yaml.load(open(path,'r')))
else:
    logging.basicConfig(level=logging.INFO)

# initial all actors
actor = {}
for rec in piston_info:
    actor_name = rec['key']
    actor[actor_name] = PistonActor.start(rec)

for rec in motor_info:
    if not rec['composite']:
        actor_name = rec['key']
        points_info = single_axis_points[actor_name]
        actor[actor_name] = MotorActor.start(actor_name, [rec], points_info)

for actor_name, rec in double_axis_info.items():
    points_info = double_axis_points[actor_name]
    actor[actor_name] = MotorActor.start(actor_name, rec, points_info)

