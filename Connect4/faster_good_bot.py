import os
import requests
from player import Player
import numpy as np # type: ignore
from move_class_v2 import MoveEvaluator
import time


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
        
        
        self.n_col = self.board_width
        self.target_depth = 6
        self.evaluator = MoveEvaluator(self.target_depth, self.n_col, self.api_url)


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
            self.player_icon = data.get('player_icon')
            if self.player_icon == 'X':
                self.opponent_icon = 'O'
            else:
                self.opponent_icon = 'X'
            
            return(self.player_icon)
        
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

    def make_move(self) -> None:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        self.visualize()

        start_time = time.time()
        board = self.get_board()
        
        if np.all(board == ''):
            best_move = 3
        else:
            best_move = self.evaluator.evaluate_moves(board, self.player_icon, self.opponent_icon)

        
        url = f"{self.api_url}/connect4/make_move"            
        data = {'column': best_move, 'player_id': str(self.id)}
        requests.post(url, json=data)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.6f} seconds")
        time.sleep(1)

                
        
            

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        
        
        
        board = self.get_board()
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




    def get_board(self) -> np.array:
        url_board = f"{self.api_url}/connect4/board"
        response = requests.get(url_board)
        data = response.json()
        board = np.array(data["board"]).reshape(7, 8)
        return board