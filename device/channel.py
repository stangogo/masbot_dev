# -*- coding: utf-8 -*-

# Title          : channel.py
# Description    : restrict the communication on a channel
# Author         : Stan Liu
# Date           : 20130418
# Dependency     : 
# usage          : some_rs232 = Channel()
# notes          : 

from threading import Thread
from queue import Queue

class Channel(object):
    def __init__(self):
        self.__channel_is_run = True
        self.__command_queue = Queue()
        thread = Thread(target=self.__handle_command)
        thread.name = thread.name.replace('Thread', self.__class__.__name__)
        thread.daemon = True
        thread.start()
    
    def __del__(self):
        pass

    def start(self):
        """ start the channel (it will start initially)
        
        Example:
            channel.start()
            
        Args:
            None
        
        Returns:
            None
            
        Raises:
            None
        """
        self.__channel_is_run = True
        
    def pause(self):
        """ pause the channel
        
        Example:
            channel.pause()
            
        Args:
            None
        
        Returns:
            None

        Raises:
            None
        """
        self.__channel_is_run = False
        
    def __handle_command(self):
        while self.__channel_is_run:
            job = self.__command_queue.get()
            func_name = job[0]
            result_queue = job[1]
            argv = job[2]
            ret = func_name(*argv)
            result_queue.put(ret)
    
    def run(self, func_name, *argv):
        """ run command by using the unique channel
        
        Example:
            channel.run(some_function, arg1, arg2, ...)
            
        Args:
            func_name(function_object): function name
            argv(list): arguments that wiil be passed to the function
        
        Returns:
            unrestricted

        Raises:
        
        """
        exe_result_queue = Queue()
        job = [func_name, exe_result_queue, argv]
        self.__command_queue.put(job)
        return exe_result_queue.get()

