"""Lot 16 : dessins F10 (add_map_drawing, pour qu'ils survivent au build).

Chaque zone a son contour à son rayon réel ET son étiquette ; ligne de front, sanctuaires, QRA, hippodromes de
soutien, arène. Étiquettes sur fond clair opaque (sans fond, l'action met du noir à moitié transparent et le texte
sombre devient illisible, Caucase 29/09/2026). Pas de trait en tirets : add_map_drawing n'écrit que du plein
(VMCT FIX-OPEN-TRAINING-CAUCASUS-FINDINGS ticket 03).
Couches : Common pour ce que les deux camps partagent (front, zones, sanctuaires, QRA, arène), Blue / Red pour
les hippodromes de soutien de chaque camp. Adapté de l'OT Mariannes.
"""
import gen_07_entrainement as e
import gen_08_zones as z
from gen_09_qra_cap import QRAS
from gen_10_joueurs import ARENA, SANCTUARIES
from lib import TANKERS, Batch, xy

LABEL_BG = "0xffffffe0"
RED, BLUE, ORANGE, GREEN, MAGENTA = "0xcc0000ff", "0x0040ccff", "0xe07000ff", "0x008000ff", "0xb000b0ff"


def above(c, r, gap=800):
    return (c[0] + r + gap, c[1])


b = Batch()


def circle(layer, name, c, r, color, fill="0x00000000", thickness=3):
    b.act("add_map_drawing", layer=layer, shape="circle", name=name, position=xy(c), radius=r, color=color,
          fill_color=fill, thickness=thickness)


def label(layer, name, p, text, color, size=12):
    b.act("add_map_drawing", layer=layer, shape="textbox", name=name, position=xy(p), text=text, color=color,
          fill_color=LABEL_BG, font_size=size)


# ── front (approximatif) : la ligne médiane du Golfe, au sud des îles tenues par l'Iran (Lavan, Kish, Sirri,
# Abu Musa, les Tunb), au nord de Musandam, puis la médiane de la mer d'Oman au sud de Jask ──
FRONT = [(20000, -340000), (-20000, -260000), (-60000, -195000), (-55000, -130000), (-40000, -80000),
         (5000, -40000), (40000, 0), (25000, 35000), (-30000, 85000), (-100000, 140000), (-160000, 190000)]
b.act("add_map_drawing", layer="Common", shape="line", name="Front", points=[xy(q) for q in FRONT], color=RED,
      thickness=6)
label("Common", "Front étiquette", (-75000, -150000), "FRONT (approximatif) : le Golfe et le détroit d'Ormuz", RED, 14)

# ── zones d'entraînement : un cercle et une étiquette par famille (niveaux imbriqués sur le même cercle) ──
for zone, c, r, fname, *_ in e.ZONES:
    if not zone.endswith("_Easy"):
        continue
    fam = fname.split()[0][0]
    text = {"H": "H1-H3 Entraînement hélicoptères — Berlin", "A": "A1-A3 Entraînement attaque — Tarif",
            "S": "S1-S3 Entraînement SEAD — Al Qua'a"}[fam]
    circle("Common", f"Zone {zone[:-5]}", c, r, ORANGE, "0xe0700018")
    label("Common", f"Zone {zone[:-5]} étiquette", above(c, r), text, ORANGE)

# ── vraies zones de combat ──
for zone, c, r, fname, *_ in z.ZONES:
    circle("Common", f"Zone {zone}", c, r, RED, "0xcc000018")
    label("Common", f"Zone {zone} étiquette", above(c, r), fname, RED, 11)

# ── QRA ──
for q in QRAS:
    col = MAGENTA if q["side"]["coalition"] == "red" else BLUE
    circle("Common", f"QRA {q['name']}", q["center"], q["radius"], col, thickness=2)
    label("Common", f"QRA {q['name']} étiquette", (q["center"][0] + q["radius"] - 6000, q["center"][1]),
          f"{q['name']} ({round(q['radius'] / 1852)} nm)", col, 11)

# ── sanctuaires ──
for name, tz, c, r, side in SANCTUARIES:
    circle("Common", name, c, r, GREEN, "0x00800018", thickness=2)
    label("Common", f"{name} étiquette", (c[0] - r - 1500, c[1]), name, GREEN, 10)

# ── arène ──
circle("Common", "Arène cercle", ARENA[0], ARENA[1], GREEN, thickness=3)
label("Common", "Arène étiquette", above(ARENA[0], ARENA[1], 3000), "ARÈNE joueurs contre joueurs (slots en vol)", GREEN, 14)

# ── hippodromes de soutien ──
TRACKS = [
    ("Blue", n, ab[0], ab[1], f"{n} — {tac} — U{f:.1f} — FL{fl}") for n, (ab, fl, tac, f, k) in TANKERS.items()
] + [
    ("Blue", "Overlord 1", (-200000, -140000), (-200000, -60000), "Overlord 1 AWACS — U282.0"),
    ("Blue", "Magic 1", (-210000, 50000), (-160000, 110000), "Magic 1 AWACS — U283.0"),
    ("Red", "Shell 1", (250000, -150000), (250000, -60000), "Shell 1 IL-78 — U294.0 — FL200"),
    ("Red", "Wizard 1", (320000, -120000), (320000, -20000), "Wizard 1 AWACS — U284.0"),
]
for layer, n, a, bb, text in TRACKS:
    col = BLUE if layer == "Blue" else RED
    b.act("add_map_drawing", layer=layer, shape="line", name=f"Piste {n}", points=[xy(a), xy(bb)], color=col,
          thickness=4)
    label(layer, f"Piste {n} étiquette", ((a[0] + bb[0]) / 2, (a[1] + bb[1]) / 2 + 6000), text, col, 10)

if __name__ == "__main__":
    b.save("16-dessins.json")
