from classes import *

if __name__ == "__main__":
    # ÁREA DE TESTE 51
    
    humano = Humano()
    guerreiro = Guerreiro()
    Player = Gladiador("Arthur", humano, guerreiro)
    NPC = Gladiador("Gilgamesh", humano, guerreiro)
    
    print(f"{Player.nome}")
    print(f"Força antes: {Player.forca}")
    print(f"Vitalidade antes: {Player.vitalidade}")

    Player.usar_habilidade(Adrenalina())
    
    print(f"Força depois: {Player.forca}")
    print(f"Vitalidade depois: {Player.vitalidade}")

    print(f"\n{NPC.nome}")
    print(f"Força: {NPC.forca}")
    print(f"Vitalidade: {NPC.vitalidade}")

    Espada = Arma("Espada", 10, RARIDADES["Comum"])
    Player.arma = Espada
    
    print(f"\nVida de {NPC.nome} antes do ataque: {NPC.vida}")
    Player.atacar(NPC)
    Player.atacar(NPC)
    print(f"Vida de {NPC.nome} depois do ataque: {NPC.vida}")
    
    print(f"\nTeste de cooldown da habilidade ativa:")
    print(f"\nVida de {NPC.nome} antes do ataque especial: {NPC.vida}")
    Player.mostrar_habilidade()
    Player.usar_habilidade(Esmagador(), NPC)    
    print(f"Vida de {NPC.nome} depois do ataque especial: {NPC.vida}")
    
    print("Testando a habilidade sem passar pelos turnos")
    Player.usar_habilidade(Esmagador(), NPC) 
    print(f"Vida de {NPC.nome} depois do ataque especial sem passar pelo cooldown: {NPC.vida}")
    
    Player.mostrar_habilidade()
    print("Novo turno")
    Player.comecar_turno()
    Player.mostrar_habilidade()
    print("Novo turno")
    Player.comecar_turno()
    Player.mostrar_habilidade()
    
    Player.usar_habilidade(Esmagador(), NPC) 
    print(f"Vida de Gilgamesh depois do ataque: {NPC.vida}")
    
    print("\nTeste de Magia")
    
    NPC.mana = 0
    NPC.mana_maxima = 100
    print(f"{NPC.nome} Mana: {NPC.mana}")
    NPC.comecar_turno()
    NPC.comecar_turno()
    NPC.comecar_turno()
    
    NPC.aprender_habilidade(MAGIAS["cura_basica"])
    
    print(f"\nVida de {NPC.nome} antes da magia: {NPC.vida}")
    print(f"Mana de {NPC.nome} antes da magia: {NPC.mana}")
    NPC.usar_habilidade(MAGIAS["cura_basica"])
    print(f"Vida de {NPC.nome} depois da magia: {NPC.vida}")
    print(f"Mana de {NPC.nome} depois da magia: {NPC.mana}")
    
    print(f"\nTécnicas do {Player.nome}")
    for i, tecnica in enumerate(Player.tecnicas):
        print(f"{i + 1} - {tecnica.nome}")
    
    print(f"Magias do {Player.nome}")
    for i, magia in enumerate(Player.magias):
        print(f"{i + 1} - {magia.nome}")
    
    print(f"\nTécnicas do {NPC.nome}")
    for i, tecnica in enumerate(NPC.tecnicas):
        print(f"{i + 1} - {tecnica.nome}")
    
    print(f"Magias do {NPC.nome}")
    for i, magia in enumerate(NPC.magias):
        print(f"{i + 1} - {magia.nome}")

    print(f"\nMagias do {Player.nome} após aprender Cura Básica")
    Player.aprender_habilidade(MAGIAS["cura_basica"])
    for i, magia in enumerate(Player.magias):
            print(f"{i + 1} - {magia.nome}")
    
    print(f"\nAtribuindo pontos de habilidade:")
    print(f"Pontos de habilidade disponíveis: {Player.pontos_habilidade}")
    print(f"Força: {Player.forca}")
    print(f"Vitalidade: {Player.vitalidade}")
    Player.atribuir_pontos(forca = 5, vitalidade = 10)
    print(f"Força após atribuição: {Player.forca}")
    print(f"Vitalidade após atribuição: {Player.vitalidade}")
    print(f"Vida Jogador pós vitalidade: {Player.vida}") 
    print(f"Pontos de habilidade disponíveis: {Player.pontos_habilidade}") 
    
    print("\nAtribuindo pontos de habilidade:")
    Player.atribuir_pontos(agilidade = 5, inteligencia = 5)
    print(f"Agilidade após atribuição: {Player.agilidade}")
    print(f"Inteligência após atribuição: {Player.inteligencia}")
    print(f"Pontos de habilidade disponíveis: {Player.pontos_habilidade}") 
    
    print(f"\nFúria: {Player.furia}")
    