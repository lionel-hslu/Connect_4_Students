import time

from sense_hat import SenseHat

from game import Connect4
from player_local import Player_Local


class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspi Player 
        Same as Local Player -> with some changed methods
            (uses Methods of Game and SenseHat)
    """

    def __init__(self, game:Connect4, sense:SenseHat, **kwargs) -> None:
        """ 
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players. (if SHARED option is used)
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        self.game = game
        self.sense = sense
        
        super().__init__(self.game, **kwargs)
        

        # Extract the SenseHat instance from kwargs  (only if SHARED instance)
        # Remove Otherwise
        '''
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")
        '''
        self.sense.clear()
        

    
    def register_in_game(self):
        """
        Register in game
            Set Player Icon 
            Set Player Color
        """
        # first do normal register
        self.icon = super().register_in_game()          # call method of Parent Class (Player_Local)

        if self.icon == 'X':
            self.color = (100,0,0)
        
        else:
            self.color = (100,100,0)

    
    def visualize_choice(self, column:int)->None:
        """ 
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """
        
        self.sense.set_pixel(column,0,self.color)
        time.sleep(0.1)
        self.sense.set_pixel(column,0,0,0,0)
        

    def visualize(self) -> None:
        """
        Override Visualization of Local Player
            Also Visualize on the Raspi 
        """
        board = self.game.get_board()
        
        for i in range(7):
            for j in range(8):
                if board[i,j] == 'X':
                    self.sense.set_pixel(j,i+1,100,0,0)
                elif board[i,j] == 'O':
                    self.sense.set_pixel(j,i+1,100,100,0)

        # OPTIONAL: also visualize on CLI
        super().visualize()


    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """
        col = 0
        
        while True:
            self.visualize_choice(col)
            
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        if col != 0:
                            col -= 1
                        else:
                            col = 7
                    
                    elif event.direction == 'right':
                        if col != 7:
                            col += 1
                        else:
                            col = 0
                            
                    elif event.direction == 'middle':
                        if self.game.check_move(col, self.id):
                            return col
                    
            time.sleep(0.1)
                
                
            '''
                move = int(input())  # Convert input to integer
                if 0 <= move <= 7:  # Check if move is within the valid range [0-7]
                    if self.game.check_move(move, self.id):  # Use self.game to validate
                        return move
                    else:
                        print('Invalid move! Column is full.')
                else:
                    print('Invalid input! Please enter a number between 0 and 7.')
            except ValueError:
                print('Invalid input! Please enter a number between 0 and 7.')
            '''
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Local Player
        """
        
        winner = self.get_game_status()['winner']
        
        if winner == 'X':
            color = (100,0,0)
        else:
            color = (100,100,0)
            
        pixels = [color]*64
            
        for i in range(10):
            self.sense.set_pixels(pixels)
            time.sleep(0.1)
            self.sense.clear()
            time.sleep(0.1)
            
        self.sense.clear()


        # Optional: also do CLI celebration
        super().celebrate_win()

