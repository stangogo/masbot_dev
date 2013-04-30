# -*- coding: utf-8 -*-

# Title          : gather_data.py
# Description    : gather data information from the database
# Author         : Stan Liu
# Date           : 20130416
# Dependency     : 
# usage          : 
# notes          : 
from pprint import pprint
from masbot.config.sqldb import sqldb
from re import compile

#==========================================================================
# gather io card
#==========================================================================
result = sqldb.execute("select * from io_card")
col_info = result.record()
col_names = []

for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

io_card_info = {}
while result.next():
    card_list = []
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if col == 'card_module' and cell_value not in io_card_info:
            card_module = cell_value
            io_card_info[cell_value] = []
        if col == 'card_num' or col == 'card_type':
            card_list.append(cell_value)
    io_card_info[card_module].append(card_list)

# define all the motion card module
card_module = ['8154', '8158', 'LPLink', 'LPMax']
for module in card_module:
    if module not in io_card_info:
        io_card_info[module] = []

#==========================================================================
# piston info
#==========================================================================
result = sqldb.execute("select * from piston")
col_info = result.record()
col_names = []

for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

piston_info = []
while result.next():
    dic = {}
    for i, col in enumerate(col_names):
        dic[col] = result.value(i)
    piston_info.append(dic)
#==========================================================================
# axis_info and construct an axis map
#==========================================================================
result = sqldb.execute("select * from single_axis")
col_info = result.record()
col_names = []

for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

axis_map = {}
axis_info = []
while result.next():
    dic = {}
    for i, col in enumerate(col_names):
        dic[col] = result.value(i)
    axis_info.append(dic)
    key = dic['key']
    axis_map[key] = dic

#==========================================================================
# construct a points map
#==========================================================================
points_map = {}

result = sqldb.execute("select * from single_axis_point")
col_info = result.record()
col_names = []

for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

while result.next():
    position_list = []
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if col == 'key' and cell_value not in points_map:
            actor_name = cell_value
            points_map[actor_name] = {}
        elif col == 'point_index':
            pt_index = result.value(i)
        elif col == 'position':
            position_list.append(cell_value)
    points_map[actor_name][pt_index] = position_list

result = sqldb.execute("select * from double_axis_point")
col_info = result.record()
col_names = []
pattern = compile('^axis[0-9]_position$')

for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

while result.next():
    position_list = []
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if col == 'key' and cell_value not in points_map:
            actor_name = cell_value
            points_map[actor_name] = {}
        elif col == 'point_index':
            pt_index = result.value(i)
        elif pattern.match(col):
            position_list.append(cell_value)
    points_map[actor_name][pt_index] = position_list
#==========================================================================
# gather single axis info
#==========================================================================
motor_info = []
necessary_attribute = ['key', 'speed', 'safe_speed', 'module_type']
for axis in axis_info:
    if axis['individual']:
        dic = {'axis_info':[]}
        for k, v in axis.items():
            if k in necessary_attribute:
                dic[k] = v
        dic['axis_info'].append(axis)
        actor_name = axis['key']
        if actor_name in points_map:
            dic['points_info'] = points_map[actor_name]
        else:
            dic['points_info'] = {}
        motor_info.append(dic)

#==========================================================================
# gather double axis info
#==========================================================================
pattern = compile('^axis[0-9]$')
result = sqldb.execute("select * from double_axis")
col_info = result.record()
col_names = []
for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

while result.next():
    dic = {'axis_info': [], 'sub_axis': []}
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if pattern.match(col):
            key = cell_value
            dic['axis_info'].append(axis_map[key])
            dic['sub_axis'].append(key)
            dic['module_type'] = axis_map[key]['module_type']
        else:
            dic[col] = cell_value
        if col == 'key':
            actor_name = cell_value
            if actor_name in points_map:
                dic['points_info'] = points_map[actor_name]
        else:
                dic['points_info'] = {}
    motor_info.append(dic)
#==========================================================================
# camera_info combined with camera, camera_job and light
#==========================================================================

# extract light information dic from db
pattern = compile('^light[0-9]$')
result = sqldb.execute("select * from light")
col_info = result.record()
col_names = []
for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

light_info = {}
while result.next():
    list_value = {}
    light_name = ''
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if col == 'light_name':
            light_name = cell_value
        else:
            list_value.update({col:cell_value})
    light_info.update({light_name:list_value})
    
# extract camera job dic from db
result = sqldb.execute("select * from camera_job")
col_info = result.record()
col_names = []
for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

job_info = []
while result.next():
    lights = []
    dic = {}
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if pattern.match(col):
            if cell_value != '' and cell_value in light_info:
                lights.append(cell_value)
        else:
            dic.update({col:cell_value})
    dic.update({'light':lights})
    job_info.append(dic)

# extract camera information dic from db and combined above
result = sqldb.execute("select * from camera")
col_info = result.record()
col_names = []
for col in range(col_info.count()):
    col_names.append(col_info.fieldName(col))

camera_info = []
while result.next():
    all_dic = {}
    cam_dic = {}
    light_dic = {}
    job_dic = {}
    for i, col in enumerate(col_names):
        cell_value = result.value(i)
        if pattern.match(col):
            if cell_value != '' and cell_value in light_info:
                light_dic.update({cell_value:light_info.get(cell_value)})
        else:
            cam_dic.update({col:cell_value})
    all_dic.update({'light':light_dic})
    all_dic.update({'camera_set':cam_dic})
    for info in job_info:
        if info.get('camera') == cam_dic.get('camera_name'):            
            info.pop('camera')
            job_name = info.pop('job_name')
            job_dic.update({job_name:info})    
    all_dic.update({'camera_job':job_dic})
    camera_info.append(all_dic)