import pygame
import time
import os
from game.board import Board
from game.game import Game
from game.rules import Rules
from ui.utils import draw_board, drawn_pawns, draw_highlight, draw_possible_moves, get_pawn
from AI.strategies import *

#reseta o log 
os.makedirs("logs", exist_ok=True)
open("logs/log.txt", "w").close()

# Inicialização
pygame.init()
screen_size = 800
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

# Cria o jogo
strategy_black = CombinedStrategy([
    (AdvanceStrategy(), 0.10),
    (MaterialStrategy(), 0.17),
    (SupportStructureStrategy(), 0.16),
    (FreePathStrategy(), 0.23),
    (ImmediateThreatsStrategy(), 0.09),
    (DefensiveStrategy(), 0.17),
    (AlternativeStrategy(), 0.09)
])  # Estratégia para o jogador preto

strategy_white = CombinedStrategy([
    (AdvanceStrategy(), 0.10),
    (MaterialStrategy(), 0.17),
    (SupportStructureStrategy(), 0.16),
    (FreePathStrategy(), 0.23),
    (ImmediateThreatsStrategy(), 0.09),
    (DefensiveStrategy(), 0.17),
    (AlternativeStrategy(), 0.09)
])


ai_players = [(-1, strategy_black), (1, strategy_white)]  # Ambos os jogadores são controlados pela IA
TIME_LIMIT = 1  # Tempo limite de 1 segundos para cada movimento da IA
game = Game(board, ai_players, TIME_LIMIT)

# Variável de estado
selected = None

# Loop principal
running = True
while running:
    #IA joga
    game.play_ai_turn()
    #time.sleep(0.1)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game.game_over:
            running = False
            

        if event.type == pygame.MOUSEBUTTONDOWN and not game.ai_turn(game.current_player):
            pos = event.pos

            x = (pos[1] - border) // pawn_size
            y = (pos[0] - border) // pawn_size

            if 0 <= x < Board.SIZE and 0 <= y < Board.SIZE:

                pawn = game.board.grid[x][y]

                # Seleciona peça
                if selected is None:

                    if pawn == game.current_player:
                        selected = (x, y)

                else:
                    
                    start = selected
                    end = (x, y)

                    game.move_pawn(start, end)

                    selected = None

    # Desenha o tabuleiro
    draw_board(screen, board_img)

    # Desenha os peões
    drawn_pawns(screen, board, white_pawn_img, black_pawn_img, border, pawn_size)

    # Desenha destaque para peão selecionado
    draw_highlight(screen, selected, border, pawn_size)

    # Desenha os movimentos possíveis
    draw_possible_moves(screen, board, selected, game.current_player, border, pawn_size)


    # Atualiza o frame
    pygame.display.flip()

print(f"Vencedor: {'Preto' if Rules.check_winner(game.board) == -1 else 'Branco'}")    

pygame.quit()