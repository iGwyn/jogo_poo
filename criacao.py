from core import Gladiador, NPC
from classes_racas import raca, classe
from itens import arma, armadura, consumivel

# Cria o jogador já feito
def criar_jogador():
    jogador = Gladiador("Maximus", raca("humano"), classe("guerreiro"),
                        arma = arma("espada"))
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    jogador.inventario.adicionar_item(armadura("peitoral"))
    jogador.inventario.adicionar_item(armadura("peitoral_teste"))
    jogador.inventario.adicionar_item(armadura("capacete"))
    jogador.inventario.adicionar_item(armadura("capacete_teste"))
    jogador.inventario.adicionar_item(arma("excalibur"))
    # Essa poção não entra no inventário devido ao limite de slot
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    return jogador

# Fazer aleatorização de inimigo e equipamentos

# Cria o inimigo
def criar_inimigo():
    return NPC("Brutus", raca("humano"), classe("guerreiro"),
                     arma = arma("espada"))
