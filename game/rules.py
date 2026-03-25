from .board import Board

class Rules:

    @staticmethod
    # retorna 0 se o movimento for inválido, 1 para movimento normal e 2 para captura
    def valid_move(board: Board, start, end, player_color):
        x1, y1 = start
        x2, y2 = end

        pawn = board.grid[x1][y1]

        if pawn == Board.EMPTY or pawn != player_color:
            return 0 

        if x1 < 0 or x1 >= Board.SIZE:
            return 0

        if y1 < 0 or y1 >= Board.SIZE:
            return 0

        if x2 < 0 or x2 >= Board.SIZE:
            return 0
        
        if y2 < 0 or y2 >= Board.SIZE:
            return 0
        
        direction = -1 if pawn == Board.WHITE else 1

        # Frente
        if (y1 == y2) and (x2 == x1 + direction) and (board.grid[x2][y2] == Board.EMPTY):
            return 1

        # Diagonal
        if (abs(y2 - y1) == 1) and (x2 == x1 + direction) and (board.grid[x2][y2] != player_color):
            if(board.grid[x2][y2] != Board.EMPTY):
                return 2
            return 1
        
        return 0

    @staticmethod
    def check_winner(board):
        for j in range(Board.SIZE):
            if board.grid[0][j] == Board.WHITE:
                return 1
            if board.grid[7][j] == Board.BLACK:
                return -1

        white_count = sum(1 for row in board.grid for p in row if p == Board.WHITE)
        black_count = sum(1 for row in board.grid for p in row if p == Board.BLACK)

        if white_count == 0: return -1
        if black_count == 0: return 1

        return None
