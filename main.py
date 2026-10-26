from classes import *

if __name__ == "__main__":
    # ÁREA DE TESTE 51
    
    humano = Humano()
    guerreiro = Guerreiro()
    Player = Gladiador("Arthur", humano, guerreiro)
    NPC = Gladiador("Gilgamesh", humano, guerreiro)
    
    print(f"Arthur")
    print(f"Força antes: {Player.forca}")
    print(f"Vitalidade antes: {Player.vitalidade}")

    Player.usar_habilidade(Adrenalina())
    
    print(f"Força depois: {Player.forca}")
    print(f"Vitalidade depois: {Player.vitalidade}")

    print(f"\nGilgamesh")
    print(f"Força: {NPC.forca}")
    print(f"Vitalidade: {NPC.vitalidade}")

    Espada = Arma("Espada", 10, RARIDADES["Comum"])
    Player.arma = Espada
    
    print(f"\nVida de Gilgamesh antes do ataque: {NPC.vida}")
    Player.atacar(NPC)
    print(f"Vida de Gilgamesh depois do ataque: {NPC.vida}")
    
    print(f"\nTeste de cooldown da habilidade ativa:")
    print(f"\nVida de Gilgamesh antes do ataque especial: {NPC.vida}")
    Player.mostrar_habilidade(Esmagador)
    Player.usar_habilidade(Esmagador(), NPC)    
    print(f"Vida de Gilgamesh depois do ataque especial: {NPC.vida}")
    
    print("Testando a habilidade sem passar pelos turnos")
    Player.usar_habilidade(Esmagador(), NPC) 
    print(f"Vida de Gilgamesh depois do ataque especial sem passar pelo cooldown: {NPC.vida}")
    
    Player.mostrar_habilidade(Esmagador)
    print("Novo turno")
    Player.comecar_turno()
    Player.mostrar_habilidade(Esmagador)
    print("Novo turno")
    Player.comecar_turno()
    Player.mostrar_habilidade(Esmagador)
    
    Player.usar_habilidade(Esmagador(), NPC) 
    print(f"Vida de Gilgamesh depois do ataque: {NPC.vida}")
    
    NPC.aprender_habilidade(Cura_basica())
    
    NPC.mana = 100
    print(f"\nVida de Gilgamesh antes da magia: {NPC.vida}")
    print(f"Mana de Gilgamesh antes da magia: {NPC.mana}")
    NPC.usar_habilidade(Cura_basica())
    print(f"Vida de Gilgamesh depois da magia: {NPC.vida}")
    print(f"Mana de Gilgamesh depois da magia: {NPC.mana}")
        
    for i, habilidade in enumerate(Player.habilidades):
        if habilidade.tipo == "Técnica":
            print(f"{i + 1} - {habilidade.nome}")
            
    for i, habilidade in enumerate(NPC.habilidades):
        if habilidade.tipo == "Magia":
            print(f"{i + 1} - {habilidade.nome}")

    for i, habilidade in enumerate(Player.habilidades):
        if habilidade.tipo == "Magia":
            print(f"{i + 1} - {habilidade.nome}")

    Player.aprender_habilidade(Cura_basica())
    
    for i, habilidade in enumerate(Player.habilidades):
        if habilidade.tipo == "Magia":
            print(f"{i + 1} - {habilidade.nome}")
    
    print(f"\nAtribuindo pontos de habilidade:")
    print(f"Pontos de habilidade disponíveis: {Player.pontos_habilidade}")
    print(f"Força: {Player.forca}")
    print(f"Vitalidade: {Player.vitalidade}")
    Player.atribuir_pontos(forca = 5, vitalidade = 10)
    print(f"Força após atribuição: {Player.forca}")
    print(f"Vitalidade após atribuição: {Player.vitalidade}")
    print(f"Vida Jogador pós vitalidade: {Player.vida}") 
    Player.atribuir_pontos(agilidade = 5, inteligencia = 5)
    print(f"Agilidade após atribuição: {Player.agilidade}")
    print(f"Inteligência após atribuição: {Player.inteligencia}")
    print(f"Pontos de habilidade disponíveis: {Player.pontos_habilidade}") 