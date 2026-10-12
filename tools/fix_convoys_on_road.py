"""Recale les trois convois sur la route : départ et points de passage sur le point de route le plus proche que DCS
donne (land.getClosestPointOnRoads, relevé en jeu par le pont le 12/10/2026), tous les points en « On Road », et le
cercle de la zone centré sur le nouveau départ.

Pourquoi : la sonde en jeu a montré le convoi de Minab à 7 km de la route au départ, celui de Jask à 3 km, et leur
premier tronçon, parti d'un point « Off Road », se faisait à travers champs (2,4 m/s au lieu de 5,5). Aucune action
MCP ne déplace ensemble une zone, son groupe et sa route : chargement de la table, modification, réécriture.
Idempotent (les points sont écrits, pas décalés).
"""
import sys

import paths
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
# zone -> points de route (x, y) : départ puis points de passage, tous sur une route (DCS)
ROAD = {
    "combatZone_ConvoiMinab": [(112923, 38998), (113357, 50790), (108125, 83215)],
    "combatZone_ConvoiLar": [(151653, -188603), (116151, -185532), (49830, -129525)],
    "combatZone_ConvoiJask": [(-47175, 152376), (38073, 85845), (69295, 85362)],
}


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


mission = load_folder_mission(paths.ROOT)
m = mission.mission_content
zones = seq(m["triggers"]["zones"])
done = 0
for zname, pts in ROAD.items():
    z = next(z for z in zones if z["name"] == zname)
    z["x"], z["y"] = pts[0]
    g = next(g for s in m["coalition"].values() for c in s.get("country") or []
             for g in (c.get("vehicle") or {}).get("group") or [] if g["name"] == f"{zname}-Convoi")
    dx, dy = pts[0][0] - g["x"], pts[0][1] - g["y"]
    g["x"], g["y"] = pts[0]
    for u in seq(g["units"]):
        u["x"] += dx
        u["y"] += dy
    route = seq(g["route"]["points"])
    assert len(route) == len(pts), zname
    for p, (x, y) in zip(route, pts):
        p["x"], p["y"] = x, y
        p["action"] = "On Road"
        p["type"] = "Turning Point"
    done += 1
    print(f"{zname}: départ décalé de {round((dx * dx + dy * dy) ** 0.5)} m, {len(pts)} points sur route")
print(save_folder_mission(mission, paths.ROOT)["mission_file"])
