"""Extrait de la v5 (lecture seule) les emports des slots de l'arène AirQuake et des ponts → tools/loadouts-v5.json."""
import json
import re
import sys
from pathlib import Path

import paths  # noqa: F401
from veaf_mission_mcp.mission_folder import load_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
V5 = Path(r"D:\dev\_VEAF\VEAF-Open-Training-Mission-PG")
txt = (V5 / "src/mission/l10n/DEFAULT/dictionary").read_text(encoding="utf-8")
d = dict(re.findall(r'\["(DictKey_[^"]+)"\]\s*=\s*"([^"]*)"', txt))
m = load_folder_mission(V5).mission_content
out = {}
for s in m["coalition"].values():
    for c in s.get("country") or []:
        for g in (c.get("plane") or {}).get("group") or []:
            n = d.get(g["name"], g["name"]).strip()
            if "AirQuake" in n or n in ("F-14B Stennis", "F/A-18C Stennis", "AV-8B N/A Tarawa"):
                u = g["units"][0]
                out[n] = {"country": c["name"], "type": u["type"], "pylons": u["payload"]["pylons"], "x": round(g["x"]),
                          "y": round(g["y"]), "alt": u["alt"], "heading": u.get("heading", 0), "n": len(g["units"])}
                print(f"{n:30} {c['name']:8} {u['type']:14} {round(g['x'])} {round(g['y'])} hdg={u.get('heading', 0):.2f}")
(paths.ROOT / "tools/loadouts-v5.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
