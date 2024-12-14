
import os
import requests
from player import Player
import numpy as np


class Player_Remote(Player):
    """ 
    Remote Player implementation for Connect4.

    Communicates with the Connect4 game server to interact with the game state.

    Attributes:
        api_url (str): The API URL for the Connect4 game server.
    """

    def __init__(self, api_url: str) -> None:
        """
        Initialize a remote player.

        Parameters:
            api_url (str): The API URL for the Connect4 game server.
        """
        super().__init__()
        self.api_url: str = api_url

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon ('X' or 'O').
        """
        url = f"{self.api_url}/connect4/register"
        data = {'player_id': str(self.id)}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            player_icon = response.json().get('player_icon')
            return player_icon
        else:
            raise ConnectionError(f"Failed to register player: {response.status_code}")

    def is_my_turn(self) -> bool:
        """
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        return self.id == self.get_game_status().get('active_player')

    def get_game_status(self) -> dict:
        """
        Retrieve the current status of the game.

        Returns:
            dict: A dictionary containing the game's status, such as active player, winner, and turn.
        """
        url = f"{self.api_url}/connect4/status"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"Failed to retrieve game status: {response.status_code}")

    def make_move(self) -> int:
        """
        Prompt the remote player to select a column and make a move.

        Returns:
            int: The column chosen by the player for their move.
        """
        url = f"{self.api_url}/connect4/make_move"
        print(f"It's {self.icon}'s turn. Which column do you select? [0-7]")
        while True:
            try:
                move = int(input())
                if 0 <= move <= 7:
                    data = {'column': move, 'player_id': str(self.id)}
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        return move
                    else:
                        print("Invalid move! Column is full.")
                else:
                    print("Invalid input! Please enter a number between 0 and 7.")
            except ValueError:
                print("Invalid input! Please enter a number between 0 and 7.")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect4 board in the console.
        """
        url = f"{self.api_url}/connect4/board"
        response = requests.get(url)
        if response.status_code == 200:
            board = np.array(response.json()["board"]).reshape(7, 8)
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
        else:
            raise ConnectionError(f"Failed to retrieve board: {response.status_code}")

    def celebrate_win(self) -> None:
        """
        Celebrate the win by displaying a message in the console.
        """
        self.visualize()
        winner = self.get_game_status().get('winner')
        print(f"Player {winner} won.")
