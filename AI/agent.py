from game.rules import Rules
from ui.utils import pawn_possible_moves
from math import modf
from AI.strategies import Strategy
from time import time

class Agent:
    def __init__(self, name, player, strategy: Strategy, time_limit=2):
        self.name = name
        self.player = player
        self.strategy = strategy
        self.time_limit = time_limit

        #variaveis para log
        self.expanded_nodes = 0


        #variavel para iterative deepening
        self.start_time = 0
        self.time_limit_reached = False

    """Minimax com poda alpha-beta, para otimização do desempenho"""
    def minimax_alpha_beta(self, board, current_player, depth, alpha=float('-inf'), beta=float('inf')):
        #iterative deepening time check
        if time() - self.start_time > self.time_limit:
            self.time_limit_reached = True
            return 0, None

        #log de nós expandidos
        self.expanded_nodes += 1

        if(depth == 0 or Rules.check_winner(board) is not None):
            return self.evaluate(board, self.player, depth), None

        if(current_player == self.player):
            max_eval = float('-inf')
            best_move = None

            moves = self.possible_moves(board, current_player)
            moveOrder = []
            
            for move in moves:
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])

                moveOrder.append((move, self.evaluate(new_board, -current_player, depth - 1)))
            
            moveOrder.sort(key=lambda x: x[1], reverse=True)

            for move, _ in moveOrder:
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])
                eval, _ = self.minimax_alpha_beta(new_board, -current_player, depth - 1, alpha, beta)

                if(self.time_limit_reached):
                    return 0, None

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

            moves = self.possible_moves(board, current_player)
            moveOrder = []
            
            for move in moves:
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])

                moveOrder.append((move, self.evaluate(new_board, -current_player, depth - 1)))
            
            moveOrder.sort(key=lambda x: x[1])

            for move, _ in moveOrder:
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])
                eval, _ = self.minimax_alpha_beta(new_board, -current_player, depth - 1, alpha, beta)

                if(self.time_limit_reached):
                    return 0, None

                if eval < min_eval:
                    min_eval = eval
                    best_move = [move[0], move[1]]

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            return min_eval, best_move
        

    """Minimax sem poda alpha-beta, para comparação de desempenho"""
    def minimax(self, board, current_player, depth):
        #iterative deepening time check
        if time() - self.start_time > self.time_limit:
            self.time_limit_reached = True
            return 0, None

        #log de nós expandidos
        self.expanded_nodes += 1

        if(depth == 0 or Rules.check_winner(board) is not None):
            return self.evaluate(board, self.player, depth), None

        if(current_player == self.player):
            max_eval = float('-inf')
            best_move = None

            for move in self.possible_moves(board, current_player):
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])
                eval, _ = self.minimax(new_board, -current_player, depth - 1)

                if(self.time_limit_reached):
                    return 0, None

                if eval > max_eval:
                    max_eval = eval
                    best_move = [move[0], move[1]]
            
            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None

            for move in self.possible_moves(board, current_player):
                new_board = board.copy()
                new_board.move_pawn(move[0], move[1])
                eval, _ = self.minimax(new_board, -current_player, depth - 1)

                if(self.time_limit_reached):
                    return 0, None

                if eval < min_eval:
                    min_eval = eval
                    best_move = [move[0], move[1]]
            
            return min_eval, best_move

    
    def iterative_deepening(self, board, player, alpha_beta=True):
        best_move = None
        self.start_time = time()
        self.time_limit_reached = False

        depth = 1
        while not self.time_limit_reached:  # Limite de tempo de 2 segundos
            _, move = self.minimax_alpha_beta(board, player, depth) if alpha_beta else self.minimax(board, player, depth)
            depth += 1
            if not self.time_limit_reached:
                best_move = move
                last_depth = depth - 1
            
        
        
        return best_move, last_depth

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


    """
    Função para escolher o melhor movimento com base na estratégia do agente
        Parâmetros:
        - board: O tabuleiro atual do jogo
        - player: O jogador para o qual escolher o movimento (1 para branco, -1 para preto)
        - depth: A profundidade de busca para o algoritmo minimax
        Retorna:
        - Uma tupla ((x1, y1), (x2, y2)) representando o movimento escolhido, onde (x1, y1) é a posição inicial do peão e (x2, y2) é a posição final do peão após o movimento
    """ 
    def choose_move(self, board, player, alpha_beta=True):
        
        move, depth = self.iterative_deepening(board, player, alpha_beta)

        with open("logs/log.txt", "a") as f:
            f.write(f"{self.name} escolheu o movimento: {move} com {self.expanded_nodes} nos expandidos e profundidade : {depth}.\n")

        return move
    
    