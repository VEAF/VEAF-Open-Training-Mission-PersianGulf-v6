"""Lot 05 : ravitailleurs, AWACS, escortes, drone laser du champ de tir, puis les trois groupes aéronavals.

Ravitailleurs AVANT porte-avions : sinon les S-3B de add_carrier_group prennent Texaco11 / Arco11 et chaque
ravitailleur est décalé sur la famille suivante (constaté aux Mariannes, retours-vmct 2).

Plan radio, hors de la bande des tours du théâtre (UHF 250.0-251.3, FM 38.4-39.7 : describe_airfield_channels) :
  AWACS 282-286, ravitailleurs 290-295 (dernier chiffre = TACAN 50Y..55Y), porte-avions 305-307,
  S-3B des porte-avions 296-297 (TACAN 56Y, 57Y).
Escortes : sur tous les ravitailleurs et AWACS (décision de David, 12/10/2026), sauf les AWACS de l'arène.
Secteur ouest : au large d'Abu Dhabi, au sud de Sir Abu Nuayr. Secteur est : mer d'Oman, à l'est de Fujairah.
"""
from lib import BLUE, RED, RED_IR, Batch, sea, xy

b = Batch()

F15 = ("F-15C", {"payload": "AIM-9*4,AIM-120*4,Fuel"})
F14 = ("F-14A", {"payload": "AIM-54C*4,AIM-9*2,AIM-7*2"})
MIG29 = ("MiG-29A", {"payload": "R-73*4,R-27R*2,Fuel-1500"})

# nom, type, camp, a, b (hippodrome), FL, kt, MHz, rôle, TACAN (canal, indicatif), escorte (type, emport)
SUPPORT = [
    # secteur ouest
    ("Texaco 1", "KC-135", BLUE, (-130000, -240000), (-130000, -180000), 220, 400, 290.0, "Refueling", (50, "TX1"), F15),
    ("Arco 1", "KC135MPRS", BLUE, (-160000, -225000), (-160000, -165000), 180, 380, 291.0, "Refueling", (51, "AR1"), F15),
    ("Overlord 1", "E-3A", BLUE, (-200000, -140000), (-200000, -60000), 300, 360, 282.0, "AWACS", None, F15),
    # secteur est, mer d'Oman
    ("Texaco 2", "KC-135", BLUE, (-150000, 45000), (-90000, 45000), 240, 400, 292.0, "Refueling", (52, "TX2"), F15),
    ("Arco 2", "KC135MPRS", BLUE, (-165000, 75000), (-105000, 75000), 200, 380, 293.0, "Refueling", (53, "AR2"), F15),
    ("Magic 1", "E-2C", BLUE, (-210000, 50000), (-160000, 110000), 280, 300, 283.0, "AWACS", None, F15),
    # rouge, à l'intérieur de l'Iran
    ("Shell 1", "IL-78M", RED_IR, (250000, -150000), (250000, -60000), 200, 380, 294.0, "Refueling", None, MIG29),
    ("Wizard 1", "A-50", RED, (320000, -120000), (320000, -20000), 300, 360, 284.0, "AWACS", None, F14),
    # arène AirQuake (v5, loin au nord-ouest) : un AWACS par camp, sans escorte
    ("Darkstar 1", "E-3A", BLUE, (300000, -660000), (300000, -720000), 300, 360, 285.0, "AWACS", None, None),
    ("Focus 1", "A-50", RED, (470000, -660000), (470000, -720000), 300, 360, 286.0, "AWACS", None, None),
]
for n, typ, side, a, bb, fl, kt, f, task, beacon, esc in SUPPORT:
    b.act("add_air_group", **side, name=n, unit_type=typ, count=1, start="air", position=xy(a),
          altitude_ft=fl * 100, speed_kt=kt, frequency_mhz=f, task=task, skill="High")
    b.act("edit_route", group_name=n, operation="add", position=xy(bb), altitude_ft=fl * 100, speed_kt=kt)
    b.act("edit_route", group_name=n, operation="add_task", index=1, task="set_unlimited_fuel", task_params={"value": True})
    if beacon:
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="activate_beacon",
              task_params={"channel": beacon[0], "mode": "Y", "callsign": beacon[1], "bearing": True, "aa": True})
    if task == "Refueling":
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="tanker", task_params={})
    else:
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="awacs", task_params={})
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="eplrs", task_params={"value": True})
    b.act("edit_route", group_name=n, operation="add_task", index=1, task="orbit",
          task_params={"pattern": "Race-Track", "altitude_ft": fl * 100, "speed_kt": kt})
    if esc:
        etype, loadout = esc
        en = n + " - Escort"
        b.act("add_air_group", **side, name=en, unit_type=etype, count=2, start="air",
              position=xy((a[0] - 3000, a[1] - 3000)), altitude_ft=fl * 100, speed_kt=kt, frequency_mhz=f,
              task="Escort", skill="High", **loadout)
        b.act("edit_route", group_name=en, operation="add_task", index=1, task="set_unlimited_fuel", task_params={"value": True})
        b.act("edit_route", group_name=en, operation="add_task", index=1, task="escort",
              task_params={"group_name": n, "engagement_distance_nm": 30})

# ── Drone de guidage laser du champ de tir d'attaque (le second, sur une vraie zone, vient avec le lot 08)
b.act("add_air_group", **BLUE, name="Reaper 1", unit_type="MQ-9 Reaper", count=1, start="air",
      position=xy((-250000, -215000)), altitude_ft=10000, speed_kt=110, task="AFAC", skill="High")

# ── Groupes aéronavals : Stennis et Roosevelt (décision du 02/10/2026) et le Tarawa (David, 12/10/2026)
CARRIERS = [
    # Golfe, à l'ouest (position v5), cap à l'ouest-nord-ouest
    dict(name="CSG-74 Stennis", carrier_type="Stennis", position=(-89300, -253900), heading_deg=290, speed_kt=10,
         tower_mhz=305.0, tacan_channel=74, tacan_callsign="STN", icls_channel=11, link4_mhz=336.0,
         tanker_tacan_channel=56, tanker_tacan_callsign="S74", tanker_frequency_mhz=296.0,
         escorts=["TICONDEROG", "USS_Arleigh_Burke_IIa"]),
    # mer d'Oman, au large de Fujairah, cap au sud-est
    dict(name="CSG-71 Roosevelt", carrier_type="CVN_71", position=(-185000, 80000), heading_deg=135, speed_kt=10,
         tower_mhz=306.0, tacan_channel=71, tacan_callsign="RSV", icls_channel=12, link4_mhz=337.0,
         tanker_tacan_channel=57, tanker_tacan_callsign="S71", tanker_frequency_mhz=297.0,
         escorts=["TICONDEROG", "USS_Arleigh_Burke_IIa"]),
    # Golfe, entre Sir Abu Nuayr et le Stennis : à portée d'hélicoptère des îles iraniennes
    dict(name="ARG-1 Tarawa", carrier_type="LHA_Tarawa", position=(-85000, -225000), heading_deg=270, speed_kt=8,
         tower_mhz=307.0, tacan_channel=73, tacan_callsign="TRW", icls_channel=13, link4_mhz=None,
         recovery_tanker=False, rescue_helicopter=True, escorts=["PERRY"]),
]
for c in CARRIERS:
    c = dict(c)
    p = c.pop("position")
    sea(p, c["name"], margin=8000)
    b.act("add_carrier_group", **BLUE, position=xy(p), **c)

if __name__ == "__main__":
    b.save("05-soutien.json")
