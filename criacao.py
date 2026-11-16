from core import Gladiador, NPC
from classes_racas import raca, classe
from itens import Arma, RARIDADES, Armadura, consumivel

def criar_jogador():
    jogador = Gladiador("Maximus", raca("humano"), classe("guerreiro"),
                        arma = Arma("Gládio", 14, RARIDADES["Comum"]))
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    jogador.inventario.adicionar_item(consumivel("pocao_de_cura"))
    jogador.inventario.adicionar_item(Armadura("Peitoral de Bronze", 3, RARIDADES["Comum"]))
    jogador.inventario.adicionar_item(Arma("Espada Rara", 14, RARIDADES["Raro"]))
    return jogador

# Fazer aleatorização de inimigo e equipamentos

def criar_inimigo():
    return NPC("Brutus", raca("humano"), classe("guerreiro"),
                     arma = Arma("Machado", 12, RARIDADES["Comum"]))