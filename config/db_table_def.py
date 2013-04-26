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
È°ûÂà•Ë£°Ê?‰æõ‰?Ë≥áÊ?Â∫´Á?Ë≥áÊ?Ë°®Ê?‰ΩçÁ?ÂÆöÁæ©
?ñÊòØUIË£°Ë°®?ºÊ??Ä?ÑÊ©´Ëª∏Ê?Á∑ÉËª∏?ÑË°®??
    TrayInfo: ?Ä?§Ë??ôÁ?Ë≥áÊ?Ë°®Ê?‰Ω?
    SingleAxis: ?ÆËª∏ÁßªÂ?Ë≥áÊ?Ë°®Ê?‰Ω?
    AxisOP: ?ÆËª∏ÁßªÂ?UIË°®Ê†ºÁ∏±Ëª∏Ë°®È†≠

"""


class DBTableDefine():
    table = {'TrayInfo': OrderedDict( [ ('LogTime',     ['varchar(20)', '?Ä?§Ê???]) , 
                                        ('CT',          ['float',       '?ÆÈ?ÁµÑË??ÇÈ?']),
                                        ('ProdName',    ['varchar(20)', '?¢Â??çÁ®±']),
                                        ('MatchAngle',  ['float',       '?çÂ?ËßíÂ∫¶']),
                                        ('AssembleMode',['varchar(20)', 'ÁµÑË?Ê®°Â?']),
                                        ('ProdBarCode', ['varchar(20)', '?êÂ??§Ê?Á¢?]),
                                        ('ProdNum',     ['varchar(20)', '?êÂ??§Ë?']),
                                        ('Total',       ['int',         '?êÂ?Á∏ΩÊï∏'])] )
                                    ,
             'AxisOP': [['position', '‰ΩçÁΩÆ'], ['state','?Ä??], [' + ','??], [' - ','Ê∏?], ['scale','?Æ‰?'], ['display','']]
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
    module_type TEXT,
    updown_action INTEGER,
    blow_action INTEGER,
    suck_action INTEGER,
    top_sensor INTEGER,
    low_sensor INTEGER,
    pressure_sensor INTEGER,
    display_text TEXT,
    get_delay INTEGER DEFAULT 200,
    suck_delay INTEGER DEFAULT 200,
    put_delay INTEGER DEFAULT 200,
    PRIMARY KEY(key)
);
"""

,
"""
CREATE TABLE IF NOT EXISTS single_axis(
    key TEXT not null,
    axis_id INTEGER,
    display_text TEXT,
    module_type TEXT,
    motor_type TEXT DEFAULT 'servo',
    proportion INTEGER DEFAULT 500,
    speed INTEGER DEFAULT 200,
    safe_speed INTEGER DEFAULT 50,
    ABSM INTEGER,
    ABSR INTEGER,
    DO1 INTEGER,
    ZSP INTEGER,
    TLC INTEGER,
    electric_brake INTEGER,
    scope_min REAL DEFAULT -999,
    scope_max REAL DEFAULT 999,
    individual INTEGER DEFAULT 1,
    PRIMARY KEY(key)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS single_axis_point(
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
    group_id INTEGER,
    axis1 TEXT,
    axis2 TEXT,
    safe_speed INTEGER DEFAULT 50,
    speed INTEGER DEFAULT 200,
    PRIMARY KEY(key),
    FOREIGN KEY(axis1) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(axis2) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS double_axis_point(
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
    group_id INTEGER,
    axis1 TEXT,
    axis2 TEXT,
    axis3 TEXT,
    safe_speed INTEGER DEFAULT 50,
    speed INTEGER DEFAULT 200,
    PRIMARY KEY(key),
    FOREIGN KEY(axis1) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(axis2) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(axis3) REFERENCES single_axis(key) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS triple_axis_point(
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
    module_type TEXT,
    output1 INTEGER,
    output2 INTEGER,
    input1 INTEGER,
    input2 INTEGER,
    input3 INTEGER,
    input4 INTEGER,
    PRIMARY KEY(key)
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
    card_num INTEGER not null,
    card_type TEXT DEFAULT 'DO_CARD',
    PRIMARY KEY(card_module, card_num)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS light(
    light_name TEXT not null,
    module_type TEXT not null,
    port INTEGER not null,
    display_text TEXT,
    PRIMARY KEY(light_name)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS camera(
    camera_name TEXT not null,
    port INTEGER not null,
    camera_type TEXT not null,
    color_type TEXT not null,
    camera_mode TEXT not null,    
    pixel_size REAL DEFAULT 0,
    reverse_type INTEGER DEFAULT 0,
    gain_value INTEGER DEFAULT 100,
    shutter_value INTEGER DEFAULT 800,
    display_text TEXT,
    light1 TEXT,
    light2 TEXT,
    light3 TEXT,
    light4 TEXT,
    light5 TEXT,
    light6 TEXT,
    light7 TEXT,
    light8 TEXT,
    PRIMARY KEY(camera_name)
);
"""
,
"""
CREATE TABLE IF NOT EXISTS camera_job(
    job_name TEXT not null,
    camera TEXT not null,
    display_text TEXT,
    dll_name TEXT,
    light1 TEXT,
    light2 TEXT,
    light3 TEXT,
    PRIMARY KEY(job_name),
    FOREIGN KEY(camera) REFERENCES camera(camera_name) ON UPDATE CASCADE ON DELETE CASCADE
);
"""
,
"""
CREATE TABLE IF NOT EXISTS job_dll_parameter(
    job_name TEXT not null,
    dll_name TEXT not null,
    parameter_name TEXT  not null,
    parameter_value REAL,
    PRIMARY KEY(job_name, dll_name)    
);
"""
]
