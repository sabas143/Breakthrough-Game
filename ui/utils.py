from game.board import Board

def draw_board(screen, board_img):
    screen.blit(board_img, (0, 0))

def draw_pawn(screen, pawn_img, x, y):
    screen.blit(pawn_img, (x, y))

def drawn_pawns(screen, board, white_pawn_img, black_pawn_img, border, tile_size): 
    for i in range (Board.SIZE):
        for j in range(Board.SIZE):
            
            pawn = board.grid[i][j]

            y_offset = -tile_size // 15

            if pawn == 1:
                x = border + j * tile_size
                y = border + i * tile_size + y_offset
                draw_pawn(screen, white_pawn_img, x, y)

            elif pawn == -1:
                x = border + j * tile_size
                y = border + i * tile_size + y_offset
                draw_pawn(screen, black_pawn_img, x, y)

def get_pawn(sheet, x, y, tile_size):
    return sheet.subsurface((y * tile_size, x * tile_size, tile_size, tile_size))