from game.board import Board
from game.rules import Rules
from ui.utils import pawn_possible_moves

class Agent:
    def __init__(self, name):
        self.name = name


    # devolve uma arvore com nós internos representando movimentos e folhas são tabuleiros resultantes desses movimentos
    def expand(self, board, player, depth):
        expansion_tree = {}
        pass #terminar implementação
        
    

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

    def evaluate(self, board, player):
        raise NotImplementedError("O método evaluate deve ser implementado por subclasses do Agent.")
    
    def choose_move(self, board, player, depth):
        raise NotImplementedError("O método choose_move deve ser implementado por subclasses do Agent.")
    
    