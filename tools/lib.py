"""Outils communs aux générateurs de lots (tools/gen_*.py).

Un générateur écrit un fichier de lot dans tools/batches/ ; `python tools/mcp.py batch <lot>` l'exécute
sur le catalogue d'actions de veaf-mission-mcp (code VMCT de develop). Un lot ne s'exécute qu'une fois.

Terre / mer : la grille d'altitude PersianGulf balayée dans DCS le 12/10/2026
(`veaf-tools dcs terrain-sweep PersianGulf`, 250 m) ; la mer y vaut 0 m.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT  # noqa: E402  (met aussi le code VMCT sur sys.path)
from veaf_libs.coordinates import latlon_to_xy, xy_to_latlon  # noqa: E402
from veaf_libs.terrain_elevation import grid_for_theatre  # noqa: E402

M = ROOT.as_posix()
THEATRE = "PersianGulf"

BLUE = dict(coalition="blue", country_id=2, country_name="USA")
BLUE_UAE = dict(coalition="blue", country_id=74, country_name="United Arab Emirates")
BLUE_OMAN = dict(coalition="blue", country_id=73, country_name="Oman")
RED = dict(coalition="red", country_id=0, country_name="Russia")       # CTLD veut la Russie dans le camp rouge
RED_IR = dict(coalition="red", country_id=34, country_name="Iran")

# Aérodromes (list_airfields, PersianGulf)
AIRFIELDS = {
    "Abu Dhabi Intl": (-188457, -162031), "Abu Musa Island": (-31505, -121335), "Al Ain Intl": (-211058, -65421),
    "Al Dhafra AFB": (-211028, -173240), "Al Maktoum Intl": (-140128, -110069), "Al Minhad AFB": (-126014, -89133),
    "Al-Bateen": (-190947, -181928), "Bandar Abbas Intl": (115766, 14258), "Bandar Lengeh": (41536, -140987),
    "Bandar-e-Jask": (-57247, 156197), "Dubai Intl": (-100594, -88875), "Fujairah Intl": (-117532, 7939),
    "Havadarya": (109298, -6279), "Jiroft": (282608, 141685), "Kerman": (454117, 71096), "Khasab": (-220, -178),
    "Kish Intl": (42784, -225094), "Lar": (168978, -182360), "Lavan Island": (75790, -286801),
    "Liwa AFB": (-275766, -248214), "Qeshm Island": (64801, -33384), "Quasoura_airport": (-374897, -123073),
    "Ras Al Khaimah Intl": (-61625, -30796), "Sas Al Nakheel": (-189610, -175974), "Sharjah Intl": (-92544, -73374),
    "Shiraz Intl": (381101, -351636), "Sir Abu Nuayr": (-103103, -202973), "Sirri Island": (-26946, -170745),
    "Tunb Island AFB": (10515, -92440), "Tunb Kochak": (9023, -109467),
}
BLUE_SLOTS = ["Al Dhafra AFB", "Al Minhad AFB", "Liwa AFB", "Al-Bateen", "Al Ain Intl", "Fujairah Intl",
              "Ras Al Khaimah Intl", "Sir Abu Nuayr", "Khasab"]
BLUE_NO_SLOTS = ["Abu Dhabi Intl", "Dubai Intl", "Sharjah Intl", "Al Maktoum Intl", "Sas Al Nakheel"]
NEUTRAL = ["Quasoura_airport"]
RED_SLOTS = ["Bandar Abbas Intl", "Lar", "Shiraz Intl"]
RED_NO_SLOTS = ["Havadarya", "Qeshm Island", "Bandar Lengeh", "Kish Intl", "Lavan Island", "Jiroft", "Kerman",
                "Bandar-e-Jask", "Abu Musa Island", "Tunb Island AFB", "Tunb Kochak", "Sirri Island"]

_GEO = json.loads((ROOT / "tools/places.json").read_text(encoding="utf-8"))
PLACES = {k: (v["x"], v["y"]) for k, v in _GEO.items()}
# Géocodage tombé sur un homonyme : coordonnées géographiques réelles (Wikipédia), converties
for _n, (_la, _lo) in {"Hajiabad": (28.3092, 55.9017), "Liwa Oasis": (23.1333, 53.7833),
                       "Masafi": (25.3167, 56.1667), "Kerman city": (30.2839, 57.0834)}.items():
    PLACES[_n] = tuple(round(c) for c in latlon_to_xy(THEATRE, _la, _lo))

# Bullseye commun : la Grande Tunb, au milieu du front (geocode « Greater Tunb »)
BULLSEYE = PLACES["Greater Tunb"]


def nm(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1852


def km(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1000


def off(p, brg, m):
    """Point à `m` mètres de `p`, au relèvement `brg` (degrés vrais, x = nord, y = est)."""
    r = math.radians(brg)
    return (p[0] + m * math.cos(r), p[1] + m * math.sin(r))


def bearing(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def bullseye(p):
    """« 123°/45 nm » depuis le bullseye : cap = atan2(Δy, Δx)."""
    return f"{bearing(BULLSEYE, p):03.0f}°/{nm(BULLSEYE, p):.0f} nm"


def xy(p):
    return {"x": round(p[0]), "y": round(p[1])}


_GRID = None


def ground(x, y):
    global _GRID
    if _GRID is None:
        _GRID = grid_for_theatre(THEATRE)
        if _GRID is None:
            raise SystemExit("pas de grille d'altitude PersianGulf (veaf-tools dcs terrain-sweep PersianGulf)")
    return _GRID.elevation_at(x, y)


def _ring(p, r, n=12):
    return [p] + [(p[0] + r * math.cos(2 * math.pi * i / n), p[1] + r * math.sin(2 * math.pi * i / n))
                  for i in range(n)]


def is_land(p, margin=300):
    """Terre ferme : le point et un cercle de `margin` m autour sont au-dessus de 0 m (la mer vaut 0)."""
    return all((ground(*q) or 0) > 0 for q in _ring(p, margin))


def is_sea(p, margin=1000):
    return all((ground(*q) or 0) <= 0 for q in _ring(p, margin, 16))


def land(p, what, margin=300):
    if not is_land(p, margin):
        raise SystemExit(f"PAS SUR LA TERRE FERME (marge {margin} m) : {what} {p}")
    return p


def sea(p, what, margin=1500):
    if not is_sea(p, margin):
        raise SystemExit(f"PAS EN PLEINE MER (marge {margin} m) : {what} {p}")
    return p


def nearest_land(x, y, margin=300, step=100, max_r=6000):
    """Le point à terre le plus proche de (x, y), à `margin` m au moins de l'eau (anneaux croissants)."""
    if is_land((x, y), margin):
        return (x, y)
    r = step
    while r <= max_r:
        n = max(8, int(2 * math.pi * r / step))
        for i in range(n):
            a = 2 * math.pi * i / n
            p = (x + r * math.cos(a), y + r * math.sin(a))
            if is_land(p, margin):
                return (round(p[0]), round(p[1]))
        r += step
    return None


def spot(center, brg, dist, what, margin=150):
    """Point à `dist` m de `center` au relèvement `brg`, ramené sur la terre ferme la plus proche."""
    p = off(center, brg, dist)
    q = nearest_land(p[0], p[1], margin=margin)
    if q is None:
        raise SystemExit(f"pas de terre près de {what} {p}")
    return q


class Batch:
    def __init__(self):
        self.items = []

    def act(self, action, **params):
        self.items.append({"name": action, "params": {"mission_path": M, **params}})

    def save(self, name):
        path = ROOT / "tools/batches" / name
        if path.exists():
            raise SystemExit(f"{path.name} existe déjà : un lot ne se régénère pas après exécution (doublons)")
        path.write_text(json.dumps(self.items, indent=1, ensure_ascii=False), encoding="utf-8")
        print(len(self.items), "actions ->", path.relative_to(ROOT))


def cmd_unit(alias_cmd, carrier_type, tag, extra=""):
    """Faux porteur de zone : `#command="<alias ...>"` + balises de tirage + suffixe unique."""
    name = f'#command="{alias_cmd}"'
    if extra:
        name += " " + extra
    return {"type": carrier_type, "name": f"{name} #{tag}"}


def interp_unit(alias_cmd, carrier_type, tag):
    """Porteur permanent : `#veafInterpreter["<alias ...>"]` + suffixe unique."""
    return {"type": carrier_type, "name": f'#veafInterpreter["{alias_cmd}"] #{tag}'}


def seg_nm(p, a, b):
    """Distance (nm) du point p au segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy) / 1852


def ddm(p):
    """« N25°11.051' E055°45.729' » (degrés, minutes décimales : ce que saisissent la plupart des avions)."""
    lat, lon = xy_to_latlon(THEATRE, *p)

    def one(v, pos, neg, w):
        h = pos if v >= 0 else neg
        v = abs(v)
        d = int(v)
        return f"{h}{d:0{w}d}°{(v - d) * 60:06.3f}'"
    return f"{one(lat, 'N', 'S', 2)} {one(lon, 'E', 'W', 3)}"


def position_text(p):
    return f"Position : bullseye {bullseye(p)} ({ddm(p)})."


# Ravitailleurs bleus : extrémités de l'hippodrome, FL, TACAN, MHz, type de ravitaillement (gen_05_soutien.py)
TANKERS = {
    "Texaco 1": (((-130000, -240000), (-130000, -180000)), 220, "50Y", 290.0, "perche"),
    "Arco 1": (((-160000, -225000), (-160000, -165000)), 180, "51Y", 291.0, "panier"),
    "Texaco 2": (((-150000, 45000), (-90000, 45000)), 240, "52Y", 292.0, "perche"),
    "Arco 2": (((-165000, 75000), (-105000, 75000)), 200, "53Y", 293.0, "panier"),
}


def tankers_text(p):
    """« Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 12 nm ; Texaco 1 (...) à 30 nm. » — le plus proche de
    chaque type, mesuré jusqu'à sa piste."""
    out = []
    for kind in ("panier", "perche"):
        n, (ab, fl, tacan, f, k) = min(((n, v) for n, v in TANKERS.items() if v[4] == kind),
                                       key=lambda kv: seg_nm(p, *kv[1][0]))
        out.append(f"{n} ({kind}, TACAN {tacan}, {f:.1f}) à {seg_nm(p, *ab):.0f} nm")
    return "Ravitailleurs : " + " ; ".join(out) + "."
