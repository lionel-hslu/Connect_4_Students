import uuid
import random

from scipy.ndimage import convolve
import numpy as np


class Connect4:
    """
    Connect 4 Game Class

        Defines rules of the Game
            - what is a win
            - where can you set / not set a coin
            - how big is the playing field

        Also keeps track of the current game  
            - what is its state
            - who is the active player?

        Is used by the Coordinator
            -> executes the methods of a Game object
    """
    
    def __init__(self) -> None:
        """ 
        Init a Connect 4 Game
            - Create an empty Board
            - Create to (non - registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to False
            - etc.
        """
        self.p1 = None
        self.p2 = None
        self.board = np.full((7,8), ' ')
        self.turn_counter = 0
        self.winner = None


    """
    Methods to be exposed to the API later on
    """
    def get_status(self):
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
        """
        active_player = None
        
        if self.turn_counter % 2:
            active_player = self.p2
        else:
            active_player = self.p1
        
        return({'active_player': active_player, 'winner': self.winner, 'turn': self.turn_counter})

    def register_player(self, player_id:uuid.UUID)->str:
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if failed)
        """
        if self.p1 == None:
            self.p1 = player_id
            return('X')
        else:
            self.p2 = player_id
            return('O')


    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """
        return(self.board)


    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """
        if player_Id == self.get_status()['active_player']:
            if self.board[0,column] == ' ':
                
                if player_Id == self.p1:
                    icon = 'X'
                if player_Id == self.p2:
                    icon = 'O'
                
                i = 1    
                while True:
                    if self.board[-i,column] == ' ':
                        self.board[-i, column] = icon
                        break
                    else:
                        i += 1
                
                self.__update_status()
                return(True)
            else:
                return(False)
        else:
            return(False)
        
    """ 
    Internal Method (for Game Logic)
    """
    def __update_status(self):
        """ 
        Update all values for the status (after each successful move)
            - active player
            - active ID
            - winner
            - turn_number
        """

        self.turn_counter += 1
        self.winner = self.__detect_win()
    

    def __detect_win(self)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """    
        # Define convolution kernels for detecting a win condition
        horizontal_group = np.array([[1, 1, 1, 1]])
        vertical_group = np.array([[1], [1], [1], [1]])
        diag_down_group = np.eye(4, dtype=int)  # Top-left to bottom-right
        diag_up_group = np.flipud(diag_down_group)  # Bottom-left to top-right

        # Check for each player if there's a winning condition
        for player_to_check in ["X", "O"]:
            player_board = (self.board == player_to_check).astype(int)

            # Check all directions using convolution for 4 in a row
            if (convolve(player_board, horizontal_group, mode="constant", cval=0) == 4).any():
                return player_to_check
            if (convolve(player_board, vertical_group, mode="constant", cval=0) == 4).any():
                return player_to_check
            if (convolve(player_board, diag_down_group, mode="constant", cval=0) == 4).any():
                return player_to_check
            if (convolve(player_board, diag_up_group, mode="constant", cval=0) == 4).any():
                return player_to_check

        # Return False if no win condition is found for either player
        return None