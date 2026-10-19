from __future__ import annotations
from abc import ABC, abstractmethod

# CLASSES ABSTRATAS

class Personagem(ABC):
    __nome : str
    __raca : Classe_Raca
    __classe : Classe_Raca
    forca : int
    agilidade : int
    inteligencia : int
    arma : Arma
    peitoral : Armadura

    def __init__(self, nome, raca, classe, forca, agilidade, inteligencia, vitalidade, arma = None, peitoral = None):
        self.__nome = nome
        self.__raca = raca
        self.__classe = classe
        
        self.__forca = forca + raca.__b_forca + classe.__b_forca
        self.__agilidade = agilidade + raca.__b_agilidade + classe.__b_agilidade
        self.__inteligencia = inteligencia + raca.__b_inteligencia + classe.__b_inteligencia
        self.__vitalidade = vitalidade + raca.__b_vitalidade + classe.__b_vitalidade

        self.arma = arma
        self.peitoral = peitoral
        self.__vida = 100 * (1 + (self.__vitalidade / 100))

        self.esta_defendendo = False
        self.bonus_bloqueio = 1.5
        
        self.pontos_habilidade = 10

    @abstractmethod
    def ataque(self):
        pass

    def defesa_atual(self):
        if self.esta_defendendo:
            return self.peitoral.defesa * self.bonus_bloqueio
        return self.peitoral.defesa
    
    def bloquear(self):
        self.esta_defendendo = True
    
    def receber_dano(self, dano):
        if self.__vida == 0:
            raise Exception(f"{self.__nome} Morreu...")
        else:
            self.__vida -= dano
            if self.__vida < 0:
                self.__vida = 0
    
    def comecar_turno(self):
        if self.esta_defendendo:
            self.esta_defendendo = False
    
    """
    def fim_de_turno(self):
        pass"""
        
class Classe_Raca(ABC):
    def __init__(self, b_forca, b_agilidade, b_inteligencia, b_vitalidade):
        self.__b_forca = b_forca
        self.__b_agilidade = b_agilidade
        self.__b_inteligencia = b_inteligencia
        self.__b_vitalidade = b_vitalidade

    @abstractmethod
    def passiva(self, personagem):
        pass
    
    @abstractmethod
    def ativa(self, personagem):
        pass
    
class Arma(ABC):
    def __init__(self, dano):
        self.dano = dano
        
class Armadura(ABC):
    def __init__(self, defesa):
        self.defesa = defesa

class Habilidade(ABC):
    def __init__(self, nome, cooldown = 0, custo_mana = 0):
        self.__nome = nome
        self.__cooldown = cooldown
        self.__custo_mana = custo_mana
        self.cooldown_atual = 0

    @abstractmethod
    def executar(self, personagem):
        pass
    
    def reduzir_cooldown(self):
        if self.cooldown_atual > 0:
            self.cooldown_atual -= 1
            
    def pode_usar(self, personagem):
        if self.cooldown_atual > 0:
            return False
        
        if self.__custo_mana > 0:
            if hasattr(personagem, 'mana') and personagem.mana >= self.__custo_mana:
                return True
            else:
                return False
            
        return True

# PLAYER/NPC

class Gladiador(Personagem):
    def __init__(self, nome, raca, classe, forca, agilidade, inteligencia, vitalidade, arma = None, peitoral = None):
        super().__init__(nome, raca, classe, forca, agilidade, inteligencia, vitalidade, arma, peitoral)
        
    def atacar(self):
        pass
        
# CLASSES

class Guerreiro(Classe_Raca):
    def __init__(self):
        super().__init__(b_forca = 5, b_agilidade = -1, b_inteligencia = -2, b_vitalidade = 8)
        
    def passiva(self, personagem):
        personagem.__vitalidade *= 1.5
        
    def ativa(self, personagem):
        """Esmagador"""
        #Formula personagem.arma.dano * 2 * (1 + self.__forca / 100)
        pass

# RAÇA

class Humano(Classe_Raca):
    def __init__(self):
        super().__init__(b_forca = 1, b_agilidade = 1, b_inteligencia = 1, b_vitalidade = 1)
        self.contador = 0
        
    def passiva(self, personagem):
        personagem.pontos_habilidade += 10
        
    def ativa(self, personagem):
        """Adrenalina"""
        pass

# TÉCNICAS

# MAGIAS

# EQUIPAMENTOS

class Raridade:
    def __init__(self, nome, multiplicador, cor):
        self.__nome = nome
        self.__multiplicador = multiplicador
        self.__cor = cor

RARIDADES = {
    "Comum": Raridade("Comum", 1.0, "Branco"),
    "Raro": Raridade("Raro", 1.5, "Azul"),
    "Epico": Raridade("Épico", 2.2, "Roxo")
}

class Peitoral(Armadura):
    def __init__(self, defesa, raridade : Raridade):
        super().__init__(defesa)
        self.__raridade = raridade
        self.__defesa = defesa * raridade.__multiplicador

# ITEMS
