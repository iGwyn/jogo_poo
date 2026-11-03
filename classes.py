from __future__ import annotations
from abc import ABC, abstractmethod

# FAZER SISTEMA DE CONTAGEM DE QUANTAS POR QUANTAS LUTAS O PERSONAGEM PASSOU, JUNTO COM CONTAGEM DE ROUNDS DE CADA COMBATE

# URGENTE PARA FAZER
# SEPARAR HABILIDADE EM TECNICA E MAGIA, MODIFICANDO OS METODOS PARA CABER AO NOVO FORMATO SE NECESSARIO - teoricamente feito, testar
# TORNAR RACA, CLASSE, E TECNICA NO ESTILO DE MAGIA COM DICIONARIO, E VER SE ESSA FORMA DE FAZER É APLICÁVEL AOS ITENS E CONSUMIVEIS
# DESENVOLVER UMA LOGICA PARA BUFF E DEBUFF
# FAZER OS DICIONARIOS EM OUTRO ARQUIVO.PY
# TENTAR TORNAR A POCAO_DE_CURA UMA POCAO QUE SERVE TANTO PARA VIDA QUANTO MANA 

# DECIDIR SE VAI USAR FLOAT NOS ATRIBUTOS/VIDA OU NÃO, CASO DECIDA USAR É POSSÍVEL FAZER UM LAST STAND ONDE SE FICAR COM VIDA < 1
# VOCÊ TEM 50% DE CHANCE DE MATAR O INIMIGO AUTOMATICAMENTE | SE FOR DECIDIDO NÃO USAR FLOAT, DA PRA FAZER COM 1HP

# TODA VEZ QUE VOCE CHEGA PERTO DA MORTE TEM UMA % DE DESBLOQUEAR FURIA
# CHANCE DE RECEBER ITEM QUE DESBLOQUEIA MANA PARA O JOGADOR

# CLASSES ABSTRATAS

# Talvez um atributo carisma, pois o loot após batalha vai ser aleatorizado já que a platéia que vai
# dar os itens ou não (chance de ganhar algo ou de n ganhar, e afetar a qualidade do item caso ganhe)
class Personagem(ABC):
    __nome : str
    __raca : Raca
    __classe : Classe
    __vida : int
    tecnica : Tecnica
    magia : Magia
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
        self.tecnicas = []
        # Talvez inserir a lista de magias no inicializador de mana
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
        
        valor_vida = round(100 * (1 + self.vitalidade / 100))
        self.__vida = valor_vida
        self.__vida_maxima = valor_vida

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
    
    @vida.setter
    def vida(self, valor):
        self.__vida = valor
    
    def atacar(self, inimigo):
        inimigo.receber_dano(self.arma.dano)
        if hasattr(self, 'furia'):
            self.gerenciar_recurso("atacar", 15)

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
        if self.esta_defendendo:
            return round(self.peitoral.defesa * self.bonus_bloqueio)
        return self.peitoral.defesa
    
    def receber_dano(self, dano):
        if self.__vida == 0:
            print(f"{self.__nome} já morreu...")
            return False
        else:
            self.__vida -= dano
            if hasattr(self, 'furia'):
                self.gerenciar_recurso("receber_dano", 10)
            if self.__vida < 0:
                self.__vida = 0
                print(f"{self.__nome} morreu...")
                return False
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
    
    # Mover esse para gladiador após os testes, já q não precisamos saber o cooldown dos NPCs | Ou deixar aqui 
    def mostrar_habilidade(self):
        if self.tecnicas:
            print("Técnicas")
            for t in self.tecnicas:
                # Mostrar quando está disponivel
                if t.cooldown > 0:
                    print(f"{t.nome} está em cooldown ({t.cooldown} turnos restantes)")
                    
        if self.magias:
            print("Magias")
            for m in self.magias:
                if m.cooldown > 0:
                    print(f"{m.nome} está em cooldown ({m.cooldown} turnos restantes)") 
                
    def gerenciar_recurso(self, evento, valor = 0):
        if hasattr(self, 'furia'):
            if evento in ["atacar", "receber_dano"]:
                self.furia = min(self.furia_maxima, self.furia + valor)
                print(f"{self.__nome} gerou fúria! Atual: {self.furia}")

        if hasattr(self, 'mana'):
            if evento == "proximo_turno":
                taxa_reg = 15 * (1 + self.inteligencia / 50)
                reg_mana = round(self.mana + taxa_reg)
                self.mana = min(self.mana_maxima, reg_mana)
                print(f"{self.__nome} regenerou mana. Atual: {self.mana}")  
                  
    """
    def fim_de_turno(self):
        self.duracao -= 1
        pass"""

class Raca(ABC):
    def __init__(self, b_forca, b_agilidade, b_inteligencia, b_vitalidade):
        self.b_forca = b_forca
        self.b_agilidade = b_agilidade
        self.b_inteligencia = b_inteligencia
        self.b_vitalidade = b_vitalidade

    @abstractmethod
    def passiva(self, personagem = None, inimigo = None):
        pass

class Classe(ABC):
    recurso : str # Furia ou Mana
    
    def __init__(self, b_forca, b_agilidade, b_inteligencia, b_vitalidade, recurso):
        self.b_forca = b_forca
        self.b_agilidade = b_agilidade
        self.b_inteligencia = b_inteligencia
        self.b_vitalidade = b_vitalidade
        self.recurso = recurso

    @abstractmethod
    def passiva(self, personagem = None, inimigo = None):
        pass

class Item(ABC):
    def __init__(self, nome, tipo = None):
        self.nome = nome
        self.tipo = tipo

class Consumivel(ABC):
    @abstractmethod
    def usar(self, personagem):
        pass

class Equipavel(ABC):
    @abstractmethod
    def equipar(self, personagem):
        pass
    
class Habilidade(ABC):
    def __init__(self, nome, custo = 0, tipo = str):
        self.__nome = nome
        self.cooldown = 0
        #self.duracao = 0
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
                print("Esse tipo de habilidade n existe.")
                return False
                
            return recurso >= self.custo
                        
        return True

# PLAYER/NPC

class Gladiador(Personagem):
    inventario : Inventario
    
    def __init__(self, nome, raca, classe, arma = None, peitoral = None):
        super().__init__(nome, raca, classe, arma, peitoral)
        self.inventario = []
    
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

# CLASSES

class Guerreiro(Classe):
    def __init__(self):
        super().__init__(b_forca = 5, b_agilidade = -1, b_inteligencia = -2, b_vitalidade = 8, recurso = "Fúria")
        
    def passiva(self, personagem):
        personagem.vitalidade = round(personagem.vitalidade * 1.5)
        personagem.aprender_habilidade(Esmagador())
        
# RAÇA

class Humano(Raca):
    def __init__(self):
        super().__init__(b_forca = 1, b_agilidade = 1, b_inteligencia = 1, b_vitalidade = 1)
        
    def passiva(self, personagem):
        personagem.pontos_habilidade += 10
        personagem.aprender_habilidade(Adrenalina())

# TÉCNICAS

class Tecnica(Habilidade):
    efeito_funcao : str # Função
    
    def __init__(self, nome, efeito_funcao, poder_da_tecnica, custo):
        super().__init__(nome, custo, tipo = "Técnica")
        self.poder = poder_da_tecnica
        self.efeito_funcao = efeito_funcao
        
    def executar(self, personagem, inimigo = None):
        personagem.furia -= self.custo
        
        self.efeito_funcao(personagem, self.poder, inimigo)
                    
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

class Magia(Habilidade):
    efeito_funcao : 'Função'
    
    def __init__(self, nome, efeito_funcao, poder_do_feitico, custo):
        super().__init__(nome, custo, tipo = "Magia")
        self.poder = poder_do_feitico
        self.efeito_funcao = efeito_funcao
        
    def executar(self, personagem, inimigo = None):
        personagem.mana -= self.custo
        
        self.efeito_funcao(personagem, self.poder, inimigo)

def logica_dano_magico(personagem, poder, inimigo):
    dano = round(poder * (1 + personagem.inteligencia / 100))
    inimigo.receber_dano(dano)

def logica_cura(personagem, poder, inimigo = None):
    cura = round(poder * (1 + personagem.inteligencia / 100))
    personagem.receber_cura(cura)

def logica_drenar_vida(personagem, poder, inimigo):
    dano = round(poder * (1 + personagem.inteligencia / 100))
    inimigo.receber_dano(dano)
    personagem.receber_cura(dano / 2) 

def logica_buff_defesa(personagem, poder, inimigo = None):
    # Vai mudar para entrar na lógica de buff quando for implementada
    personagem.defesa += poder

MAGIAS = {
    "bola_de_fogo": Magia(
        nome = "Bola de Fogo", 
        custo = 25,
        poder_do_feitico = 35, 
        efeito_funcao = logica_dano_magico
        ),
    "cura_basica": Magia(
        nome = "Cura Básica",
        custo = 20,
        poder_do_feitico = 35,
        efeito_funcao = logica_cura
    ),
    "cura_avancada": Magia(
        nome = "Cura Avançada",
        custo = 40,
        poder_do_feitico = 70,
        efeito_funcao = logica_cura
    ),
    "drenar_vida": Magia(
        nome = "Drenar Vida", 
        custo = 30,
        poder_do_feitico = 25, 
        efeito_funcao = logica_drenar_vida
    ),
    "escudo_arcano": Magia(
        nome = "Escudo Arcano", 
        custo = 15,
        poder_do_feitico = 15, 
        efeito_funcao = logica_buff_defesa
    ),
}

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
        super().__init__(nome, tipo = "Arma")
        self.raridade = raridade
        self.dano = round(dano * raridade.multiplicador)

class Armadura(Item):
    defesa : int
    raridade : Raridade
    
    def __init__(self, nome, defesa, raridade):
        super().__init__(nome, tipo = "Armadura")
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
    
# Fazer igual com as Habilidades para poder adicionar um dicionario caso queira mais tipos de poção
class Pocao(Item, Consumivel):
    def __init__(self, nome, valor, tipo_efeito):
        super().__init__(nome, tipo = "Poção")
        self.valor = valor
        self.tipo_efeito = tipo_efeito

    def usar(self, personagem):
        personagem.tipo_efeito(personagem)
            
def pocao_de_cura(personagem):
    personagem.receber_cura(self.valor)
    print(f"{personagem.nome} bebeu {self.nome}.")        


    