# -*- coding: utf-8 -*-

# Title          : ftd2xx_dll.py
# Description    : define functions format in ftd2xx.dll
# Author         : Stan Liu
# Date           : 20130430
# Dependency     : ftd2xx.dll (ftd2xx64.dll if 64 bit)
# usage          : import ftd2xx_dll
# notes          : 

from time import sleep
from ctypes import *
from platform import architecture

# detect 32 bit or 64 bit
os_format = architecture()
if os_format[0] == '64bit':
    suffix = '64'
else:
    suffix = ''

# loaded shared libraries
d2xx = WinDLL(__file__ + '/../ftd2xx{}.dll'.format(suffix))

FT_HANDLE = c_void_p
FT_STATUS = c_ulong

# Device status
FT_OK = 0
FT_INVALID_HANDLE = 1
FT_DEVICE_NOT_FOUND = 2
FT_DEVICE_NOT_OPENED = 3
FT_IO_ERROR = 4
FT_INSUFFICIENT_RESOURCES = 5
FT_INVALID_PARAMETER = 6
FT_INVALID_BAUD_RATE = 7
FT_DEVICE_NOT_OPENED_FOR_ERASE = 8
FT_DEVICE_NOT_OPENED_FOR_WRITE = 9
FT_FAILED_TO_WRITE_DEVICE = 10
FT_EEPROM_READ_FAILED = 11
FT_EEPROM_WRITE_FAILED = 12
FT_EEPROM_ERASE_FAILED = 13
FT_EEPROM_NOT_PRESENT = 14
FT_EEPROM_NOT_PROGRAMMED = 15
FT_INVALID_ARGS = 16
FT_NOT_SUPPORTED = 17
FT_OTHER_ERROR = 18
FT_DEVICE_LIST_NOT_READY = 19

#def FT_SUCCESS(status):
#    return (status == FT_OK)

# FT_OpenEx_Flags
FT_OPEN_BY_SERIAL_NUMBER = 1
FT_OPEN_BY_DESCRIPTION = 2
FT_OPEN_BY_LOCATION = 4

# FT_ListDevices Flags (used in conjunction with FT_OpenEx Flags)
FT_LIST_NUMBER_ONLY= 0x80000000
FT_LIST_BY_INDEX = 0x40000000
FT_LIST_ALL = 0x20000000

FT_LIST_MASK  = (FT_LIST_NUMBER_ONLY|FT_LIST_BY_INDEX|FT_LIST_ALL)

# Baud Rates
FT_BAUD_300 = 300
FT_BAUD_600 = 600
FT_BAUD_1200 = 1200
FT_BAUD_2400 = 2400
FT_BAUD_4800 = 4800
FT_BAUD_9600 = 9600
FT_BAUD_14400 = 14400
FT_BAUD_19200 = 19200
FT_BAUD_38400 = 38400
FT_BAUD_57600 = 57600
FT_BAUD_115200 = 115200
FT_BAUD_230400 = 230400
FT_BAUD_460800 = 460800
FT_BAUD_921600 = 921600

# Word Lengths
FT_BITS_8 = c_ubyte(8)
FT_BITS_7 = c_ubyte(7)

# Stop Bits
FT_STOP_BITS_1 = c_ubyte(0)
FT_STOP_BITS_2 = c_ubyte(2)

# Parity
FT_PARITY_NONE = c_ubyte(0)
FT_PARITY_ODD = c_ubyte(1)
FT_PARITY_EVEN = c_ubyte(2)
FT_PARITY_MARK = c_ubyte(3)
FT_PARITY_SPACE = c_ubyte(4)

# Flow Control
FT_FLOW_NONE = 0x0000
FT_FLOW_RTS_CTS = 0x0100
FT_FLOW_DTR_DSR = 0x0200
FT_FLOW_XON_XOFF = 0x0400

# Purge rx and tx buffers
FT_PURGE_RX = 1
FT_PURGE_TX = 2

# Events
# typedef void (*PFT_EVENT_HANDLER)(DWORD,DWORD);
FT_EVENT_RXCHAR = 1
FT_EVENT_MODEM_STATUS = 2
FT_EVENT_LINE_STATUS = 4

# Timeouts
FT_DEFAULT_RX_TIMEOUT = 300
FT_DEFAULT_TX_TIMEOUT = 300

# Device types
FT_DEVICE = c_ulong

FT_DEVICE_BM = 0
FT_DEVICE_AM = 1
FT_DEVICE_100AX = 2
FT_DEVICE_UNKNOWN = 3
FT_DEVICE_2232C = 4
FT_DEVICE_232R = 5
FT_DEVICE_2232H = 6
FT_DEVICE_4232H = 7
FT_DEVICE_232H = 8

# Bit Modes
FT_BITMODE_RESET = 0x00
FT_BITMODE_ASYNC_BITBANG = 0x01
FT_BITMODE_MPSSE = 0x02
FT_BITMODE_SYNC_BITBANG = 0x04
FT_BITMODE_MCU_HOST = 0x08
FT_BITMODE_FAST_SERIAL = 0x10
FT_BITMODE_CBUS_BITBANG = 0x20
FT_BITMODE_SYNC_FIFO = 0x40

#  FT232R CBUS Options EEPROM values
FT_232R_CBUS_TXDEN = 0x00	#	Tx Data Enable
FT_232R_CBUS_PWRON = 0x01	#	Power On
FT_232R_CBUS_RXLED = 0x02	#	Rx LED
FT_232R_CBUS_TXLED = 0x03	#	Tx LED
FT_232R_CBUS_TXRXLED = 0x04	#	Tx and Rx LED
FT_232R_CBUS_SLEEP = 0x05	#	Sleep
FT_232R_CBUS_CLK48 = 0x06	#	48MHz clock
FT_232R_CBUS_CLK24 = 0x07	#	24MHz clock
FT_232R_CBUS_CLK12 = 0x08	#	12MHz clock
FT_232R_CBUS_CLK6 = 0x09	#	6MHz clock
FT_232R_CBUS_IOMODE = 0x0A	#	IO Mode for CBUS bit-bang
FT_232R_CBUS_BITBANG_WR = 0x0B	#	Bit-bang write strobe
FT_232R_CBUS_BITBANG_RD = 0x0C	#	Bit-bang read strobe

# FT232H CBUS Options EEPROM values
FT_232H_CBUS_TRISTATE = 0x00	#	Tristate
FT_232H_CBUS_RXLED = 0x01	#	Rx LED
FT_232H_CBUS_TXLED = 0x02	#	Tx LED
FT_232H_CBUS_TXRXLED = 0x03	#	Tx and Rx LED
FT_232H_CBUS_PWREN = 0x04	#	Power Enable
FT_232H_CBUS_SLEEP = 0x05	#	Sleep
FT_232H_CBUS_DRIVE_0 = 0x06	#	Drive pin to logic 0
FT_232H_CBUS_DRIVE_1 = 0x07	#	Drive pin to logic 1
FT_232H_CBUS_IOMODE = 0x08	#	IO Mode for CBUS bit-bang
FT_232H_CBUS_TXDEN = 0x09	#	Tx Data Enable
FT_232H_CBUS_CLK30 = 0x0A	#	30MHz clock
FT_232H_CBUS_CLK15 = 0x0B	#	15MHz clock
FT_232H_CBUS_CLK7_5 = 0x0C	#	7.5MHz clock

# define the argument and return type for the functions
d2xx.FT_Open.restype = FT_STATUS
d2xx.FT_Open.argtypes = [c_int, POINTER(FT_HANDLE)]

d2xx.FT_OpenEx.restype = FT_STATUS
d2xx.FT_OpenEx.argtypes = [c_char_p, c_ulong, POINTER(FT_HANDLE)]

d2xx.FT_ResetDevice.restype = FT_STATUS
d2xx.FT_ResetDevice.argtypes = [FT_HANDLE]

d2xx.FT_SetUSBParameters.restype = FT_STATUS
d2xx.FT_SetUSBParameters.argtypes = [FT_HANDLE, c_ulong, c_ulong]

d2xx.FT_SetChars.restype = FT_STATUS
d2xx.FT_SetChars.argtypes = [FT_HANDLE, c_ulong, c_ulong, c_ulong, c_ulong]

d2xx.FT_SetTimeouts.restype = FT_STATUS
d2xx.FT_SetTimeouts.argtypes = [FT_HANDLE, c_ulong, c_ulong]

d2xx.FT_SetLatencyTimer.restype = FT_STATUS
d2xx.FT_SetLatencyTimer.argtypes = [FT_HANDLE, c_ulong]

d2xx.FT_SetFlowControl.restype = FT_STATUS
d2xx.FT_SetFlowControl.argtypes = [FT_HANDLE, c_ulong, c_ulong, c_ulong]

d2xx.FT_SetBitMode.restype = FT_STATUS
d2xx.FT_SetBitMode.argtypes = [FT_HANDLE, c_ulong, c_ulong]

d2xx.FT_Write.restype = FT_STATUS
d2xx.FT_Write.argtypes = [FT_HANDLE, c_void_p, c_ulong, POINTER(c_ulong)]

d2xx.FT_Close.restype = FT_STATUS
d2xx.FT_Close.argtypes = [FT_HANDLE]

d2xx.FT_Read.restype = FT_STATUS
d2xx.FT_Read.argtypes = [FT_HANDLE, c_ubyte, c_ulong, POINTER(c_ulong)]

#d2xx..restype = FT_STATUS
#d2xx..argtypes = [FT_HANDLE]

# the format is byte
SNA = b"FTWIQLXYA"
SNB = b"FTWIQLXYB"

def passive_serial_download():
    ft_handle = c_void_p()
    ret = d2xx.FT_OpenEx(SNB, 1, ft_handle)
    if ret:
        print('FT_OpenEx', ret)
        return ret
    ret = d2xx.FT_ResetDevice(ft_handle)
    if ret:
        print('FT_ResetDevice', ret)
        return ret
    ret = d2xx.FT_SetUSBParameters(ft_handle, 65536, 65536)
    if ret:
        print('FT_SetUSBParameters',ret)
        return ret
    ret = d2xx.FT_SetChars(ft_handle, 0, 0, 0, 0)
    if ret:
        print('FT_SetChars',ret)
        return ret
    ret = d2xx.FT_SetTimeouts(ft_handle, 500, 500)
    if ret:
        print('FT_SetTimeouts',ret)
        return ret
    ret = d2xx.FT_SetLatencyTimer(ft_handle, 2)
    if ret:
        print('FT_SetLatencyTimer',ret)
        return ret
    ret = d2xx.FT_SetFlowControl(ft_handle, FT_FLOW_RTS_CTS, 0, 0)
    if ret:
        print('FT_SetFlowControl',ret)
        return ret
    ret = d2xx.FT_SetBitMode(ft_handle, 0, 0)
    if ret:
        print('FT_SetBitMode',ret)
        return ret
    ret = d2xx.FT_SetBitMode(ft_handle, 0, 2)
    if ret:
        print('FT_SetBitMode',ret)
        return ret

    send_size = pointer(c_ulong(0))
    buffer_size = 3
    TxBuffer = (c_ubyte * buffer_size)()
    
    # set up the hi-speed specific command for the ftx232h
    TxBuffer[0] = 0x8A
    TxBuffer[1] = 0x97
    TxBuffer[2] = 0x8D
    ret = d2xx.FT_Write(ft_handle, TxBuffer, 3, send_size)
    if ret:
        print('FT_Write',ret)
        return ret

    # set tck frequency
    TxBuffer[0] = 0x86
    TxBuffer[1] = 0x04
    TxBuffer[2] = 0x00
    ret = d2xx.FT_Write(ft_handle, TxBuffer, buffer_size, send_size)
    if ret:
        print('FT_Write',ret)
        return ret

    #  set initial states of the mpsse interface
    # low byte
    TxBuffer[0] = 0x80
    TxBuffer[1] = 0xFA
    TxBuffer[2] = 0xD3
    ret = d2xx.FT_Write(ft_handle, TxBuffer, buffer_size, send_size)
    if ret:
        print('FT_Write',ret)
        return ret
    
    # high byte
    TxBuffer[0] = 0x82
    TxBuffer[1] = 0xFF
    TxBuffer[2] = 0xFF
    ret = d2xx.FT_Write(ft_handle, TxBuffer, buffer_size, send_size)
    if ret:
        print('FT_Write',ret)
        return ret

    # clear nConfig
    TxBuffer[0] = 0x80
    TxBuffer[1] = 0xEA
    TxBuffer[2] = 0xD3
    ret = d2xx.FT_Write(ft_handle, TxBuffer, buffer_size, send_size)
    if ret:
        print('FT_Write',ret)
        return ret
    sleep(0.01)
    
    # set nConfig
    TxBuffer[0] = 0x80
    TxBuffer[1] = 0xFA
    TxBuffer[2] = 0xD3
    ret = d2xx.FT_Write(ft_handle, TxBuffer, buffer_size, send_size)
    if ret:
        print('FT_Write',ret)
        return ret
    sleep(0.01)
    
    print('download1 ok')
    return 0

def passive_serial_download2():
    rbf_raw = (c_ubyte * 500001)()
    rbf_buf = (c_ubyte * 65539)()
    
passive_serial_download()
passive_serial_download2()

