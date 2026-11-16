import pygame
import ui
from combate import Combate
from criacao import criar_jogador, criar_inimigo

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = 30

info_objeto = pygame.display.Info()
screen_width = info_objeto.current_w
screen_height = info_objeto.current_h

resolucao = pygame.FULLSCREEN | pygame.RESIZABLE
screen = pygame.display.set_mode((screen_width, screen_height), resolucao)
pygame.display.set_caption("Coliseu")

bg_image = pygame.image.load("imagens/bg1.png").convert_alpha()
painel_image = pygame.image.load("imagens/painel.png").convert_alpha()

AREA_INFO = (0.025, 0.10, 0.45, 0.80)
AREA_MENU = (0.525, 0.10, 0.45, 0.80)

bg_copy = painel_copy = None
painel_altura_atual = 0

def atualizar_tamanhos(w, h):
    global bg_copy, painel_copy, painel_altura_atual

    painel_altura_atual = max(int(h * 0.25), int(h * 0.10))
    painel_copy = pygame.transform.scale(painel_image, (w, painel_altura_atual))
    bg_copy = pygame.transform.scale(bg_image, (w, h - painel_altura_atual))
    ui.atualizar_fontes(painel_altura_atual)

def area_do_painel(fracao):
    fx, fy, fw, fh = fracao
    topo = screen_height - painel_altura_atual
    return pygame.Rect(int(screen_width * fx),
                       topo + int(painel_altura_atual * fy),
                       int(screen_width * fw),
                       int(painel_altura_atual * fh))

atualizar_tamanhos(screen_width, screen_height)

combate = None
menu = None
inimigos_derrotados = 0
vitoria_registrada = False

def novo_combate():
    global combate, menu, vitoria_registrada, turno
    vitoria_registrada = False
    combate = Combate(criar_jogador(), criar_inimigo())
    menu = ui.MenuCombate(combate.jogador)

novo_combate()

def draw_bg():
    screen.blit(bg_copy, (0, 0))

def draw_painel():
    screen.blit(painel_copy, (0, screen_height - painel_altura_atual))

def draw_interface():
    ui.desenhar_info(screen, area_do_painel(AREA_INFO), combate.jogador)
    menu.desenhar(screen, area_do_painel(AREA_MENU),
                  ativo=(combate.estado == Combate.TURNO_JOGADOR))

    ui.desenhar_log(screen, combate.mensagens)
    ui.desenhar_inimigo(screen, combate.inimigo)
    if combate.terminou:
        ui.desenhar_fim(screen, combate.estado == Combate.VITORIA,
                        screen_height - painel_altura_atual, inimigos_derrotados)

run = True
tela_cheia = True

while run:
    clock.tick(fps)
    agora = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), resolucao)
            atualizar_tamanhos(screen_width, screen_height)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            tela_cheia = not tela_cheia
            if tela_cheia:
                screen_width = info_objeto.current_w
                screen_height = info_objeto.current_h
                resolucao = pygame.FULLSCREEN | pygame.RESIZABLE
            else:
                screen_width, screen_height = 1280, 720
                resolucao = pygame.RESIZABLE
            screen = pygame.display.set_mode((screen_width, screen_height), resolucao)
            atualizar_tamanhos(screen_width, screen_height)

        elif combate.estado == Combate.TURNO_JOGADOR:
            acao = menu.tratar_evento(event)
            if acao:
                combate.executar_acao_jogador(acao, agora)

        elif combate.terminou:
            if combate.estado == Combate.VITORIA and not vitoria_registrada:
                inimigos_derrotados += 1
                vitoria_registrada = True
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if combate.estado == Combate.DERROTA:
                    inimigos_derrotados = 0
                novo_combate()        

    combate.atualizar(agora)

    draw_bg()
    draw_painel()
    draw_interface()
    pygame.display.update()

pygame.quit()