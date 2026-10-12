"""Lot 09 : QRA (rouges, et bleues puisque le rouge est jouable) et CAP à la demande.

QRA : cercle dans le territoire du camp qui défend, réponse graduée, deux appareils différents par niveau tirés
au sort, délai 90 s, pas de réaction aux hélicoptères, pas de menu radio ouvert à tous ; départ de la piste
(données de parking PersianGulf présentes).
  - Bandar Abbas : 25 nm autour du détroit au sud de Bandar Abbas (Qeshm, Hormuz, Larak) ; Khasab à 54 nm du
    centre, hors du cercle. Couvre Z01, Z06, Z11, Z15.
  - Lar : 25 nm autour de Lar. Couvre la centrale (Z12).
  Couloirs libres : îles de l'ouest (Kish, Lavan, Abu Musa, Tunb), Bandar Lengeh, Minab, Jask et la mer d'Oman,
  et toute la profondeur au-delà.
  - Al Minhad (Dubaï) et Al Dhafra : 25 nm et 30 nm, contre les joueurs rouges.
CAP rouges dans le territoire rouge, CAP bleues dans le territoire bleu.
"""
from lib import AIRFIELDS, BLUE, BLUE_UAE, RED_IR, Batch, xy

A = AIRFIELDS
MIG29 = {"payload": "R-73*4,R-27R*2,Fuel-1500"}
F14 = {"payload": "AIM-54C*4,AIM-9*2,AIM-7*2"}
F4 = {"payload": "AIM-9*4,AIM-7*4,Fuel*2"}
F16 = {"payload": "AIM-120C*4, AIM-9M*2, Fuel"}
F15 = {"payload": "AIM-9*4,AIM-120*4,Fuel"}
M2000 = {"payload": "R 550*2,MICA AR*4,Fuel*3"}

QRAS = [
    dict(name="QRA Bandar Abbas", side=RED_IR, zone="QRA-BandarAbbas", center=(95000, 0), radius=46300,
         airfield="Bandar Abbas Intl", enemy="BLUE", levels=[
             (1, [("QRA-BandarAbbas-MiG29", "MiG-29A", 2, MIG29), ("QRA-BandarAbbas-F4", "F-4E", 2, F4)]),
             (3, [("QRA-BandarAbbas-F14", "F-14A", 2, F14), ("QRA-BandarAbbas-MiG29x4", "MiG-29A", 4, MIG29)])]),
    dict(name="QRA Lar", side=RED_IR, zone="QRA-Lar", center=A["Lar"], radius=46300, airfield="Lar",
         enemy="BLUE", levels=[
             (1, [("QRA-Lar-F4", "F-4E", 2, F4), ("QRA-Lar-MiG29", "MiG-29A", 2, MIG29)]),
             (3, [("QRA-Lar-F14", "F-14A", 2, F14), ("QRA-Lar-F4x4", "F-4E", 4, F4)])]),
    dict(name="QRA Al Minhad", side=BLUE_UAE, zone="QRA-AlMinhad", center=(-115000, -80000), radius=46300,
         airfield="Al Minhad AFB", enemy="RED", levels=[
             (1, [("QRA-AlMinhad-F16", "F-16C bl.50", 2, F16), ("QRA-AlMinhad-M2000", "Mirage 2000-5", 2, M2000)]),
             (3, [("QRA-AlMinhad-F15", "F-15C", 4, F15), ("QRA-AlMinhad-M2000x4", "Mirage 2000-5", 4, M2000)])]),
    dict(name="QRA Al Dhafra", side=BLUE, zone="QRA-AlDhafra", center=A["Al Dhafra AFB"], radius=55560,
         airfield="Al Dhafra AFB", enemy="RED", levels=[
             (1, [("QRA-AlDhafra-F15", "F-15C", 2, F15), ("QRA-AlDhafra-F16", "F-16C bl.50", 2, F16)]),
             (3, [("QRA-AlDhafra-F15x4", "F-15C", 4, F15), ("QRA-AlDhafra-F16x4", "F-16C bl.50", 4, F16)])]),
]

# (nom, type, nombre, camp, a, b, FL, kt, emport, menu, briefing)
CAPS = [
    ("CAP-Qeshm-MiG29", "MiG-29A", 2, RED_IR, (70000, -60000), (90000, -20000), 220, 420, MIG29,
     "CAP rouge MiG-29 (Fox 1) — Qeshm — FL220",
     "Deux MiG-29A armés de R-27R et R-73 patrouillent au-dessus de l'île de Qeshm, au FL220. "
     "Emport : R-73*4,R-27R*2,Fuel-1500."),
    ("CAP-Lengeh-F4", "F-4E", 2, RED_IR, (60000, -165000), (75000, -110000), 200, 420, F4,
     "CAP rouge F-4E (Fox 1) — Bandar Lengeh — FL200",
     "Deux F-4E armés d'AIM-7 et d'AIM-9 patrouillent au-dessus de Bandar Lengeh et de Kong, au FL200. "
     "Emport : AIM-9*4,AIM-7*4,Fuel*2."),
    ("CAP-Lar-F14", "F-14A", 2, RED_IR, (150000, -230000), (190000, -150000), 350, 500, F14,
     "CAP rouge F-14A (intercepteur haut et rapide, AIM-54) — Lar — FL350",
     "Deux F-14A armés de Phoenix patrouillent haut et vite au-dessus de Lar, au FL350. "
     "Emport : AIM-54C*4,AIM-9*2,AIM-7*2."),
    ("Raid-Kish-Su24", "Su-24M", 2, RED_IR, (70000, -250000), (40000, -195000), 150, 420, {"payload": "FAB-500*4,R-60M*2"},
     "Raid rouge Su-24M à intercepter — Kish — FL150",
     "Deux Su-24M chargés de bombes tournent au-dessus de Kish, au FL150, prêts à frapper Sir Abu Nuayr : les "
     "intercepter. Emport : FAB-500*4,R-60M*2."),
    ("CAP-RAK-F16", "F-16C bl.50", 2, BLUE, (-75000, -45000), (-50000, -20000), 220, 420, F16,
     "CAP bleue F-16 (Fox 3) — Ras Al Khaimah — FL220",
     "Deux F-16C patrouillent au-dessus de Ras Al Khaimah et de la base de Musandam, au FL220. "
     "Emport : AIM-120C*4, AIM-9M*2, Fuel."),
    ("CAP-AbuDhabi-M2000", "Mirage 2000-5", 2, BLUE_UAE, (-175000, -205000), (-150000, -150000), 250, 440, M2000,
     "CAP bleue Mirage 2000-5 (Fox 3) — Abu Dhabi — FL250",
     "Deux Mirage 2000-5 émiriens couvrent la côte d'Abu Dhabi, au FL250. Emport : R 550*2,MICA AR*4,Fuel*3."),
]

if __name__ == "__main__":
    b = Batch()
    for q in QRAS:
        groups, levels = [], []
        for count, members in q["levels"]:
            names = []
            for gname, typ, n, loadout in members:
                groups.append({"name": gname, "units": [{"type": typ, "count": n}], "position": xy(q["center"]),
                               "airfield": q["airfield"], **loadout})
                names.append(gname)
            levels.append({"enemy_count": count, "groups": names, "random_pick": 1})
        side = q["side"]
        b.act("create_qra", name=q["name"], coalition=side["coalition"], country_id=side["country_id"],
              country_name=side["country_name"], trigger_zone=q["zone"], position=xy(q["center"]), radius=q["radius"],
              groups=groups, enemy_coalitions=[q["enemy"]],
              qra={"groups_by_enemy_count": levels, "delay_before_activating": 90, "delay_before_rearming": 600,
                   "react_on_helicopters": False, "airport_link": q["airfield"]})
    for name, typ, n, side, a, bb, fl, kt, loadout, menu, brief in CAPS:
        b.act("create_cap_mission", mission_name=name, units=[{"type": typ, "count": n}], **side, position=xy(a),
              route=[{**xy(bb), "altitude_ft": fl * 100}], altitude_ft=fl * 100, speed_kt=kt,
              cap={"menu_name": menu, "briefing": brief}, **loadout)
    b.save("09-qra-cap.json")
