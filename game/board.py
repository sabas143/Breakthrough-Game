class Board:
    EMPTY = 0
    WHITE = 1
    BLACK = -1

    SIZE = 8

    def __init__(self):
        self.grid = self.create_board()

    def create_board(self):
        board = []

        for i in range(self.SIZE):
            row = []

            for _ in range(self.SIZE):
                if i < 2:
                    row.append(self.BLACK)

                elif i < 6:
                    row.append(self.EMPTY)

                else:
                    row.append(self.WHITE)
            
            board.append(row)
        
        return board
    
    def place_pawn(self, x, y, pawn):
        self.grid[x][y] = pawn

    def remove_pawn(self, x, y):
        self.grid[x][y] = self.EMPTY

    def move_pawn(self, start, end):
        x1, y1 = start
        x2, y2 = end

        pawn = self.grid[x1][y1]
        self.remove_pawn(x1, y1)
        self.place_pawn(x2, y2, pawn)
        