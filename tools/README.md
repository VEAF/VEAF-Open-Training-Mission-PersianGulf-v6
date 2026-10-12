# Outils de la mission

Scripts Python qui ont construit la mission et qui produisent ce qu'on ne tape pas à la main : le briefing, les cartes, la mission de test, les contrôles.
Ils importent le code Python de VMCT : par défaut le dépôt voisin `../VEAF-Mission-Creation-Tools` (branche `develop`), ou le dossier désigné par la variable `VMCT_PY` (le dossier `src/python/veaf-tools` d'un autre checkout).
Ils se lancent depuis `tools/`, avec le Python de l'environnement poetry de VMCT :

```powershell
$PY = (poetry -C ..\..\VEAF-Mission-Creation-Tools env info -p) + "\Scripts\python.exe"
& $PY gather.py
```

Le contrôle terre / mer (`lib.land`, `lib.sea`, `lib.spot`) lit la grille d'altitude PersianGulf de `~/.veaf/terrain/`, balayée une fois dans DCS (`.\veaf-tools.exe dcs terrain-sweep PersianGulf`, 6 minutes).

## Construction (historique, à ne pas rejouer)

Chaque `gen_NN_*.py` écrit un lot d'actions `veaf-mission-mcp` dans `batches/`, que `mcp.py batch batches/<lot>.json` exécute dans le processus.
**Un lot ne se rejoue pas** : `add_group` ne dédoublonne pas, un second passage crée des doublons (les dessins F10, eux, sont refusés par nom). `lib.Batch.save` refuse d'écraser un lot existant.
Le journal de chaque lot est à côté (`batches/<lot>.log`).

| Script | Lot |
|---|---|
| `geocode_places.py` | Lieux réels (`places.json`) ; les homonymes relevés sont remplacés dans `lib.py` |
| `gen_04_bases.py` | Camp des aérodromes, slots dynamiques, FARP Berlin et London |
| `gen_05_soutien.py` | Ravitailleurs, AWACS et leurs escortes, drone Reaper 1, porte-avions (Stennis, Roosevelt, Tarawa) |
| `gen_06_defense.py` | Défense aérienne permanente (`#veafInterpreter`) |
| `gen_07_entrainement.py` | Les 3 familles × 3 niveaux d'entraînement |
| `gen_08_zones.py` | Les 17 vraies zones de combat, drone Reaper 2 |
| `gen_09_qra_cap.py` | QRA et CAP à la demande |
| `gen_10_joueurs.py` | Sanctuaires, arène, slots des ponts, groupes des missions scénarisées |
| `gen_11_config.py` | Blocs ASSETS et SANCTUARY, `combat_missions:`, rayon logistique CTLD, `jtacLaserCodeMax` |
| `gen_12_presets.py`, `gen_13_waypoints.py`, `gen_14_slots_dynamiques.py` | `src/presets.yaml` (+ canaux de base par `set_airfield_channels`), `src/waypoints.yaml`, `src/dynamic-slot-templates.yaml` |
| `gen_15_identite.py`, `gen_16_dessins.py` | Date, bullseye, briefing DCS (rejouable : `gen_15_identite.py <suffixe>`) ; dessins F10 |
| `inert_targets.py`, `ground_control_roles.py`, `fix_sa18_carriers.py` | Cibles inertes (tir interdit, sans dispersion) ; rôles sans avion à 5 par camp ; type des porteurs SA-18 |
| `gen_17` (lot écrit à la main, `batches/17-deplacements-sonde.json`) | Les trois groupes déplacés après la sonde du sol |
| `fix_convoys_on_road.py` | Départ et points des convois sur la route (points relevés dans DCS), tous en « On Road » |
| `gen_18_persepolis.py`, `gen_19_meteo.py` | Zone Z18 Tourisme — Persépolis et son dessin ; météo de base (pas de variantes : le serveur fixe la météo) |
| `extract_v5_loadouts.py` | Emports de l'arène et des ponts de la v5 → `loadouts-v5.json` |

## Après tout changement

| Script | Ce qu'il fait |
|---|---|
| `sync_zones.py` | Réécrit le bloc `COMBATZONE` de `mission.yaml` (noms, menus, inclusions, briefings) depuis `gen_07` et `gen_08`, qui en sont la source |
| `gather.py` | Relève dans la mission tout ce que le briefing affiche → `briefing_data.json` |
| `gen_readme.py` | Écrit `README.md` (le briefing des pilotes) et redessine les cartes par `gen_map.py` |
| `gen_map.py` | Carte générale `docs/carte.jpg` et zooms `docs/cartes/` sur fond OpenStreetMap (tuiles en cache dans `tiles/`, hors dépôt), copiés dans `src/mission/l10n/DEFAULT/` et déclarés dans la mission |
| `check_portees.py` | Portée de chaque défense et de chaque zone face à ce qu'elle ne doit pas atteindre → `docs/portees.md` ; ligne `VERDICT` |
| `check_presets.py` | Plan radio : pas de doublon dans une liste, aucun canal non-aérodrome sur une tour ; ligne `VERDICT` |
| `verify.py` | Contrôles des `.miz` construits (noms, slots, soutien, porteurs, images, météo, sécurité) ; ligne `VERDICT` |
| `make_test_mission.py` | Mission de test locale `bridge/bridge-PersianGulf-OT.miz` (LOCAL_TEST, game master, A-10C II à Al Dhafra, dcs-bridge), puis rebuild serveur |
| `inspect_groups.py [filtre]` | Relecture des groupes de la mission (type, indicatif, altitude, tâches) |
| `test_en_jeu.py <étape>`, `probe_scenery.py` | Sonde en jeu par le pont dcs-bridge (repris de GermanyCW) : `probe` (sol sous les véhicules, en premier), `nesting`, `activate`, `statics`, `ships`, `convoys` (deux fois, une minute d'écart), `cap` puis `cap-result` (5 à 10 minutes après) |
| `find_clear.py <groupe> …` | Demande à DCS le point dégagé le plus proche d'un groupe (terre, place libre) |

Ordre : `sync_zones.py`, `gather.py`, `gen_readme.py`, build serveur (`.\veaf-tools.exe mission build`, les cartes sont dans le `.miz`), `check_portees.py`, `check_presets.py`, `verify.py`.

`retours-vmct.md` : ce que la construction a appris sur les outils, à reporter dans le backlog de VMCT.
