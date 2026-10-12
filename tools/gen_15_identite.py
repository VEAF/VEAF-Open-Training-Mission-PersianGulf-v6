"""Lot 15 : date, bullseye commun et briefing DCS de la mission.

Le texte est composé depuis les données (fréquences DCS des aérodromes, soutien, zones), pas tapé.
`python gen_15_identite.py [suffixe]` : un lot de briefing se rejoue sans danger (set_* remplacent), d'où le suffixe
de nom de lot pour garder chaque passage.
"""
import json
import sys

from gen_05_soutien import CARRIERS
from gen_09_qra_cap import QRAS
from gen_10_joueurs import SANCTUARIES
from lib import BLUE_SLOTS, BULLSEYE, RED_SLOTS, ROOT, TANKERS, Batch, xy

_t = (ROOT / "tools/airfield_channels.json").read_text(encoding="utf-8")
CH = {a["name"]: a for a in json.loads(_t[_t.index("{"):])["candidates"]}


def base(n):
    a = CH[n]
    f = a["freqs"]
    tac = f", TACAN {a['tacan']}" if a.get("tacan") else ""
    return f"{n} (U{f['uhf']:.2f} / V{f['vhf']:.2f}{tac})"


def carriers():
    out = []
    for c in CARRIERS:
        s = f"{c['name'].split(' ', 1)[1]} U{c['tower_mhz']:.1f}, TACAN {c['tacan_channel']}X, ICLS {c['icls_channel']}"
        if c.get("link4_mhz"):
            s += f", Link 4 {c['link4_mhz']:.1f}"
        out.append(s)
    return " ; ".join(out)


def tankers():
    return ", ".join(f"{n} ({k}) {tac} U{f:.1f} FL{fl}" for n, (ab, fl, tac, f, k) in TANKERS.items())


def qras(side):
    return ", ".join(f"{q['name'].replace('QRA ', '')} ({q['radius'] / 1852:.0f} nm)" for q in QRAS
                     if q["side"]["coalition"] == side)


SITUATION = f"""VEAF Open Training — Golfe Persique (moderne, novembre 2025).
L'Iran ferme le détroit d'Ormuz ; une coalition (Émirats, Oman, États-Unis) tient la rive sud du Golfe et la mer d'Oman. Le front est le Golfe lui-même, de Lavan à Jask ; l'Iran tient aussi Abu Musa, les Tunb, Sirri, Kish et Lavan. Bullseye commun : la Grande Tunb.

BASES BLEUES (slots dynamiques) : {", ".join(base(n) for n in BLUE_SLOTS)}. FARP Berlin (V127.5) et FARP London (V128.5).
PORTE-AVIONS : {carriers()}.
SOUTIEN : AWACS Overlord 1 U282.0 (ouest) et Magic 1 U283.0 (est). Ravitailleurs : {tankers()} ; S-3B du Stennis 56Y U296.0, du Roosevelt 57Y U297.0. Tous escortés. Drones laser : Reaper 1 (code 1511, FM 35.55) sur le champ de tir de Tarif, Reaper 2 (1512, FM 35.6) sur Bandar Lengeh.

ENTRAÎNEMENT (menu F10 VEAF, zones) : H Berlin (hélicoptères), A Tarif (attaque), S Al Qua'a (SEAD), trois niveaux chacun.
COMBAT : 18 zones (front, SEAD, convois, frappes, bases aériennes, antinavire, et un vol touristique sur Persépolis), chacune avec son briefing dans le menu. Missions à la demande : CAP rouges et bleues, raid iranien sur Al Minhad, interception d'un transport VIP.
QRA rouges : {qras('red')} ; QRA bleues : {qras('blue')}. Décollage 90 s après l'entrée du premier intrus ; elles ignorent les hélicoptères. Couloirs sans QRA : îles de l'ouest, Bandar Lengeh, Minab, Jask, mer d'Oman.
JOUEURS CONTRE JOUEURS : libre hors des sanctuaires. Sanctuaire bleu : Al Dhafra, Liwa et les champs d'entraînement ({SANCTUARIES[0][3] // 1000} km) ; rouges : Lar ({SANCTUARIES[1][3] // 1000} km) et Shiraz ({SANCTUARIES[2][3] // 1000} km). Un intrus y est détruit après 60 s ; un missile tiré sur un défenseur est détruit. Arène AirQuake au fond du Golfe, au large du Koweït, slots en vol Fox 1 et Fox 3.

Plan radio, cartes et détail de chaque zone : voir les images du briefing et le README de la mission."""

BLUE_TASK = ("Rouvrir le détroit : s'entraîner sur les champs de tir H, A et S, puis frapper les zones de combat iraniennes. "
             "Al Dhafra est la base mère ; Khasab, dans l'enclave omanaise de Musandam, est la base la plus proche du "
             "front ; le Tarawa est dans le Golfe, le Roosevelt en mer d'Oman.")
RED_TASK = (f"Tenir le détroit. Bases rouges avec slots : {', '.join(base(n) for n in RED_SLOTS)}. "
            "AWACS Wizard 1 U284.0, ravitailleur Shell 1 (IL-78) U294.0 FL200. Arène : AWACS Focus 1 U286.0.")

if __name__ == "__main__":
    b = Batch()
    b.act("set_mission_date", date="2025-11-15", start_time="09:00")
    for side in ("blue", "red"):
        b.act("set_bullseye", coalition=side, position=xy(BULLSEYE))
    b.act("set_briefing", sortie="VEAF Open Training — Golfe Persique", situation=SITUATION, blue_task=BLUE_TASK,
          red_task=RED_TASK)
    b.save(f"15-identite{('-' + sys.argv[1]) if len(sys.argv) > 1 else ''}.json")
    print(SITUATION)
