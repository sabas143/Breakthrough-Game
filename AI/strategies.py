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
        score = 0
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            x = pawn // 8
            white_score += x  # Peões mais avançados têm um valor maior

        for pawn in board.black_pawns:
            x = pawn // 8
            black_score += (7 - x)  # Peões mais avançados têm um valor maior

        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score

