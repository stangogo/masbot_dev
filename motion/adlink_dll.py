# -- coding: utf-8 --

# Title          : adlink_dll.py
# Description    : define functions format in 8154.dll and 8158.dll of ADLink
# Author         : Stan Liu
# Date           : 20130314
# Dependency     : 8154.dll 8158.dll
# usage          : import adlink_dll
# notes          : 

from ctypes import *

# loaded shared libraries
pci_8154 = WinDLL(__file__ + '/../../dlls/8154.dll')
pci_8158 = WinDLL(__file__ + '/../../dlls/8158.dll')

# define the argument and return type for the functions
pci_8154._8154_initial.restype = c_short
pci_8154._8154_initial.argtypes = [POINTER(c_ushort), c_short]
pci_8158._8158_initial.restype = c_short
pci_8158._8158_initial.argtypes = [POINTER(c_ushort), c_short]

pci_8154._8154_close.restype = c_short
pci_8154._8154_close.argtypes = []
pci_8158._8158_close.restype = c_short
pci_8158._8158_close.argtypes = []

pci_8154._8154_config_from_file.restype = c_short
pci_8154._8154_config_from_file.argtypes = []
pci_8158._8158_config_from_file.restype = c_short
pci_8158._8158_config_from_file.argtypes = []

pci_8158._8158_config_from_file2.restype = c_short
pci_8158._8158_config_from_file2.argtypes = [c_char_p]

pci_8154._8154_db51_HSL_initial.restype = c_short
pci_8154._8154_db51_HSL_initial.argtypes = [c_short]
pci_8158._8158_db51_HSL_initial.restype = c_short
pci_8158._8158_db51_HSL_initial.argtypes = [c_short]

pci_8154._8154_db51_HSL_auto_start.restype = c_short
pci_8154._8154_db51_HSL_auto_start.argtypes = [c_short]
pci_8158._8158_db51_HSL_auto_start.restype = c_short
pci_8158._8158_db51_HSL_auto_start.argtypes = [c_short]

pci_8154._8154_db51_HSL_stop.restype = c_short
pci_8154._8154_db51_HSL_stop.argtypes = [c_short]
pci_8158._8158_db51_HSL_stop.restype = c_short
pci_8158._8158_db51_HSL_stop.argtypes = [c_short]

pci_8154._8154_db51_HSL_close.restype = c_short
pci_8154._8154_db51_HSL_close.argtypes = [c_short]
pci_8158._8158_db51_HSL_close.restype = c_short
pci_8158._8158_db51_HSL_close.argtypes = [c_short]

pci_8154._8154_db51_HSL_set_scan_condition.restype = c_short
pci_8154._8154_db51_HSL_set_scan_condition.argtypes = [c_short, c_short, c_short]
pci_8158._8158_db51_HSL_set_scan_condition.restype = c_short
pci_8158._8158_db51_HSL_set_scan_condition.argtypes = [c_short, c_short, c_short]

pci_8154._8154_db51_HSL_slave_live.restype = c_short
pci_8154._8154_db51_HSL_slave_live.argtypes = [c_short, c_short, POINTER(c_short)]
pci_8158._8158_db51_HSL_slave_live.restype = c_short
pci_8158._8158_db51_HSL_slave_live.argtypes = [c_short, c_short, POINTER(c_short)]

pci_8154._8154_db51_HSL_D_write_channel_output.restype = c_short
pci_8154._8154_db51_HSL_D_write_channel_output.argtypes = [c_short, c_short, c_short, c_short]
pci_8158._8158_db51_HSL_D_write_channel_output.restype = c_short
pci_8158._8158_db51_HSL_D_write_channel_output.argtypes = [c_short, c_short, c_short, c_short]

pci_8154._8154_db51_HSL_D_read_output.restype = c_short
pci_8154._8154_db51_HSL_D_read_output.argtypes = [c_short, c_short, POINTER(c_ulong)]
pci_8158._8158_db51_HSL_D_read_output.restype = c_short
pci_8158._8158_db51_HSL_D_read_output.argtypes = [c_short, c_short, POINTER(c_ulong)]

pci_8154._8154_set_servo.restype = c_short
pci_8154._8154_set_servo.argtypes = [c_short, c_short]
pci_8158._8158_set_servo.restype = c_short
pci_8158._8158_set_servo.argtypes = [c_short, c_short]

pci_8154._8154_get_io_status.restype = c_short
pci_8154._8154_get_io_status.argtypes = [c_short, POINTER(c_ushort)]
pci_8158._8158_get_io_status.restype = c_short
pci_8158._8158_get_io_status.argtypes = [c_short, POINTER(c_ushort)]

pci_8154._8154_emg_stop.restype = c_short
pci_8154._8154_emg_stop.argtypes = [c_short]
pci_8158._8158_emg_stop.restype = c_short
pci_8158._8158_emg_stop.argtypes = [c_short]

pci_8154._8154_motion_done.restype = c_short
pci_8154._8154_motion_done.argtypes = [c_short]
pci_8158._8158_motion_done.restype = c_short
pci_8158._8158_motion_done.argtypes = [c_short]

pci_8154._8154_get_command.restype = c_short
pci_8154._8154_get_command.argtypes = [c_short, POINTER(c_long)]
pci_8158._8158_get_command.restype = c_short
pci_8158._8158_get_command.argtypes = [c_short, POINTER(c_long)]

pci_8154._8154_set_command.restype = c_short
pci_8154._8154_set_command.argtypes = [c_short, c_long]
pci_8158._8158_set_command.restype = c_short
pci_8158._8158_set_command.argtypes = [c_short, c_long]

pci_8154._8154_get_position.restype = c_short
pci_8154._8154_get_position.argtypes = [c_short, POINTER(c_double)]
pci_8158._8158_get_position.restype = c_short
pci_8158._8158_get_position.argtypes = [c_short, POINTER(c_double)]

pci_8154._8154_set_position.restype = c_short
pci_8154._8154_set_position.argtypes = [c_short, c_double]
pci_8158._8158_set_position.restype = c_short
pci_8158._8158_set_position.argtypes = [c_short, c_double]

pci_8154._8154_start_sr_move.restype = c_short
pci_8154._8154_start_sr_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sr_move.restype = c_short
pci_8158._8158_start_sr_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sr_line2.restype = c_short
pci_8154._8154_start_sr_line2.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sr_line2.restype = c_short
pci_8158._8158_start_sr_line2.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sr_line3.restype = c_short
pci_8154._8154_start_sr_line3.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sr_line3.restype = c_short
pci_8158._8158_start_sr_line3.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sr_line4.restype = c_short
pci_8154._8154_start_sr_line4.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sr_line4.restype = c_short
pci_8158._8158_start_sr_line4.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sa_move.restype = c_short
pci_8154._8154_start_sa_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sa_move.restype = c_short
pci_8158._8158_start_sa_move.argtypes = [c_short, c_double, c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sa_line2.restype = c_short
pci_8154._8154_start_sa_line2.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sa_line2.restype = c_short
pci_8158._8158_start_sa_line2.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sa_line3.restype = c_short
pci_8154._8154_start_sa_line3.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sa_line3.restype = c_short
pci_8158._8158_start_sa_line3.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_start_sa_line4.restype = c_short
pci_8154._8154_start_sa_line4.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]
pci_8158._8158_start_sa_line4.restype = c_short
pci_8158._8158_start_sa_line4.argtypes = [POINTER(c_short), POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double]

pci_8154._8154_home_search.restype = c_short
pci_8154._8154_home_search.argtypes = [c_short, c_double, c_double, c_double, c_double]
pci_8158._8158_home_search.restype = c_short
pci_8158._8158_home_search.argtypes = [c_short, c_double, c_double, c_double, c_double]

pci_8154._8154_set_home_config.restype = c_short
pci_8154._8154_set_home_config.argtypes = [c_short, c_short, c_short, c_short, c_short, c_short]
pci_8158._8158_set_home_config.restype = c_short
pci_8158._8158_set_home_config.argtypes = [c_short, c_short, c_short, c_short, c_short, c_short]

pci_8154._8154_set_inp.restype = c_short
pci_8154._8154_set_inp.argtypes = [c_short, c_short, c_short]
pci_8158._8158_set_inp.restype = c_short
pci_8158._8158_set_inp.argtypes = [c_short, c_short, c_short]