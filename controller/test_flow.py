from masbot.controller.wake_actor import *
#from masbot.device.device_manager import DeviceManager
#DM = DeviceManager()
#device_proxy = DM._get_device_proxy()

# utility sample
# actor['tbar'].send('servo_on')
# actor['tbar'].send('servo_off')
# actor['tbar'].send('abs_move', position=(10,20))

# actor['axis_z'].send('set_speed', speed=100)
# actor['axis_z'].send('set_acc_time', acc_time=0.2)
# actor['axis_z'].send('get_position')
# actor['axis_z'].send('rel_move', position=5)
# actor['axis_z'].send('pt_move', pt='z1')

# adlink.DO(31, 1)
# ret = adlink.DO_read(31)
# ret = adlink.DI(31)

def func1():
    print("this is function 1")
    
def func2():
    print("this is function 2")
    
func1()
func2()
