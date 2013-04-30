#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Cigar Huang
last edited: August 2013
"""
import sys

camera_data = [{'name': '1',
                'rate': 0.00625,
                'gain': 100,
                'gain_min': 0,
                'gain_max': 100,
                'shutter': 10,
                'shutter_min': 0,
                'shutter_max': 10,
                'module': '5DW5F65E65EFE6',
                'resolution': '1624*1224',
                'FPS': 30,
                'light': ['積分球', '背光源', '同軸']
                }, 
               {'name': '2',
                'rate': 0.00703,
                'gain': 200,
                'gain_min': 0,
                'gain_max': 300,
                'shutter': 5,
                'shutter_min': 0,
                'shutter_max': 20,
                'module': '5DW5F6DFDSWD63',
                'resolution': '1624*1224',
                'FPS': 30,
                'light': ['積分球', '環形', '背光源', '環形2']
                }, 
               {'name': '3',
                'rate': 0.00662,
                'gain': 233,
                'gain_min': 0,
                'gain_max': 250,
                'shutter': 30,
                'shutter_min': 0,
                'shutter_max': 15,
                'module': '5GRTESFD6W5555',
                'resolution': '1624*1224',
                'FPS': 30,
                'light': ['背光源', '環形2']
                }, 
               {'name': '4',
                'rate': 0.00730,
                'gain': 443,
                'gain_min': 0,
                'gain_max': 500,
                'shutter': 100,
                'shutter_min': 0,
                'shutter_max': 250,
                'module': '5DW5DGDG6WEWC5',
                'resolution': '1624*1224',
                'FPS': 30,
                'light': ['積分球', '同軸', '圈圈', '背光源']
                }, 
               {'name': '5',
                'rate': 1,
                'gain': 11,
                'gain_min': 0,
                'gain_max': 150,
                'shutter': 2,
                'shutter_min': 0,
                'shutter_max': 15,
                'module': 'USB影像裝置',
                'resolution': '640*480',
                'FPS': 20,
                'light': ['積分球']
                }]


identification_data = [{'name': 'BARREL_DETECT',
                        'camera': '1',                                            
                        'light': ['積分球', '環形', '同軸', '圈圈', '背光源', '環形2'],
                        'IPI_file': 'IPQC_9598A1'
                        }
                       ,
                       {'name': 'TRAY_DETECT',
                        'camera': '3',
                        'light': ['積分球', '背光源'],                        
                        'IPI_file': 'IPQC_30003A2'
                        }
                       ,
                       {'name': 'CAMERA_CHECK',
                        'camera': '4',         
                        'light': ['積分球', '同軸'],
                        'IPI_file': 'IPQC_40019A2'
                        }
                       ]

IPI_files = ['Barrel_Orientation', 'Circle_Orientation', 'Camera_Check', 
             'IPQC_9552A1', 'IPQC_9582A1', 'IPQC_9538B1', 
             'IPQC_9450B', 'IPQC_30003A2', 'IPQC_50001B1']


demo_image_message = [['2013/03/04 AM 9:02.27', 'IPI', 'OK', 0.125, 'D:\\Images\\LPCam2\\Image20120809_211043_287.bmp'], 
                      ['2013/03/04 AM 9:02.51', 'IPI', 'OK', 0.125, 'D:\\Images\\LPCam2\\Image20120809_211044_068.bmp'], 
                      ['2013/03/04 AM 9:03.03', 'IPI', 'OK', 0.125, 'D:\\Images\\LPCam2\\Image20120809_211044_396.bmp'],
                      ['2013/03/04 AM 9:03.33', 'IPI', 'NG', 0.125, 'D:\\Images\\LPCam1\\Image20120809_211044_381.bmp'],
                      ['2013/03/04 AM 9:04.25', 'IPI', 'OK', 0.125, 'D:\\Images\\LPCam2\\Image20120809_211043_584.bmp'],
                      ]

def get_specific_fields_camera_data(fields):
    """
    傳入所所需camera資料的欄位, 回傳原始資料的內容
    @fields: field list. (皆為字串值)
    
    """
    keys = fields
    data_list = []
    
    # 從每一筆的原始資料
    for one_data in camera_data: 
        one = [] 
        # 所有指定的欄位
        for key in keys: 
            # 比對到所需的欄位, 把它加進 one 裡
            one = one + list(value for key_name, value in one_data.items() if key_name == key) 
            
        # 所有的欄位走一遍後, 把結果加進 data_list 裡
        data_list.append(one)

    # 走過每一筆camera_data 後的 data_list 就是結果
    return data_list



