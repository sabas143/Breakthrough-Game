from AI.strategies import *
import numpy as np
from game import game
from game.board import Board
from game.game import Game

class Tournament:
    def __init__(self):
        pass 


    def select_parent(self, ranked_population):
        tournament_size = 5
        indices = np.random.choice(len(ranked_population), tournament_size, replace=False)
        indices.sort()
        return ranked_population[indices[0]]  
    
    def crossover(self, parent1, parent2):
        child_weights = []
        for w1, w2 in zip(parent1.weights, parent2.weights):
            child_weights.append((w1 + w2) / 2)  # Média dos pesos dos pais
        return child_weights
    
    def mutate(self, weights, mutation_rate):
        for i in range(len(weights)):
            if np.random.rand() < mutation_rate:
                weights[i] += np.random.normal(0, 0.1)  # Pequena mutação gaussiana
        weights = np.clip(weights, 0, 1)  # Garante que os pesos permaneçam entre 0 e 1
        weights /= np.sum(weights)  # Normaliza os pesos para somarem 1
        return weights

    def genetic_selection(self, population_size=20, generations=10, mutation_rate=0.1):
        # Inicializa a população com estratégias aleatórias
        population = []
        for _ in range(population_size):
            weights = np.random.rand(7)  
            weights /= np.sum(weights)  # Normaliza os pesos para somarem 1
            strategy = CombinedStrategy([
                (AdvanceStrategy(), weights[0]),
                (MaterialStrategy(), weights[1]),
                (SupportStructureStrategy(), weights[2]),
                (FreePathStrategy(), weights[3]),
                (ImmediateThreatsStrategy(), weights[4]),
                (DefensiveStrategy(), weights[5]),
                (AlternativeStrategy(), weights[6])
            ])
            population.append(strategy)

        elite_size = population_size // 5  # Mantém os 20% melhores

        for generation in range(generations):
            # Avalia a população
            ranked_population = self.tournament(population)

            # Seleciona os melhores para reprodução
            new_population = ranked_population[:elite_size]

            # Reproduz os melhores para criar a nova população
            while len(new_population) < population_size:
                parent1 = self.select_parent(ranked_population)
                parent2 = self.select_parent(ranked_population)
                child_weights = self.crossover(parent1, parent2)
                child_weights = self.mutate(child_weights, mutation_rate)
                child_strategy = CombinedStrategy([
                    (AdvanceStrategy(), child_weights[0]),
                    (MaterialStrategy(), child_weights[1]),
                    (SupportStructureStrategy(), child_weights[2]),
                    (FreePathStrategy(), child_weights[3]),
                    (ImmediateThreatsStrategy(), child_weights[4]),
                    (DefensiveStrategy(), child_weights[5]),
                    (AlternativeStrategy(), child_weights[6])
                ])
                new_population.append(child_strategy)

            population = new_population

        return population[0]  # Retorna a melhor estratégia após as gerações


    def tournament(self, competitors):
        scores = {competitor: 0 for competitor in competitors}

        total_games =  len(competitors) * len(competitors) // 5  # Cada competidor joga contra 20% dos outros competidores

        for i in range(total_games):   
            c1,c2 = np.random.choice(competitors, 2, replace=False)

            ai_players = [(-1, c1), (1, c2)]  # Ambos os jogadores são controlados pela IA
            game = Game(Board(), ai_players, 0.1)

            winner = game.play()

            if winner == -1:
                scores[c1] += 1
            elif winner == 1:
                scores[c2] += 1

        ranked_competitors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ranked_competitors = [score[0] for score in ranked_competitors]
        return ranked_competitors
    


if __name__ == "__main__":
    tournament = Tournament()
    best = tournament.genetic_selection(20, 10, 0.1)
    print("Best strategy:", best)