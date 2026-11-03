import pygame

pygame.init()

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

def atualizar_tamanhos(w, h):
    global bg_copy, painel_copy, painel_altura_atual
    
    painel_altura_atual = int(h * 0.25)
    
    if painel_altura_atual < (h * 0.10):
        painel_altura_atual = int(h * 0.10)
    
    painel_copy = pygame.transform.scale(painel_image, (w, painel_altura_atual))
    
    altura_bg = h - painel_altura_atual
    bg_copy = pygame.transform.scale(bg_image, (w, altura_bg))

atualizar_tamanhos(screen_width, screen_height)

def draw_bg():
    screen.blit(bg_copy, (0, 0))

def draw_painel():
    screen.blit(painel_copy, (0, screen_height - painel_altura_atual))

run = True
tela_cheia = True

while run:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), resolucao)
            atualizar_tamanhos(screen_width, screen_height)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
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
    
    draw_bg()
    draw_painel()
    pygame.display.update()

pygame.quit()