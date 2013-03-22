#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 Title          : db_table_def.py
 Description    : define the field of table in database or the header of table in UI
 Author         : Cigar Huang
 Date           : 20130320
 usage          : DBTableDefine().table[table_name]. ex. 'TrayInfo', 'SingleAxis'
 notes          : 

"""
from collections import OrderedDict

"""
類別裡提供了資料庫的資料表欄位的定義
或是UI裡表格所需的橫軸或緃軸的表頭
    TrayInfo: 退盤資料的資料表欄位
    SingleAxis: 單軸移動資料表欄位
    AxisOP: 單軸移動UI表格縱軸表頭

"""

class DBTableDefine():
    table = {'TrayInfo': OrderedDict( [ ('LogTime',     ['varchar(20)', '退盤時間']) , 
                                        ('CT',          ['float',       '單顆組裝時間']),
                                        ('ProdName',    ['varchar(20)', '產品名稱']),
                                        ('MatchAngle',  ['float',       '配對角度']),
                                        ('AssembleMode',['varchar(20)', '組裝模式']),
                                        ('ProdBarCode', ['varchar(20)', '成品盤條碼']),
                                        ('ProdNum',     ['varchar(20)', '成品盤號']),
                                        ('Total',       ['int',         '成品總數'])] )
                                        ,
             'SingleAxis': OrderedDict( [('axis_key', ['varchar(20)']),
                                        ('axis_name',['varchar(20)']),
                                        ('motor_type', ['int']),
                                        ('proportion', ['int']),
                                        ('accelerative_time', ['float']),
                                        ('ABSM', ['int']),
                                        ('ABSR', ['int']),
                                        ('TLC', ['int']),
                                        ('DO1', ['int']),
                                        ('ZSP', ['int']),
                                        ('scope_min', ['int']),
                                        ('scope_max', ['int']),
                                        ('state', ['int'])] )
                                        , 
            'Nozzle': OrderedDict([ ('key', ['varchar(20)']),
                                    ('updown_action', ['int']),
                                    ('blow_action',['int']),
                                    ('suck_action', ['int']),
                                    ('top_sensor', ['int']),
                                    ('low_senser', ['int']),
                                    ('pressure_sensor', ['int']),
                                    ('header_name', ['varchar(20)']),
                                    ('get_delay', ['int']),
                                    ('suck_delay', ['int']),
                                    ('put_delay', ['int'])
                                ])
                                ,
            'Nozzle_UI': OrderedDict([ ('nozzle_property', ['varchar(30)']),
                                       ('header_name', ['varchar(30)']),
                                       ('col_order', ['int']),
                                       ('display_type', ['int']),
                                       ('btn_on_str', ['varchar(10)']),
                                       ('btn_off_str', ['varchar(10)']),
                                       ('value_set', ['int'])
                                     ])
                                ,
            'options': OrderedDict([ ('id', ['varchar(30)']),
                                     ('value', ['varchar(30)'])                                     
                                    ])
                                    ,
                    
             'AxisOP': ['position', 'state', ' + ', ' - ', 'scale']
            }           
    
    def get_table_def(self, table_name):
        return self.table[table_name]
