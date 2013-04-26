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

# enum is like in c++ (eg. num = enum('a','b','c')) 
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return enums

# setup logging
masbot_dir = os.path.abspath(__file__ + "/../../")
os.chdir(masbot_dir)
path = masbot_dir + "/config/logging.yaml"
if os.path.exists(path):
    logging.config.dictConfig(yaml.load(open(path,'r')))
else:
    logging.basicConfig(level=logging.INFO)

