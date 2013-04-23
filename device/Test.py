import os
import logging.config
import yaml
import codecs
from masbot.device.image_module import *
""" Initialization of Logger
"""
#change working directory.
masbot_dir = os.path.abspath(__file__ + "/../../")
os.chdir(masbot_dir)

# setup logging  
path = masbot_dir + "/config/logging.yaml"

if os.path.exists(path):
    logging.config.dictConfig(yaml.load(codecs.open(path,'r','utf-8')))            
else:
    logging.basicConfig(level=logging.INFO)   
    
img = ImageHandler('cam_check')
img._assign_dll('camera_check')
