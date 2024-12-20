from multiprocessing import Pool
import numpy as np
from scipy.ndimage import convolve


class MoveEvaluator:
    def __init__(self, target_depth, n_col, api_url):
        self.target_depth = target_depth
        self.n_col = n_col
        self.api_url = api_url
        
        
    
    def evaluate_moves(self, board, player_icon, opponent_icon):
        self.player_icon = player_icon
        self.opponent_icon = opponent_icon
        with Pool(processes=self.n_col) as pool:
            results = pool.starmap(self.evaluate_column, [(col, board.copy()) for col in range(self.n_col)])
        print(results)
        best_move = max(results, key=lambda x: x[1])
        return best_move[0]
        

    def evaluate_column(self, col, board):
        score_list = []
        depth = 0
        if self.check_move(col, board):
            board = self.place(col,self.player_icon, board)
            if np.sum(board != '') > 6:
                if self.__detect_win(board):
                    score_list.append(10000000)
            else:
                score_list,board, depth = self.evaluate_position(score_list,board, depth, self.opponent_icon)
        else:
            score_list.append(-10000000)
        print(sum(score_list))
        return col, sum(score_list)


    def evaluate_position(self, score_list, board, depth, current_icon):
        depth += 1

        for col in range(self.n_col):
            if self.check_move(col, board):
                board = self.place(col, current_icon, board)
                if np.sum(board != '') > 6:
                    if self.__detect_win(board):
                        if current_icon == self.player_icon:
                            score_list.append(self.target_depth - depth)
                        else:
                            score_list.append(-10 * (self.target_depth - depth))
                    else:
                        if depth != self.target_depth:
                            next_icon = self.opponent_icon if current_icon == self.player_icon else self.player_icon
                            score_list, board, depth = self.evaluate_position(score_list, board, depth, next_icon)

                else:
                    if depth != self.target_depth:
                        next_icon = self.opponent_icon if current_icon == self.player_icon else self.player_icon
                        score_list, board, depth = self.evaluate_position(score_list, board, depth, next_icon)
                board = self.undo(col, board)

        depth -= 1
        return score_list, board, depth
    


    def check_move(self, move, board):
        if board[0,move] == '':
            return True
        else:
            return False
        

    def place(self, c, icon, board):
        if board[-1,c] == '':
            board[-1,c] = icon
            return board
        else:
            row = np.argmax(board[:, c] != '')
            board[row-1, c] = icon
            return board
                    
                    
    def undo(self, c, board):
        row = np.argmax(board[:, c] != '')
        board[row, c] = ''
        return board
            
        
        
    def __detect_win(self, board)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """    
        # Define convolution kernels for detecting a win condition
        horizontal_group = np.array([[1, 1, 1, 1]])
        vertical_group = np.array([[1], [1], [1], [1]])
        diag_down_group = np.eye(4, dtype=int)  # Top-left to bottom-right
        diag_up_group = np.flipud(diag_down_group)  # Bottom-left to top-right

        # Check for each player if there's a winning condition
        for player_to_check in ["X", "O"]:
            player_board = (board == player_to_check).astype(int)

            # Check all directions using convolution for 4 in a row
            if (convolve(player_board, horizontal_group, mode="constant", cval=0) == 4).any():
                return True
            if (convolve(player_board, vertical_group, mode="constant", cval=0) == 4).any():
                return True
            if (convolve(player_board, diag_down_group, mode="constant", cval=0) == 4).any():
                return True
            if (convolve(player_board, diag_up_group, mode="constant", cval=0) == 4).any():
                return True

        # Return False if no win condition is found for either player
        return False
