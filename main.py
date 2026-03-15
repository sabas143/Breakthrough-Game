import pygame
from utils import draw_board, drawn_pieces, get_piece

# Inicialização
pygame.init()
screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Breakthrough")

# Carrega o tabuleiro
board_img = pygame.image.load("assets/board.png").convert_alpha()
board_img = pygame.transform.scale(board_img, (screen_size, screen_size))   

# Carrega os peões
pieces = pygame.image.load("assets/pieces.png").convert_alpha()
piece_tile = 16

white_pawn_img = get_piece(pieces, 0, 5, piece_tile)
black_pawn_img = get_piece(pieces, 1, 5, piece_tile)

# Ajuste de borda e tamanho dos peões
border = 60
board_area = screen_size - 2 * border
tile_size = board_area // 8

white_pawn_img = pygame.transform.scale(white_pawn_img, (tile_size, tile_size))
black_pawn_img = pygame.transform.scale(black_pawn_img, (tile_size, tile_size))

# Matriz do Tabuleiro (w = white & b = black)
board = [
    ["b","b","b","b","b","b","b","b"],
    ["b","b","b","b","b","b","b","b"],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    ["w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w"],
]

# Loop principal
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha o tabuleiro
    draw_board(screen, board_img)

    # Desenha os peões
    drawn_pieces(screen, board, white_pawn_img, black_pawn_img, border, tile_size)

    # Atualiza o frame
    pygame.display.flip()

pygame.quit()