class Combate:
    TURNO_JOGADOR = "turno_jogador"
    TURNO_INIMIGO = "turno_inimigo"
    VITORIA = "vitoria"
    DERROTA = "derrota"

    ESPERA_INIMIGO_MS = 1000

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo
        self.estado = self.TURNO_JOGADOR
        self.mensagens = []
        self._proximo_evento = 0

        self.registrar("Um novo desafio no Coliseu!")
        self.jogador.comecar_turno()

    @property
    def terminou(self):
        return self.estado in (self.VITORIA, self.DERROTA)

    # Log
    
    def registrar(self, texto):
        self.mensagens.append(texto)
        del self.mensagens[:-50]

    def _tentar(self, func, *args):
        try:
            func(*args)
            return True
        except Exception as erro:
            if "morreu" not in str(erro):
                self.registrar(f"! {erro}")
            return False

    @staticmethod
    def _descrever(descricao, dano, cura):
        texto = descricao
        if dano > 0:
            texto += f" Causa {dano} de dano."
        if cura > 0:
            texto += f" Recupera {cura} de vida."
        return texto

    # Turno do jogador
    
    def executar_acao_jogador(self, acao, agora):
        if self.estado != self.TURNO_JOGADOR:
            return False

        j, i = self.jogador, self.inimigo
        tipo = acao[0]

        if tipo == "aviso":
            self.registrar(acao[1])
            return False

        vida_j, vida_i = j.vida, i.vida

        if tipo == "atacar":
            descricao = f"{j.nome} ataca!"
            ok = self._tentar(j.atacar, i)
        elif tipo == "habilidade":
            habilidade = acao[1]
            descricao = f"{j.nome} usa {habilidade.nome}!"
            ok = self._tentar(j.usar_habilidade, habilidade, i)
        elif tipo == "item":
            item = j.inventario.verificar_item(acao[1])
            descricao = f"{j.nome} usa {item.nome}."
            ok = self._tentar(j.usar_item, acao[1])
        else:
            return False
        
        if not ok and i.vida > 0 and j.vida > 0:
            return False

        self.registrar(self._descrever(descricao, vida_i - i.vida, j.vida - vida_j))

        if i.vida <= 0:
            self.registrar(f"{i.nome} foi derrotado!")
            self.estado = self.VITORIA
        else:
            self.estado = self.TURNO_INIMIGO
            self._proximo_evento = agora + self.ESPERA_INIMIGO_MS
        return True

    # Turno do inimigo

    def atualizar(self, agora):
        if self.estado == self.TURNO_INIMIGO and agora >= self._proximo_evento:
            self._turno_inimigo()

    def _turno_inimigo(self):
        j, i = self.jogador, self.inimigo
        i.comecar_turno()
        vida_j, vida_i = j.vida, i.vida

        acao = i.decidir_acao(j)
        if acao[0] == "habilidade":
            habilidade = acao[1]
            descricao = f"{i.nome} usa {habilidade.nome}!"
            self._tentar(i.usar_habilidade, habilidade, j)
        else:
            descricao = f"{i.nome} ataca!"
            self._tentar(i.atacar, j)

        self.registrar(self._descrever(descricao, vida_j - j.vida, i.vida - vida_i))

        if j.vida <= 0:
            self.registrar(f"{j.nome} caiu na arena...")
            self.estado = self.DERROTA
        else:
            j.comecar_turno()
            self.estado = self.TURNO_JOGADOR
            self.registrar("Sua vez!")