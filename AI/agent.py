from game.rules import Rules
from ui.utils import pawn_possible_moves
from math import modf
from AI.strategies import Strategy

class Agent:
    def __init__(self, name, player, strategy: Strategy):
        self.name = name
        self.player = player
        self.strategy = strategy

    def minimax(self, board, current_player, depth, alpha=float('-inf'), beta=float('inf')):
        if(depth == 0 or Rules.check_winner(board) is not None):
            return self.evaluate(board, self.player, depth), None

        if(current_player == self.player):
            max_eval = float('-inf')
            best_move = None

            for move in self.possible_moves(board, current_player):
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])
                eval, _ = self.minimax(new_board, -current_player, depth - 1, alpha, beta)

                if eval > max_eval:
                    max_eval = eval
                    best_move = [move[0], move[1]]

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            
            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None

            for move in self.possible_moves(board, current_player):
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])
                eval, _ = self.minimax(new_board, -current_player, depth - 1, alpha, beta)

                if eval < min_eval:
                    min_eval = eval
                    best_move = [move[0], move[1]]

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            return min_eval, best_move

    """
    Função para obter os movimentos possíveis de um jogador específico
    Parametros:
    - board: O tabuleiro atual do jogo
    - player: O jogador para o qual obter os movimentos (1 para branco, -1 para preto)
    Retorna:
    - Uma lista de movimentos possíveis, onde cada movimento é representado como uma tupla ((x1, y1), (x2, y2), move_type)
    - (x1, y1): A posição inicial do peão
    - (x2, y2): A posição final do peão após o movimento
    - move_type: O tipo de movimento (1 para movimento normal, 2 para captura)
    """
    def possible_moves(self, board, player):
        if(player == 1):
            pawns = board.white_pawns
        else:
            pawns = board.black_pawns

        moves = []


        for pos in pawns:
            x = pos // 8
            y = pos % 8

            for move in pawn_possible_moves(board, (x, y), player):
                moves.append(((x, y), (move[0], move[1]), move[2]))
        
        return moves

    def evaluate(self, board, player, depth=0):
        return self.strategy.evaluate(board, player, depth)
    
    def choose_move(self, board, player, depth):
        
        _, move = self.minimax(board, player, True, depth)
        return move
    
    