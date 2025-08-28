import pygame
import time
import random

# Inicializa o pygame
pygame.init()

# Cores neon estilo arcade
preto = (0, 0, 0)
verde_neon = (0, 255, 0)
roxo_neon = (255, 0, 255)
ciano = (0, 255, 255)
amarelo = (255, 255, 0)
vermelho = (255, 80, 80)

# Configurações da tela
largura = 600
altura = 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Arcade 🐍✨")

# FPS
clock = pygame.time.Clock()
velocidade = 15
tamanho_cobra = 10

# Fonte retrô arcade
try:
    fonte = pygame.font.Font("retro.ttf", 15)
except:
    fonte = pygame.font.SysFont("Courier New", 20, bold=True)


def mostrar_pontos(pontos):
    valor = fonte.render(f"SCORE: {pontos}", True, verde_neon)
    tela.blit(valor, [10, 10])


def desenhar_cobra(tamanho, lista_cobra):
    for x in lista_cobra:
        pygame.draw.rect(tela, ciano, [x[0], x[1], tamanho, tamanho])
        pygame.draw.rect(tela, roxo_neon, [x[0], x[1], tamanho, tamanho], 2)


def mensagem_central(texto, cor, deslocamento_y=0):
    texto_render = fonte.render(texto, True, cor)
    rect = texto_render.get_rect(center=(largura/2, altura/2 + deslocamento_y))
    tela.blit(texto_render, rect)


def jogo():
    game_over = False
    game_close = False

    x = largura / 2
    y = altura / 2
    dx = 0
    dy = 0

    lista_cobra = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, largura - tamanho_cobra) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanho_cobra) / 10.0) * 10.0

    while not game_over:

        while game_close:
            tela.fill(preto)
            mensagem_central("GAME OVER", vermelho, deslocamento_y=-50)  # sobe um pouco
            mensagem_central("Pressione C para continuar ou Q para sair", amarelo, deslocamento_y=20)
            mostrar_pontos(comprimento_cobra - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        jogo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -tamanho_cobra
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = tamanho_cobra
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -tamanho_cobra
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = tamanho_cobra
                    dx = 0

        x += dx
        y += dy

        if x >= largura or x < 0 or y >= altura or y < 0:
            game_close = True

        tela.fill(preto)
        pygame.draw.rect(tela, amarelo, [comida_x, comida_y, tamanho_cobra, tamanho_cobra])
        lista_cobra.append([x, y])

        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        for parte in lista_cobra[:-1]:
            if parte == [x, y]:
                game_close = True

        desenhar_cobra(tamanho_cobra, lista_cobra)
        mostrar_pontos(comprimento_cobra - 1)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_cobra) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - tamanho_cobra) / 10.0) * 10.0
            comprimento_cobra += 1

        clock.tick(velocidade)

    pygame.quit()
    quit()

# Inicia o jogo
jogo()
