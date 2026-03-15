def draw_board(screen, board_img):
    screen.blit(board_img, (0, 0))

def draw_pawn(screen, pawn_img, x, y):
    screen.blit(pawn_img, (x, y))

def drawn_pieces(screen, board, white_pawn_img, black_pawn_img, border, tile_size): 
    for linha in range(len(board)):
        for coluna in range(len(board[0])):
            piece = board[linha][coluna]

            y_offset = -tile_size // 15

            if piece == "w":
                x = border + coluna * tile_size
                y = border + linha * tile_size + y_offset
                draw_pawn(screen, white_pawn_img, x, y)

            elif piece == "b":
                x = border + coluna * tile_size
                y = border + linha * tile_size + y_offset
                draw_pawn(screen, black_pawn_img, x, y)

def get_piece(sheet, linha, coluna, tile_size):
    return sheet.subsurface((coluna * tile_size, linha * tile_size, tile_size, tile_size))