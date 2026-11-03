from __future__ import annotations
from core import Raca_abs, Classe_abs
from habilidades import tecnica, magia

# CLASSES

class Classe(Classe_abs):
    def __init__(self, nome, b_forca, b_agilidade, b_inteligencia, b_vitalidade, recurso, passiva_funcao):
        super().__init__(b_forca = b_forca, b_agilidade = b_agilidade, b_inteligencia = b_inteligencia, b_vitalidade = b_vitalidade, recurso = recurso)
        self.nome = nome
        self.passiva_funcao = passiva_funcao

    def passiva(self, personagem):
        self.passiva_funcao(personagem)

def logica_passiva_guerreiro(personagem):
    personagem.vitalidade = round(personagem.vitalidade * 1.5)
    personagem.aprender_habilidade(tecnica("esmagador"))

DICIONARIO_CLASSES = {
    "guerreiro": {
        "nome": "Guerreiro",
        "b_forca": 5,
        "b_agilidade": -1,
        "b_inteligencia": -2,
        "b_vitalidade": 8,
        "recurso": "Fúria",
        "passiva_funcao": logica_passiva_guerreiro
    }
}

def classe(classe):
    if classe not in DICIONARIO_CLASSES:
        raise ValueError(f"Classe '{classe}' não encontrada.")
    
    config = DICIONARIO_CLASSES[classe]
    return Classe(
        nome = config["nome"],
        b_forca = config["b_forca"],
        b_agilidade = config["b_agilidade"],
        b_inteligencia = config["b_inteligencia"],
        b_vitalidade = config["b_vitalidade"],
        recurso = config["recurso"],
        passiva_funcao = config["passiva_funcao"]
    )

# RAÇA

class Raca(Raca_abs):
    def __init__(self, nome, b_forca, b_agilidade, b_inteligencia, b_vitalidade, funcao_passiva):
        super().__init__(b_forca = b_forca, b_agilidade = b_agilidade, b_inteligencia = b_inteligencia, b_vitalidade = b_vitalidade)
        self.nome = nome
        self.funcao_passiva = funcao_passiva
        
    def passiva(self, personagem):
        self.funcao_passiva(personagem)
        
def logica_passiva_humano(personagem):
    personagem.pontos_habilidade += 10
    personagem.aprender_habilidade(tecnica("adrenalina"))
    
DICIONARIO_RACAS = {
    "humano": {
        "nome": "Humano",
        "b_forca": 1,
        "b_agilidade": 1,
        "b_inteligencia": 1,
        "b_vitalidade": 1,
        "funcao_passiva": logica_passiva_humano
    }
}

def raca(raca):
    if raca not in DICIONARIO_RACAS:
        raise ValueError(f"Raça '{raca}' não encontrada.")
    
    config = DICIONARIO_RACAS[raca]
    return Raca(
        nome = config["nome"],
        b_forca = config["b_forca"],
        b_agilidade = config["b_agilidade"],
        b_inteligencia = config["b_inteligencia"],
        b_vitalidade = config["b_vitalidade"],
        funcao_passiva = config["funcao_passiva"]
    )
