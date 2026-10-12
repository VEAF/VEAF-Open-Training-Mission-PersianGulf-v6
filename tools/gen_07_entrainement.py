"""Lot 07 : les 3 familles d'entraînement × 3 niveaux (facile ⊂ moyen ⊂ difficile, clé `includes:`).

H — hélicoptères, à 6 km à l'ouest du FARP Berlin (FARP de la v5), 29 nm de Liwa, 33 nm d'Al Dhafra.
    Le difficile s'arrête au SA-13 et aux SA-18, posés à l'ouest du centre : le FARP reste hors de portée.
A — attaque, désert au nord de Tarif, à 23 nm de Liwa et 31 nm d'Al Dhafra, à 122 nm du front.
    Le champ de tir de la v5 (côte à l'ouest de Berlin) est en sebkha au niveau de la mer : la grille DCS n'y
    distingue pas la terre de l'eau, donc champ de tir déplacé à l'intérieur des terres.
S — SEAD, désert au sud d'Al Dhafra (Al Qua'a), à 42 nm d'Al Dhafra. SA-11 au plus (27 nm) : Al Dhafra à
    42 nm, piste d'Overlord 1 à 46 nm, champ d'attaque à 39 nm. Pas de longue portée (décision du 01/10/2026).

Cibles inertes des niveaux faciles : groupes d'un véhicule nommés « …-Inert-… », rendus chauds, tir interdit
et sans dispersion par tools/inert_targets.py (aucune action MCP ne règle ROE ni dispersion).
"""
from lib import RED_IR, Batch, cmd_unit, position_text, spot, tankers_text, xy

H = (-217391, -238497)
A = (-250000, -215000)
S = (-285000, -150000)


def inert(zone_center, items, prefix):
    """Groupes d'un véhicule, en couronne autour du centre : (type, relèvement, distance)."""
    groups = []
    for i, (typ, brg, dist) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{prefix}{i}")
        groups.append({"name": f"Inert-{typ.split()[0]}-{i}", "position": xy(p), "keep_position": True,
                       "units": [{"type": typ, "count": 1}]})
    return groups


def fake(zone_center, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    groups = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{tagbase}-{i}")
        groups.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                       "units": [cmd_unit(alias + ", country iran", carrier, f"{tagbase}-{i}", extra)]})
    return groups


ZONES = [
    # ── H : hélicoptères ──
    ("combatZone_Berlin_Easy", H, 2500, "H1 Hélico Berlin — facile", "Entraînement hélicoptères", None,
     inert(H, [("T-72B", 0, 600), ("T-72B", 60, 700), ("BMP-2", 120, 500), ("BMP-2", 180, 800),
               ("BRDM-2", 240, 600), ("Ural-375", 300, 700), ("Ural-375", 330, 400)], "H1-"),
     "Champ de tir hélicoptères à 3 nm à l'ouest du FARP Berlin : cibles inertes (chars, blindés et camions "
     "immobiles, tir interdit)."),
    ("combatZone_Berlin_Medium", H, 2500, "H2 Hélico Berlin — moyen", "Entraînement hélicoptères",
     "combatZone_Berlin_Easy",
     fake(H, [("-zu23", "Ural-375 ZU-23", 30, 1200, '#spawngroup="H2AAA" #spawncount=2'),
              ("-zu23", "Ural-375 ZU-23", 150, 1100, '#spawngroup="H2AAA" #spawncount=2'),
              ("-zu23", "Ural-375 ZU-23", 270, 1300, '#spawngroup="H2AAA" #spawncount=2'),
              ("-shilka", "ZSU-23-4 Shilka", 210, 900, "#spawnchance=50")], "H2"),
     "Champ de tir hélicoptères de Berlin : de l'artillerie antiaérienne légère (ZU-23, parfois un Shilka) en "
     "plus des cibles du niveau facile."),
    ("combatZone_Berlin_Hard", H, 2500, "H3 Hélico Berlin — difficile", "Entraînement hélicoptères",
     "combatZone_Berlin_Medium",
     fake(H, [("-sa13", "Strela-10M3", 230, 1000, '#spawngroup="H3SR" #spawncount=1'),
              ("-sa13", "Strela-10M3", 300, 1000, '#spawngroup="H3SR" #spawncount=1'),
              ("-sa18", "SA-18 Igla manpad", 250, 1500, '#spawngroup="H3MP" #spawncount=1'),
              ("-sa18", "SA-18 Igla manpad", 200, 1400, '#spawngroup="H3MP" #spawncount=1')], "H3"),
     "Champ de tir hélicoptères de Berlin, avec une défense courte portée réaliste : un SA-13 et une équipe de "
     "lance-missiles portatifs SA-18, à guidage infrarouge."),
    # ── A : attaque ──
    ("combatZone_Tarif_Easy", A, 2500, "A1 Attaque Tarif — facile", "Entraînement attaque", None,
     inert(A, [("T-72B", 0, 700), ("T-72B", 40, 900), ("T-72B", 80, 600), ("BMP-2", 120, 800),
               ("BMP-2", 160, 500), ("BTR-80", 200, 700), ("BTR-80", 240, 900), ("Ural-375", 280, 600),
               ("Ural-375", 320, 800), ("KAMAZ Truck", 350, 400)], "A1-"),
     "Champ de tir air-sol au nord de Tarif, à 23 nm de Liwa : blindés et camions immobiles en tir interdit, "
     "dépôt de carburant et poste de commandement. Le drone Reaper 1 tourne au-dessus."),
    ("combatZone_Tarif_Medium", A, 2500, "A2 Attaque Tarif — moyen", "Entraînement attaque",
     "combatZone_Tarif_Easy",
     fake(A, [("-armor, defense 0", "T-72B", 220, 1300, ""),
              ("-zu23", "Ural-375 ZU-23", 60, 1500, '#spawngroup="A2AAA" #spawncount=1'),
              ("-zu23", "Ural-375 ZU-23", 300, 1400, '#spawngroup="A2AAA" #spawncount=1')], "A2"),
     "Champ de tir de Tarif : une compagnie blindée active et de l'artillerie antiaérienne légère en plus des "
     "cibles du niveau facile."),
    ("combatZone_Tarif_Hard", A, 2500, "A3 Attaque Tarif — difficile", "Entraînement attaque",
     "combatZone_Tarif_Medium",
     fake(A, [("-armor, defense 1", "T-72B", 260, 1600, ""),
              ("-sa13", "Strela-10M3", 200, 1200, '#spawngroup="A3SR" #spawncount=1'),
              ("-sa9", "Strela-1 9P31", 320, 1200, '#spawngroup="A3SR" #spawncount=1'),
              ("-shilka", "ZSU-23-4 Shilka", 250, 800, "")], "A3"),
     "Champ de tir de Tarif : un second groupe blindé et une défense courte portée à guidage infrarouge (SA-13 "
     "ou SA-9), avec un Shilka."),
    # ── S : SEAD ──
    ("combatZone_AlQua_Easy", S, 3000, "S1 SEAD Al Qua'a — facile", "Entraînement SEAD", None,
     fake(S, [("-sa6", "Kub 2P25 ln", 0, 0, '#spawngroup="S1MR" #spawncount=1'),
              ("-sa11", "SA-11 Buk LN 9A310M1", 90, 300, '#spawngroup="S1MR" #spawncount=1')], "S1"),
     "Site SEAD dans le désert d'Al Qua'a, au sud d'Al Dhafra : une batterie sol-air moyenne portée, SA-6 ou "
     "SA-11 tirée au sort."),
    ("combatZone_AlQua_Medium", S, 3000, "S2 SEAD Al Qua'a — moyen", "Entraînement SEAD",
     "combatZone_AlQua_Easy",
     fake(S, [("-sa15", "Tor 9A331", 45, 1500, '#spawngroup="S2SR" #spawncount=2'),
              ("-sa8", "Osa 9A33 ln", 165, 1500, '#spawngroup="S2SR" #spawncount=2'),
              ("-sa15", "Tor 9A331", 285, 1500, '#spawngroup="S2SR" #spawncount=2')], "S2"),
     "Site SEAD d'Al Qua'a : la batterie moyenne portée est protégée par une défense courte portée (SA-15, SA-8)."),
    ("combatZone_AlQua_Hard", S, 3000, "S3 SEAD Al Qua'a — difficile", "Entraînement SEAD",
     "combatZone_AlQua_Medium",
     fake(S, [("-ewr", "55G6 EWR", 120, 2200, "")], "S3"),
     "Site SEAD d'Al Qua'a en réseau Skynet : un radar d'alerte avancée guide les batteries, qui restent "
     "éteintes jusqu'au dernier moment."),
]

# Statiques du niveau facile attaque : ce qui ne vit pas (dépôt, poste de commandement)
A1_STATICS = [("Fuel tank", 100, 1100), ("Fuel tank", 110, 1200), (".Command Center", 20, 1300)]

if __name__ == "__main__":
    b = Batch()
    for zone, c, r, fname, menu, inc, groups, text in ZONES:
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": True,
              "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"}
        if inc:
            cz["includes"] = [inc]
        b.act("create_combat_zone", zone_name=zone, position=xy(c), radius=r, groups=groups, **RED_IR,
              category="vehicle", combat_zone=cz)
    for i, (typ, brg, dist) in enumerate(A1_STATICS, 1):
        p = spot(A, brg, dist, f"A1-static-{i}")
        b.act("add_group", **RED_IR, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
              position=xy(p), units=[{"type": typ}], for_combat_zone="combatZone_Tarif_Easy", keep_position=True)
    b.save("07-entrainement.json")
