"""Géocode une fois les lieux réels dont la mission a besoin → tools/places.json (x/y DCS).

Relancer ajoute seulement les lieux absents. Chaque point est à relire : l'outil peut tomber sur un
homonyme (osm_type et nom affiché sont gardés pour ça).
"""
import json
import sys

from paths import ROOT  # noqa: F401  (met aussi le code VMCT sur sys.path)
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
PLACES = [
    # Iran — côte et îles
    "Qeshm, Hormozgan", "Laft, Qeshm", "Dargahan", "Bandar Lengeh", "Bandar Abbas", "Shahid Rajaee Port",
    "Minab", "Hajiabad, Hormozgan", "Jask", "Kish Island", "Lavan Island", "Abu Musa Island",
    "Greater Tunb", "Lesser Tunb", "Larak Island", "Hormuz Island", "Hengam Island", "Sirri Island",
    "Bandar Khamir", "Kong, Hormozgan", "Parsian, Hormozgan", "Bastak", "Gerash", "Lar, Fars",
    "Jiroft", "Kahnuj", "Rudan, Hormozgan", "Sirik", "Bandar-e Jask", "Kerman", "Sirjan", "Baft",
    "Jahrom", "Shiraz", "Persepolis", "Marvdasht", "Darab", "Fasa", "Khonj",
    # EAU / Oman
    "Madinat Zayed, Abu Dhabi", "Liwa Oasis", "Mezairaa", "Ruwais", "Mirfa", "Sweihan", "Al Khatim",
    "Al Wathba", "Hatta", "Dibba Al-Fujairah", "Masafi", "Jebel Jais", "Ras Musandam", "Kumzar", "Bukha",
    "Khasab", "Al Hamra, Ras Al Khaimah", "Ghayathi", "Sila, Abu Dhabi", "Jebel Hafeet", "Al Qua'a",
    "Umm al Zumul", "Habshan", "Bab, Abu Dhabi", "Tarif, Abu Dhabi", "Jebel Dhanna",
]
out_path = ROOT / "tools" / "places.json"
places = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
cat = ActionCatalog()
register_default_actions(cat)
for q in PLACES:
    if q in places:
        continue
    try:
        r = cat.run_action("geocode", {"mission_path": str(ROOT), "query": q})
    except Exception as e:  # noqa: BLE001
        print("ERREUR", q, e)
        continue
    if not r.get("found"):
        print("INTROUVABLE", q)
        continue
    places[q] = {"x": round(r["xy"]["x"]), "y": round(r["xy"]["y"]), "osm": r.get("osm_type"), "name": r["display_name"][:90]}
    print(f"{q:28} {places[q]['x']:>8} {places[q]['y']:>8}  {places[q]['osm']:<14} {places[q]['name']}")
    out_path.write_text(json.dumps(places, indent=1, ensure_ascii=False), encoding="utf-8")
