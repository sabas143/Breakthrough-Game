class Board:
    EMPTY = 0
    WHITE = 1
    BLACK = -1

    SIZE = 8

    # posicão dos peões no formato linha*8 + coluna
    def __init__(self, black_pawns= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],\
                  white_pawns= [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]):
        #posiçao dos peões no formato linha*8 + coluna
        self.black_pawns = black_pawns
        self.white_pawns = white_pawns

        self.grid = self.create_board()


    def create_board(self):
        board = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]

        for i in range(16):
            x = self.black_pawns[i] // 8
            y = self.black_pawns[i] % 8
            board[x][y] = self.BLACK

            x = self.white_pawns[i] // 8
            y = self.white_pawns[i] % 8
            board[x][y] = self.WHITE

        
        
        return board
    
    def place_pawn(self, x, y, pawn):
        self.grid[x][y] = pawn

        if pawn == self.BLACK:
            self.black_pawns.append(8*x + y)
        elif pawn == self.WHITE:
            self.white_pawns.append(8*x + y)


    def remove_pawn(self, x, y):
        self.grid[x][y] = self.EMPTY

        if self.grid[x][y] == self.BLACK:
            self.black_pawns.remove(8*x + y)
        elif self.grid[x][y] == self.WHITE:
            self.white_pawns.remove(8*x + y)

    def move_pawn(self, start, end):
        x1, y1 = start
        x2, y2 = end

        pawn = self.grid[x1][y1]
        self.remove_pawn(x1, y1)
        self.place_pawn(x2, y2, pawn)
        