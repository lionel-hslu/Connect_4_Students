from time import sleep
from player_remote import Player_Remote


class Coordinator_Remote:
    """ 
    Coordinator for two Remote players
        - either playing over CLI or
        - playing over SenseHat

    This class manages the game flow, player registration, turn management, 
    and game status updates for Remote players using the Server.


    Attributes:
        api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        player (Player_Remote):    Local Instance of ONE remote Player (Raspi or Normal)
        sense (Optional[SenseHat]):   Optional Local Instance of a SenseHat (if on Raspi)
    """

    def __init__(self, api_url: str, on_raspi: bool = False) -> None:
        """
        Initialize the Coordinator_Remote.

        Parameters:
            api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
            on_raspi (bool):    Specifies if the game is played on a Raspberry Pi with SenseHat (default: False).

        Raises:
            ImportError: If `on_raspi` is True and the SenseHat module is not installed.
        """
        self.api_url: str = api_url

        if on_raspi:
            try:
                from sense_hat import SenseHat
                from player_raspi_remote import Player_Raspi_Remote
                self.sense = SenseHat()
                self.player = Player_Raspi_Remote(self.api_url, self.sense)
            except ImportError:
                raise ImportError("sense_hat module is not installed, but 'on_raspi' is set to True.")
        else:
            self.player = Player_Remote(self.api_url)

    def wait_for_second_player(self) -> None:
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.
        """
        self.player.visualize()
        print('Waiting for other Player.')
        sleep(1)

    def play(self) -> None:
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.
        """
        self.player.icon = self.player.register_in_game()
        while True:
            status = self.player.get_game_status()
            winner = status.get('winner')
            active = status.get('active_id')
            if winner:
                self.player.celebrate_win()
                break
            else:
                if str(active) == str(self.player.id):
                    self.player.visualize()
                    self.player.make_move()
                else:
                    self.wait_for_second_player()


if __name__ == "__main__":
    api_url = "http://127.0.0.1:5000"  # Connect 4 API server URL
    
    # Uncomment the following lines to specify different URLs
    pc_url = "http://169.254.189.184:5000"
    # pc_url = "http://10.147.97.97:5000"
    # pc_url = "http://127.0.1.1:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url)
    c_remote.play()
