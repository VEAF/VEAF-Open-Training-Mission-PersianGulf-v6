"""Lot 08 : les vraies zones de combat, côté iranien (training: false), et le drone laser Reaper 2.

17 zones : front 3, SEAD 2, convois en mouvement 3, frappes dans la profondeur 4, OCA 2, antinavire 3.
Lieux réels (tools/places.json, geocode) ou repris de la v5 (Minab, Lavan, Weapon Factory, centrale de Lar,
champ pétrolier de Mubarek). Chaque position est ramenée sur la terre ferme (grille DCS) ; les navires
sont contrôlés en pleine mer. Portée des SAM de zone (aucune zone n'est active au démarrage) : SA-11 de Minab
(27 nm) à 75 nm de Khasab, Hawk de Lavan (24 nm) à 92 nm du Stennis, SA-2 de Jask (23 nm) à 49 nm de la piste
d'Arco 2 : check_portees.py le mesure. Reaper 2 tourne sur Bandar Lengeh, zone sans SAM au-delà de 10 km.
"""
from lib import (AIRFIELDS, BLUE, PLACES, RED_IR, Batch, cmd_unit, land, off, position_text, sea, spot,
                 tankers_text, xy)

A = AIRFIELDS
P = PLACES
ZONES = []


def g_fake(c, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    out = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(c, brg, dist, f"{tagbase}-{i}")
        out.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                    "units": [cmd_unit(alias + ", country iran", carrier, f"{tagbase}-{i}", extra)]})
    return out


def g_native(c, name, brg, dist, units, route=None):
    p = spot(c, brg, dist, name)
    g = {"name": name, "position": xy(p), "keep_position": True, "units": units}
    if route:
        g["route"] = [xy(p)] + [xy(q) for q in route]
    return g


def s_items(c, items):
    """Statiques : (type, relèvement, distance)."""
    return [(typ, spot(c, brg, dist, typ)) for typ, brg, dist in items]


def zone(name, c, r, fname, menu, text, groups, statics=(), side=RED_IR, cat="vehicle", extra=()):
    ZONES.append((name, c, r, fname, menu, text, side, cat, groups, list(statics), list(extra)))


# ── Front ────────────────────────────────────────────────────────────────────
C = spot((76000, -28000), 0, 0, "Qeshm")
zone("combatZone_Qeshm", C, 2500, "Z01 Front — brigade IRGC de Qeshm", "Front",
     "La brigade des Gardiens de la révolution qui tient l'île de Qeshm et le détroit d'Ormuz : chars, blindés et "
     "lance-roquettes multiples en position. Détruire les blindés et l'artillerie ; défense SA-15 possible et "
     "artillerie antiaérienne. Sous la couverture lointaine du SA-10 au nord de Bandar Abbas.",
     g_fake(C, [("-armor, defense 2", "T-72B", 0, 800, ""), ("-armor, defense 1", "T-72B", 120, 900, ""),
                ("-sa15", "Tor 9A331", 240, 600, "#spawnchance=50"),
                ("-zu23", "Ural-375 ZU-23", 300, 1200, "")], "Z01")
     + [g_native(C, "Artillerie", 200, 1300, [{"type": "Grad-URAL", "count": 4}])],
     s_items(C, [(".Command Center", 60, 1500), ("Fuel tank", 70, 1700)]))

C = spot(P["Bandar Lengeh"], 0, 6000, "Bandar Lengeh")
zone("combatZone_BandarLengeh", C, 2500, "Z02 Front — défense côtière de Bandar Lengeh", "Front",
     "La brigade de défense côtière de Bandar Lengeh, face à Abu Musa et aux Tunb : blindés et artillerie. "
     "Défense courte portée seulement (SA-13, Shilka) : le drone Reaper 2 la désigne au laser.",
     g_fake(C, [("-armor, defense 1", "T-72B", 30, 800, ""), ("-armor, defense 0", "BMP-2", 150, 900, ""),
                ("-sa13", "Strela-10M3", 270, 700, ""), ("-shilka", "ZSU-23-4 Shilka", 90, 500, "")], "Z02")
     + [g_native(C, "Artillerie", 210, 1200, [{"type": "SAU Msta", "count": 3}])],
     s_items(C, [("Barracks 2", 330, 1300), ("Barracks 2", 340, 1500)]))

C = spot((109400, 86371), 0, 0, "Minab")
zone("combatZone_Minab", C, 1500, "Z03 Front — base IRGC de Minab", "Front",
     "La base des Gardiens de la révolution de Minab, à l'est de Bandar Abbas : casernes, dépôts, lance-roquettes "
     "Smerch. Défendue par une batterie SA-11, un SA-15 et des ZU-23 : traiter le SA-11 d'abord.",
     g_fake(C, [("-sa11", "SA-11 Buk LN 9A310M1", 300, 800, ""), ("-sa15", "Tor 9A331", 120, 500, ""),
                ("-zu23", "Ural-375 ZU-23", 0, 400, ""), ("-zu23", "Ural-375 ZU-23", 180, 400, "")], "Z03")
     + [g_native(C, "Smerch", 60, 600, [{"type": "Smerch", "count": 2}, {"type": "Ural-375", "count": 2}])],
     s_items(C, [("Barracks 2", 90, 300), ("Barracks 2", 100, 380), ("Fuel tank", 200, 300),
                 ("Fuel tank", 210, 350), ("Workshop A", 240, 250), ("TV tower", 20, 650)]))

# ── SEAD ─────────────────────────────────────────────────────────────────────
C = spot((75496, -294522), 0, 0, "Lavan")
zone("combatZone_Lavan", C, 1500, "Z04 SEAD — site Hawk de Lavan", "SEAD",
     "Le site Hawk de l'île de Lavan, à l'ouest du Golfe, couvert par un radar d'alerte avancée en réseau Skynet. "
     "Détruire le radar de poursuite et les lanceurs.",
     g_fake(C, [("-hawk", "Hawk ln", 0, 0, ""), ("-ewr", "55G6 EWR", 90, 900, ""),
                ("-zu23", "Ural-375 ZU-23", 200, 500, "")], "Z04"))

C = spot(P["Jask"], 0, 7000, "Jask")
zone("combatZone_Jask", C, 2000, "Z05 SEAD — site sol-air de Jask", "SEAD",
     "Le site sol-air qui protège la base navale de Jask, sur la mer d'Oman : une batterie SA-2 ou SA-3 tirée au "
     "sort, son radar d'alerte avancée et un Shilka.",
     g_fake(C, [("-sa2", "S_75M_Volhov", 0, 0, '#spawngroup="Z05MR" #spawncount=1'),
                ("-sa3", "5p73 s-125 ln", 60, 300, '#spawngroup="Z05MR" #spawncount=1'),
                ("-ewr", "55G6 EWR", 180, 1200, ""), ("-shilka", "ZSU-23-4 Shilka", 300, 500, "")], "Z05"))

# ── Convois en mouvement (un groupe natif, route sur route, AAA dans le groupe) ──
C = (112923, 38998)   # sur la route, relevé en jeu (fix_convoys_on_road.py)
zone("combatZone_ConvoiMinab", C, 1500, "Z06 Convoi — Bandar Abbas vers Minab", "Convois",
     "Un convoi logistique quitte Bandar Abbas par la route côtière de l'est vers la base de Minab. L'arrêter "
     "avant Minab ; il porte sa propre artillerie antiaérienne (ZU-23).",
     [g_native(C, "Convoi", 0, 0, [{"type": "BTR-80", "count": 1}, {"type": "Ural-375", "count": 4},
                                   {"type": "Ural-375 ZU-23", "count": 1}],
               route=[(113357, 50790), (108125, 83215)])])

C = (151653, -188603)   # sur la route, hors du sanctuaire rouge de Lar (12 km) ; fix_convoys_on_road.py
zone("combatZone_ConvoiLar", C, 1500, "Z07 Convoi — Lar vers Bandar Lengeh", "Convois",
     "Des renforts blindés descendent de Lar vers la côte par Bastak et Kong. Les arrêter avant la côte ; le "
     "convoi est escorté par un SA-13.",
     [g_native(C, "Convoi", 0, 0, [{"type": "T-72B", "count": 2}, {"type": "BMP-2", "count": 2},
                                   {"type": "Ural-375", "count": 2}, {"type": "Strela-10M3", "count": 1}],
               route=[(116151, -185532), (49830, -129525)])])

C = (-47175, 152376)   # sur la route, relevé en jeu (fix_convoys_on_road.py)
zone("combatZone_ConvoiJask", C, 1500, "Z08 Convoi — Jask vers Sirik", "Convois",
     "Un convoi de carburant remonte la côte de la mer d'Oman, de Jask vers Sirik et Minab. Le détruire avant "
     "Sirik ; il porte sa propre artillerie antiaérienne.",
     [g_native(C, "Convoi", 0, 0, [{"type": "BTR-80", "count": 1}, {"type": "ATZ-10", "count": 3},
                                   {"type": "Ural-375 ZU-23", "count": 1}],
               route=[(38073, 85845), (69295, 85362)])])

# ── Frappes dans la profondeur ───────────────────────────────────────────────
C = spot((324196, -86766), 0, 0, "Weapon Factory")
zone("combatZone_WeaponFactory", C, 1200, "Z09 Frappe — usine d'armement de Sirjan", "Frappes en profondeur",
     "L'usine d'armement de la région de Sirjan, loin dans les terres : ateliers, hangars, réservoirs chimiques. "
     "Tout détruire ; défense SA-6 et ZU-23. Long trajet : prévoir le ravitaillement.",
     g_fake(C, [("-sa6", "Kub 2P25 ln", 300, 700, ""), ("-zu23", "Ural-375 ZU-23", 120, 400, ""),
                ("-zu23", "Ural-375 ZU-23", 240, 400, "")], "Z09"),
     s_items(C, [("Workshop A", 0, 150), ("Workshop A", 20, 250), ("Tech hangar A", 90, 200),
                 ("Hangar B", 140, 250), ("Chemical tank A", 200, 150), ("Chemical tank A", 210, 200),
                 ("Fuel tank", 250, 250), ("Garage small B", 320, 200)]))

C = spot((150000, 40000), 0, 0, "Missiles")
zone("combatZone_Missiles", C, 1500, "Z10 Frappe — base de missiles balistiques", "Frappes en profondeur",
     "Une base de missiles balistiques des Gardiens de la révolution dans les montagnes au nord-est de Bandar "
     "Abbas : lanceurs Scud et leurs camions. Détruire les lanceurs ; défense SA-15 et Shilka, sous la couverture "
     "du SA-10 au nord de Bandar Abbas.",
     [g_native(C, "Lanceurs", 0, 0, [{"type": "Scud_B", "count": 3}, {"type": "Ural-375", "count": 2}])]
     + g_fake(C, [("-sa15", "Tor 9A331", 200, 600, ""), ("-shilka", "ZSU-23-4 Shilka", 60, 400, "")], "Z10"),
     s_items(C, [("Bunker", 300, 300), ("Military staff", 320, 400)]))

C = spot(P["Shahid Rajaee Port"], 0, 0, "Port")
zone("combatZone_PortRajaee", C, 1000, "Z11 Frappe — port Shahid Rajaee", "Frappes en profondeur",
     "Les dépôts logistiques militaires du port Shahid Rajaee, à l'ouest de Bandar Abbas : entrepôts, "
     "réservoirs, conteneurs. Tout détruire ; ZU-23 sur place, et les défenses permanentes de Bandar Abbas à "
     "moins de 15 nm.",
     g_fake(C, [("-zu23", "Ural-375 ZU-23", 0, 300, ""), ("-zu23", "Ural-375 ZU-23", 180, 300, "")], "Z11"),
     s_items(C, [("Warehouse", 30, 150), ("Warehouse", 60, 200), ("Fuel tank", 120, 200), ("Fuel tank", 130, 250),
                 ("Container red 1", 240, 120), ("Container red 1", 250, 150), ("Tank", 300, 200)]))

C = spot((167610, -201530), 0, 0, "Lar Power")
zone("combatZone_CentraleLar", C, 800, "Z12 Frappe — centrale électrique de Lar", "Frappes en profondeur",
     "La centrale électrique au sud de Lar. Détruire les bâtiments ; ZU-23 sur place, et le SA-10 et le SA-15 de "
     "Lar à 10 nm au nord.",
     g_fake(C, [("-zu23", "Ural-375 ZU-23", 90, 300, "")], "Z12"),
     s_items(C, [("Boiler-house A", 0, 0), ("Workshop A", 60, 80), ("Workshop A", 120, 80),
                 ("Tech hangar A", 200, 100), ("Shelter B", 260, 90), ("Electric power box", 320, 120)]))

# ── Bases aériennes (OCA) ────────────────────────────────────────────────────
C = spot(off(A["Kish Intl"], 0, 500), 0, 0, "Kish")
zone("combatZone_Kish", C, 1500, "Z13 OCA — base aérienne de Kish", "Bases aériennes",
     "La base aérienne de l'île de Kish : chasseurs au parking, hangars et carburant. Tout détruire au sol ; "
     "défense SA-15 et Shilka.",
     g_fake(C, [("-sa15", "Tor 9A331", 90, 900, ""), ("-shilka", "ZSU-23-4 Shilka", 270, 700, "")], "Z13"),
     s_items(C, [("F-14A", 0, 300), ("F-14A", 10, 340), ("F-4E", 30, 300), ("F-4E", 40, 340),
                 ("Hangar A", 330, 300), ("Fuel tank", 180, 400)]))

C = spot(off(A["Jiroft"], 90, 600), 0, 0, "Jiroft")
zone("combatZone_Jiroft", C, 1500, "Z14 OCA — base aérienne de Jiroft", "Bases aériennes",
     "La base aérienne de Jiroft, au nord de Minab : chasseurs-bombardiers au parking, hangars. Tout détruire au "
     "sol ; défense SA-6 et ZU-23.",
     g_fake(C, [("-sa6", "Kub 2P25 ln", 90, 1000, ""), ("-zu23", "Ural-375 ZU-23", 270, 600, "")], "Z14"),
     s_items(C, [("Su-24M", 0, 300), ("Su-24M", 15, 340), ("MiG-29A", 40, 300), ("MiG-29A", 50, 340),
                 ("Hangar A", 330, 300), ("Fuel tank", 180, 400)]))

# ── Antinavire ───────────────────────────────────────────────────────────────
C = (95000, 5000)
zone("combatZone_Flottille", C, 4000, "Z15 Antinavire — flottille devant Bandar Abbas", "Antinavire",
     "Une flottille de la marine iranienne en patrouille dans le détroit, entre Qeshm, Larak et Bandar Abbas : deux "
     "vedettes lance-missiles et une corvette. Les couler ; elles sont sous les défenses permanentes de Bandar "
     "Abbas.",
     [{"name": "Flottille", "position": xy(C), "keep_position": True, "patrol": True,
       "units": [{"type": "La_Combattante_II", "count": 2}, {"type": "MOLNIYA", "count": 1}],
       "route": [xy(C), xy((90000, 20000))]}], cat="ship")

C = (-28500, -118500)   # contient les vedettes (à l'est) et la batterie Silkworm (sur l'île)
zone("combatZone_AbuMusa", C, 5000, "Z16 Antinavire — vedettes et Silkworm d'Abu Musa", "Antinavire",
     "Les Gardiens de la révolution tiennent Abu Musa : un essaim de vedettes rapides à l'est de l'île et une "
     "batterie de missiles antinavires (HY-2 Silkworm) sur l'île. Couler les vedettes, détruire les lanceurs et leur "
     "radar ; SA-15 permanent sur l'île.",
     [{"name": "Vedettes", "position": xy((-26000, -116000)), "keep_position": True, "patrol": True,
       "units": [{"type": "speedboat", "count": 6}], "route": [xy((-26000, -116000)), xy((-20000, -110000))]}], cat="ship",
     extra=[("Silkworm", spot(A["Abu Musa Island"], 200, 1500, "Silkworm", margin=200),
             [{"type": "hy_launcher", "count": 2}, {"type": "Silkworm_SR", "count": 1}])])

C = (8000, -61000)
zone("combatZone_Mubarek", C, 3000, "Z17 Antinavire — champ pétrolier de Mubarek", "Antinavire",
     "Le champ pétrolier offshore de Mubarek, au sud-est des Tunb, sert de base avancée aux vedettes des Gardiens "
     "de la révolution : plates-formes et vedettes en patrouille. Détruire les plates-formes et couler les vedettes.",
     [{"name": "Vedettes", "position": xy((7000, -62600)), "keep_position": True, "patrol": True,
       "units": [{"type": "speedboat", "count": 4}], "route": [xy((7000, -62600)), xy((11000, -58000))]}],
     cat="ship", statics=[("Oil rig", (6021, -59790)), ("Oil rig", (9350, -62056)), ("Gas platform", (8483, -61357)),
                          ("Gas platform", (9837, -60788))])

# ── Tourisme (demande de David, 12/10/2026 : « fais la CZ, ça peut être marrant ») ─────────────
# Persépolis, à 23 nm au nord-est de Shiraz, sur le plateau à 1 600 m. Rien n'est posé sur les ruines : le détachement
# est à 2 km au nord-est, du côté opposé au SA-11 de Shiraz (50 km de portée, à 54,8 km du site). Posée après coup par
# gen_18_persepolis.py ; décrite ici parce que gen_08 est la source de sync_zones.py.
C = PLACES["Persepolis"]
P18 = spot(C, 45, 2000, "Persepolis detachement")
zone("combatZone_Persepolis", C, 3000, "Z18 Tourisme — Persépolis", "Tourisme",
     "Persépolis, la capitale des rois achéménides, au pied du mont Rahmat : un vol touristique à basse altitude sur le "
     "plateau de Marvdasht, à 1 600 m. Les Gardiens de la révolution ont installé un détachement à 2 km au nord-est du "
     "site : blindés, camions et deux ZU-23. Le neutraliser sans toucher aux ruines. Le SA-11 de Shiraz porte jusqu'à "
     "3 nm au sud-ouest du site : arriver par l'est. Les colonnes et l'escalier de l'Apadana sont modélisés dans DCS.",
     g_fake(P18, [("-zu23", "Ural-375 ZU-23", 0, 300, ""), ("-zu23", "Ural-375 ZU-23", 180, 300, "")], "Z18")
     + [g_native(P18, "Detachement", 90, 200, [{"type": "BTR-80", "count": 2}, {"type": "Ural-375", "count": 2}])])

if __name__ == "__main__":
    b = Batch()
    for name, c, r, fname, menu, text, side, cat, groups, statics, extra in ZONES:
        if cat == "ship":
            sea(c, name, margin=1500)
        for g in groups:
            for q in g.get("route") or []:
                (sea if cat == "ship" else land)((q["x"], q["y"]), f"{name} route", 1000 if cat == "ship" else 100)
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": False,
              "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"}
        b.act("create_combat_zone", zone_name=name, position=xy(c), radius=r, groups=groups, **side,
              category=cat, combat_zone=cz)
        for i, (typ, p) in enumerate(statics, 1):
            b.act("add_group", **side, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
                  position=xy(p), units=[{"type": typ}], for_combat_zone=name, keep_position=True)
        for gname, p, units in extra:
            b.act("add_group", **side, category="vehicle", name=gname, position=xy(p), units=units,
                  for_combat_zone=name, keep_position=True)
        print(f"{fname:52} {round(c[0]):>8} {round(c[1]):>8}  r={r}")
    # Drone laser sur la défense côtière de Bandar Lengeh (SA-13 et Shilka seulement)
    b.act("add_air_group", **BLUE, name="Reaper 2", unit_type="MQ-9 Reaper", count=1, start="air",
          position=xy(spot(P["Bandar Lengeh"], 0, 6000, "Reaper 2")), altitude_ft=10000, speed_kt=110,
          task="AFAC", skill="High")
    b.save("08-zones.json")
