# -*- coding: utf-8 -*-

# Title          : image_tools.py
# Description    : All the image access tools
# Author         : Henry Chang 
# Date           : 20130430
# Dependency     : 
# usage          : 
# notes          : 

import os
from time import clock
from PySide.QtGui import QImage, QPainter
from PIL import Image


def QImagefromData(data_list):
    try:     
        if isinstance(data_list, list):
            if data_list[3] == 1:
                im = Image.frombuffer('L', [data_list[1],data_list[2]], data_list[0], 'raw', 'L', 0, 1)
                image_path = 'R:\\tmp1_{0:.5f}.bmp'.format(clock())
                im.save(image_path)                
                Qim = QImage()
                Qim.load(image_path)
            elif data_list[3] == 3:
                im = Image.frombuffer('RGB', [data_list[1],data_list[2]], data_list[0], 'raw', 'RGB', 0, 1) 
                image_path = 'R:\\tmp1_{0:.5f}.bmp'.format(clock())
                im.save(image_path)                
                Qim = QImage()
                Qim.load(image_path)  
            else:
                Qim = None    
                image_path = None
            
            if os.path.exists(image_path):
                os.remove(image_path)  
        else:
            Qim = QImage()
            Qim.load(data_list)   
            if os.path.exists(data_list):
                os.remove(data_list)                  
    except:
        Qim = None           
            
    return Qim
        
class Painter(QPainter):
    def __init__(self):
        super(Painter, self).__init__()
        
    #def drawline(self, CenterX, CenterY, length, angle = 0):
            #try:
                #self.drawline()  
            #except:
                #pass        