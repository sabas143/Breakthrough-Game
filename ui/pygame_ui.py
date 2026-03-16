import pygame
from game.board import Board
from game.rules import Rules
from ui.utils import draw_board, drawn_pawns, draw_highlight, draw_possible_moves, get_pawn

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
tile_size = 16

white_pawn_img = get_pawn(pieces, 0, 5, tile_size)
black_pawn_img = get_pawn(pieces, 1, 5, tile_size)

# Ajuste de borda e tamanho dos peões
border = screen_size // 10
board_area = screen_size - 2 * border
pawn_size = board_area // 8

white_pawn_img = pygame.transform.scale(white_pawn_img, (pawn_size, pawn_size))
black_pawn_img = pygame.transform.scale(black_pawn_img, (pawn_size, pawn_size))

# Cria o tabuleiro
board = Board()

# Variáveis de estado
current_player = 1
selected = None

# Loop principal
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            x = (pos[1] - border) // pawn_size
            y = (pos[0] - border) // pawn_size

            if 0 <= x < Board.SIZE and 0 <= y < Board.SIZE:

                pawn = board.grid[x][y]

                # Seleciona peça
                if selected is None:

                    if pawn == current_player:
                        selected = (x, y)

                else:
                    
                    start = selected
                    end = (x, y)

                    if Rules.valid_move(board, start, end, current_player):

                        board.move_pawn(start, end)

                        # Troca jogador
                        current_player = -current_player

                    selected = None

    # Desenha o tabuleiro
    draw_board(screen, board_img)

    # Desenha os peões
    drawn_pawns(screen, board, white_pawn_img, black_pawn_img, border, pawn_size)

    # Desenha destaque para peão selecionado
    draw_highlight(screen, selected, border, pawn_size)

    # Desenha os movimentos possíveis
    draw_possible_moves(screen, board, selected, current_player, border, pawn_size)

    if (Rules.check_winner(board) is not None):
        running = False

    # Atualiza o frame
    pygame.display.flip()

pygame.quit()