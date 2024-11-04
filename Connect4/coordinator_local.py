from game import Connect4
from player_local import Player_Local
from player_raspi_local import Player_Raspi_Local



class Coordinator_Local:
    """ 
    Coordinator for two Local players
    
    This class manages the game flow, player registration, turn management, 
    and game status updates for local players.


    Attributes:
        game (Connect4):    Local Instance of a Connect4 Game
        player1 (Player_Local or Player_Raspi_Local):   Local Instance of a Player
        player2 (Player_Local or Player_Raspi_Local):   Local Instance of a Player
    """

    def __init__(self, on_raspi:bool = False) -> None:
        """
        Initialize the Coordinator_Local with a Game and 2 Players

        Parameters:
            on_raspi (bool):            If game is played on raspi (default False)
        """
        # TODO init correct player
        if on_raspi:
            # Potentially share SenseHat instance between two players
            from sense_hat import SenseHat
        else:
            pass
        raise NotImplementedError(f"You need to write this code first")
    

    def play(self):
        """ 
        Main function to run the game with two local players.
        
            This method handles player registration, turn management, 
            and checking for a winner until the game concludes.
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")



if __name__ == "__main__":
    # Create a coordinator
    # play a game
    # TODO
    raise NotImplementedError(f"You need to write this code first")
