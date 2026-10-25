from __future__ import annotations
from abc import ABC, abstractmethod

# CLASSES ABSTRATAS
# Talvez um atributo carisma, pois o loot após batalha vai ser aleatorizado já que a platéia que vai
# dar os itens ou não (chance de ganhar algo ou de n ganhar, e afetar a qualidade do item caso ganhe)
class Personagem(ABC):
    __nome : str
    __raca : Classe_Raca
    __classe : Classe_Raca
    magia : Habilidade
    tecnica : Habilidade
    forca : int
    agilidade : int
    inteligencia : int
    vitalidade : int
    arma : Arma
    peitoral : Armadura

    def __init__(self, nome, raca, classe, arma = None, peitoral = None):
        self.__nome = nome
        self.__raca = raca
        self.__classe = classe
        self.magia = []
        self.tecnica = []
        
        self.forca = raca.b_forca + classe.b_forca
        self.agilidade = raca.b_agilidade + classe.b_agilidade
        self.inteligencia = raca.b_inteligencia + classe.b_inteligencia
        self.vitalidade = raca.b_vitalidade + classe.b_vitalidade

        classe.passiva(self)
        
        self.arma = arma
        self.peitoral = peitoral
        self.__vida = 100 * (1 + (self.vitalidade / 100))

        self.esta_defendendo = False
        self.bonus_bloqueio = 1.5

    @property
    def classe(self):
        return self.__classe
    
    @property
    def raca(self):
        return self.__raca
    
    @property
    def vida(self):
        return self.__vida
    
    @abstractmethod
    def atacar(self):
        pass

    def bloquear(self):
        self.esta_defendendo = True

    def defesa_atual(self):
        if self.esta_defendendo:
            return self.peitoral.defesa * self.bonus_bloqueio
        return self.peitoral.defesa
    
    def receber_dano(self, dano):
        if self.__vida == 0:
            raise Exception(f"{self.__nome} já morreu...")
        else:
            self.__vida -= dano
            if self.__vida < 0:
                self.__vida = 0
                raise Exception(f"{self.__nome} morreu...")
    
    def comecar_turno(self):
        if self.esta_defendendo:
            self.esta_defendendo = False
            
    def usar_raca(self, inimigo = None):
        self.raca.ativa(self, inimigo)
        
    def usar_classe(self, inimigo = None):
        self.classe.ativa(self, inimigo)
    
    """
    def fim_de_turno(self):
        pass"""
        
class Classe_Raca(ABC):
    def __init__(self, b_forca, b_agilidade, b_inteligencia, b_vitalidade):
        self.b_forca = b_forca
        self.b_agilidade = b_agilidade
        self.b_inteligencia = b_inteligencia
        self.b_vitalidade = b_vitalidade

    @abstractmethod
    def passiva(self, personagem = None, inimigo = None):
        pass
    
    @abstractmethod
    def ativa(self, personagem = None, inimigo = None):
        pass

class Item(ABC):
    def __init__(self, nome):
        self.nome = nome

class Habilidade(ABC):
    def __init__(self, nome, custo_mana = 0):
        self.__nome = nome
        self.cooldown = 0
        self.custo_mana = custo_mana

    @abstractmethod
    def executar(self, personagem = None, inimigo = None):
        pass
    
    def reduzir_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            
    def pode_usar(self, personagem):
        if self.cooldown > 0:
            return False
        
        if self.custo_mana > 0:
            if hasattr(personagem, 'mana') and personagem.mana >= self.custo_mana:
                return True
            else:
                return False
            
        return True

# PLAYER/NPC

class Gladiador(Personagem):
    inventario : Inventario
    
    def __init__(self, nome, raca, classe, arma = None, peitoral = None):
        super().__init__(nome, raca, classe, arma, peitoral)
        self.pontos_habilidade = 10
        self.inventario = []
        
    def atacar(self, inimigo):
        inimigo.receber_dano(self.arma.dano)
        
# CLASSES

class Guerreiro(Classe_Raca):
    def __init__(self):
        super().__init__(b_forca = 5, b_agilidade = -1, b_inteligencia = -2, b_vitalidade = 8)
        self.habilidade_ativa = Esmagador()
        
    def passiva(self, personagem = None, inimigo = None):
        personagem.vitalidade *= 1.5
        
    def ativa(self, personagem = None, inimigo = None):
        """Esmagador"""
        if self.habilidade_ativa.pode_usar(personagem):
            self.habilidade_ativa.executar(personagem, inimigo)

# RAÇA

class Humano(Classe_Raca):
    def __init__(self):
        super().__init__(b_forca = 1, b_agilidade = 1, b_inteligencia = 1, b_vitalidade = 1)
        self.habilidade_ativa = Adrenalina()
        
    def passiva(self, personagem = None, inimigo = None):
        personagem.pontos_habilidade += 10
        
    def ativa(self, personagem = None, inimigo = None):
        """Adrenalina"""
        if self.habilidade_ativa.pode_usar(personagem):
            self.habilidade_ativa.executar(personagem, inimigo)

# TÉCNICAS

class Adrenalina(Habilidade):
    def __init__(self):
        super().__init__(nome = "Adrenalina")

    def executar(self, personagem = None, inimigo = None):
        personagem.forca *= 1.2
        personagem.vitalidade *= 1.2
        self.cooldown = 3
        
class Esmagador(Habilidade):
    def __init__(self):
        super().__init__(nome = "Esmagador")

    def executar(self, personagem = None, inimigo = None):
        dano = personagem.arma.dano * 2 * (1 + personagem.forca / 100)
        inimigo.receber_dano(dano)
        self.cooldown = 2

# MAGIAS

class Cura_basica(Habilidade):
    def __init__(self):
        super().__init__(nome = "Cura Básica", custo_mana = 20)

    def executar(self, personagem):
        personagem.cura = 35 * (1 + personagem.inteligencia / 100)

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

class Arma(Item):
    def __init__(self, nome, dano, raridade : Raridade):
        super().__init__(nome)
        self.dano = dano * raridade.multiplicador

class Armadura(Item):
    def __init__(self, nome, defesa, raridade : Raridade):
        super().__init__(nome)
        self.defesa = defesa * raridade.multiplicador

# ITEMS

class Inventario:
    def __init__(self):
        self.slots = [None] * 9
    
    def adicionar_item(self, item):
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = item
                return True
        return False
        
    def remover_item(self, numero_do_slot):
        posicao = numero_do_slot - 1
        if 0 <= posicao < len(self.slots) and self.slots[posicao] is not None:
            item_removido = self.slots[posicao]
            self.slots[posicao] = None
            return item_removido
        return False