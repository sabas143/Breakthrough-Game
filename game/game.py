class Game:
    def __init__(self, board, rules):
        self.board = board
        self.rules = rules
        self. current_player = 1
        self. game_over = False

    def change_player(self):
        self.current_player = -self.current_player
    
    def valid_move(self, start, end):
        return self.rules.valid_move(self.board, start, end, self.current_player)
    
    def move_pawn(self, start, end):
        if self.valid_move(start, end):
            self.board.move_pawn(start, end)

            winner = self.rules.check_winner(self.board)
            if winner is not None:
                self.game_over = True
            
            self.change_player()
    
