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


"""
Função para obter os movimentos possíveis de um peão específico
Parametros:
- board: O tabuleiro atual do jogo
- pawn: A posição do peão (x, y)
- current_player: O jogador atual (1 para branco, -1 para preto)
Retorna:
- Uma lista de movimentos possíveis, onde cada movimento é representado como uma tupla (x, y, move_type)
  - x: A coordenada x do movimento
  - y: A coordenada y do movimento
  - move_type: O tipo de movimento (1 para movimento normal, 2 para captura)
"""
def pawn_possible_moves(board, pawn, current_player):

    x, y = pawn
    direction = -1 if current_player == 1 else 1

    moves = []

    for j in range(y - 1, y + 2):
        if Rules.valid_move(board, (x, y), (x + direction, j), current_player) > 0:
            moves.append((x + direction, j, Rules.valid_move(board, (x, y), (x + direction, j), current_player)))
    
    return moves


def draw_possible_moves(screen, board, selected, current_player, border, pawn_size):
    if selected is None:
        return
    
    moves = pawn_possible_moves(board, selected, current_player)

    for move in moves:
        x, y, move_type = move

        
        x_pos = border + y * pawn_size
        y_pos = border + x * pawn_size
        
        
        if move_type == 1:
            pygame.draw.circle(screen, (0, 255, 0), (x_pos + pawn_size // 2, y_pos + pawn_size // 2), pawn_size // 6)

        if move_type == 2:
            pygame.draw.circle(screen, (0, 255, 0), (x_pos + pawn_size // 2, y_pos + pawn_size // 2), pawn_size // 2.2, 6)
        
        
        

def get_pawn(sheet, x, y, tile_size):
    return sheet.subsurface((y * tile_size, x * tile_size, tile_size, tile_size))