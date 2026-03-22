from game.rules import Rules

class Strategy:
    def evaluate(self, board):
        raise NotImplementedError("Subclasses must implement this method")
    
""" Estratégia de material: Avalia a posição com base na contagem de peões, dando um valor positivo para o jogador e negativo para o oponente."""
class MaterialStrategy(Strategy):
    def evaluate(self, board, player):
        white_count = sum(1 for row in board.grid for p in row if p == 1)
        black_count = sum(1 for row in board.grid for p in row if p == -1)

        if player == 1:
            return white_count - black_count
        else:
            return black_count - white_count


"""Estratégia de avanço: Avalia a posição dos peões, dando mais valor para peões que estão mais avançados no tabuleiro."""     
class AdvanceStrategy(Strategy):
    def evaluate(self, board, player):
        white_score = 0
        black_score = 0

        for pawn in board.black_pawns:
            x = pawn // 8
            black_score += x / 7  # Peões mais avançados têm um valor maior

        for pawn in board.white_pawns:
            x = pawn // 8
            white_score += (7 - x) / 7  # Peões mais avançados têm um valor maior

        white_score = white_score / len(board.white_pawns) if board.white_pawns else 0
        black_score = black_score / len(board.black_pawns) if board.black_pawns else 0

        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score



"""Estratégia de estruturas de apoio: Avalia a posição com base na formação dos peões, dando mais valor para peões que estão protegidos por outros peões."""
class SupportStructureStrategy(Strategy):
    def evaluate(self, board, player):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            back_diagonals = [pawn + 7, pawn + 9]  # Diagonais de apoio para peões brancos
            for diag in back_diagonals:
                if diag in board.white_pawns:
                    white_score += 1  # Peão protegido por outro peão branco
        
        for pawn in board.black_pawns:
            back_diagonals = [pawn - 7, pawn - 9]  # Diagonais de apoio para peões pretos
            for diag in back_diagonals:
                if diag in board.black_pawns:
                    black_score += 1  # Peão protegido por outro peão preto

        white_score = white_score / len(board.white_pawns) if board.white_pawns else 0
        black_score = black_score / len(board.black_pawns) if board.black_pawns else 0

        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score      


"""Estratégia de caminhos livres: Avalia a posição com base na quantidade de caminhos livres até a linha de chegada, dando mais valor para peões que têm um caminho mais claro para avançar."""
class FreePathStrategy(Strategy):
    def evaluate(self, board, player):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            x = pawn // 8
            y = pawn % 8
            free_path = True

            for i in range(x - 1, -1, -1):
                if board.grid[i][y] != 0:
                    free_path = False
                    break
            
            if free_path:
                white_score += 1

        for pawn in board.black_pawns:
            x = pawn // 8
            y = pawn % 8
            free_path = True

            for i in range(x + 1, 8):
                if board.grid[i][y] != 0:
                    free_path = False
                    break
            
            if free_path:
                black_score += 1


        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score
        

""""Estratégia de ameaças imediatas: com base na quantidade de peões que irão ganhar inevitavelmente ( não podem mais ser capturados)"""
class ImmediateThreatsStrategy(Strategy):
    def evaluate(self, board, player):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            x = pawn // 8
            y = pawn % 8

            if x == 0:  # Peão branco na linha de chegada
                white_score += 1
            else:
                # Verifica se o peão pode ser capturado
                if (y > 0 and board.grid[x - 1][y - 1] == -1) or (y < 7 and board.grid[x - 1][y + 1] == -1):
                    continue  
                else:
                    white_score += 1  
        
        for pawn in board.black_pawns:
            x = pawn // 8
            y = pawn % 8

            if x == 7:  # Peão preto na linha de chegada
                black_score += 1
            else:
                # Verifica se o peão pode ser capturado
                if (y > 0 and board.grid[x + 1][y - 1] == 1) or (y < 7 and board.grid[x + 1][y + 1] == 1):
                    continue  
                else:
                    black_score += 1  


        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score



class CombinedStrategy(Strategy):
    def __init__(self, strategies_with_weights):
        self.strategies = [s for s, w in strategies_with_weights]
        self.weights = [w for s, w in strategies_with_weights]

    def evaluate(self, board, player):
        total_score = 0
        for strategy, weight in zip(self.strategies, self.weights):
            total_score += weight * strategy.evaluate(board, player)
        
        if Rules.check_winner(board) == player:
            total_score += 1000  
        elif Rules.check_winner(board) == -player:
            total_score -= 1000
        
        return total_score