# Automata Maze Challenge

![preview](./_.github/preview.png)

> Stone Automata Maze Challenge (Português)

Esse desafio foi criado pela Stone e publicado em: https://sigmageek.com/solution/stone-automata-maze-challenge

## Sobre o labirinto:
O labirinto muda conforme o movimento do jogador, porém possui uma particularidade, no momento que o jogador se move, o labirinto muda antes do jogador chegar na nova posição. Logo, o jogador precisa "prever" que aquela posição será válida (espaço em branco), senão, caso caia em um espaço proibido (espaço verde), ele perde o jogo.

## Objetivo:
Enviar todas as coordenadas necessárias para chegar no final do labirinto.

![preview](./_.github/preview.gif)

## Métodos e tentativas:
Inicialmente criei o jogo via terminal e tentei alguns caminhos.

Sem sucesso, usei o módulo pygame para poder jogar usando redes neurais NEAT, mas não concluí. Optei por mudar para o PyTorch, me baseando num modelo usado para o jogo 'snake'.

Coloquei mais de um jogador para a IA jogar, mas pesava demais no pc e ainda assim não encontrou o caminho.

Por fim, criei um modelo "celular" onde começa um jogador e esse jogador se multiplica em todas
as opções possíveis de movimento. Depois, cada jogador faz o mesmo, até que algum chegue no fim do labirinto, finalizando o jogo e retornando a resposta com os comandos realizados.

### Modelo via terminal, com 0's e 1's (stone_pelo_terminal/stone.py)
- O modelo mais simples e eu criei também algumas formas de jogar:
-- comandos individuais
-- comandos automáticos aleatórios
-- uma sequência inicial predefinida e depois seguido por comando aleatório ou comandos individuais

Essas formas precisam ser alteradas no arquivo .py do jogo.
Também coloquei pra que ele atualize um CSV para salvar comandos anteriores e durante as tentativas automáticas não repetir a mesma jogada.

### Modelo via Pygame:
- Individual (stone_pygame/stone_pygame.py)
- Jogo por IA (stone_pygame_ia/)
-- versão com NEAT não finalizada (NEAT/stone_pygame_ia.py)
-- Versão PyTorch, 1 jogador (game_single.py)
-- Versão PyTorch, 50 jogadores (game.py)
- Celular (stone_pygame_all/game_all.py)

[Clique aqui para ver o vídeo 'celular'](https://www.youtube.com/watch?v=gXJsaNt7J_A)

## Tecnologias

- Python
- Pygame
- Pytorch

## Contato

Linkedin: https://www.linkedin.com/in/bruno-della-volpe-alves/