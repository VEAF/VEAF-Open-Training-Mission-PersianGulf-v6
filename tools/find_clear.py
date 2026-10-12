"""Cherche, dans DCS (pont dcs-bridge), le point dégagé le plus proche d'un groupe : terre (land.getSurfaceType == LAND,
sur un cercle de 60 m) et place libre (Disposition.getSimpleZones, un point libre de 5 m dans 20 m).
Anneaux de 150 m en 150 m jusqu'à 2 km. Usage : python find_clear.py <nom de groupe> [...]"""
import json
import sys

from paths import ROOT  # noqa: F401
from probe_scenery import exec_lua
from veaf_mission_mcp.mission_folder import load_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
m = load_folder_mission(ROOT).mission_content
pos = {}
for s in m["coalition"].values():
    for c in s.get("country") or []:
        for g in (c.get("vehicle") or {}).get("group") or []:
            pos[g["name"]] = (g["x"], g["y"])
LUA = """local c = {x=%f, y=%f}
local function ok(x, y)
  for a = 0, 7 do
    local px, py = x + 60 * math.cos(a * math.pi / 4), y + 60 * math.sin(a * math.pi / 4)
    if land.getSurfaceType({x = px, y = py}) ~= land.SurfaceType.LAND then return false end
  end
  if land.getSurfaceType({x = x, y = y}) ~= land.SurfaceType.LAND then return false end
  local z = Disposition.getSimpleZones({x = x, y = land.getHeight({x = x, y = y}), z = y}, 20, 5, 1)
  return z ~= nil and #z > 0
end
if ok(c.x, c.y) then return '=' .. net.lua2json({c.x, c.y, 0}) end
for r = 150, 2000, 150 do
  local n = math.floor(2 * math.pi * r / 150)
  for i = 0, n - 1 do
    local a = 2 * math.pi * i / n
    local x, y = c.x + r * math.cos(a), c.y + r * math.sin(a)
    if ok(x, y) then return '=' .. net.lua2json({x, y, r}) end
  end
end
return '=null'"""
for name in sys.argv[1:]:
    x, y = pos[name]
    r = json.loads(exec_lua(LUA % (x, y))[1:])
    print(name, (round(x), round(y)), "->", None if r is None else (round(r[0]), round(r[1]), f"{r[2]} m"))
