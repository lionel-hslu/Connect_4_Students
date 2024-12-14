from game import Connect4
from player_local import Player_Local
from typing import Optional

class Coordinator_Local:
    """
    Coordinator for two Local players.

    Manages the game flow, player registration, turn management, and game status updates for local players.

    Attributes:
        game (Connect4): Local instance of a Connect4 game.
        player1 (Player_Local | Player_Raspi_Local): Instance of the first player.
        player2 (Player_Local | Player_Raspi_Local): Instance of the second player.
        sense (Optional[SenseHat]): SenseHat instance used for visualization on Raspberry Pi.
    """

    def __init__(self, on_raspi: bool = True) -> None:
        """
        Initialize the Coordinator_Local with a Connect4 game and two players.

        Parameters:
            on_raspi (bool): Specifies if the game is played on a Raspberry Pi with SenseHat (default: True).
        """
        self.game: Connect4 = Connect4()
        self.sense: Optional[SenseHat] = None

        if on_raspi:
            from sense_hat import SenseHat
            from player_raspi_local import Player_Raspi_Local
            self.sense = SenseHat()
            self.player1: Player_Raspi_Local = Player_Raspi_Local(self.game, self.sense)
            self.player2: Player_Raspi_Local = Player_Raspi_Local(self.game, self.sense)
        else:
            self.player1: Player_Local = Player_Local(self.game)
            self.player2: Player_Local = Player_Local(self.game)

        self.player1.icon = self.player1.register_in_game()
        self.player2.icon = self.player2.register_in_game()

    def play(self) -> None:
        """
        Run the Connect4 game with two local players.

        Handles player registration, turn management, and checking for a winner until the game concludes.
        """
        while self.game.get_status()['winner'] is None:
            if self.player1.is_my_turn():
                self.player1.visualize()
                self.player1.make_move()
            elif self.player2.is_my_turn():
                self.player2.visualize()
                self.player2.make_move()

        self.player1.visualize()
        self.player1.celebrate_win()

if __name__ == "__main__":
    coordinator = Coordinator_Local(on_raspi=False)
    coordinator.play()
