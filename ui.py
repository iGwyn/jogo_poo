import pygame
from math import ceil
from itens import Arma, Armadura, Consumivel

BRANCO = (245, 238, 225)
CREME = (222, 205, 170)
CINZA = (150, 140, 130)
CINZA_ESCURO = (115, 106, 98)
PRETO = (15, 12, 10)
DOURADO = (240, 200, 90)
BRONZE = (160, 112, 52)
VERMELHO = (200, 50, 45)
LARANJA = (225, 125, 35)
AZUL = (60, 115, 220)

ESTILOS = {
    "normal": ((98, 68, 38, 225), (52, 34, 20, 225), BRONZE),
    "selecionado": ((135, 96, 50, 240), (84, 56, 28, 240), DOURADO),
    "desabilitado": ((62, 52, 46, 225), (38, 32, 28, 225), (92, 84, 78)),
}

fonte_mini = None
fonte_pequena = None
fonte = None
fonte_grande = None


def atualizar_fontes(altura_painel):
    global fonte_mini, fonte_pequena, fonte, fonte_grande
    base = max(14, int(altura_painel * 0.10))
    fonte_mini = pygame.font.SysFont("Arial", max(10, int(base * 0.62)), bold = True)
    fonte_pequena = pygame.font.SysFont("Arial", max(11, int(base * 0.82)))
    fonte = pygame.font.SysFont("Arial", base, bold = True)
    fonte_grande = pygame.font.SysFont("Arial", int(base * 1.3), bold = True)

def vida_maxima(p):
    v = getattr(p, "vida_maxima")
    return v

def recurso_de(p):
    if hasattr(p, "furia"):
        return ("Fúria", p.furia, p.furia_maxima, LARANJA)
    if hasattr(p, "mana"):
        return ("Mana", p.mana, p.mana_maxima, AZUL)
    return None

def defesa_de(p):
    try:
        return p.defesa_atual()
    except Exception:
        return "?"

def detalhe_item(item):
    if isinstance(item, Arma):
        return f"Dano {item.dano}"
    if isinstance(item, Armadura):
        return f"Defesa {item.defesa}"
    if isinstance(item, Consumivel):
        return f"Efeito +{item.valor}"
    return ""

def cortar_texto(txt, fnt, largura):
    if fnt.size(txt)[0] <= largura:
        return txt
    while txt and fnt.size(txt + "...")[0] > largura:
        txt = txt[:-1]
    return txt + "..."

def texto(surf, fnt, txt, cor, pos):
    surf.blit(fnt.render(txt, True, PRETO), (pos[0] + 1, pos[1] + 1))
    surf.blit(fnt.render(txt, True, cor), pos)

def texto_centro(surf, fnt, txt, cor, centro_x, y):
    texto(surf, fnt, txt, cor, (centro_x - fnt.size(txt)[0] // 2, y))

def gradiente_arredondado(w, h, cima, baixo, raio):
    w, h = max(1, w), max(1, h)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for y in range(h):
        t = y / max(1, h - 1)
        cor = tuple(int(cima[k] + (baixo[k] - cima[k]) * t) for k in range(4))
        pygame.draw.line(surf, cor, (0, y), (w, y))
    mascara = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius = raio)
    surf.blit(mascara, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)
    return surf

def losango(surf, centro, tam, cor):
    x, y = centro
    pygame.draw.polygon(surf, cor, [(x, y - tam), (x + tam, y), (x, y + tam), (x - tam, y)])

def placa(surf, rect, estado = "normal"):
    cima, baixo, borda = ESTILOS[estado]
    raio = max(6, rect.h // 8)
    surf.blit(gradiente_arredondado(rect.w, rect.h, cima, baixo, raio), rect.topleft)

    if estado == "selecionado":
        brilho = pygame.Surface((rect.w + 16, rect.h + 16), pygame.SRCALPHA)
        for e, a in ((7, 30), (5, 55), (3, 90)):
            r = pygame.Rect(8 - e, 8 - e, rect.w + 2 * e, rect.h + 2 * e)
            pygame.draw.rect(brilho, (*DOURADO, a), r, 2, border_radius = raio + e)
        surf.blit(brilho, (rect.x - 8, rect.y - 8))

def ornamento(surf, x1, x2, y):
    meio = (x1 + x2) // 2
    pygame.draw.line(surf, BRONZE, (x1, y), (meio - 12, y), 2)
    pygame.draw.line(surf, BRONZE, (meio + 12, y), (x2, y), 2)
    losango(surf, (meio, y), 6, DOURADO)

def cabecalho(surf, x1, x2, y, titulo, cor, dica=""):
    h = fonte_pequena.get_height()
    w = fonte_pequena.size(titulo)[0]
    tx = (x1 + x2) // 2 - w // 2
    cy = y + h // 2
    texto(surf, fonte_pequena, titulo, cor, (tx, y))

    x_fim = x2
    if dica:
        wd = fonte_mini.size(dica)[0]
        texto(surf, fonte_mini, dica, CREME, (x2 - wd, cy - fonte_mini.get_height() // 2))
        x_fim = x2 - wd - 12

    pygame.draw.line(surf, BRONZE, (x1, cy), (tx - 20, cy), 2)
    pygame.draw.line(surf, BRONZE, (tx + w + 20, cy), (max(tx + w + 20, x_fim), cy), 2)
    losango(surf, (tx - 11, cy), 5, DOURADO)
    losango(surf, (tx + w + 11, cy), 5, DOURADO)

def barra(surf, rect, atual, maximo, cor, rotulo):
    maximo = max(1, maximo)
    prop = max(0.0, min(1.0, atual / maximo))
    raio = max(4, rect.h // 3)

    pygame.draw.rect(surf, (22, 15, 10), rect, border_radius=raio)
    interno = rect.inflate(-6, -6)
    largura_cheia = int(interno.w * prop)
    if largura_cheia > 0:
        claro = tuple(min(255, int(c * 1.35)) for c in cor) + (255,)
        escuro = tuple(int(c * 0.65) for c in cor) + (255,)
        g = gradiente_arredondado(interno.w, interno.h, claro, escuro, max(2, interno.h // 3))
        surf.blit(g, interno.topleft, area=pygame.Rect(0, 0, largura_cheia, interno.h))
    for f in (0.25, 0.5, 0.75):
        x = interno.x + int(interno.w * f)
        pygame.draw.line(surf, (25, 18, 12), (x, interno.y + 3), (x, interno.bottom - 4), 1)
    pygame.draw.rect(surf, BRONZE, rect, 2, border_radius=raio)

    txt = f"{rotulo}  {int(atual)}/{int(maximo)}"
    texto_centro(surf, fonte_pequena, txt, BRANCO, rect.centerx,
                 rect.centery - fonte_pequena.get_height() // 2)

def desenhar_info(surf, rect, p):
    gap = max(6, rect.h // 24)
    largura_esq = int(rect.w * 0.50)
    x_dir = rect.x + largura_esq + gap * 2
    larg_dir = rect.right - x_dir

    y = rect.y
    texto(surf, fonte_grande, p.nome, DOURADO, (rect.x, y))
    y += fonte_grande.get_height()
    texto(surf, fonte_pequena, f"{p.raca.nome} {p.classe.nome}", CREME, (rect.x, y))
    y += fonte_pequena.get_height() + 6
    ornamento(surf, rect.x, rect.x + largura_esq, y)
    y += 8

    barras = [("HP", p.vida, vida_maxima(p), VERMELHO)]
    rec = recurso_de(p)
    if rec:
        rotulo, atual, maximo, cor = rec
        barras.append((rotulo, atual, maximo, cor))

    restante = rect.bottom - y
    alt_barra = min(int(fonte_pequena.get_height() * 1.8), restante // (len(barras) + 1))
    espaco = max(4, (restante - alt_barra * len(barras)) // (len(barras) + 1))
    for rotulo, atual, maximo, cor in barras:
        y += espaco
        barra(surf, pygame.Rect(rect.x, y, largura_esq, alt_barra), atual, maximo, cor, rotulo)
        y += alt_barra

    arma = f"{p.arma.nome} ({p.arma.dano})" if p.arma else "Desarmado (5)"
    placas = [
        ("FORÇA", str(p.forca), fonte),
        ("AGILIDADE", str(p.agilidade), fonte),
        ("INTELIGÊNCIA", str(p.inteligencia), fonte),
        ("VITALIDADE", str(p.vitalidade), fonte),
        ("DEFESA", str(defesa_de(p)), fonte),
        ("ARMA", arma, fonte_pequena),
    ]
    pw = (larg_dir - gap) // 2
    ph = (rect.h - gap * 2) // 3
    for k, (rotulo, valor, fnt) in enumerate(placas):
        r = pygame.Rect(x_dir + (k % 2) * (pw + gap), rect.y + (k // 2) * (ph + gap), pw, ph)
        placa(surf, r)
        valor = cortar_texto(valor, fnt, pw - 16)
        total = fonte_mini.get_height() + fnt.get_height()
        y0 = r.centery - total // 2
        texto_centro(surf, fonte_mini, rotulo, CREME, r.centerx, y0)
        texto_centro(surf, fnt, valor, BRANCO, r.centerx, y0 + fonte_mini.get_height())

class Opcao:
    def __init__(self, txt, ativo = True, valor = None, detalhe = "", motivo = ""):
        self.texto = txt
        self.ativo = ativo
        self.valor = valor      
        self.detalhe = detalhe  
        self.motivo = motivo    

class MenuCombate:
    TITULOS = {"principal": "AÇÃO", "magias": "MAGIAS",
               "tecnicas": "TÉCNICAS", "itens": "ITENS"}
    COLUNAS = 2
    LINHAS = 2

    def __init__(self, personagem):
        self.p = personagem
        self.rects = []
        self.voltar()

    def opcoes(self):
        p = self.p

        if self.estado == "principal":
            n_itens = sum(1 for s in p.inventario.slots if s is not None)
            dano = p.arma.dano if p.arma else 5
            return [
                Opcao("Atacar", valor = ("atacar",), detalhe = f"Dano {dano}"),
                Opcao("Magia", ativo = bool(p.magias), valor = "magias",
                      detalhe = f"Conhecidas: {len(p.magias)}",
                      motivo = "Você não conhece nenhuma magia."),
                Opcao("Técnica", ativo = bool(p.tecnicas), valor = "tecnicas",
                      detalhe = f"Conhecidas: {len(p.tecnicas)}",
                      motivo = "Você não conhece nenhuma técnica."),
                Opcao("Itens", ativo = n_itens > 0, valor = "itens",
                      detalhe = f"Mochila: {n_itens}/{len(p.inventario.slots)}",
                      motivo = "Seu inventário está vazio."),
            ]

        if self.estado in ("magias", "tecnicas"):
            lista = p.magias if self.estado == "magias" else p.tecnicas
            ops = []
            for h in lista:
                rotulo = "Mana" if h.tipo == "Magia" else "Fúria"
                partes = []
                if h.custo > 0:
                    partes.append(f"{h.custo} {rotulo}")
                if h.cooldown > 0:
                    partes.append(f"Recarga {h.cooldown}")
                    motivo = f"{h.nome} está em recarga ({h.cooldown} turnos)."
                else:
                    motivo = f"{rotulo} insuficiente para {h.nome}."
                ops.append(Opcao(h.nome, h.pode_usar(p), ("habilidade", h),
                                 " | ".join(partes) or "Sem custo", motivo))
            return ops or [Opcao("(vazio)", ativo=False)]

        ops = []
        for i, item in enumerate(p.inventario.slots):
            if item is not None:
                ops.append(Opcao(f"{i + 1}. {item.nome}", True, ("item", i + 1),
                                 detalhe_item(item)))
        return ops or [Opcao("(vazio)", ativo=False)]

    def voltar(self):
        self.estado = "principal"
        self.indice = 0
        self.scroll = 0 

    def mover(self, dx, dy):
        total = len(self.opcoes())
        self.indice = max(0, min(total - 1, self.indice + dx + dy * self.COLUNAS))
        linha = self.indice // self.COLUNAS
        if linha < self.scroll:
            self.scroll = linha
        elif linha >= self.scroll + self.LINHAS:
            self.scroll = linha - self.LINHAS + 1

    def confirmar(self):
        ops = self.opcoes()
        self.indice = min(self.indice, len(ops) - 1)
        op = ops[self.indice]

        if not op.ativo:
            return ("aviso", op.motivo) if op.motivo else None

        if isinstance(op.valor, str):
            self.estado = op.valor
            self.indice = 0
            self.scroll = 0
            return None

        self.voltar()
        return op.valor

    def tratar_evento(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.mover(0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.mover(0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.mover(-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.mover(1, 0)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.confirmar()
            elif event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.voltar()

        elif event.type == pygame.MOUSEMOTION:
            for rect, i in self.rects:
                if rect.collidepoint(event.pos):
                    self.indice = i

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rect, i in self.rects:
                    if rect.collidepoint(event.pos):
                        self.indice = i
                        return self.confirmar()
            elif event.button == 3:
                self.voltar()

        elif event.type == pygame.MOUSEWHEEL:
            self.mover(0, -event.y)

        return None

    def desenhar(self, surf, rect, ativo = True):
        self.rects = []
        ops = self.opcoes()
        
        titulo = self.TITULOS[self.estado] if ativo else "AGUARDE..."
        dica = "Esc: voltar" if (ativo and self.estado != "principal") else ""
        cabecalho(surf, rect.x, rect.right, rect.y, titulo, DOURADO if ativo else CINZA, dica)

        altura_cab = fonte_pequena.get_height() + 8
        grade = pygame.Rect(rect.x, rect.y + altura_cab, rect.w, rect.h - altura_cab)
        gap = max(8, grade.h // 14)
        larg = (grade.w - gap) // self.COLUNAS
        alt = (grade.h - gap) // self.LINHAS

        total_linhas = ceil(len(ops) / self.COLUNAS)
        self.scroll = max(0, min(self.scroll, max(0, total_linhas - self.LINHAS)))
        primeiro = self.scroll * self.COLUNAS
        visiveis = ops[primeiro:primeiro + self.COLUNAS * self.LINHAS]

        for pos, op in enumerate(visiveis):
            i = primeiro + pos
            celula = pygame.Rect(grade.x + (pos % self.COLUNAS) * (larg + gap),
                                 grade.y + (pos // self.COLUNAS) * (alt + gap), larg, alt)
            self.rects.append((celula, i))

            if not ativo or not op.ativo:
                estado, cor_txt = "desabilitado", CINZA_ESCURO
            elif i == self.indice:
                estado, cor_txt = "selecionado", DOURADO
            else:
                estado, cor_txt = "normal", BRANCO
            placa(surf, celula, estado)

            pad = max(12, celula.h // 7)
            x_texto = celula.x + pad
            largura_txt = celula.right - pad * 2 - x_texto + pad

            nome = cortar_texto(op.texto, fonte, largura_txt)
            if op.detalhe:
                total = fonte.get_height() + fonte_pequena.get_height()
                y0 = celula.centery - total // 2
                texto(surf, fonte, nome, cor_txt, (x_texto, y0))
                texto(surf, fonte_pequena, cortar_texto(op.detalhe, fonte_pequena, largura_txt),
                      cor_txt if estado == "desabilitado" else CREME,
                      (x_texto, y0 + fonte.get_height()))
            else:
                texto(surf, fonte, nome, cor_txt, (x_texto, celula.centery - fonte.get_height() // 2))

def desenhar_inimigo(surf, inimigo):
    largura_tela, altura_tela = surf.get_size()
    largura = int(largura_tela * 0.28)
    x = largura_tela - largura - int(largura_tela * 0.015)
    y = int(altura_tela * 0.02)
    pad = 14
    altura_barra = int(fonte_pequena.get_height() * 1.5)

    rec = recurso_de(inimigo)
    n_barras = 2 if rec else 1
    caixa = pygame.Rect(x, y, largura,
                        pad * 2 + fonte_grande.get_height() + (altura_barra + 6) * n_barras)
    placa(surf, caixa)

    cy = caixa.y + pad
    texto(surf, fonte_grande, inimigo.nome, DOURADO, (caixa.x + pad, cy))
    cy += fonte_grande.get_height() + 2
    area = pygame.Rect(caixa.x + pad, cy, caixa.w - pad * 2, altura_barra)
    barra(surf, area, inimigo.vida, vida_maxima(inimigo), VERMELHO, "HP")
    if rec:
        rotulo, atual, maximo, cor = rec
        area.y += altura_barra + 6
        barra(surf, area, atual, maximo, cor, rotulo)

def desenhar_log(surf, mensagens):
    linhas = mensagens[-5:]
    if not linhas:
        return
    largura_tela, altura_tela = surf.get_size()
    altura_linha = fonte_pequena.get_height() + 4
    pad = 14
    caixa = pygame.Rect(int(largura_tela * 0.015), int(altura_tela * 0.02),
                        int(largura_tela * 0.42), pad * 2 + altura_linha * len(linhas))
    placa(surf, caixa)
    for i, linha in enumerate(linhas):
        cor = BRANCO if i == len(linhas) - 1 else CINZA
        txt = cortar_texto(linha, fonte_pequena, caixa.w - pad * 2)
        texto(surf, fonte_pequena, txt, cor, (caixa.x + pad, caixa.y + pad + i * altura_linha))

def desenhar_fim(surf, venceu, altura_cena, derrotados):
    largura_tela = surf.get_width()
    titulo = "VITÓRIA!" if venceu else "DERROTA..."
    cor = DOURADO if venceu else VERMELHO
 
    grande = pygame.font.SysFont("Arial", fonte_grande.get_height() * 2, bold=True)
    t1 = grande.render(titulo, True, cor)
        
    t2 = fonte.render(f"Inimigos derrotados: {derrotados}", True, CREME)
    t3 = fonte_pequena.render("Pressione R para reiniciar", True, BRANCO)
 
    fundo = t1.get_rect(center=(largura_tela // 2, altura_cena // 2)).inflate(120, 70)
    fundo.height += t2.get_height() + t3.get_height() + 20
    placa(surf, fundo)
 
    y = fundo.y + 35
    for t, espaco in ((t1, 10), (t2, 6), (t3, 0)):
        surf.blit(t, t.get_rect(midtop=(largura_tela // 2, y)))
        y += t.get_height() + espaco