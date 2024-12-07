class Connect4:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for _ in range(columns)] for _ in range(rows)]
        self.current_player = 1

    def is_valid_move(self, column):
        return self.board[0][column] == 0

    def make_move(self, column):
        for row in reversed(range(self.rows)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.current_player = 3 - self.current_player
                break

    def undo_move(self, column):
        for row in range(self.rows):
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                self.current_player = 3 - self.current_player
                break

    def check_winner(self):
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] != 0 and all(self.board[row][col + i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

        for row in range(self.rows - 3):
            for col in range(self.columns):
                if self.board[row][col] != 0 and all(self.board[row + i][col] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if self.board[row][col] != 0 and all(self.board[row + i][col + i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

                if self.board[row + 3][col] != 0 and all(self.board[row + 3 - i][col + i] == self.board[row + 3][col] for i in range(4)):
                    return self.board[row + 3][col]

        return 0

    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(self.columns))

def depth_first_search(game, depth, maximizing_player):
    if depth == 0 or game.is_full() or game.check_winner():
        winner = game.check_winner()
        if winner == 1:
            return 1
        elif winner == 2:
            return -1
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for col in range(game.columns):
            if game.is_valid_move(col):
                game.make_move(col)
                eval = depth_first_search(game, depth - 1, False)
                game.undo_move(col)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(game.columns):
            if game.is_valid_move(col):
                game.make_move(col)
                eval = depth_first_search(game, depth - 1, True)
                game.undo_move(col)
                min_eval = min(min_eval, eval)
        return min_eval

game = Connect4()
best_score = float('-inf')
best_move = None

for col in range(game.columns):
    if game.is_valid_move(col):
        game.make_move(col)
        score = depth_first_search(game, 4, False)
        game.undo_move(col)
        if score > best_score:
            best_score = score
            best_move = col

print(f"Best move: {best_move}")
