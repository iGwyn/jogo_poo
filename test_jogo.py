import pytest
from core import Gladiador, NPC
from classes_racas import raca, classe
from itens import Arma, Armadura, consumivel, RARIDADES
from combate import Combate
from habilidades import tecnica, magia

def test_criacao_personagem_e_atributos():
    """Testa se o gladiador é criado corretamente com raça, classe e atributos base."""
    j = Gladiador("Maximus", raca("humano"), classe("guerreiro"))
    
    assert j.nome == "Maximus"
    assert j.vida > 0
    # Guerreiro usa fúria
    assert hasattr(j, "furia")
    # Passiva de humano/guerreiro adiciona técnicas
    assert len(j.tecnicas) > 0

def test_inventario_adicionar_e_remover():
    """Testa o gerenciamento de itens no inventário."""
    j = Gladiador("Maximus", raca("humano"), classe("guerreiro"))
    
    # Adiciona poção
    pocao = consumivel("pocao_de_cura")
    adicionou = j.inventario.adicionar_item(pocao)
    assert adicionou is True
    
    # Verifica o item no slot 1
    item_verificado = j.inventario.verificar_item(1)
    assert item_verificado.nome == "Poção de Cura"
    
    # Remove o item
    removido = j.inventario.remover_item(1)
    assert removido.nome == "Poção de Cura"
        
    # Confirma que o slot ficou vazio (retorna None)
    item_vazio = j.inventario.verificar_item(1)
    assert item_vazio is None

def test_equipar_arma_e_armadura():
    """Testa se equipar itens altera os atributos do personagem."""
    j = Gladiador("Maximus", raca("humano"), classe("guerreiro"))
    
    espada = Arma("Espada Rara", 14, RARIDADES["Raro"])
    espada.equipar(j)
    assert j.arma.nome == "Espada Rara"
    # Multiplicador do item raro
    assert j.arma.dano > 14
    
    peitoral = Armadura("Peitoral de Bronze", 3, RARIDADES["Comum"])
    peitoral.equipar(j)
    assert j.peitoral.nome == "Peitoral de Bronze"

def test_fluxo_combate_vitoria():
    """Testa a inicialização e o fluxo básico de um combate até a vitória."""
    j = Gladiador("Maximus", raca("humano"), classe("guerreiro"), arma = Arma("Gládio", 50, RARIDADES["Comum"]))
    i = NPC("Alvo de Teste", raca("humano"), classe("guerreiro"))
    
    i.vida = 10 
    
    combate = Combate(j, i)
    assert combate.estado == Combate.TURNO_JOGADOR
    assert not combate.terminou
    
    # Jogador executa um ataque letal
    combate.executar_acao_jogador(("atacar",), 0)
    
    # Verifica se o combate entrou no estado de vitória
    assert combate.estado == Combate.VITORIA
    assert combate.terminou is True