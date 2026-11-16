from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
import random

# Classe abstrata base de Gladiador e NPC
class Personagem(ABC):
    __nome : str
    __raca : Raca_abs
    __classe : Classe_abs
    __vida : int
    tecnica : Habilidade
    magia : Habilidade
    forca : int
    agilidade : int
    inteligencia : int
    vitalidade : int
    arma : Item
    peitoral : Item
    capacete : Item
    
    def __init__(self, nome, raca, classe, arma = None, peitoral = None, capacete = None):
        self.__nome = nome
        self.__raca = raca
        self.__classe = classe
        self.tecnicas = []
        self.magias = []
        self.buffs_ativos = []
        self.debuffs_ativos = []
        
        self.forca = raca.b_forca + classe.b_forca
        self.agilidade = raca.b_agilidade + classe.b_agilidade
        self.inteligencia = raca.b_inteligencia + classe.b_inteligencia
        self.vitalidade = raca.b_vitalidade + classe.b_vitalidade
        self.pontos_habilidade = 10
        
        self.arma = arma
        self.peitoral = peitoral
        self.capacete = capacete
        self.esta_defendendo = False
        self.bonus_bloqueio = 1.5
        
        classe.passiva(self)
        raca.passiva(self)
        
        match self.classe.recurso:
            case "Fúria":
                self.furia = 0
                self.furia_maxima = 100
            case "Mana":
                max_mana = 100 * (1 + self.inteligencia / 100)
                self.mana = max_mana
                self.mana_maxima = max_mana
        
        self.__vida = round(100 * (1 + self.vitalidade / 100))
        self.__vida_maxima = round(100 * (1 + self.vitalidade / 100))

    @property
    def nome(self):
        return self.__nome
    
    @property
    def classe(self):
        return self.__classe

    @property
    def raca(self):
        return self.__raca
    
    @property
    def vida(self):
        return self.__vida
    
    @property
    def vida_maxima(self):
        return self.__vida_maxima

    @vida.setter
    def vida(self, valor):
        self.__vida = valor
    
    def atacar(self, inimigo):
        if hasattr(self, 'furia'):
            self.gerenciar_recurso("atacar", 15)
        
        if self.arma:
            inimigo.receber_dano(self.arma.dano)
        else:
            inimigo.receber_dano(5)     
        
    @abstractmethod
    def atribuir_pontos(self):
        pass
    
    def comecar_turno(self):
        if self.esta_defendendo:
            self.esta_defendendo = False
            
        for t in self.tecnicas:
            t.reduzir_cooldown()
        for m in self.magias:
            m.reduzir_cooldown()
            
        self.gerenciar_recurso("proximo_turno")
            
    def bloquear(self):
        self.esta_defendendo = True

    def defesa_atual(self):
        defesa_natural = self.vitalidade * 0.15
        if self.peitoral is None and self.capacete is None:
            AC = round(defesa_natural)
        elif self.capacete is None:
            AC = round(self.peitoral.defesa + defesa_natural)
        elif self.peitoral is None:
            AC = round(self.capacete.defesa + defesa_natural)
        else:
            AC = round(self.peitoral.defesa + self.capacete.defesa + defesa_natural)

        if self.esta_defendendo:
            return round(AC * self.bonus_bloqueio)
        return AC
    
    def receber_dano(self, dano):
        if self.__vida == 0:
            raise Exception(f"{self.__nome} já morreu...")
        else:
            dano -= self.defesa_atual()
            if dano < 0:
                dano = 0
            self.__vida -= dano
            if hasattr(self, 'furia'):
                self.gerenciar_recurso("receber_dano", 10)
            if self.__vida < 0:
                self.__vida = 0
                raise Exception(f"{self.__nome} morreu...")
        return True

    def receber_cura(self, cura):
        self.__vida = min(self.__vida_maxima, round(self.__vida + cura))
    
    def aprender_habilidade(self, habilidade):
        if habilidade.tipo == "Técnica":
            self.tecnicas.append(habilidade)
        elif habilidade.tipo == "Magia":
            self.magias.append(habilidade)
    
    def usar_habilidade(self, habilidade, inimigo = None):
        todas_habilidades = self.tecnicas + self.magias
        habilidade_encontrada = None
        for h in todas_habilidades:
            if h.nome.lower() == habilidade.nome.lower():
                habilidade_encontrada = h
                break
    
        if not habilidade_encontrada:
            raise Exception(f"{self.__nome} não conhece a habilidade {habilidade.nome}.")
        
        if habilidade_encontrada.pode_usar(self):
            if inimigo:
                habilidade_encontrada.executar(self, inimigo)
            else:
                habilidade_encontrada.executar(self)
            return True
        else:
            raise Exception(f"{self.__nome} não pode usar {habilidade.nome} agora.")
    
    # Mover esse para gladiador após os testes, já q não precisamos saber o cooldown dos NPCs | Ou deixar aqui 
    def mostrar_habilidade(self):
        if self.tecnicas:
            print("Técnicas")
            for t in self.tecnicas:
                if t.cooldown == 0:
                    print(f"{t.nome} está disponível para uso")
                else:
                    print(f"{t.nome} está em cooldown ({t.cooldown} turnos restantes)")
                    
        if self.magias:
            print("Magias")
            for m in self.magias:
                if m.cooldown == 0:
                    print(f"{m.nome} está disponível para uso")
                else:
                    print(f"{m.nome} está em cooldown ({m.cooldown} turnos restantes)") 
                
    def gerenciar_recurso(self, evento, valor = 0):
        if hasattr(self, 'furia'):
            if evento in ["atacar", "receber_dano"]:
                self.furia = min(self.furia_maxima, self.furia + valor)

        if hasattr(self, 'mana'):
            if evento == "proximo_turno":
                taxa_reg = 15 * (1 + self.inteligencia / 50)
                reg_mana = round(self.mana + taxa_reg)
                self.mana = min(self.mana_maxima, reg_mana)
                print(f"{self.__nome} regenerou mana. Atual: {self.mana}")  
                  
    """
    def fim_de_turno(self):
        pass"""

class Raca_abs(ABC):
    def __init__(self, chave, nome, b_forca, b_agilidade, b_inteligencia, b_vitalidade):
        self.chave = chave
        self.nome = nome
        self.b_forca = b_forca
        self.b_agilidade = b_agilidade
        self.b_inteligencia = b_inteligencia
        self.b_vitalidade = b_vitalidade

class Classe_abs(ABC):
    recurso : str # Furia ou Mana
    
    def __init__(self, chave, nome, b_forca, b_agilidade, b_inteligencia, b_vitalidade, recurso):
        self.chave = chave
        self.nome = nome
        self.b_forca = b_forca
        self.b_agilidade = b_agilidade
        self.b_inteligencia = b_inteligencia
        self.b_vitalidade = b_vitalidade
        self.recurso = recurso

    @abstractmethod
    def passiva(self, personagem = None, inimigo = None):
        pass

class Item(ABC):
    def __init__(self, chave, nome):
        self.chave = chave
        self.nome = nome

class IConsumivel(ABC):
    @abstractmethod
    def usar(self, personagem):
        pass

class IEquipavel(ABC):
    @abstractmethod
    def equipar(self, personagem):
        pass
    
class Habilidade(ABC):
    def __init__(self, chave, nome, custo = 0, cooldown = 0, tipo = str):
        self.chave = chave
        self.__nome = nome
        self.cooldown = cooldown
        self.custo = custo
        self.tipo = tipo

    @property
    def nome(self):
        return self.__nome
    
    @abstractmethod
    def executar(self, personagem = None, inimigo = None):
        pass
    
    def reduzir_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def pode_usar(self, personagem):   
        if self.cooldown > 0:
            return False
                    
        if self.custo > 0:
            if self.tipo == "Técnica":
                recurso = getattr(personagem, 'furia', 0)
            elif self.tipo == "Magia":
                recurso = getattr(personagem, 'mana', 0)
            else:
                recurso = 0
            return recurso >= self.custo
                        
        return True

######################################################################################### 
#PLAYER/NPC

class Gladiador(Personagem):
    inventario : Inventario
    
    def __init__(self, nome, raca, classe, arma = None, peitoral = None, capacete = None):
        super().__init__(nome, raca, classe, arma, peitoral, capacete)
        self.inventario = Inventario()
    
    # Passivel de sofrer alterações, atribuição de pontos de habilidade
    def atribuir_pontos(self, forca = 0, agilidade = 0, inteligencia = 0, vitalidade = 0):
        atributos = [forca, agilidade, inteligencia, vitalidade]
        
        for atributo in atributos:
            if not isinstance(atributo, int) or isinstance(atributo, bool):
                print("Valores errados, utilize apenas int.")
                return False
        
        total_gasto = forca + agilidade + inteligencia + vitalidade
        
        if total_gasto > self.pontos_habilidade:
            print("Você não tem pontos de habilidade suficientes!")
            return False
        
        self.forca += forca
        self.agilidade += agilidade
        self.inteligencia += inteligencia
        self.vitalidade += vitalidade
    
        self.pontos_habilidade -= total_gasto
        
        self.vida = round(100 * (1 + self.vitalidade / 100))
        
    def usar_item(self, numero_do_slot):
        item = self.inventario.verificar_item(numero_do_slot)
        if item is None:
            raise Exception(f"Slot {numero_do_slot} está vazio.")
        
        if isinstance(item, IConsumivel):
            item.usar(self)
            self.inventario.remover_item(numero_do_slot)
            return True
        elif isinstance(item, IEquipavel):
            item.equipar(self)
            self.inventario.remover_item(numero_do_slot)
            return True
        else:
            raise Exception(f"O {item.nome} não pode ser usado.")
        
class Inventario:
    def __init__(self):
        self.slots = [None] * 8
    
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
        raise Exception(f"Slot {numero_do_slot} está vazio.")
    
    def listar_itens(self):
        for i, item in enumerate(self.slots):
            if item is not None:
                print(f"Slot {i + 1}: {item.nome}")
            else:
                print(f"Slot {i + 1}: Vazio")
                
    def verificar_item(self, numero_do_slot):
        posicao = numero_do_slot - 1
        if 0 <= posicao < len(self.slots):
            return self.slots[posicao]
        raise Exception(f"Slot {numero_do_slot} está vazio.")
    
class NPC(Personagem):
    def __init__(self, nome, raca, classe, arma = None, peitoral = None, capacete = None, chance_habilidade = 0.5):
        super().__init__(nome, raca, classe, arma, peitoral, capacete)
        self.chance_habilidade = chance_habilidade

    # Randomizar os atributos do NPC com base na sua classe    
    
    def atribuir_pontos(self):
        pass

    def habilidades_disponiveis(self):
        resultados = []
        todas_habilidades = self.tecnicas + self.magias
    
        for h in todas_habilidades:
            if h.pode_usar(self):
                resultados.append(h)
    
        return resultados
    
    def decidir_acao(self, alvo = None):
        disponiveis = self.habilidades_disponiveis()
        if disponiveis and random.random() < self.chance_habilidade:
            return ("habilidade", random.choice(disponiveis))
        return ("atacar",)