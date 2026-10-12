# Points ouverts

Ce qui reste à vérifier ou à décider, au fil de l'eau. Ce qui concerne les outils part dans le backlog de VMCT (voir `tools/retours-vmct.md`).

## Sonde en jeu du 12/10/2026 (pont dcs-bridge, `tools/test_en_jeu.py`)

- **Sol** : 3 groupes mal posés (Smerch de Minab et radar de Jask dans l'eau, SA-10 de Hajiabad bloqué), déplacés de 150 m sur un point que DCS confirme dégagé (`tools/find_clear.py`) ; resonde : 104 véhicules dégagés, 0 bloqué, 0 dans l'eau.
- **Imbrication des niveaux d'entraînement** : correcte dans les trois familles.
- **Statiques** : 50 sur 50 à leur place (elles apparaissent en différé après l'activation).
- **Navires** : 6 groupes à flot et en route.
- **Convois** : départs recalés sur la route (`tools/fix_convoys_on_road.py`) ; les trois roulent sur la route dès la première minute.
- **Persépolis** (Z18) : modélisée dans DCS (22 objets de décor `PERSEPOLIS_COLUMN` et `PERSEPOLIS_STAIRS` à l'emplacement) ; la zone apparaît bien, sur la terre ferme.
- **CAP** : 4 sur 5 ont tiré sur leur cible en moins de 10 minutes ; la Mirage 2000 d'Abu Dhabi pas encore (cible à 32 km qui s'éloignait), à revoir.

## À vérifier dans DCS

- **QRA** : décollage de la piste et patrouille sur le cercle (non testé).
- **Dessins F10** : 76 objets (front, contours et étiquettes des zones, QRA, sanctuaires, arène, hippodromes) — ils ne se voient qu'en jeu.
- **CAP bleue Mirage 2000** d'Abu Dhabi : engage-t-elle ?
