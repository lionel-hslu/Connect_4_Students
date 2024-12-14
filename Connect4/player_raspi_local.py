import time
from sense_hat import SenseHat
from game import Connect4
from player_local import Player_Local

class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspberry Pi Player implementation for Connect4.

    Extends the local player with visualization and input using the Raspberry Pi Sense HAT.

    Attributes:
        sense (SenseHat): Instance of the Sense HAT for input and visualization.
        color (tuple[int, int, int]): RGB color for the player's icon on the Sense HAT.
    """

    def __init__(self, game: Connect4, sense: SenseHat, **kwargs) -> None:
        """
        Initialize a local Raspberry Pi player with a shared Sense HAT instance.

        Parameters:
            game (Connect4): The Connect4 game instance.
            sense (SenseHat): The shared Sense HAT instance.
        """
        self.sense: SenseHat = sense
        super().__init__(game, **kwargs)
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
        board = self.game.get_board()
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
        while True:
            self.visualize_choice(col)
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        col = (col - 1) % 8
                    elif event.direction == 'right':
                        col = (col + 1) % 8
                    elif event.direction == 'middle':
                        if self.game.check_move(col, self.id):
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
