
import os
import requests
from player import Player
import numpy as np
from random import randint
from scipy.ndimage import convolve


class Bot_Player(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, api_url: str) -> None:
        """ 
        Initialize a local player.
            Must Implement all Methods from Abstract Player Class

        Parameters:
            game (Connect4): Instance of Connect4 game
        
       
        """
        super().__init__()  # Initialize id and icon from the abstract Player class
        self.api_url = api_url


    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.
        """
        url = f"{self.api_url}/connect4/register"
        data = {
            'player_id' : str(self.id)
        }
        
        
        response = requests.post(url, json=data)
        
        
        if response.status_code == 200:
            data = response.json()
            player_icon = data.get('player_icon')
            return(player_icon)
        
        else:
            return(response.status_code)


    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        return(self.id == self.get_game_status()['active_player'])

    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
      
        """
        url = f"{self.api_url}/connect4/status"
        
        response = requests.get(url)
        data = response.json()
        return(data)

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        url_move = f"{self.api_url}/connect4/make_move"

        def get_board():
            url_board = f"{self.api_url}/connect4/board"
            response = requests.get(url_board)
            data = response.json()
            board = np.array(data["board"]).reshape(7, 8)
            return board
        
        def check_move(board, move):
            if board[0,move] == '':
                return True
            else:
                return False

        score = 100000
        move = 0

        col = 8
        row = 7
        
        while True:
            for i in range(col):
                board = get_board()
                if check_move(board, i):
                    break

                

                
        
            

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        
        
        url = f"{self.api_url}/connect4/board"
        
        response = requests.get(url)
        data = response.json()
        
        board = np.array(data["board"]).reshape(7, 8)
        board = np.where(board == '', ' ', board)
        
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print('│  0  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │')
        print('╔═════╦═════╦═════╦═════╦═════╦═════╦═════╦═════╗')
        for i in range(13):
            if i % 2:
                print('╠═════╬═════╬═════╬═════╬═════╬═════╬═════╬═════╣')
            else:
                for j in range(8):
                    print(f'║  {board[int(i/2), j]}  ', end='')
                print('║')
        print('╚═════╩═════╩═════╩═════╩═════╩═════╩═════╩═════╝')


    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        self.visualize()
        winner = self.get_game_status()['winner']
        print(f'Player {winner} won.')








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
    

