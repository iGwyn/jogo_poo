from __future__ import annotations
from core import Habilidade

# TÉCNICAS

class Tecnica(Habilidade):
    efeito_funcao : str # Função
    
    def __init__(self, nome, efeito_funcao, custo = 0, poder_da_tecnica = 0, cooldown_padrao = 0):
        super().__init__(nome, custo, tipo = "Técnica")
        self.poder = poder_da_tecnica
        self.efeito_funcao = efeito_funcao
        self.cooldown_padrao = cooldown_padrao

    def executar(self, personagem, inimigo = None):
        personagem.furia -= self.custo
        
        self.efeito_funcao(personagem, self.poder, inimigo)
        self.cooldown = self.cooldown_padrao

def logica_dano_tecnico(personagem, poder, inimigo):
    dano = round(poder * (1 + personagem.forca / 100))
    inimigo.receber_dano(dano)   

def logica_buff(personagem, poder = None, inimigo = None):
    personagem.forca = round(personagem.forca * 1.2)
    personagem.vitalidade = round(personagem.vitalidade * 1.2)

def logica_cura_habilidade(personagem, poder, inimigo = None):
    cura = round(poder * (1 + personagem.inteligencia / 100))
    personagem.receber_cura(cura)

DICIONARIO_TECNICAS = {
    "adrenalina": {
        "nome": "Adrenalina",
        "custo": 15,
        "poder_da_tecnica": 0,
        "cooldown_padrao": 3,
        "efeito_funcao": logica_buff
    },
    "esmagador": {
        "nome": "Esmagador",
        "custo": 25,
        "poder_da_tecnica": 30,
        "cooldown_padrao": 2,
        "efeito_funcao": logica_dano_tecnico
    },
    "primeiros_socorros": {
        "nome": "Primeiros Socorros",
        "custo": 0,
        "poder_da_tecnica": 20,
        "cooldown_padrao": 3,
        "efeito_funcao": logica_cura_habilidade
    }
}

def tecnica(tecnica):
    if tecnica not in DICIONARIO_TECNICAS:
        raise ValueError(f"Técnica '{tecnica}' não encontrada.")
    
    config = DICIONARIO_TECNICAS[tecnica]
    return Tecnica(
        nome = config["nome"],
        custo = config["custo"],
        poder_da_tecnica = config["poder_da_tecnica"],
        cooldown_padrao = config["cooldown_padrao"],
        efeito_funcao = config["efeito_funcao"]
    )
       
# MAGIAS

class Magia(Habilidade):
    efeito_funcao : str # Função
    
    def __init__(self, nome, efeito_funcao, custo = 0, poder_do_feitico = 0, cooldown_padrao = 0):
        super().__init__(nome, custo, tipo = "Magia")
        self.poder = poder_do_feitico
        self.efeito_funcao = efeito_funcao
        self.cooldown_padrao = cooldown_padrao

    def executar(self, personagem, inimigo = None):
        personagem.mana -= self.custo
        
        self.efeito_funcao(personagem, self.poder, inimigo)
        self.cooldown = self.cooldown_padrao

def logica_dano_magico(personagem, poder, inimigo):
    dano = round(poder * (1 + personagem.inteligencia / 100))
    inimigo.receber_dano(dano)

def logica_drenar_vida(personagem, poder, inimigo):
    dano = round(poder * (1 + personagem.inteligencia / 100))
    inimigo.receber_dano(dano)
    personagem.receber_cura(dano / 2) 

def logica_buff_defesa(personagem, poder, inimigo = None):
    # Vai mudar para entrar na lógica de buff quando for implementada
    personagem.defesa += poder

DICIONARIO_MAGIAS = {
    "bola_de_fogo": {
        "nome" : "Bola de Fogo", 
        "custo" : 25,
        "poder_do_feitico" : 35, 
        "cooldown_padrao" : 0,
        "efeito_funcao" : logica_dano_magico
    },
    "cura_basica": {
        "nome" : "Cura Básica",
        "custo" : 20,
        "poder_do_feitico" : 35,
        "cooldown_padrao" : 1,
        "efeito_funcao" : logica_cura_habilidade
    },
    "cura_avancada": {
        "nome" : "Cura Avançada",
        "custo" : 40,
        "poder_do_feitico" : 70,
        "cooldown_padrao" : 3,
        "efeito_funcao" : logica_cura_habilidade
    },
    "drenar_vida": {
        "nome" : "Drenar Vida", 
        "custo" : 30,
        "poder_do_feitico" : 25, 
        "cooldown_padrao" : 2,
        "efeito_funcao" : logica_drenar_vida
    },
    "escudo_arcano": {
        "nome" : "Escudo Arcano", 
        "custo" : 15,
        "poder_do_feitico" : 15, 
        "cooldown_padrao" : 2,
        "efeito_funcao" : logica_buff_defesa
    }
}

def magia(magia):
    if magia not in DICIONARIO_MAGIAS:
        raise ValueError(f"Magia '{magia}' não encontrada.")
    
    config = DICIONARIO_MAGIAS[magia]
    return Magia(
        nome = config["nome"],
        custo = config["custo"],
        poder_do_feitico = config["poder_do_feitico"],
        cooldown_padrao = config["cooldown_padrao"],
        efeito_funcao = config["efeito_funcao"]
    )