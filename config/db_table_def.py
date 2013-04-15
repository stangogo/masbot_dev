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
            #                            ,
            # 'SingleAxis': OrderedDict( [('axis_key', ['varchar(20)']),
            #                            ('axis_name',['varchar(20)']),
            #                            ('motor_type', ['int']),
            #                            ('proportion', ['int']),
            #                            ('ABSM', ['int']),
            #                            ('ABSR', ['int']),
            #                            ('TLC', ['int']),
            #                            ('DO1', ['int']),
            #                            ('ZSP', ['int']),
            #                            ('scope_min', ['int']),
            #                            ('scope_max', ['int']),
            #                            ('state', ['int'])] )
            #                            , 
            #'Nozzle': OrderedDict([ ('key', ['varchar(20)']),
            #                        ('updown_action', ['int']),
            #                        ('blow_action',['int']),
            #                        ('suck_action', ['int']),
            #                        ('top_sensor', ['int']),
            #                        ('low_sensor', ['int']),
            #                        ('pressure_sensor', ['int']),
            #                        ('display_text', ['varchar(20)']),
            #                        ('get_delay', ['int']),
            #                        ('suck_delay', ['int']),
            #                        ('put_delay', ['int'])
            #                    ])
            #                    ,
            #'Nozzle_UI': OrderedDict([ ('reference_val', ['varchar(30)']),
            #                           ('display_text', ['varchar(30)']),
            #                           ('col_order', ['int']),
            #                           ('display_type', ['int']),
            #                           ('btn_on_str', ['varchar(10)']),
            #                           ('btn_off_str', ['varchar(10)']),
            #                           ('value_set', ['int'])
            #                         ])
            #                    ,
            #'options': OrderedDict([ ('id', ['varchar(30)']),
            #                         ('value', ['varchar(30)'])
            #                        ])
                                    ,
                    
             'AxisOP': [['position', '位置'], ['state','狀態'], [' + ','加'], [' - ','減'], ['scale','單位']]
             #                       ,
             #'ImageThumbnailID': ['1stCorrect', 'GlueIdentify', '2stCorrect', '66Six']
             
            }           
    
    def get_table_def(self, table_name):
        return self.table[table_name]

table_schemas = [
"""
CREATE TABLE IF NOT EXISTS options(
    id TEXT not null,
    value REAL not null,
    PRIMARY KEY(id, value)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS nozzle(
    key TEXT not null,
    updown_action INTEGER,
    blow_action INTEGER,
    suck_action INTEGER,
    top_sensor INTEGER,
    low_sensor INTEGER,
    pressure_sensor INTEGER,
    display_text TEXT,
    get_delay INTEGER,
    suck_delay INTEGER,
    put_delay INTEGER,
    PRIMARY KEY(key)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS nozzle_ui(
    ui_id INTEGER not null,
    reference_val TEXT,
    display_text TEXT,
    col_order INTEGER,
    display_type TEXT,
    btn_on_str TEXT,
    btn_off_str TEXT,
    value_set TEXT,
    PRIMARY KEY(ui_id)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS single_axis(
    key TEXT not null,
    axis_id INTEGER,
    display_text TEXT,
    motion_module TEXT,
    motor_type TEXT,
    proportion INTEGER,
    speed INTEGER,
    ABSM INTEGER,
    ABSR INTEGER,
    DO1 INTEGER,
    ZSP INTEGER,
    TLC INTEGER,
    electric_brake INTEGER,
    scope_min REAL,
    scope_max REAL,
    composite INTEGER, 
    PRIMARY KEY(key)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS single_axis_points(
    key TEXT not null,
    point_index REAL not null,
    position REAL,
    display_text TEXT,   
    PRIMARY KEY(key, point_index),
    FOREIGN KEY(key) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS double_axis(
    key TEXT not null,
    display_text TEXT,
    motion_module INTEGER,
    group_id INTEGER,
    axis1 TEXT,
    axis2 TEXT,
    safe_speed INTEGER,
    speed INTEGER,
    PRIMARY KEY(key),
    FOREIGN KEY(axis1) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(axis2) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS double_axis_points(
    key TEXT not null,
    point_index TEXT not null,
    axis1_position REAL,
    axis2_position REAL,
    display_text TEXT,
    PRIMARY KEY(key, point_index),
    FOREIGN KEY(key) REFERENCES double_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS triple_axis(
    key TEXT not null,
    display_text TEXT,
    motion_module INTEGER,
    group_id INTEGER,
    axis1 TEXT,
    axis2 TEXT,
    axis3 TEXT,
    safe_speed INTEGER,
    speed INTEGER,
    PRIMARY KEY(key),
    FOREIGN KEY(axis1) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(axis2) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(axis3) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS triple_axis_points(
    key TEXT not null,
    point_index TEXT not null,
    axis1_position REAL,
    axis2_position REAL,
    axis3_position REAL,
    display_text TEXT, 
    PRIMARY KEY(key, point_index),
    FOREIGN KEY(key) REFERENCES triple_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS piston(
    key TEXT not null,
    `1st_output` INTEGER,
    `2nd_output` INTEGER,
    `1st_input` INTEGER,
    `2nd_input` INTEGER,
    `3rd_input` INTEGER,
    `4th_input` INTEGER,
    PRIMARY KEY(key)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS point(
    id INTEGER not null,
    x_axis REAL,
    y_axis REAL,
    note TEXT,
    display_text TEXT,
    key TEXT,
    go INTEGER,
    replace INTEGER,
    PRIMARY KEY(id)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS point_ui(
    id INTEGER not null,
    reference_val TEXT,
    display_text TEXT,
    col_order INTEGER,
    display_type TEXT,
    btn_on_str TEXT,
    btn_off_str TEXT,
    value_set TEXT,
    PRIMARY KEY(id)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS ui_layout(
    ui_name TEXT not null,
    col_id INTEGER not null,
    reference_val TEXT,
    display_text TEXT,
    col_order INTEGER,
    display_type TEXT,
    btn_on_str TEXT,
    btn_off_str TEXT,
    value_set TEXT,
    PRIMARY KEY(ui_name, col_id)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS io_card(
    card_module TEXT not null,
    card_id INTEGER not null,
    card_type TEXT,
    PRIMARY KEY(card_module, card_id)
);
"""
]


"""
SELECT trackid as id, trackname, artistname FROM artist inner join track on
artist.artistid = track.trackartist
"""