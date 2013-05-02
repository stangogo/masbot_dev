# -*- coding: utf-8 -*-

# Title          : display_controller.py
# Description    : The display controller for image widget 
# Author         : Henry Chang 
# Date           : 20130502
# Dependency     : 
# usage          : 
# notes          : 

import logging
from masbot.device.channel import Channel
from masbot.controller.image_tools import *
from masbot.config.utils import SigName, UISignals

class DisplayController(Channel):
    def __init__(self):
        super(DisplayController, self).__init__()
        self.__logger = logging.getLogger(__name__)
        self.__slot = UISignals.GetSignal(SigName.QIMAGE_THUMBNAIL)
        
    def display_image(self, actor_name, display_text, infopath):
        self.run(self.__display, actor_name, display_text, infopath)
        
    def __display(self, actor_name, display_text, infopath):
        if actor_name:
            Qim = QImagefromData(infopath)
            msg = [Qim, actor_name, display_text]
            self.__slot.emit(msg)