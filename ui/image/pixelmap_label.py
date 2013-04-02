# Title          : PixelmapLabel.py
# Description    : Present a pixel map. Default height is 400.
#                  Using signal-slot to change the image
# Author         : Cigar Huang
# Date           : 20130307
# usage          : 
# notes          : 

import sys
import logging
from PySide import QtGui, QtCore


class PixelMapLabel(QtGui.QLabel):
    
    image_index = 0
    height = 400
    
    def __init__(self):
        super(PixelMapLabel, self).__init__()
        self.logger = logging.getLogger('ui.log')

    def set_height(self, height):
        self.height = height
    
    def update_pixmap(self, image_path, height=0):
        if height != 0:
            self.set_height(height)            
        pixmap = QtGui.QPixmap(image_path).scaledToHeight(self.height)
        self.setPixmap(pixmap)
        
    @QtCore.Slot(str)
    def change_image(self, image_path):
        self.update_pixmap(image_path)
        self.logger.debug("new image path: {0}".format(image_path))
