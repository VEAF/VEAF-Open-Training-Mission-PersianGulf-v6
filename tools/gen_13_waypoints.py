"""Écrit src/waypoints.yaml : plans de vol des groupes joueurs, par catégorie et par camp jouable.

Le build ajoute lui-même le BULLSEYE (Grande Tunb) à chaque plan. Ravitailleurs : début de piste (gen_05_soutien.py).
"""
import yaml

from gen_04_bases import FARPS
from gen_07_entrainement import A, H, S
from lib import M

KT = 0.514444
FARP = {n: p for n, p, *_ in FARPS}
WP = {
    "TX1": ((-130000, -240000), 22000, 300), "AR1": ((-160000, -225000), 18000, 280),
    "TX2": ((-150000, 45000), 24000, 300), "AR2": ((-165000, 75000), 20000, 280),
    "SH1": ((250000, -150000), 20000, 300),
    "RNG_A": (A, 3000, 250), "RNG_S": (S, 15000, 350), "RNG_H": (H, 500, 100),
    "FARP_BER": (FARP["FARP Berlin"], 500, 100), "FARP_LON": (FARP["FARP London"], 500, 100),
}
waypoints = {k: {"type": "Turning Point", "action": "Turning Point", "alt": round(ft * 0.3048), "alt_type": "BARO",
                 "speed": round(kt * KT, 1), "speed_type": "TAS", "x": p[0], "y": p[1], "name": k}
             for k, (p, ft, kt) in WP.items()}
settings = {
    "blue_planes": {"category": "plane", "coalition": "blue", "waypoints": ["TX1", "AR1", "TX2", "AR2", "RNG_A", "RNG_S"]},
    "blue_helicopters": {"category": "helicopter", "coalition": "blue", "waypoints": ["FARP_BER", "RNG_H", "FARP_LON"]},
    "red_planes": {"category": "plane", "coalition": "red", "waypoints": ["SH1"]},
}
HEADER = """# Plans de vol injectés dans les groupes joueurs (Open Training Golfe Persique) — écrit par tools/gen_13_waypoints.py.
# TX1/AR1/TX2/AR2 = début de piste des ravitailleurs bleus ; SH1 = ravitailleur rouge ; RNG_H/A/S = champs de tir
# hélicoptères (Berlin), attaque (Tarif), SEAD (Al Qua'a) ; FARP_BER / FARP_LON = FARP Berlin et London. Le build
# ajoute le BULLSEYE (Grande Tunb) à chaque plan.
"""
if __name__ == "__main__":
    with open(M + "/src/waypoints.yaml", "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump({"waypoints": waypoints, "settings": settings}, f, allow_unicode=True, sort_keys=False)
    print("waypoints.yaml :", len(waypoints), "points,", len(settings), "plans")
