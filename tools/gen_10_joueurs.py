"""Lot 10 : sanctuaires, arène AirQuake, slots sur les ponts, groupes des missions scénarisées.

Sanctuaires (cercles tirés de zones de déclenchement), plan validé par David le 12/10/2026 :
  - bleu : Al Dhafra, Liwa, Al-Bateen et les trois champs d'entraînement (80 km autour du désert de Tarif) ;
  - rouge : 12 km autour de Lar (la centrale Z12 est à 19 km, le départ du convoi Z07 à 18 km) et 20 km autour
    de Shiraz. Bandar Abbas n'en a pas : il bloquerait les zones d'Ormuz.
Arène AirQuake : celle de la v5, loin au nord-ouest, au fond du Golfe au large du Koweït (en mer) ; mêmes positions, types et emports (FOX1 =
AIM-7M / Super 530D, FOX3 = AIM-120C / AIM-54C), départ en vol au FL250.
"""
import json

from lib import AIRFIELDS, BLUE, RED, RED_IR, ROOT, Batch, xy

V5 = json.loads((ROOT / "tools/loadouts-v5.json").read_text(encoding="utf-8"))

SANCTUARIES = [
    ("Sanctuaire Al Dhafra", "SANCT-AlDhafra", (-245000, -200000), 80000, "BLUE"),
    ("Sanctuaire Lar", "SANCT-Lar", AIRFIELDS["Lar"], 12000, "RED"),
    ("Sanctuaire Shiraz", "SANCT-Shiraz", AIRFIELDS["Shiraz Intl"], 20000, "RED"),
]

ARENA = ((380000, -690000), 74000)   # centre, rayon (40 nm)
ARENA_SLOTS = [
    # nom v6, groupe v5, camp
    ("Arène bleue F-14B Fox 3", "BLUE F-14B AirQuake FOX3", BLUE),
    ("Arène bleue F-14B Fox 1", "F-14B AirQuake FOX1 BLUE", BLUE),
    ("Arène bleue F/A-18C Fox 3", "BLUE F/A-18C AirQuake FOX3", BLUE),
    ("Arène bleue F/A-18C Fox 1", "F/A-18C AirQuake FOX1 BLUE", BLUE),
    ("Arène bleue M-2000C Fox 1", "M2000C AirQuake FOX1 BLUE", BLUE),
    ("Arène rouge F-14B Fox 3", "RED F-14B AirQuake FOX3", RED_IR),
    ("Arène rouge F-14B Fox 1", "RED F-14B AirQuake FOX1", RED_IR),
    ("Arène rouge F/A-18C Fox 3", "RED F/A-18C AirQuake FOX3", RED),
    ("Arène rouge F/A-18C Fox 1", "RED F/A-18C AirQuake FOX1", RED),
    ("Arène rouge M-2000C Fox 1", "RED M2000C AirQuake FOX1", RED),
]

DECKS = [
    # porte-avions, nom du groupe, type, nombre, départ
    ("CSG-74 Stennis", "Stennis F/A-18C #1", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-74 Stennis", "Stennis F/A-18C #2", "FA-18C_hornet", 2, "deck-hot"),
    ("CSG-74 Stennis", "Stennis F-14B #1", "F-14B", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F/A-18C #1", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F-14B #1", "F-14B", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F-14B #2", "F-14B", 2, "deck-hot"),
    ("ARG-1 Tarawa", "Tarawa AV-8B #1", "AV8BNA", 2, "deck-cold"),
    ("ARG-1 Tarawa", "Tarawa AV-8B #2", "AV8BNA", 2, "deck-hot"),
]

MINHAD = AIRFIELDS["Al Minhad AFB"]
SHIRAZ = AIRFIELDS["Shiraz Intl"]
# Missions scénarisées : groupes en activation différée (combat_missions: de mission.yaml)
SCENARIO = [
    # nom, camp, type, nombre, départ, altitude ft, kt, tâche, emport, points suivants
    ("SC-Defense-AlMinhad-SEAD", RED_IR, "Su-24M", 2, (60000, -40000), 18000, 480, "SEAD",
     {"payload": "Kh31P*2_Kh25ML*2_L-081"}, [(-60000, -70000), MINHAD]),
    ("SC-Defense-AlMinhad-Bombers", RED_IR, "F-4E", 4, (65000, -45000), 20000, 450, "Ground Attack",
     {"payload": "Mk-82*18,AIM-7*2,ECM"}, [(-55000, -75000), MINHAD]),
    ("SC-Defense-AlMinhad-Escort", RED_IR, "F-14A", 2, (63000, -43000), 24000, 450, "Escort",
     {"payload": "AIM-54C*4,AIM-9*2,AIM-7*2"}, [(-55000, -75000), MINHAD]),
    ("SC-Intercept-VIP-Il76", RED_IR, "IL-76MD", 1, (125000, 5000), 22000, 350, "Transport",
     {}, [(250000, -200000), SHIRAZ]),
    ("SC-Intercept-VIP-Escort", RED_IR, "MiG-29A", 2, (123000, 3000), 24000, 350, "Escort",
     {"payload": "R-73*4,R-27R*2,Fuel-1500"}, [(250000, -200000), SHIRAZ]),
]

if __name__ == "__main__":
    b = Batch()
    for name, zone, c, r, side in SANCTUARIES:
        b.act("add_trigger_zone", name=zone, position=xy(c), radius=r)
    b.act("add_trigger_zone", name="Arene", position=xy(ARENA[0]), radius=ARENA[1])
    for name, v5name, side in ARENA_SLOTS:
        g = V5[v5name]
        hdg = 0 if side is BLUE else 180
        b.act("add_air_group", **side, name=name, unit_type=g["type"], count=2, start="air",
              position=xy((g["x"], g["y"])), altitude_ft=25000, speed_kt=450, heading_deg=hdg, skill="Client",
              task="CAP", pylons=g["pylons"])
    for carrier, name, typ, n, start in DECKS:
        b.act("add_air_group", **BLUE, name=name, unit_type=typ, count=n, start=start, carrier=carrier,
              skill="Client", task="CAP")
    for name, side, typ, n, p, alt, kt, task, loadout, route in SCENARIO:
        b.act("add_air_group", **side, name=name, unit_type=typ, count=n, start="air", position=xy(p),
              altitude_ft=alt, speed_kt=kt, task=task, skill="High", late_activation=True, **loadout)
        for q in route:
            b.act("edit_route", group_name=name, operation="add", position=xy(q), altitude_ft=alt, speed_kt=kt)
    b.act("edit_route", group_name="SC-Defense-AlMinhad-Bombers", operation="add_task", index=3, task="bombing",
          task_params={"position": xy(MINHAD), "expend": "All", "attack_qty": 1})
    for esc, target in [("SC-Defense-AlMinhad-Escort", "SC-Defense-AlMinhad-Bombers"),
                        ("SC-Intercept-VIP-Escort", "SC-Intercept-VIP-Il76")]:
        b.act("edit_route", group_name=esc, operation="add_task", index=1, task="escort",
              task_params={"group_name": target, "engagement_distance_nm": 30})
    b.save("10-joueurs.json")
