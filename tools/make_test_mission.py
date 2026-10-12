"""Construit la mission de test locale : profil LOCAL_TEST + game master + un A-10C II en slot classique + dcs-bridge.

Les slots dynamiques ne fonctionnent qu'en multijoueur : un test en solo a besoin d'un slot `Client` classique.
Ces ajouts vont dans la COPIE DE TEST seulement, jamais dans les sources : le build serveur ne doit pas les gagner.

Usage (depuis le dossier de la mission, environnement poetry de VMCT) :
    poetry -C ../VEAF-Mission-Creation-Tools run python "$PWD/tools/make_test_mission.py"
Sortie : bridge/bridge-PersianGulf-OT.miz.
"""

import glob
import os
import shutil
import subprocess
import sys

from paths import ROOT
from mission_tools.miz_tools import read_miz, write_miz
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
BRIDGE_LUA = os.environ.get("BRIDGE_LUA", str(ROOT.parent / "VEAF-dcs-bridge" / "src" / "lua" / "dcs-bridge.lua"))
OUT = ROOT / "bridge" / "bridge-PersianGulf-OT.miz"
EXE = str(ROOT / "veaf-tools.exe")

# le build LOCAL_TEST réécrit src/scripts/veaf-config.lua (sécurité coupée, logs debug) : on garde la copie des
# sources et on la remet, pour qu'un commit après un test n'embarque jamais la configuration de test
CONFIG = ROOT / "src" / "scripts" / "veaf-config.lua"
config_before = CONFIG.read_bytes()
try:
    subprocess.run([EXE, "mission", "build", "--profile", "LOCAL_TEST"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
finally:
    CONFIG.write_bytes(config_before)
built = max(glob.glob(str(ROOT / "VEAF_OpenTraining_PersianGulf_ICAO_OMAA_2*.miz")), key=os.path.getmtime)
OUT.parent.mkdir(exist_ok=True)
shutil.copy(built, OUT)

# un game master par camp
miz = read_miz(OUT)
miz.mission_content["groundControl"]["roles"]["instructor"] = {"blue": 1, "red": 1, "neutrals": 0}
write_miz(miz, OUT)

# A-10C II, au parking moteur chaud à Al Dhafra (base mère) : PersianGulf a des données de parking dans VMCT
catalog = ActionCatalog()
register_default_actions(catalog)
print(catalog.run_action("add_air_group", dict(
    mission_path=str(OUT), coalition="blue", country_id=2, country_name="USA", name="TEST A-10C II Al Dhafra",
    unit_type="A-10C_2", count=1, start="parking-hot", airfield="Al Dhafra AFB", skill="Client", task="CAS")))

subprocess.run([EXE, "dcs", "inject-bridge", "--bridge-lua", BRIDGE_LUA, str(OUT)], cwd=ROOT, check=True)

# le build LOCAL_TEST a remplacé le .miz serveur du jour : le reconstruire, pour que la mission livrée reste celle du serveur
# journal gardé : un METAR non récupéré n'y est qu'un avertissement, et la variante « réelle » vole alors le ciel par défaut
with open(ROOT / ".veaf-backups" / "build-serveur.log", "w", encoding="utf-8") as log:
    subprocess.run([EXE, "mission", "build"], cwd=ROOT, check=True, stdout=log, stderr=subprocess.STDOUT)
if "METAR" in (ROOT / ".veaf-backups" / "build-serveur.log").read_text(encoding="utf-8", errors="replace"):
    print("ATTENTION : le build serveur parle du METAR, lire .veaf-backups/build-serveur.log")
print("OK", OUT)
