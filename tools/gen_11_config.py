"""Lot 11 : blocs ASSETS et SANCTUARY de mission.yaml, missions scénarisées (combat_missions:), réglages CTLD.

Un nom partout : nom de groupe = indicatif = libellé de preset = texte ASSETS. Chaque camp ne voit que ses
moyens (coalition). Drones : code laser imposé et fréquence que CTLD calcule pour ce code (35.55 / 35.6 FM,
mesuré sur Syrie v6, limitation ctld-jtac-imposed-code-and-radio), sous un jtacLaserCodeMax abaissé à 1686.
CTLD : rayon logistique des aérodromes 2 500 m. La zone est centrée sur le parking le plus proche du centre de
tous les parkings (veafTransportMission.findAirbaseLogisticsPoint) ; mesuré sur les données de parking
PersianGulf, 2 500 m couvrent 81 % des 254 places d'Al Dhafra (2 % à 250 m) et 89 à 100 % des autres bases bleues.
"""
import re

from gen_10_joueurs import SANCTUARIES
from lib import M
from mcp import cat

ASSETS = [
    ("Overlord 1", "Overlord 1 (E-3A) — AWACS ouest", "BLUE", "U282.0 — FL300 — orbite au sud d'Abu Dhabi et d'Al Ain", "Overlord 1 - Escort"),
    ("Magic 1", "Magic 1 (E-2C) — AWACS est", "BLUE", "U283.0 — FL280 — orbite au-dessus de la mer d'Oman, au sud de Fujairah", "Magic 1 - Escort"),
    ("Texaco 1", "Texaco 1 (KC-135, perche) — ouest", "BLUE", "TACAN 50Y TX1 — U290.0 — FL220 — piste nord-sud au large d'Abu Dhabi, à l'ouest de Sir Abu Nuayr", "Texaco 1 - Escort"),
    ("Arco 1", "Arco 1 (KC-135 MPRS, panier) — ouest", "BLUE", "TACAN 51Y AR1 — U291.0 — FL180 — piste nord-sud au large d'Abu Dhabi", "Arco 1 - Escort"),
    ("Texaco 2", "Texaco 2 (KC-135, perche) — est", "BLUE", "TACAN 52Y TX2 — U292.0 — FL240 — piste nord-sud en mer d'Oman, à l'est de Fujairah", "Texaco 2 - Escort"),
    ("Arco 2", "Arco 2 (KC-135 MPRS, panier) — est", "BLUE", "TACAN 53Y AR2 — U293.0 — FL200 — piste nord-sud en mer d'Oman, près du Roosevelt", "Arco 2 - Escort"),
    ("CSG-74 Stennis", "CVN-74 Stennis — Golfe", "BLUE", "TACAN 74X STN — ICLS 11 — Link 4 336.0 — ACLS — U305.0", None),
    ("CSG-71 Roosevelt", "CVN-71 Roosevelt — mer d'Oman", "BLUE", "TACAN 71X RSV — ICLS 12 — Link 4 337.0 — ACLS — U306.0", None),
    ("ARG-1 Tarawa", "LHA-1 Tarawa — Golfe", "BLUE", "TACAN 73X TRW — ICLS 13 — U307.0", None),
    ("CSG-74 Stennis S3B-Tanker", "S-3B du Stennis (ravitailleur embarqué)", "BLUE", "TACAN 56Y S74 — U296.0", None),
    ("CSG-71 Roosevelt S3B-Tanker", "S-3B du Roosevelt (ravitailleur embarqué)", "BLUE", "TACAN 57Y S71 — U297.0", None),
    ("Darkstar 1", "Darkstar 1 (E-3A) — AWACS bleu de l'arène", "BLUE", "U285.0 — FL300", None),
    ("Wizard 1", "Wizard 1 (A-50) — AWACS rouge", "RED", "U284.0 — FL300 — orbite au sud de Sirjan", "Wizard 1 - Escort"),
    ("Shell 1", "Shell 1 (IL-78M) — ravitailleur rouge", "RED", "U294.0 — FL200 — orbite à l'est de Lar", "Shell 1 - Escort"),
    ("Focus 1", "Focus 1 (A-50) — AWACS rouge de l'arène", "RED", "U286.0 — FL300", None),
]
DRONES = [
    ("Reaper 1", "Reaper 1 (drone laser) — champ de tir de Tarif", 1511, "35.55",
     "Laser 1511 — FM 35.55. 3 000 m sol au-dessus du champ de tir attaque (zone A)."),
    ("Reaper 2", "Reaper 2 (drone laser) — Bandar Lengeh", 1512, "35.6",
     "Laser 1512 — FM 35.6. 3 000 m sol au-dessus de la défense côtière de Bandar Lengeh (Z02)."),
]

if __name__ == "__main__":
    assets = []
    for i, (name, desc, side, info, linked) in enumerate(ASSETS, 1):
        a = {"sort": i, "name": name, "description": desc, "coalition": side, "information": info}
        if linked:
            a["linked"] = linked
        assets.append(a)
    for name, desc, code, freq, info in DRONES:
        assets.append({"sort": len(assets) + 1, "name": name, "description": desc, "coalition": "BLUE",
                       "information": info, "jtac": code, "freq": freq, "mod": "FM"})
    print(cat.run_action("set_mission_module", {"mission_yaml_path": M + "/mission.yaml", "module_id": "ASSETS",
                                                 "value": {"enabled": True, "assets": assets}}))
    sanct = [{"name": n, "trigger_zone": z, "coalition": side, "delay_warning": 0, "delay_instant": 60,
              "protect_from_missiles": True} for n, z, c, r, side in SANCTUARIES]
    print(cat.run_action("set_mission_module", {"mission_yaml_path": M + "/mission.yaml", "module_id": "SANCTUARY",
                                                 "value": {"enabled": True, "sanctuary_zones": sanct}}))

    path = M + "/mission.yaml"
    t = open(path, encoding="utf-8").read()
    old = "    airbase_logistics_radius: 250    # metres of logistic zone around each airfield's stand\n"
    assert old in t
    t = t.replace(old, "    airbase_logistics_radius: 2500   # mesuré : 81 % des parkings d'Al Dhafra (2 % à 250 m), 89-100 % ailleurs (tools/gen_11_config.py)\n")
    t = re.sub(r"\n# ── Missions scénarisées \(module COMBATMISSION\).*", "", t, flags=re.S)
    t = t.rstrip("\n") + "\n" + '''
# ── Missions scénarisées (module COMBATMISSION) — écrites par tools/gen_11_config.py ──
combat_missions:
- name: Defense-AlMinhad
  friendly_name: Défense — raid iranien sur Al Minhad
  secured: false
  briefing: "Deux Su-24M armés de missiles antiradar ouvrent la route à quatre F-4E chargés de bombes, escortés de deux F-14A, partis de Qeshm vers Al Minhad. Abattez les bombardiers avant le largage.\\nÉchec si la base est bombardée (constaté par vous : la mission ne le vérifie pas)."
  elements:
  - name: SEAD
    groups:
    - SC-Defense-AlMinhad-SEAD
    scalable: false
  - name: Bombardiers
    groups:
    - SC-Defense-AlMinhad-Bombers
    scalable: false
  - name: Escorte
    groups:
    - SC-Defense-AlMinhad-Escort
    scalable: true
- name: Interception-VIP
  friendly_name: Interception — transport VIP de Bandar Abbas à Shiraz
  secured: false
  briefing: "Un IL-76 emmène l'état-major des Gardiens de la révolution de Bandar Abbas vers Shiraz, escorté par deux MiG-29A. Interceptez-le avant Shiraz : la fin de la route est dans le sanctuaire rouge de Shiraz, sous son SA-11."
  elements:
  - name: Transport
    groups:
    - SC-Intercept-VIP-Il76
    scalable: false
  - name: Escorte
    groups:
    - SC-Intercept-VIP-Escort
    scalable: true
'''
    open(path, "w", encoding="utf-8").write(t)
    print("CTLD et combat_missions écrits")

    ctld = M + "/ctld-config.yaml"
    c = open(ctld, encoding="utf-8").read()
    old = "  jtacLaserCodeMax: 1688\n"
    if old in c:
        c = c.replace(old, "  jtacLaserCodeMax: 1686   # codes imposés des drones (1511, 1512) sous le maximum, comme Syrie v6 (limitation ctld-jtac-imposed-code-and-radio)\n")
        open(ctld, "w", encoding="utf-8").write(c)
    assert "jtacLaserCodeMax: 1686" in open(ctld, encoding="utf-8").read()
    print("ctld-config : jtacLaserCodeMax 1686")
