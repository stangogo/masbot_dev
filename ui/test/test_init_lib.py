# -*- coding: utf-8 -*-

# Title          : test_init_lib.py
# Description    : The initialization of ui test
# Author         : Cigar Huang
# Date           : 20130328
# Dependency     : 
# usage          : 
# notes          : 

import os
import logging.config
import yaml
import codecs


#change working directory.
masbot_dir = os.path.abspath(__file__ + "/../../../")
os.chdir(masbot_dir)

# setup logging  
path = masbot_dir + "/config/logging.yaml"

if os.path.exists(path):
    logging.config.dictConfig(yaml.load(codecs.open(path,'r','utf-8')))            
else:
    logging.basicConfig(level=logging.INFO)   

