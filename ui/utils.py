from game.board import Board
from game.rules import Rules
import pygame

def draw_board(screen, board_img):
    screen.blit(board_img, (0, 0))

def draw_pawn(screen, pawn_img, x, y):
    screen.blit(pawn_img, (x, y))

def drawn_pawns(screen, board, white_pawn_img, black_pawn_img, border, pawn_size): 
    for i in range (Board.SIZE):
        for j in range(Board.SIZE):
            
            pawn = board.grid[i][j]

            y_offset = -pawn_size // 15

            x = border + j * pawn_size
            y = border + i * pawn_size + y_offset

            if pawn == 1:
                draw_pawn(screen, white_pawn_img, x, y)

            elif pawn == -1:
                draw_pawn(screen, black_pawn_img, x, y)

def draw_highlight(screen, selected, border, pawn_size):
    if selected is None:
        return

    x = border + selected[1] * pawn_size
    y = border + selected[0] * pawn_size
    highlight_color = (255, 255, 0)  # Amarelo
    pygame.draw.rect(screen, highlight_color, (x - 5, y - 5, pawn_size + 10, pawn_size + 10), 3)

def draw_possible_moves(screen, board, selected, current_player, border, pawn_size):
    if selected is None:
        return
    
    x, y = selected
    direction = -1 if current_player == 1 else 1

    for j in range(y - 1, y + 2):
        if Rules.valid_move(board, (x, y), (x + direction, j), current_player):
            cx = border + j * pawn_size + pawn_size // 2
            cy = border + (x + direction) * pawn_size + pawn_size // 2
            pygame.draw.circle(screen, (0, 255, 0), (cx, cy), pawn_size // 6)

def get_pawn(sheet, x, y, tile_size):
    return sheet.subsurface((y * tile_size, x * tile_size, tile_size, tile_size))