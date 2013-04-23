#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
顯示單軸狀態, 控制表單
                        author: Cigar Huang
                        website: zetcode.com 
                        last edited: 18 Mar. 2013
"""

import sys
import os
import threading
import time 
from threading import Thread
from PySide import QtGui, QtCore

from masbot.ui.robot.axis_table import AxisTable
from masbot.config.utils import Path, UISignals, SigName



class AxisBanner(QtGui.QWidget):

    def __init__(self):
        super(AxisBanner, self).__init__()
        
        self.init_ui()        
        
    def init_ui(self):
        title_label = QtGui.QLabel('單\n軸\n移\n動')
        title_label.setStyleSheet("QLabel { color:green; font-family: sans-serif; font-size: 18px;}")
        
        self.mode_button = QtGui.QPushButton()
        
        self.mode_button.setToolTip('只顯示有勾選的欄位')
        self.mode_button.setCheckable(True)
        self.mode_button.clicked.connect(self.mode_changed)
        self.mode_button.setIcon( self.get_rotate_qicon('top_right_expand.png', 270) )
        
        title_vbox = QtGui.QVBoxLayout()
        title_vbox.addWidget(title_label)
        title_vbox.addWidget(self.mode_button)
        title_vbox.setAlignment(title_label, QtCore.Qt.AlignCenter)
        
        self.table = AxisTable()        
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addLayout(title_vbox, 1)
        hbox.addWidget(self.table,40)
        hbox.addLayout(self.init_buttons())

        self.setLayout(hbox)
        self.setWindowTitle('Axis Banner')
        self.show()
    
    def init_buttons(self):
        push_ico = QtGui.QIcon("{0}/push.ico".format(Path.imgs_dir()))
        self.di_do_btn = QtGui.QPushButton(push_ico, "DIO\n顯示")
        self.di_do_btn.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.di_do_btn.setStyleSheet ("QPushButton{text-align:left}")
        self.di_do_btn.setFixedWidth(50)
        self.di_do_btn.setFixedHeight(50)
        self.di_do_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.di_do_btn.setCheckable(True)
        UISignals.RegisterSignal(self.di_do_btn.clicked, SigName.DI_DO_SHOW)
                
        to_robot_banner_btn = QtGui.QPushButton('至機台\n資訊')
        to_robot_banner_btn.setFixedWidth(50)
        to_robot_banner_btn.setFixedHeight(50)
        UISignals.RegisterSignal(to_robot_banner_btn.clicked, SigName.TO_ROBOT_BANNER)
        
        self.remove_image_btn = QtGui.QPushButton('右側\n開關')
        self.remove_image_btn.setCheckable(True)
        self.remove_image_btn.setChecked(True)
        self.remove_image_btn.setFixedWidth(50)
        self.remove_image_btn.setFixedHeight(50)
        self.remove_image_btn.clicked.connect(self.remove_image_btn_clicked)
        UISignals.RegisterSignal(self.remove_image_btn.clicked, SigName.REMOVE_IMG_SIDE)
        
        btn_v_layout = QtGui.QVBoxLayout()
        btn_v_layout.addWidget(self.remove_image_btn, 1)
        btn_v_layout.addWidget(to_robot_banner_btn, 0)
        btn_v_layout.addWidget(self.di_do_btn, 0)        
    
        return btn_v_layout
    
    def remove_image_btn_clicked(self):
        self.di_do_btn.setEnabled(self.remove_image_btn.isChecked()) 
        
    def mode_changed(self):
        self.table.change_diaplay_mode(self.sender().isChecked())
        if self.sender().isChecked():
            self.mode_button.setIcon( self.get_rotate_qicon('top_right_expand.png', 90) )
        else:
            self.mode_button.setIcon( self.get_rotate_qicon('top_right_expand.png', 270) )
   
    def get_rotate_qicon(self, file_name, r_angle):
        file_path = "{0}/{1}".format(Path.imgs_dir(), file_name)
        qimage = QtGui.QImage(file_path)        
        rotate = QtGui.QTransform()
        rotate.rotate(r_angle)
        r_qimage = qimage.transformed(rotate)
    
        return QtGui.QIcon(QtGui.QPixmap.fromImage(r_qimage))    
    
def main():    
    app = QtGui.QApplication(sys.argv)
    ex = AxisBanner()
    app.exec_()

if __name__ == '__main__':
    main()        