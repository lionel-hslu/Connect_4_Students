import os
from game import Connect4
from player import Player
import numpy as np

class Player_Local(Player):
    """ 
    Local Player implementation for Connect4.

    A local player directly interacts with the game methods for making moves
    and visualizing the game board.

    Attributes:
        game (Connect4): Instance of the Connect4 game.
    """

    def __init__(self, game: Connect4) -> None:
        """
        Initialize a local player with a reference to the Connect4 game instance.

        Parameters:
            game (Connect4): The Connect4 game instance.
        """
        super().__init__()
        self.game: Connect4 = game

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon ('X' or 'O').
        """
        return self.game.register_player(self.id)

    def is_my_turn(self) -> bool:
        """
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        return self.id == self.get_game_status()['active_id']

    def get_game_status(self) -> dict:
        """
        Retrieve the current status of the game.

        Returns:
            dict: The game's current status, including active player, winner, and turn.
        """
        return self.game.get_status()

    def make_move(self) -> int:
        """
        Prompt the local player to make a move by selecting a column.

        Returns:
            int: The column chosen by the player for their move.
        """
        print(f"It's {self.icon}'s turn. Which column do you select? [0-7]")
        while True:
            try:
                move = int(input())
                if 0 <= move <= 7:
                    if self.game.check_move(move, self.id):
                        return move
                    else:
                        print("Invalid move! Column is full.")
                else:
                    print("Invalid input! Please enter a number between 0 and 7.")
            except ValueError:
                print("Invalid input! Please enter a number between 0 and 7.")

    def visualize(self) -> None:
        """
        Print the current state of the Connect4 board to the console.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        board = self.game.get_board()
        board = np.where(board == '', ' ', board)

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
        Celebrate the win by displaying a message on the console.
        """
        winner = self.get_game_status()['winner']
        print(f"Player {winner} won.")
