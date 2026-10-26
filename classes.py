from __future__ import annotations
from abc import ABC, abstractmethod

# DECIDIR SE VAI USAR FLOAT NOS ATRIBUTOS/VIDA OU NÃO, CASO DECIDA USAR É POSSÍVEL FAZER UM LAST STAND ONDE SE FICAR COM VIDA < 1
# VOCÊ TEM 50% DE CHANCE DE MATAR O INIMIGO AUTOMATICAMENTE | SE FOR DECIDIDO NÃO USAR FLOAT, DA PRA FAZER COM 1HP

# CLASSES ABSTRATAS

# Talvez um atributo carisma, pois o loot após batalha vai ser aleatorizado já que a platéia que vai
# dar os itens ou não (chance de ganhar algo ou de n ganhar, e afetar a qualidade do item caso ganhe)
class Personagem(ABC):
    __nome : str
    __raca : Classe_Raca
    __classe : Classe_Raca
    __vida : int
    #mana : int
    habilidades : Habilidade
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
        self.habilidades = []
        
        self.forca = raca.b_forca + classe.b_forca
        self.agilidade = raca.b_agilidade + classe.b_agilidade
        self.inteligencia = raca.b_inteligencia + classe.b_inteligencia
        self.vitalidade = raca.b_vitalidade + classe.b_vitalidade
        self.pontos_habilidade = 10
        
        self.arma = arma
        self.peitoral = peitoral

        self.esta_defendendo = False
        self.bonus_bloqueio = 1.5
            
        classe.passiva(self)
        raca.passiva(self)
        
        self.__vida = round(100 * (1 + self.vitalidade / 100))

    @property
    def classe(self):
        return self.__classe

    @property
    def raca(self):
        return self.__raca
    
    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, valor):
        self.__vida = valor
    
    @abstractmethod
    def atacar(self):
        pass

    @abstractmethod
    def atribuir_pontos(self):
        pass
    
    def comecar_turno(self):
        if self.esta_defendendo:
            self.esta_defendendo = False
            
        for h in self.habilidades:
            h.reduzir_cooldown()
            
    def bloquear(self):
        self.esta_defendendo = True

    def defesa_atual(self):
        if self.esta_defendendo:
            return round(self.peitoral.defesa * self.bonus_bloqueio)
        return self.peitoral.defesa
    
    def receber_dano(self, dano):
        if self.__vida == 0:
            print(f"{self.__nome} já morreu...")
            return False
        else:
            self.__vida -= dano
            if self.__vida < 0:
                self.__vida = 0
                print(f"{self.__nome} morreu...")
                return False
        return True

    def receber_cura(self, cura):
        self.__vida += round(cura)
        if self.__vida > 100 * (1 + (self.vitalidade / 100)):
            self.__vida = 100 * (1 + (self.vitalidade / 100))
    
    def aprender_habilidade(self, habilidade):
        self.habilidades.append(habilidade)
    
    def usar_habilidade(self, habilidade, inimigo = None):
        habilidade_encontrada = None
        for h in self.habilidades:
            if h.nome.lower() == habilidade.nome.lower():
                habilidade_encontrada = h
                break
    
        if not habilidade_encontrada:
            print(f"{self.__nome} não conhece a habilidade {habilidade.nome}.")
            return False
        
        if habilidade_encontrada.pode_usar(self):
            if inimigo:
                habilidade_encontrada.executar(self, inimigo)
            else:
                habilidade_encontrada.executar(self)
            return True
        else:
            print(f"{self.__nome} não pode usar {habilidade.nome} agora.")
            return False
    
    def mostrar_habilidade(self, habilidade):
        for h in self.habilidades:
            if h.cooldown > 0:
                print(f"- {h.nome}: Em recarga ({h.cooldown} turnos restantes)")
            else:
                print(f"- {h.nome}: Disponível")    
                  
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

class Item(ABC):
    def __init__(self, nome):
        self.nome = nome

class Habilidade(ABC):
    def __init__(self, nome, custo_mana = 0, tipo = None):
        self.__nome = nome
        self.cooldown = 0
        #self.duracao = 0
        self.custo_mana = custo_mana
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
        self.inventario = []
        
    def atacar(self, inimigo):
        inimigo.receber_dano(self.arma.dano)
    
    # Passivel de sofrer alterações
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
        
        # Ou
        
        ''''
        def atribuir_pontos(self):
        while self.pontos_habilidade > 0:
            print(f"\nPontos de habilidade restantes: {self.pontos_habilidade}")
            print("Escolha uma das opções para atribuir pontos:")
            print("1 - Força")
            print("2 - Agilidade")
            print("3 - Inteligência")
            print("4 - Vitalidade")
            
            escolha = input("Digite o número da opção desejada: ")
            quantidade = input("Digite a quantidade de pontos que deseja atribuir: ")
            if not quantidade.isdigit() or int(quantidade) <= 0 or int(quantidade) > self.pontos_habilidade:
                print("Quantidade inválida. Tente novamente.")
                continue
            
            match escolha:
                case "1":
                    self.forca += int(quantidade)
                    self.pontos_habilidade -= int(quantidade)
                    print(f"{quantidade} pontos atribuídos a Força.")
                case "2":
                    self.agilidade += int(quantidade)
                    self.pontos_habilidade -= int(quantidade)
                    print(f"{quantidade} pontos atribuídos a Agilidade.")
                case "3":
                    self.inteligencia += int(quantidade)
                    self.pontos_habilidade -= int(quantidade)
                    print(f"{quantidade} pontos atribuídos a Inteligência.")
                case "4":
                    self.vitalidade += int(quantidade)
                    self.pontos_habilidade -= int(quantidade)
                    print(f"{quantidade} pontos atribuídos a Vitalidade.")
                case _:
                    print("Opção inválida. Tente novamente.")
        '''
        
# CLASSES

class Guerreiro(Classe_Raca):
    def __init__(self):
        super().__init__(b_forca = 5, b_agilidade = -1, b_inteligencia = -2, b_vitalidade = 8)
        
    def passiva(self, personagem):
        personagem.vitalidade = round(personagem.vitalidade * 1.5)
        personagem.aprender_habilidade(Esmagador())
        
# RAÇA

class Humano(Classe_Raca):
    def __init__(self):
        super().__init__(b_forca = 1, b_agilidade = 1, b_inteligencia = 1, b_vitalidade = 1)
        
    def passiva(self, personagem):
        personagem.pontos_habilidade += 10
        personagem.aprender_habilidade(Adrenalina())

# TÉCNICAS

class Adrenalina(Habilidade):
    def __init__(self):
        super().__init__(nome = "Adrenalina", tipo = "Técnica")

    def executar(self, personagem):
        # FAZER A LÓGICA DELE PERDER O BUFF DE FORÇA E VITALIDADE EM 2 RODADAS
        personagem.forca = round(personagem.forca * 1.2)
        personagem.vitalidade = round(personagem.vitalidade * 1.2)
        #self.duracao = 2
        self.cooldown = 3
        
class Esmagador(Habilidade):
    def __init__(self):
        super().__init__(nome = "Esmagador", tipo = "Técnica")

    def executar(self, personagem, inimigo):
        dano = round(personagem.arma.dano * 2 * (1 + personagem.forca / 100))
        inimigo.receber_dano(dano)
        self.cooldown = 2

class Primeiros_socorros(Habilidade):
    def __init__(self):
        super().__init__(nome = "Primeiro Socorros", tipo = "Técnica")

    def executar(self, personagem):
        cura = 20 * (1 + personagem.vitalidade / 100)
        personagem.receber_cura(cura)
        self.cooldown = 3
        
# MAGIAS

class Cura_basica(Habilidade):
    def __init__(self):
        super().__init__(nome = "Cura Básica", custo_mana = 20, tipo = "Magia")

    def executar(self, personagem):
        cura = 35 * (1 + personagem.inteligencia / 100)
        personagem.receber_cura(cura)
        personagem.mana -= self.custo_mana
        
class Cura_avancada(Habilidade):
    def __init__(self):
        super().__init__(nome = "Cura Avançada", custo_mana = 40, tipo = "Magia")

    def executar(self, personagem):
        cura = 60 * (1 + personagem.inteligencia / 100)
        personagem.receber_cura(cura)
        personagem.mana -= self.custo_mana

class Bola_de_fogo(Habilidade):
    def __init__(self):
        super().__init__(nome = "Bola de Fogo", custo_mana = 25, tipo = "Magia")

    def executar(self, personagem, inimigo):
        dano = 35 * (1 + personagem.inteligencia / 100)
        inimigo.receber_dano(dano)
        personagem.mana -= self.custo_mana

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
    dano : int
    raridade : Raridade
    
    def __init__(self, nome, dano, raridade):
        super().__init__(nome)
        self.raridade = raridade
        self.dano = round(dano * raridade.multiplicador)

class Armadura(Item):
    defesa : int
    raridade : Raridade
    
    def __init__(self, nome, defesa, raridade):
        super().__init__(nome)
        self.raridade = raridade
        self.defesa = round(defesa * raridade.multiplicador)

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
        
    # Implementar método para listar os itens presentes no inventário.
    # Implementar equipar e desequipar itens
    