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
import codecs
from masbot.config.global_settings import *
from masbot.actor.piston_actor import PistonActor
from masbot.actor.motor_actor import MotorActor

# setup logging  
path = 'config/logging.yaml'
if os.path.exists(path):
    logging.config.dictConfig(yaml.load(codecs.open(path,'r','utf-8')))
else:
    logging.basicConfig(level=logging.INFO)

# initial actors
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