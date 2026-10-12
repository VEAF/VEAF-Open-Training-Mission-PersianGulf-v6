"""Lot 06 : défense aérienne permanente des bases et des arrières (#veafInterpreter).

Porteur = le lanceur que génère l'alias (l'éditeur montre son cercle de portée), nom unique.
Portées DCS (list_unit_types, threat_range_m) : Patriot 54 nm, SA-10 65 nm, SA-11 27 nm, Hawk 24 nm,
SA-15 8,6 nm, NASAMS 8,1 nm. Aucune ne doit couvrir une base adverse avec slots : Khasab est à 63 nm de
Bandar Abbas, donc Hawk à Khasab (un Patriot y couvrirait Bandar Abbas à 9 nm près) ; les SA-10 rouges sont à
Lar et à 90 km au nord de Bandar Abbas. Le contrôle des distances est check_portees.py.
Chaque emplacement est ramené sur la terre ferme (grille DCS) à `spot()`.
"""
from lib import AIRFIELDS, BLUE, PLACES, RED_IR, Batch, interp_unit, land, spot, xy

A = AIRFIELDS

# (camp, nom de groupe, centre, relèvement, distance (m), alias, type du porteur, cap)
SITES = [
    # ── Bleu : Al Dhafra (base mère) ──
    (BLUE, "AD Al Dhafra Patriot", A["Al Dhafra AFB"], 20, 4000, "-patriot", "Patriot ln", 0),
    (BLUE, "AD Al Dhafra Hawk", A["Al Dhafra AFB"], 200, 4500, "-hawk", "Hawk ln", 0),
    (BLUE, "AD Al Dhafra Avenger", A["Al Dhafra AFB"], 110, 2500, "-avenger_squad", "M1097 Avenger", 0),
    # ── Bleu : Al-Bateen, Liwa, Al Ain (arrière) ──
    (BLUE, "AD Al-Bateen NASAMS", A["Al-Bateen"], 160, 2500, "-nasams", "NASAMS_LN_C", 0),
    (BLUE, "AD Al-Bateen Avenger", A["Al-Bateen"], 340, 1800, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Liwa Hawk", A["Liwa AFB"], 30, 4000, "-hawk", "Hawk ln", 30),
    (BLUE, "AD Liwa Avenger", A["Liwa AFB"], 210, 2000, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Al Ain Patriot", A["Al Ain Intl"], 0, 5000, "-patriot", "Patriot ln", 0),
    (BLUE, "AD Al Ain Avenger", A["Al Ain Intl"], 180, 2000, "-avenger_squad", "M1097 Avenger", 0),
    # ── Bleu : Al Minhad, Ras Al Khaimah, Fujairah, Sir Abu Nuayr, Khasab (avant) ──
    (BLUE, "AD Al Minhad Patriot", A["Al Minhad AFB"], 150, 4000, "-patriot", "Patriot ln", 0),
    (BLUE, "AD Al Minhad Avenger", A["Al Minhad AFB"], 330, 2000, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Ras Al Khaimah NASAMS", A["Ras Al Khaimah Intl"], 120, 2500, "-nasams", "NASAMS_LN_C", 0),
    (BLUE, "AD Ras Al Khaimah Avenger", A["Ras Al Khaimah Intl"], 300, 1500, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Fujairah Hawk", A["Fujairah Intl"], 250, 3500, "-hawk", "Hawk ln", 60),
    (BLUE, "AD Fujairah Avenger", A["Fujairah Intl"], 20, 1500, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Sir Abu Nuayr NASAMS", A["Sir Abu Nuayr"], 90, 600, "-nasams", "NASAMS_LN_C", 0),
    (BLUE, "AD Khasab Hawk", A["Khasab"], 180, 3000, "-hawk", "Hawk ln", 0),
    (BLUE, "AD Khasab Avenger", A["Khasab"], 20, 1200, "-avenger_squad", "M1097 Avenger", 0),
    # ── Bleu : guet ──
    (BLUE, "EWR Jebel Jais", PLACES["Jebel Jais"], 0, 0, "-blue_ewr", "FPS-117 Dome", 0),
    (BLUE, "EWR Jebel Hafeet", PLACES["Jebel Hafeet"], 0, 0, "-blue_ewr", "FPS-117 Dome", 0),
    # ── Rouge : Bandar Abbas (base avancée avec slots) ──
    (RED_IR, "AD Bandar Abbas SA-11", A["Bandar Abbas Intl"], 20, 5000, "-sa11", "SA-11 Buk LN 9A310M1", 200),
    (RED_IR, "AD Bandar Abbas Hawk", A["Bandar Abbas Intl"], 300, 6000, "-hawk", "Hawk ln", 200),
    (RED_IR, "AD Bandar Abbas SA-15", A["Bandar Abbas Intl"], 120, 2000, "-sa15", "Tor 9A331", 0),
    (RED_IR, "AD Havadarya SA-15", A["Havadarya"], 330, 1500, "-sa15", "Tor 9A331", 0),
    (RED_IR, "AD Hajiabad SA-10", A["Bandar Abbas Intl"], 15, 90000, "-sa10", "S-300PS 5P85C ln", 200),
    # ── Rouge : Lar et Shiraz (arrière avec slots) ──
    (RED_IR, "AD Lar SA-10", A["Lar"], 60, 6000, "-sa10", "S-300PS 5P85C ln", 180),
    (RED_IR, "AD Lar SA-15", A["Lar"], 240, 2000, "-sa15", "Tor 9A331", 0),
    (RED_IR, "AD Shiraz SA-11", A["Shiraz Intl"], 150, 5000, "-sa11", "SA-11 Buk LN 9A310M1", 180),
    (RED_IR, "AD Shiraz SA-15", A["Shiraz Intl"], 330, 2000, "-sa15", "Tor 9A331", 0),
    # ── Rouge : îles ──
    (RED_IR, "AD Abu Musa SA-15", A["Abu Musa Island"], 60, 1200, "-sa15", "Tor 9A331", 0),
    # ── Rouge : guet ──
    (RED_IR, "EWR Bandar Abbas", A["Bandar Abbas Intl"], 350, 25000, "-ewr", "55G6 EWR", 0),
    (RED_IR, "EWR Bandar Lengeh", PLACES["Bandar Lengeh"], 0, 6000, "-ewr", "55G6 EWR", 0),
    (RED_IR, "EWR Jask", PLACES["Jask"], 0, 4000, "-ewr", "55G6 EWR", 0),
    (RED_IR, "EWR Lar", A["Lar"], 0, 9000, "-ewr", "55G6 EWR", 0),
    (RED_IR, "EWR Shiraz", A["Shiraz Intl"], 90, 8000, "-ewr", "55G6 EWR", 0),
]

if __name__ == "__main__":
    b = Batch()
    for side, name, c, brg, dist, alias, carrier, hdg in SITES:
        p = spot(c, brg, dist, name, margin=300)
        land(p, name, margin=300)
        tag = name.replace("AD ", "").replace("EWR ", "EWR-").replace(" ", "-")
        cmd = f"{alias}, hdg {hdg}" + (", country iran" if side is RED_IR else "")
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p), keep_position=True,
              units=[interp_unit(cmd, carrier, tag)])
        print(f"{name:30} {round(p[0]):>8} {round(p[1]):>8}")
    b.save("06-defense.json")
