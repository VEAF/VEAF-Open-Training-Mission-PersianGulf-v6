"""Corrige le type des porteurs #command="-sa18" : la commande pose l'escouade sa18_squad (« SA-18 Igla manpad »),
pas l'unité de l'alias sa18 (« SA-18 Igla-S manpad ») — relevé par verify.py. Aucune action MCP ne change le type
d'une unité : chargement de la table, modification, réécriture. Idempotent."""
import sys

import paths
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
mission = load_folder_mission(paths.ROOT)
n = 0
for side in mission.mission_content["coalition"].values():
    for c in side.get("country") or []:
        for g in (c.get("vehicle") or {}).get("group") or []:
            for u in g["units"]:
                if '#command="-sa18' in u["name"] and u["type"] != "SA-18 Igla manpad":
                    u["type"] = "SA-18 Igla manpad"
                    n += 1
print(n, "porteurs corrigés")
if n:
    print(save_folder_mission(mission, paths.ROOT))
