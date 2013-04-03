# -*- coding: utf-8 -*-

# Title          : bulletin.py
# Description    : provide a actor the board to declare or wipe the restriction
# Author         : Stan Liu
# Date           : 20130403
# Dependency     : 
# usage          : 
# notes          : 

import logging

class Bulletin(object):
    def __init__(self, author, board):
        """ initial the board from DeviceManager
        
        Example:
            
        Args:
            author: the actor who will write the restriction
            board: the shared board to all actors
        
        Returns:
            None
        
        Raises:
            
        """
        self.__logger = logging.getLogger(__name__)
        self.__author = author
        self.__board = board
        self.__board[self.__author] = []

    def declare(self, actor_name, restrict):
        """ declare the restriction to some actor on the board
        
        Example:
            nozzle.declare('tbar', 'move')
            piston1.declare('axis_r', 'move')
            piston2.declare('piston3', 'action_on')
            
        Args:
            actor_name: the actor who will be restricted
            restrict: the action that is not allowed
        
        Returns:
            None
        
        Raises:
            
        """     
        self.__board[self.__author].append([actor_name, restrict])
        self.__logger.debug("%s declares %s can't %s", self.__author, actor_name, restrict)

    def wipe(self, actor_name):
        """ wipe the restriction to some actor on the board
        
        Example:
            nozzle.wipe('tbar')
            
        Args:
            actor_name: the actor who was restricted
        
        Returns:
            None
        
        Raises:
            
        """
        for i, rec in enumerate(self.__board[self.__author]):
            if rec[0] == actor_name:
                del self.__board[self.__author][i]
        # when restriction of the author is empty , wipe it from the dictionary
        if not self.__board[self.__author]:
            del self.__board[self.__author]
        self.__logger.debug("%s wipes restriction of %s", self.__author, actor_name)

    def wipe_all(self):
        """ wipe all the restrictions to some actor on the board
        
        Example:
            nozzle.wipe_all()
            
        Args:
            None
        
        Returns:
            None
        
        Raises:
            
        """
        del self.__board[self.__author]
        self.__logger.debug("%s wipes his restriction", self.__author)
        
    def board_info(self):
        """ show the information from the shared board
        
        Example:
            nozzle.show_board()
            
        Args:
            None
        
        Returns:
            dict
        
        Raises:
            
        """
        return self.__board
    