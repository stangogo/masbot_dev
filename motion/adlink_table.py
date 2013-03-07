# -- coding: utf-8 --

err_table = {}

err_table[-10000] = "Error Card number"
err_table[-10001] = "Error operation system version"
err_table[-10002] = "Error card's ID conflict"
err_table[-10300] = "Error other process exist"
err_table[-10301] = "Error card not found"
err_table[-10302] = "Error Open driver failed"
err_table[-10303] = "Error ID mapping failed"
err_table[-10304] = "Error trigger channel"
err_table[-10305] = "Error trigger type"
err_table[-10306] = "Error event already enable"
err_table[-10307] = "Error event not enable yet"
err_table[-10308] = "Error on board FIFO full"
err_table[-10309] = "Error unknown command type"
err_table[-10310] = "Error unknown chip type"
err_table[-10311] = "Error card not initial"
err_table[-10312] = "Error position out of range"
err_table[-10313] = "Error motion busy"
err_table[-10314] = "Error speed error"
err_table[-10315] = "Error slow down point"
err_table[-10316] = "Error axis range error"
err_table[-10317] = "Error compare parameter error"
err_table[-10318] = "Error compare method"
err_table[-10319] = "Error axis already stop"
err_table[-10320] = "Error axis INT wait failed"
err_table[-10321] = "Error user code write failed"
err_table[-10322] = "Error array size exceed"
err_table[-10323] = "Error factor number"
err_table[-10324] = "Error enable range"
err_table[-10325] = "Error auto accelerate time"
err_table[-10326] = "Error dwell time"
err_table[-10327] = "Error dwell distance"
err_table[-10328] = "Error new position"
err_table[-10329] = "Error motion not in running"
err_table[-10330] = "Error velocity change time"
err_table[-10331] = "Error speed target"
err_table[-10332] = "Error velocity percent"
err_table[-10333] = "Error position change backward"
err_table[-10334] = "Error counter number"
err_table[-10335] = "Error gpio input function parameter"
err_table[-10336] = "Error channel number"
err_table[-10337] = "Error ERC mode"
err_table[-10338] = "Error security code"

def get_msg(err_code):
    """ return the error message by the return code
    
    Example:
        get_msg(0) return 0
        get_msg(-10301) return "Error card not found"
        
    Args:
        error(integer): error code
    
    Returns:
        0 means sucess, or return the error message(string)

    Raises:
    
    """
    if err_code == 0:
        return 0
    elif err_code in err_table:
        return err_table[err_code]
    else:
        return 'Unknow Error code = %d' % err_code
