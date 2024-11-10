from game import Connect4
from player_local import Player_Local
#from player_raspi_local import Player_Raspi_Local



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
        
        self.game = Connect4()
        
        self.player1 = Player_Local(self.game)
        self.player2 = Player_Local(self.game)
        
        self.player1.icon = self.player1.register_in_game()
        self.player2.icon = self.player2.register_in_game()
        
        '''
        if on_raspi:
            # Potentially share SenseHat instance between two players
            from sense_hat import SenseHat
        else:
            pass
        raise NotImplementedError(f"You need to write this code first")
        '''
    

    def play(self):
        """ 
        Main function to run the game with two local players.
        
            This method handles player registration, turn management, 
            and checking for a winner until the game concludes.
        """
        
        while self.game.get_status()['winner'] == None:
            if self.player1.is_my_turn():
                self.player1.visualize()
                self.player1.make_move()
            
            elif self.player2.is_my_turn():
                self.player2.visualize()
                self.player2.make_move()
        
        
        self.player1.visualize()        
        self.player1.celebrate_win()



if __name__ == "__main__":
    C = Coordinator_Local()
    C.play()

