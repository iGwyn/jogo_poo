from __future__ import annotations
from core import Item, IConsumivel, IEquipavel

# EQUIPAMENTOS

class Raridade:
    def __init__(self, nome, multiplicador, cor):
        self.__nome = nome
        self.__multiplicador = multiplicador
        self.__cor = cor
        
    @property
    def multiplicador(self):
        return self.__multiplicador

RARIDADES = {
    "Comum": Raridade("Comum", 1.0, "Branco"),
    "Raro": Raridade("Raro", 1.5, "Azul"),
    "Epico": Raridade("Épico", 2.2, "Roxo")
}

class Arma(Item, IEquipavel):
    dano : int
    raridade : Raridade
    
    def __init__(self, nome, dano, raridade):
        super().__init__(nome)
        self.raridade = raridade
        self.dano = round(dano * raridade.multiplicador)
        
    def equipar(self, personagem):
        personagem.arma = self

class Armadura(Item, IEquipavel):
    defesa : int
    raridade : Raridade
    
    def __init__(self, nome, defesa, raridade):
        super().__init__(nome)
        self.raridade = raridade
        self.defesa = round(defesa * raridade.multiplicador)
    
    def equipar(self, personagem):
        personagem.peitoral = self
        
class Consumivel(Item, IConsumivel):
    def __init__(self, nome, valor, efeito_funcao):
        super().__init__(nome)
        self.valor = valor
        self.efeito_funcao = efeito_funcao

    def usar(self, personagem):
        self.efeito_funcao(personagem, self.valor)
    
def logica_cura_consumivel(personagem, valor):
    personagem.receber_cura(valor)
    
def logica_mana_consumivel(personagem, valor):
    personagem.mana = min(personagem.mana_maxima, round(personagem.mana + valor))    
    
DICIONARIO_POCOES = {
    "pocao_de_cura": {
        "nome": "Poção de Cura",
        "valor": 50,
        "efeito_funcao": logica_cura_consumivel
    },
    "pocao_de_mana": {
        "nome": "Poção de Mana",
        "valor": 35,
        "efeito_funcao": logica_mana_consumivel
    }
}

def consumivel(consumivel):
    if consumivel not in DICIONARIO_POCOES:
        raise ValueError(f"Consumível '{consumivel}' não encontrado.")
    
    config = DICIONARIO_POCOES[consumivel]
    return Consumivel(
        nome = config["nome"],
        valor = config["valor"],
        efeito_funcao = config["efeito_funcao"]
    )


