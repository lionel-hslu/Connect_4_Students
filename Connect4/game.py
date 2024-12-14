import uuid
import random
from scipy.ndimage import convolve
import numpy as np

class Connect4:
    """
    Connect 4 Game Class

    Manages the rules and logic of the Connect 4 game, including:
        - Defining win conditions
        - Validating moves
        - Managing the game board and player turns

    Attributes:
        p1 (Optional[uuid.UUID]): The unique identifier of Player 1.
        p2 (Optional[uuid.UUID]): The unique identifier of Player 2.
        p1_icon (str): Icon for Player 1 ('X').
        p2_icon (str): Icon for Player 2 ('O').
        board (np.ndarray): The game board represented as a 7x8 numpy array.
        turn_counter (int): Tracks the current turn number.
        winner (Optional[str]): Icon of the winning player, or None if no winner.
    """
    def __init__(self) -> None:
        """
        Initialize a new Connect 4 game.

        Sets up the game board, player icons, and game state.
        """
        self.p1: uuid.UUID | None = None
        self.p2: uuid.UUID | None = None
        self.p1_icon: str = 'X'
        self.p2_icon: str = 'O'
        self.board: np.ndarray = np.full((7, 8), '', dtype=str)
        self.turn_counter: int = -1
        self.winner: str | None = None

    def get_status(self) -> dict[str, uuid.UUID | str | int | None]:
        """
        Retrieve the current game status.

        Returns:
            dict: A dictionary containing:
                - 'active_id' (uuid.UUID | None): ID of the active player.
                - 'active_player' (str | None): Icon of the active player.
                - 'winner' (str | None): Icon of the winner, if any.
                - 'turn' (int): Current turn number.
        """
        if self.turn_counter == -1:
            active_player = None
            active_id = None
        elif self.turn_counter % 2:
            active_player = self.p2_icon
            active_id = self.p2
        else:
            active_player = self.p1_icon
            active_id = self.p1

        return {
            'active_id': active_id,
            'active_player': active_player,
            'winner': self.winner,
            'turn': self.turn_counter,
        }

    def register_player(self, player_id: uuid.UUID) -> str | bool:
        """
        Register a player in the game.

        Parameters:
            player_id (uuid.UUID): Unique identifier for the player.

        Returns:
            str: The player's assigned icon ('X' or 'O').
            bool: False if the game is full and no more players can register.
        """
        if self.p1 is None:
            self.p1 = player_id
            return 'X'
        elif self.p2 is None:
            self.p2 = player_id
            self.turn_counter += 1
            return 'O'
        else:
            return False

    def get_board(self) -> np.ndarray:
        """
        Get the current state of the game board.

        Returns:
            np.ndarray: A 7x8 numpy array representing the game board.
        """
        return self.board

    def check_move(self, column: int, player_id: uuid.UUID) -> bool:
        """
        Validate and execute a player's move.

        Parameters:
            column (int): The column where the player wants to drop their piece (0-indexed).
            player_id (uuid.UUID): The unique identifier of the player making the move.

        Returns:
            bool: True if the move is valid and executed, False otherwise.
        """
        if player_id == self.get_status()['active_id']:
            if self.board[0, column] == '':
                icon = 'X' if player_id == self.p1 else 'O'
                i = 1
                while True:
                    if self.board[-i, column] == '':
                        self.board[-i, column] = icon
                        break
                    else:
                        i += 1
                self.__update_status()
                return True
        return False

    def __update_status(self) -> None:
        """
        Update the game status after a valid move.

        Updates turn counter, active player, and checks for a winner.
        """
        self.turn_counter += 1
        self.winner = self.__detect_win()

    def __detect_win(self) -> str | None:
        """
        Detect if there is a winner in the game.

        Returns:
            str: The winning player's icon ('X' or 'O'), or None if no winner.
        """
        horizontal_group = np.array([[1, 1, 1, 1]])
        vertical_group = np.array([[1], [1], [1], [1]])
        diag_down_group = np.eye(4, dtype=int)
        diag_up_group = np.flipud(diag_down_group)

        for player_to_check in ['X', 'O']:
            player_board = (self.board == player_to_check).astype(int)
            if (convolve(player_board, horizontal_group, mode="constant", cval=0) == 4).any():
                return player_to_check
            if (convolve(player_board, vertical_group, mode="constant", cval=0) == 4).any():
                return player_to_check
            if (convolve(player_board, diag_down_group, mode="constant", cval=0) == 4).any():
                return player_to_check
            if (convolve(player_board, diag_up_group, mode="constant", cval=0) == 4).any():
                return player_to_check

        return None
