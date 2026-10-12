"""Lot 18 : la zone Z18 Tourisme — Persépolis (décrite dans gen_08_zones.py) et son dessin F10."""
import gen_08_zones as z
from gen_16_dessins import LABEL_BG, RED
from lib import RED_IR, Batch, position_text, tankers_text, xy

if __name__ == "__main__":
    name, c, r, fname, menu, text, side, cat, groups, statics, extra = next(x for x in z.ZONES if x[0] == "combatZone_Persepolis")
    b = Batch()
    b.act("create_combat_zone", zone_name=name, position=xy(c), radius=r, groups=groups, **RED_IR, category=cat,
          combat_zone={"friendly_name": fname, "radio_group_name": menu, "training": False,
                       "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"})
    b.act("add_map_drawing", layer="Common", shape="circle", name=f"Zone {name}", position=xy(c), radius=r, color=RED,
          fill_color="0xcc000018", thickness=3)
    b.act("add_map_drawing", layer="Common", shape="textbox", name=f"Zone {name} étiquette", position=xy((c[0] + r + 800, c[1])),
          text=fname, color=RED, fill_color=LABEL_BG, font_size=11)
    b.save("18-persepolis.json")
