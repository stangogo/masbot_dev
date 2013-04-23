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
        if self.__author not in self.__board:
            self.__board[self.__author] = {}
        self.__board[self.__author][actor_name] = restrict
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
        del self.__board[self.__author][actor_name]
        # when restriction of the author is empty , wipe it from the dictionary
        if not self.__board[self.__author]:
            del self.__board[self.__author]
        self.__logger.debug("%s wipes restriction of %s", self.__author, actor_name)

    def wipe_all(self):
        """ wipe own all the restrictions on the board
        
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
            nozzle.board_info()
            
        Args:
            None
        
        Returns:
            dict
        
        Raises:
            
        """
        return self.__board

    def check_emg(self):
        """ check emergency status
        
        Example:
            supervisor.check_emg()

        Args:
        
        Returns:
            boolean
        
        Raises:
            
        """     
        if 'supervisor' not in self.__board:
            return False
        if self.__board['supervisor']['emg'] == 1:
            return True
        else:
            return False
            
    def check_workable(self, action):
        """ check if the actor is workable
        
        Example:
            axis_z.check_workable('move')
            
        Args:
            None
        
        Returns:
            boolean
        
        Raises:
            
        """
        if self.check_emg():
            return False
        for author, rec in self.__board.items():
            for actor, restrict in rec.items():
                if actor == self.__author and restrict == action:
                    return False
        return True
        
