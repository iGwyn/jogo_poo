from classes import *

if __name__ == "__main__":
    # ÁREA DE TESTE
    
    humano = Humano()
    guerreiro = Guerreiro()
    Player = Gladiador("Arthur", humano, guerreiro)
    NPC = Gladiador("Gilgamesh", humano, guerreiro)
    
    Espada = Arma("Espada", 10, RARIDADES["Comum"])
    Player.arma = Espada
    
    print(f'Arthur')
    print("Força antes:", Player.forca)
    print("Vitalidade antes:", Player.vitalidade)

    Player.usar_raca()
    
    print(f'Força depois: {Player.forca:.2f}')
    print(f'Vitalidade depois: {Player.vitalidade:.2f}')

    print(f"\nGilgamesh")
    print(f'Força: {NPC.forca:.2f}')
    print(f'Vitalidade: {NPC.vitalidade:.2f}')

    print(f"\nVida de Gilgamesh antes do ataque: {NPC.vida:.2f}")
    Player.atacar(NPC)
    print(f"Vida de Gilgamesh depois do ataque: {NPC.vida:.2f}")
    
    print(f"\nVida de Gilgamesh antes do ataque: {NPC.vida:.2f}")
    Player.usar_classe(NPC)
    Player.classe.habilidade_ativa.reduzir_cooldown()
    print(f"Cooldown da habilidade: {Player.classe.habilidade_ativa.cooldown}")
    Player.classe.habilidade_ativa.reduzir_cooldown()
    print(f"Cooldown da habilidade: {Player.classe.habilidade_ativa.cooldown}")
    
    print(f"Vida de Gilgamesh depois do ataque: {NPC.vida:.2f}")

    Player.usar_classe(NPC)
    print(f"Vida de Gilgamesh depois do ataque: {NPC.vida:.2f}")
    
