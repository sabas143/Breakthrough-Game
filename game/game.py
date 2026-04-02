from game.rules import Rules
from AI.agent import Agent
from game.board import Board

class Game:
    def __init__(self, board = Board(), ai_players=None, time_limit=2):
        self.board = board
        self.current_player = 1
        self.game_over = False
        self.ai_players = {}
        self.time_limit = time_limit

        if ai_players is not None:
            for player in ai_players:
                if player[0] not in [1, -1]:
                    raise ValueError("Player must be 1 (white) or -1 (black)")
                
                agent = Agent(f"AI_preto", player[0], player[1], time_limit=self.time_limit) if player[0] == -1 else Agent(f"AI_branco", player[0], player[1], time_limit=self.time_limit)
                self.ai_players[player[0]] = agent
            
    def _change_player(self):
        self.current_player = -self.current_player

    def move_pawn(self, start, end):
        if self.game_over:
            return

        if Rules.valid_move(self.board, start, end, self.current_player):
            self.board.move_pawn(start, end)

            winner = Rules.check_winner(self.board)
            if winner is not None:
                self.game_over = True
            
            self._change_player()

    def play_ai_turn(self):
        if (self.ai_turn(self.current_player)) and not self.game_over:
            agent = self.ai_players[self.current_player]
            move = agent.choose_move(self.board, self.current_player)

            if move is not None:
                self.move_pawn(move[0], move[1])
            else:
                self.game_over = True  

    def ai_turn(self, player):
        return player in self.ai_players.keys()
    
    def play(self):
        turns = 0

        while not self.game_over and turns < 200:  # Limite de turnos para evitar jogos infinitos
            self.play_ai_turn()
            turns += 1
        return Rules.check_winner(self.board)
                

    
    
