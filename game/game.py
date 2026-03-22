from game.rules import Rules
from AI.agent import Agent

class Game:
    def __init__(self, board, ai_players=None, depth=3):
        self.board = board
        self.current_player = 1
        self.game_over = False
        self.ai_players = {}
        self.depth = depth

        if ai_players is not None:
            for player in ai_players:
                if player[0] not in [1, -1]:
                    raise ValueError("Player must be 1 (white) or -1 (black)")
                
                agent = Agent(f"AI_{player[0]}", player[0], player[1])
                print(f"Player {player[0]} is controlled by {agent.name} with strategy {type(agent.strategy).__name__}")
                self.ai_players[player[0]] = agent
            

    def change_player(self):
        self.current_player = -self.current_player
    

    def move_pawn(self, start, end):
        if self.game_over:
            return

        if Rules.valid_move(self.board, start, end, self.current_player):
            self.board.move_pawn(start, end)

            winner = Rules.check_winner(self.board)
            if winner is not None:
                self.game_over = True
                print(f"Player {winner} wins!")
            
            self.change_player()

    def play_ai_turn(self):
        if (self.ai_turn(self.current_player)) and not self.game_over:
            agent = self.ai_players[self.current_player]
            _, move = agent.minimax(self.board, self.current_player, depth=self.depth)

            if move is not None:
                self.move_pawn(move[0], move[1])

    def ai_turn(self, player):
        return player in self.ai_players.keys()
                

    
    
