import pygame
import sys
import random
from collections import deque

# Configurações iniciais do Pygame
pygame.init()
tam_peca = 100
cols, rows = 3, 3
largura, altura = tam_peca * cols, tam_peca * rows + 100
tamanho = largura, altura
preto = 0, 0, 0
fonte = pygame.font.Font(None, 36)

# Inicialização da janela do Pygame
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("8 Puzzle Solver")

# Variáveis globais para estatísticas do solver
puzzle_resolvido = False
num_jogadas = 0
estados_testados = 0
estados_testados_tempo = []
jogadas_tempo = []

# Função para embaralhar o tabuleiro inicial
def embaralhar_tabuleiro(tabuleiro):
    movimentos = [-1, 1, -3, 3]
    indice_branco = tabuleiro.index(0)
    
    for _ in range(1000):
        movimento = random.choice(movimentos)
        if 0 <= indice_branco + movimento < 9:
            tabuleiro[indice_branco], tabuleiro[indice_branco + movimento] = tabuleiro[indice_branco + movimento], tabuleiro[indice_branco]
            indice_branco += movimento
    return tabuleiro

# Função para desenhar o tabuleiro na tela do Pygame
def desenhar_tabuleiro(tabuleiro):
    tela.fill(preto)
    
    for i in range(rows):
        for j in range(cols):
            valor = tabuleiro[i * cols + j]
            if valor != 0:
                pygame.draw.rect(tela, (255, 255, 255), (j * tam_peca, i * tam_peca + 100, tam_peca, tam_peca))
                texto = fonte.render(str(valor), True, preto)
                rect_texto = texto.get_rect(center=(j * tam_peca + tam_peca / 2, i * tam_peca + tam_peca / 2 + 100))
                tela.blit(texto, rect_texto)
    
    texto_jogadas = fonte.render(f"Jogadas: {num_jogadas}", True, (255, 255, 255))
    texto_estados = fonte.render(f"Estados: {estados_testados}", True, (255, 255, 255))
    tela.blit(texto_jogadas, (10, 10))
    tela.blit(texto_estados, (10, 50))
    
    pygame.display.flip()

# Função para verificar se o estado atual é o estado objetivo
def objetivo_alcancado(tabuleiro):
    return tabuleiro == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para obter os vizinhos possíveis de um estado do tabuleiro
def obter_vizinhos(tabuleiro):
    vizinhos = []  # Lista para armazenar os vizinhos encontrados
    indice = tabuleiro.index(0)  # Encontra o índice da peça vazia (0)
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Define os movimentos possíveis: cima, baixo, esquerda, direita
    i, j = divmod(indice, 3)  # Converte o índice para coordenadas (linha, coluna)

    # Itera sobre os movimentos possíveis
    for di, dj in movimentos:
        ni, nj = i + di, j + dj  # Calcula as novas coordenadas do vizinho
        if 0 <= ni < 3 and 0 <= nj < 3:  # Verifica se as novas coordenadas estão dentro dos limites do tabuleiro
            novo_tabuleiro = tabuleiro[:]  # Copia o tabuleiro atual para modificar uma cópia
            novo_indice = ni * 3 + nj  # Calcula o índice do vizinho no tabuleiro
            novo_tabuleiro[indice], novo_tabuleiro[novo_indice] = novo_tabuleiro[novo_indice], novo_tabuleiro[indice]  # Troca a peça vazia pelo vizinho
            vizinhos.append(novo_tabuleiro)  # Adiciona o novo tabuleiro à lista de vizinhos
    
    return vizinhos  # Retorna a lista de vizinhos encontrados

def resolver_bfs(inicial):
    fila = deque([(inicial, [])])  # Inicializa a fila com o estado inicial e um caminho vazio
    visitados = set()  # Conjunto para armazenar estados visitados
    visitados.add(tuple(inicial))  # Adiciona o estado inicial ao conjunto de visitados (usando tupla para torná-lo imutável)
    global estados_testados, num_jogadas  # Declara variáveis globais para contar estados testados e número de jogadas
    estados_testados += 1  # Incrementa o contador de estados testados

    while fila:  # Loop enquanto houver estados na fila
        tabuleiro_atual, caminho = fila.popleft()  # Remove o estado mais antigo da fila
        if objetivo_alcancado(tabuleiro_atual):  # Verifica se o estado atual é o estado objetivo
            global puzzle_resolvido  # Declara a variável global que indica se o puzzle foi resolvido
            puzzle_resolvido = True  # Define como verdadeiro, indicando que o puzzle foi resolvido
            num_jogadas = len(caminho)  # Define o número de jogadas como o tamanho do caminho até o estado objetivo
            return caminho + [tabuleiro_atual]  # Retorna o caminho até o estado objetivo, incluindo o próprio estado
        
        for vizinho in obter_vizinhos(tabuleiro_atual):  # Para cada vizinho do estado atual
            if tuple(vizinho) not in visitados:  # Verifica se o vizinho ainda não foi visitado
                visitados.add(tuple(vizinho))  # Adiciona o vizinho ao conjunto de visitados
                fila.append((vizinho, caminho + [tabuleiro_atual]))  # Adiciona o vizinho à fila com o caminho até ele
                estados_testados += 1  # Incrementa o contador de estados testados
                estados_testados_tempo.append(estados_testados)  # Armazena o número de estados testados ao longo do tempo
                jogadas_tempo.append(len(caminho) + 1)  # Armazena o número de jogadas até o vizinho
    
    return None  # Retorna None se não encontrar solução

# Função principal para inicializar, resolver e mostrar o resultado do puzzle
def principal():
    tabuleiro_inicial = list(range(1, 9)) + [0]
    tabuleiro_inicial = embaralhar_tabuleiro(tabuleiro_inicial)

    caminho_solucao = resolver_bfs(tabuleiro_inicial)

    if caminho_solucao:
        print("Caminho da Solução:")
        for passo in caminho_solucao:
            print(passo)
        print(f"Número de Jogadas: {num_jogadas}")
        print(f"Estados: {estados_testados}")

        for passo in caminho_solucao:
            desenhar_tabuleiro(passo)
            pygame.time.delay(500)
    else:
        print("Nenhuma solução encontrada.")

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

    pygame.quit()

if __name__ == "__main__":
    principal()
