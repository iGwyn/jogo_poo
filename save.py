import json
import os
from core import Gladiador, NPC
from classes_racas import raca, classe
from itens import Arma, Armadura, Consumivel, arma, armadura, consumivel
from habilidades import tecnica, magia
from combate import Combate


def _desmontar_item(item):
    if item is None:
        return None
    if isinstance(item, Arma):
        return {
            "tipo": "arma",
            "chave": item.chave,
        }
    if isinstance(item, Armadura):
        return {
            "tipo": "armadura",
            "chave": item.chave,
        }
    if isinstance(item, Consumivel):
        return {
            "tipo": "consumivel",
            "chave": item.chave,
        }
    return None


def _montar_item(dados):
    if dados is None:
        return None
    tipo = dados["tipo"]
    if tipo == "arma":
        return arma(dados["chave"])
    if tipo == "armadura":
        return armadura(dados["chave"])
    if tipo == "consumivel":
        return consumivel(dados["chave"])
    return None


def _desmontar_personagem(p):
    lista_tecnicas = []
    for t in p.tecnicas:
        lista_tecnicas.append({"chave": t.chave, "cooldown": t.cooldown})

    lista_magias = []
    for m in p.magias:
        lista_magias.append({"chave": m.chave, "cooldown": m.cooldown})
    
    dados = {
        "nome": p.nome,
        "raca": p.raca.chave,
        "classe": p.classe.chave,
        "vida": p.vida,
        "forca": p.forca,
        "agilidade": p.agilidade,
        "inteligencia": p.inteligencia,
        "vitalidade": p.vitalidade,
        "pontos_habilidade": p.pontos_habilidade,
        "esta_defendendo": p.esta_defendendo,
        "furia": getattr(p, "furia", None),
        "mana": getattr(p, "mana", None),
        "equipamento": {
            "arma": _desmontar_item(p.arma),
            "peitoral": _desmontar_item(p.peitoral),
            "capacete": _desmontar_item(p.capacete),
        },
        "tecnicas": lista_tecnicas,
        "magias": lista_magias,
    }

    if isinstance(p, Gladiador):
        inventario_desmontado = []
        for slot in p.inventario.slots:
            item_desmontado = _desmontar_item(slot)
            inventario_desmontado.append(item_desmontado)
        dados["inventario"] = inventario_desmontado
    elif isinstance(p, NPC):
        dados["chance_habilidade"] = p.chance_habilidade

    return dados


def _restaurar_estado_personagem(personagem, dados):
    personagem.forca = dados["forca"]
    personagem.agilidade = dados["agilidade"]
    personagem.inteligencia = dados["inteligencia"]
    personagem.vitalidade = dados["vitalidade"]
    personagem.pontos_habilidade = dados["pontos_habilidade"]
    personagem.esta_defendendo = dados.get("esta_defendendo", False)
    personagem.vida = dados["vida"]

    if dados["furia"] is not None:
        personagem.furia = dados["furia"]
    if dados["mana"] is not None:
        personagem.mana = dados["mana"]

    personagem.tecnicas.clear()
    for t_info in dados["tecnicas"]:
        t = tecnica(t_info["chave"])
        t.cooldown = t_info["cooldown"]
        personagem.aprender_habilidade(t)

    personagem.magias.clear()
    for m_info in dados["magias"]:
        m = magia(m_info["chave"])
        m.cooldown = m_info["cooldown"]
        personagem.aprender_habilidade(m)


def _montar_gladiador(dados):
    eq = dados["equipamento"]
    jogador = Gladiador(
        nome = dados["nome"],
        raca = raca(dados["raca"]),
        classe = classe(dados["classe"]),
        arma = _montar_item(eq["arma"]),
        peitoral = _montar_item(eq["peitoral"]),
        capacete = _montar_item(eq["capacete"]),
    )
    _restaurar_estado_personagem(jogador, dados)

    slots = []
    for slot_salvo in dados["inventario"]:
        item = _montar_item(slot_salvo)
        slots.append(item)
    jogador.inventario.slots = slots

    return jogador


def _montar_npc(dados):
    eq = dados["equipamento"]
    inimigo = NPC(
        nome = dados["nome"],
        raca = raca(dados["raca"]),
        classe = classe(dados["classe"]),
        arma = _montar_item(eq["arma"]),
        peitoral = _montar_item(eq["peitoral"]),
        chance_habilidade = dados.get("chance_habilidade", 0.5),
    )
    inimigo.capacete = _montar_item(eq["capacete"])
    _restaurar_estado_personagem(inimigo, dados)

    return inimigo

caminho_save = os.path.join(os.path.expanduser("~"), "Downloads", "save_jogo_POO.json")
def salvar_jogo(combate, inimigos_derrotados = 0, caminho = caminho_save):
    dados = {
        "inimigos_derrotados": inimigos_derrotados,
        "combate": {
            "turno": combate.turno,
            "estado": combate.estado,
            "mensagens": combate.mensagens[-10:],
        },
        "jogador": _desmontar_personagem(combate.jogador),
        "inimigo": _desmontar_personagem(combate.inimigo),
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_jogo(caminho = "save_jogo_POO.json"):
    if not os.path.exists(caminho):
        return None

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    jogador = _montar_gladiador(dados["jogador"])
    inimigo = _montar_npc(dados["inimigo"])

    combate = Combate(jogador, inimigo, iniciar_combate = False)
    dc = dados["combate"]
    combate.turno = dc["turno"]
    combate.estado = dc["estado"]
    combate.mensagens = dc.get("mensagens", [])

    if combate.estado == Combate.TURNO_INIMIGO:
        combate._proximo_evento = 0

    return combate, dados.get("inimigos_derrotados", 0)