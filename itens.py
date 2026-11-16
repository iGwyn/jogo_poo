from __future__ import annotations
from core import Item, IConsumivel, IEquipavel

# EQUIPAMENTOS

class Raridade:
    def __init__(self, chave, nome, multiplicador, cor):
        self.chave = chave
        self.__nome = nome
        self.__multiplicador = multiplicador
        self.__cor = cor
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def multiplicador(self):
        return self.__multiplicador

RARIDADES = {
    "Comum" : Raridade("comum", "Comum", 1.0, "Branco"),
    "Raro" : Raridade("raro", "Raro", 1.5, "Azul"),
    "Epico" : Raridade("epico", "Épico", 2.2, "Roxo")
}

########################################################################
# Armas

class Arma(Item, IEquipavel):
    dano : int
    raridade : Raridade
    
    def __init__(self, chave, nome, dano, raridade):
        super().__init__(chave, nome)
        self.raridade = raridade
        self.dano_base = dano
        self.dano = round(self.dano_base * raridade.multiplicador)
        
    def equipar(self, personagem):
        personagem.arma = self

DICIONARIO_ARMAS = {
    "espada" : {
        "nome" : "Espada",
        "dano" : 15,
        "raridade" : "Comum"
    },
    "excalibur" : {
        "nome" : "Excalibur",
        "dano" : 50,
        "raridade" : "Epico"
    }
}

def arma(arma):
    if arma not in DICIONARIO_ARMAS:
        raise ValueError(f"Arma '{arma}' não encontrada.")
    
    config = DICIONARIO_ARMAS[arma]
    return Arma(
        chave = arma,
        nome = config["nome"],
        dano = config["dano"],
        raridade = RARIDADES[config["raridade"]]
    )

########################################################################
# Armaduras

class Armadura(Item, IEquipavel):
    defesa : int
    raridade : Raridade
    
    def __init__(self, chave, nome, tipo, defesa, raridade):
        super().__init__(chave, nome)
        self.tipo = tipo
        self.raridade = raridade
        self.defesa_base = defesa
        self.defesa = round(self.defesa_base * raridade.multiplicador)
    
    def equipar(self, personagem):
        if self.tipo == "peitoral":
            personagem.peitoral = self
        else:
            personagem.capacete = self

DICIONARIO_ARMADURAS = {
    "peitoral" : {
        "nome" : "Peitoral",
        "tipo" : "peitoral",
        "defesa" : 10,
        "raridade" : "Comum"
    },
    "peitoral_teste" : {
        "nome" : "Peitoral -10 defesa",
        "tipo" : "peitoral",
        "defesa" : -10,
        "raridade" : "Comum"
    },
    "capacete" : {
        "nome" : "Capacete",
        "tipo" : "capacete",
        "defesa" : 5,
        "raridade" : "Comum"
    },
    "capacete_teste" : {
        "nome" : "Capacete da morte",
        "tipo" : "capacete",
        "defesa" : -100,
        "raridade" : "Comum"
    }  
}

def armadura(armadura):
    if armadura not in DICIONARIO_ARMADURAS:
        raise ValueError(f"Armadura '{armadura}' não encontrada.")
    
    config = DICIONARIO_ARMADURAS[armadura]
    return Armadura(
        chave = armadura,
        nome = config["nome"],
        tipo = config["tipo"],
        defesa = config["defesa"],
        raridade = RARIDADES[config["raridade"]]
    )

#######################################################################
# Consumiveis

class Consumivel(Item, IConsumivel):
    def __init__(self, chave, nome, valor, efeito_funcao):
        super().__init__(chave, nome)
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
        chave = consumivel,
        nome = config["nome"],
        valor = config["valor"],
        efeito_funcao = config["efeito_funcao"]
    )


