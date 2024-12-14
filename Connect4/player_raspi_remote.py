import time
import requests
from player_remote import Player_Remote
import numpy as np
from sense_hat import SenseHat


class Player_Raspi_Remote(Player_Remote):
    """ 
    Remote Raspberry Pi Player implementation for Connect4.

    Extends the remote player with visualization and input using the Raspberry Pi Sense HAT.

    Attributes:
        sense (SenseHat): Instance of the Sense HAT for input and visualization.
        color (tuple[int, int, int]): RGB color for the player's icon on the Sense HAT.
    """

    def __init__(self, api_url: str, sense: SenseHat, **kwargs) -> None:
        """
        Initialize a remote Raspberry Pi player with a shared Sense HAT instance.

        Parameters:
            api_url (str): The API URL for the Connect4 game server.
            sense (SenseHat): The shared Sense HAT instance.
        """
        self.sense: SenseHat = sense
        self.api_url: str = api_url
        super().__init__(self.api_url, **kwargs)
        self.sense.clear()

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Additionally, sets the player's color based on their assigned icon.

        Returns:
            str: The player's icon ('X' or 'O').
        """
        self.icon = super().register_in_game()
        self.color = (100, 0, 0) if self.icon == 'X' else (100, 100, 0)
        return self.icon

    def visualize_choice(self, column: int) -> None:
        """
        Visualize the column selection process using the Sense HAT.

        Parameters:
            column (int): The currently selected column.
        """
        self.sense.set_pixel(column, 0, self.color)
        time.sleep(0.1)
        self.sense.set_pixel(column, 0, 0, 0, 0)

    def visualize(self) -> None:
        """
        Override visualization to update the Sense HAT LED matrix with the current board state.
        """
        url = f"{self.api_url}/connect4/board"
        response = requests.get(url)
        data = response.json()
        board = np.array(data["board"]).reshape(7, 8)
        for i in range(7):
            for j in range(8):
                if board[i, j] == 'X':
                    self.sense.set_pixel(j, i + 1, 100, 0, 0)
                elif board[i, j] == 'O':
                    self.sense.set_pixel(j, i + 1, 100, 100, 0)
        super().visualize()

    def make_move(self) -> int:
        """
        Use the Sense HAT joystick to select a column for the move.

        Returns:
            int: The selected column for the move.
        """
        col = 0
        url = f"{self.api_url}/connect4/make_move"
        while True:
            self.visualize_choice(col)
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        col = (col - 1) % 8
                    elif event.direction == 'right':
                        col = (col + 1) % 8
                    elif event.direction == 'middle':
                        data = {"column": col, "player_id": str(self.id)}
                        response = requests.post(url, json=data)
                        if response.status_code == 200:
                            return col
            time.sleep(0.1)

    def celebrate_win(self) -> None:
        """
        Celebrate a win by flashing the Sense HAT LEDs in the player's color.
        """
        winner = self.get_game_status()['winner']
        color = (100, 0, 0) if winner == 'X' else (100, 100, 0)
        pixels = [color] * 64
        for _ in range(10):
            self.sense.set_pixels(pixels)
            time.sleep(0.1)
            self.sense.clear()
            time.sleep(0.1)
        self.sense.clear()
        super().celebrate_win()
