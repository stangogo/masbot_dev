# -*- coding: utf-8 -*-

# Title          : image_tools.py
# Description    : All the image access tools
# Author         : Henry Chang 
# Date           : 20130430
# Dependency     : 
# usage          : 
# notes          : 

#import os
import os
from time import clock
from PySide.QtGui import *
from PIL import Image


class ImageTool():        
    def __init__(self):
        pass
    def QImagefromData(self, data_list):
        try:     
            if data_list[3] == 1:
                im = Image.frombuffer('L', [data_list[1],data_list[2]], data_list[0], 'raw', 'L', 0, 1)
                image_path = 'R:\\tmp1_{0:06d}.bmp'.format((int(clock()*100000)%100000))
                im.save(image_path)                
                Qim = QImage()
                Qim.load(image_path)
            elif data_list[3] == 3:
                im = Image.frombuffer('RGB', [data_list[1],data_list[2]], data_list[0], 'raw', 'RGB', 0, 1) 
                image_path = 'R:\\tmp3_{0:06d}.bmp'.format((int(clock()*100000)%100000))
                im.save(image_path)                
                Qim = QImage()
                Qim.load(image_path)  
            else:
                Qim = None    
        except:
            Qim = None
            
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except:
                pass            
        return Qim

class Painter(QPainter):
    def __init__(self):
        super(Painter, self).__init__()
        
    #def drawline(self, CenterX, CenterY, length, angle = 0):
            #try:
                #self.drawline()  
            #except:
                #pass        