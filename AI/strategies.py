from game.rules import Rules
from collections import deque

class Strategy:
    def evaluate(self, board):
        raise NotImplementedError("Subclasses must implement this method")
    
""" Estratégia de material: Avalia a posição com base na contagem de peões, dando um valor positivo para o jogador e negativo para o oponente."""
class MaterialStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        white_count = sum(1 for row in board.grid for p in row if p == 1)
        black_count = sum(1 for row in board.grid for p in row if p == -1)

        if player == 1:
            return white_count - black_count
        else:
            return black_count - white_count


"""Estratégia de avanço: Avalia a posição dos peões, dando mais valor para peões que estão mais avançados no tabuleiro."""     
class AdvanceStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        white_score = 0
        black_score = 0

        for pawn in board.black_pawns:
            x = pawn // 8
            black_score += x / 7  # Peões mais avançados têm um valor maior

        for pawn in board.white_pawns:
            x = pawn // 8
            white_score += (7 - x) / 7  # Peões mais avançados têm um valor maior

        white_score = white_score / len(board.white_pawns) if board.white_pawns else 0
        black_score = black_score / len(board.black_pawns) if board.black_pawns else 0

        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score



"""Estratégia de estruturas de apoio: Avalia a posição com base na formação dos peões, dando mais valor para peões que estão protegidos por outros peões."""
class SupportStructureStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            back_diagonals = [pawn + 7, pawn + 9]  # Diagonais de apoio para peões brancos
            for diag in back_diagonals:
                if diag in board.white_pawns:
                    white_score += 1  # Peão protegido por outro peão branco
        
        for pawn in board.black_pawns:
            back_diagonals = [pawn - 7, pawn - 9]  # Diagonais de apoio para peões pretos
            for diag in back_diagonals:
                if diag in board.black_pawns:
                    black_score += 1  # Peão protegido por outro peão preto

        white_score = white_score / len(board.white_pawns) if board.white_pawns else 0
        black_score = black_score / len(board.black_pawns) if board.black_pawns else 0

        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score      


"""Estratégia de caminhos livres: Avalia a posição com base na quantidade de caminhos livres até a linha de chegada, dando mais valor para peões que têm um caminho mais claro para avançar."""
class FreePathStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            x = pawn // 8
            y = pawn % 8
            free_path = True

            for i in range(x - 1, -1, -1):
                if board.grid[i][y] != 0:
                    free_path = False
                    break
            
            if free_path:
                white_score += 1

        for pawn in board.black_pawns:
            x = pawn // 8
            y = pawn % 8
            free_path = True

            for i in range(x + 1, 8):
                if board.grid[i][y] != 0:
                    free_path = False
                    break
            
            if free_path:
                black_score += 1


        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score
        

""""Estratégia de ameaças imediatas: com base na quantidade de peões que irão ganhar inevitavelmente ( não podem mais ser capturados)"""
class ImmediateThreatsStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            x = pawn // 8
            y = pawn % 8

            if x == 0:  # Peão branco na linha de chegada
                white_score += 1
            else:
                # Verifica se o peão pode ser capturado
                if (y > 0 and board.grid[x - 1][y - 1] == -1) or (y < 7 and board.grid[x - 1][y + 1] == -1):
                    continue  
                else:
                    white_score += 1  
        
        for pawn in board.black_pawns:
            x = pawn // 8
            y = pawn % 8

            if x == 7:  # Peão preto na linha de chegada
                black_score += 1
            else:
                # Verifica se o peão pode ser capturado
                if (y > 0 and board.grid[x + 1][y - 1] == 1) or (y < 7 and board.grid[x + 1][y + 1] == 1):
                    continue  
                else:
                    black_score += 1  


        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score

"""Estratégia defensiva: peões que estão bloqueando o avanço do oponente recebem pontuação maior"""
class DefensiveStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        white_score = 0
        black_score = 0

        for pawn in board.white_pawns:
            x = pawn // 8
            y = pawn % 8

            blocked_pawns = [(x, y-2), (x+1, y-2), (x-1, y-2)]

            for bx, by in blocked_pawns:
                if not (0 <= bx < 8 and 0 <= by < 8):
                    continue
                if board.grid[bx][by] == -1:
                    white_score += 1

        for pawn in board.black_pawns:
            x = pawn // 8
            y = pawn % 8

            blocked_pawns = [(x, y+2), (x+1, y+2), (x-1, y+2)]

            for bx, by in blocked_pawns:
                if not (0 <= bx < 8 and 0 <= by < 8):
                    continue
                if board.grid[bx][by] == 1:
                    black_score += 1

        if player == 1:
            return white_score - black_score
        else:
            return black_score - white_score


class CombinedStrategy(Strategy):
    def __init__(self, strategies_with_weights):
        self.strategies = [s for s, w in strategies_with_weights]
        self.weights = [w for s, w in strategies_with_weights]

    def evaluate(self, board, player, depth=0):
        total_score = 0
        for strategy, weight in zip(self.strategies, self.weights):
            total_score += weight * strategy.evaluate(board, player, depth)
        
        if Rules.check_winner(board) == player:
            total_score += 1000000  + (depth * 1000)  
        elif Rules.check_winner(board) == -player:
            total_score -= 1000000 - (depth * 1000)  
        
        return total_score
    
    def __str__(self):
        return "[" + ", ".join(f"{type(s).__name__}: {w:.2f}" for s, w in zip(self.strategies, self.weights)) + "]"

"""
DominationStrategy avalia um tabuleiro com base
no número de casas que são alcançadas primeiro por
cada jogador.
"""    
INF = 10**9

class DominationStrategy(Strategy):
    def inside(self, n, x, y):
        return 0 <= x < n and 0 <= y < n

    def bfs(self, board, sources, directions):
        n = board.SIZE
        dist = [[INF] * n for _ in range(n)]
        q = deque()

        for x, y in sources:
            dist[x][y] = 0
            q.append((x, y))

        while q:
            x, y = q.popleft()

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if not self.inside(n, nx, ny):
                    continue

                if dy == 0 and board.grid[nx][ny] != board.EMPTY:
                    continue

                if dist[nx][ny] > dist[x][y] + 1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

        return dist

    def reachable_count(self, board, player):
        n = board.SIZE

        white = [(p // n, p % n) for p in board.white_pawns]
        black = [(p // n, p % n) for p in board.black_pawns]

        WHITE_DIRS = [(-1, 0), (-1, -1), (-1, 1)]
        BLACK_DIRS = [(1, 0), (1, -1), (1, 1)]

        dist_white = self.bfs(board, white, WHITE_DIRS)
        dist_black = self.bfs(board, black, BLACK_DIRS)

        if player == board.WHITE:
            dist_me, dist_enemy = dist_white, dist_black
            start_pawns = white
            dirs = WHITE_DIRS
        else:
            dist_me, dist_enemy = dist_black, dist_white
            start_pawns = black
            dirs = BLACK_DIRS

        count = [[0] * n for _ in range(n)]
        q = deque()

        for x, y in start_pawns:
            if dist_me[x][y] < dist_enemy[x][y]:
                count[x][y] = 1
                q.append((x, y))

        while q:
            x, y = q.popleft()

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy

                if not self.inside(n, nx, ny):
                    continue

                if dy == 0 and board.grid[nx][ny] != board.EMPTY:
                    continue

                if dist_me[nx][ny] < dist_enemy[nx][ny]:
                    if count[nx][ny] < 10:  # limite pq vai ter mto overcounting sem isso
                        count[nx][ny] += count[x][y]
                        q.append((nx, ny))

        return count

    def evaluate(self, board, player, depth):
        white_reachable = self.reachable_count(board, board.WHITE)
        black_reachable = self.reachable_count(board, board.BLACK)
        
        lineWeights = [1, 1, 2, 3, 5, 9, 15, 5000] # pesos para cada distância alcançável
        score = 0
        
        for i in range(0, board.SIZE):
            for j in range(0, board.SIZE):
                score += lineWeights[board.SIZE - i - 1] * white_reachable[i][j]
                score -= lineWeights[i] * black_reachable[i][j]

        return score
    
class AlternativeStrategy(Strategy):
    def evaluate(self, board, player, depth=0):
        val = Rules.check_winner(board)

        if val is not None:
            return (val * 1000000) + (val * depth * 1000)
        
        return DominationStrategy().evaluate(board, player, depth)
        