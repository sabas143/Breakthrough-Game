# 🧠 Breakthrough AI

Este projeto implementa uma Inteligência Artificial para jogar **Breakthrough**, utilizando algoritmos clássicos de busca como **Minimax** e **Minimax com poda Alpha-Beta**, combinados com heurísticas para avaliação de posições.

---

## 🎮 O que é Breakthrough?

Breakthrough é um jogo de tabuleiro para dois jogadores em um grid (geralmente 8x8), onde:

- Cada jogador controla peões
- Os peões se movem para frente e diagonal (e capturam na diagonal)
- O objetivo é:
  - chegar na última linha do adversário **ou**
  - eliminar todos os peões inimigos



---

## 🤖 O que é a IA neste projeto?

A IA funciona assim:

1. Gera todos os movimentos possíveis
2. Simula jogadas futuras (árvore de jogo)
3. Avalia posições usando heurísticas
4. Escolhe o melhor movimento usando:
   - **Minimax** (básico)
   - **Alpha-Beta pruning** (otimizado)

---

## ▶️ Como rodar o projeto

Para evitar problemas com imports de módulos, execute:

    python -m ui.main

Isso garante que o Python resolve corretamente os módulos do projeto.

---

## 🧠 Estrutura do Agente

A classe principal da IA é:

    class Agent

Ela contém:

- nome do agente
- jogador (1 ou -1)
- estratégia de avaliação
- contador de nós expandidos

---

## 🌳 Algoritmos de busca

### 🔹 Minimax

Explora a árvore de jogo assumindo:

- o jogador atual tenta **maximizar**
- o adversário tenta **minimizar**

---

### 🔹 Alpha-Beta Pruning

Versão otimizada do Minimax que:

- corta ramos desnecessários da árvore
- reduz drasticamente o número de nós explorados
- mantém o mesmo resultado final

---


## 🔢 Nós expandidos

A IA conta quantos nós foram explorados:

    self.expanded_nodes += 1

Isso mede:
- eficiência do algoritmo
- impacto da poda Alpha-Beta

---

## 📝 Sistema de logs

Cada jogada gera um log em:

    logs/log.txt

Exemplo:

    Agent1 escolheu o movimento: ((2,3),(3,3)) com 1543 nos expandidos.

O log registra:
- qual agente jogou
- qual movimento foi escolhido
- número de nós expandidos

---

## 🧩 Geração de movimentos

Função:

    possible_moves(board, player)

Ela:
- percorre todos os peões do jogador
- usa pawn_possible_moves
- retorna todos os movimentos válidos

Formato:

    ((x1, y1), (x2, y2), tipo)

---

## ⚖️ Avaliação de posições (Heurísticas)

A IA não entende o jogo diretamente — ela usa heurísticas para estimar o quão boa é uma posição.

Temos várias estratégias:

---

### 📊 1. Material

Conta peões:

    (# seus peões) - (# inimigos)

---

### 🚀 2. Avanço

Valoriza peões mais avançados no tabuleiro.

---

### 🛡️ 3. Estrutura de suporte

Valoriza peões protegidos por outros peões.

---

### 🛣️ 4. Caminhos livres

Conta peões com caminho livre até o final.

---

### ⚠️ 5. Ameaças imediatas

Conta peões que não podem mais ser capturados.

---

### 🛡️ 6. Estratégia Defensiva

Valoriza posições com menor ameaça inimiga próxima.

---

## 🔗 Combinação de heurísticas

As heurísticas são combinadas com:

    class CombinedStrategy

Ela faz uma **combinação linear ponderada**:

    score = w1*h1 + w2*h2 + ... + wn*hn

Onde:
- hi = valor de uma heurística
- wi = peso

Isso permite ajustar o comportamento da IA facilmente.

---

## 🧪 Avaliação experimental

O projeto permite comparar:

- Minimax vs Alpha-Beta
- diferentes heurísticas
- número de nós expandidos
- tempo por jogada
- taxa de vitória

---

## 💡 Observações importantes

- Alpha-Beta reduz nós, mas mantém a mesma decisão
- A qualidade da IA depende fortemente das heurísticas
- A profundidade define o “quanto à frente” a IA pensa

---

## 🚀 Possíveis melhorias

- Ordenação de movimentos (melhora muito Alpha-Beta)
- Iterative deepening
- Transposition tables
- Aprendizado automático de pesos

---

## 📌 Resumo

Esse projeto implementa uma IA clássica baseada em busca, mostrando:

- como algoritmos de decisão funcionam
- como heurísticas influenciam comportamento
- como otimizações impactam desempenho