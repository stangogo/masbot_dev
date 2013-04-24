#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: Mar. 2013
"""
import sys
from PySide.QtGui import *
from masbot.config.utils import Path

def create_button(icon_file, text, hint):
    if icon_file:
        btn = QPushButton(QIcon('{0}/{1}'.format(Path.imgs_dir(), icon_file)),text)
    else:
        btn = QPushButton(text)

    btn.setToolTip(hint)
    return btn

def get_rotate_qicon(file_name, r_angle):
    file_path = "{0}/{1}".format(Path.imgs_dir(), file_name)
    qimage = QImage(file_path)        
    rotate = QTransform()
    rotate.rotate(r_angle)
    r_qimage = qimage.transformed(rotate)

    return QIcon(QPixmap.fromImage(r_qimage))