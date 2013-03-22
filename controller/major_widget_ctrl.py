#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from masbot.ui.ui_interface.i_major_widget import IMajorWidget

from masbot.config.global_settings import *
from masbot.actor.piston_actor import PistonActor
from masbot.actor.motor_actor import MotorActor

#===========================test====================

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

#===========================test====================

class MajorWidgetCtrl(IMajorWidget):
    """
    繼承IRobotMajor的示範類別. 用來接收 MajorWidget 
    四個按鈕的click event.

    """
    def login_clicked(self):
        print('login is clicked')
        
    def servo_on_clicked(self):
        msg = 'default'
        motor['axis_z'].ask({'msg':'servo_on'})
        motor['axis_z'].ask({'msg':'sync_pulse'})
        position = motor['axis_z'].ask({'msg':'get_position'})
        msg = 'current msg = {}'.format(position)
        print(msg)
        self.flow_msg(msg)

    def pause_clicked(self):
        print('sss pause is clicked')
        self.alarm_msg('alarm message from interface')
        
    def start_clicked(self):     
        print('start is clicked')
        self.product_info_msg({ 'CT': 4.25, 
                                'ProdName': '9552A1', 
                                'MatchAngle':3.11, 
                                'AssembleMode': 'manually', 
                                'ProdBarCode': 'A222dsd323', 
                                'ProdNum': '11op98733', 
                                'Total': 200})
