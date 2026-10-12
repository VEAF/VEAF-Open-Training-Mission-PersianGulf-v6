"""Lot 04 : camp de chaque aérodrome et slots dynamiques, puis les deux FARP de la v5 (Berlin, London).

Bleu avec slots : 9 terrains (lib.BLUE_SLOTS). Bleu sans slots : les grands aéroports civils.
Rouge avec slots : Bandar Abbas (avancée), Lar et Shiraz (arrière). Tous les autres terrains iraniens : rouges
sans slots. Neutre : Quasoura (sud d'Oman), hors du théâtre.
FARP Berlin (zone d'entraînement hélicoptères, ouest d'Abu Dhabi) et FARP London (près de Ras Al Khaimah, à
40 nm du front) : positions de la v5, contrôlées sur la terre ferme (grille DCS).
"""
from lib import BLUE, BLUE_NO_SLOTS, BLUE_SLOTS, NEUTRAL, RED_NO_SLOTS, RED_SLOTS, Batch, land, xy

FARPS = [("FARP Berlin", (-217391, -232497), 127.5, 1), ("FARP London", (-66742, -17757), 128.5, 2)]

if __name__ == "__main__":
    b = Batch()
    for n in BLUE_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="blue")
    for n in BLUE_NO_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="blue", dynamic_spawn=False)
    for n in RED_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="red")
    for n in RED_NO_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="red", dynamic_spawn=False)
    for n in NEUTRAL:
        b.act("set_airbase_coalition", name=n, coalition="neutral", dynamic_spawn=False)
    for name, p, f, cs in FARPS:
        land(p, name, margin=200)
        b.act("add_farp", name=name, position=xy(p), **BLUE, frequency_mhz=f, callsign_id=cs)
    b.save("04-bases.json")
