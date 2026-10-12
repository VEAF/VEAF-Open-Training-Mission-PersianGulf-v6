# Retours pour VMCT — construction de l'OT Golfe Persique v6 (12/10/2026)

Tenu au fil de la construction (prompt `new-open-training-mission.fr.md`, veaf-tools 6.29.0 installé par `scaffold_mission`, actions MCP sur VMCT `develop` 1bc3d423).
Chaque entrée : quoi, où, comment je l'ai vu, ce que j'ai fait à la place.

1. **`capabilities` annonce 6.28.0 alors que les outils installés et le code du serveur sont en 6.29.0.**
   Vu au premier appel ; `scaffold_mission` a bien installé 6.29.0 (`veaf_tools_version` de sa réponse). Le numéro du serveur MCP est resté en arrière.
2. **Pas de grille d'altitude livrée pour PersianGulf**, alors que c'est l'un des trois théâtres qui ont des données de parking.
   `terrain_elevation` : `available: false`. Balayée avec David devant DCS (`veaf-tools dcs terrain-sweep PersianGulf`, 5 min 45, 34 M points, 10 Mo dans `~/.veaf/terrain/`). La grille pourrait être livrée avec les outils, comme les parkings.
3. **La grille ne distingue pas une terre au niveau de la mer d'un bras de mer : les deux valent 0 m.**
   Sur la côte ouest d'Abu Dhabi (sebkha, lagunes), l'ancien champ de tir de la v5 tombe sur un damier de 0 et de 2-13 m. Un test « terre = au-dessus de 0 » refuse donc des terres réelles, et un test « mer = 0 » accepterait une sebkha. J'ai placé les champs de tir à l'intérieur des terres (sol à 13-110 m). La sonde `land.getSurfaceType` (3 = eau) lèverait l'ambiguïté si le balayage l'enregistrait.
4. **`add_group` avertit « is in the sea » pour des plates-formes pétrolières** (`Oil rig`, `Gas platform`), qui sont en mer par nature (zone Z17).
   Avertissement ignoré ; l'action pourrait reconnaître les types offshore (catégorie `Heliports` posée en mer).
5. **L'alias d'unité `sa18` et la commande `-sa18` ne posent pas le même type.**
   `list_shortcuts` : unité `sa18` → `SA-18 Igla-S manpad` ; commande `-sa18` → `_spawn group, name sa18_squad` → `SA-18 Igla manpad`. J'avais pris le premier comme porteur ; `tools/verify.py` l'a refusé. Aucune action ne change le type d'une unité existante : corrigé par `tools/fix_sa18_carriers.py` (table chargée, modifiée, réécrite). `list_shortcuts` pourrait donner, pour chaque commande, le type du lanceur à prendre comme porteur.
6. **`list_shortcuts` ne donne pas la composition des groupes**, alors que le prompt demande de vérifier ce qu'un alias génère vraiment.
   `tools/verify.py` lit `veaf_libs/data/veaf-units.yaml` directement pour comparer porteur et groupe généré.
7. **Le gabarit 6.29 coupe tous les presets rouges** (`presets_assignments: red: plane: all: none`, `helicopter: all: none`), sans commentaire dans le fichier.
   Une mission où le rouge vole (cas prévu par le prompt, 4.1) n'a alors aucun preset rouge, sans un mot. Vu en relisant le gabarit avant de le réécrire ; `tools/gen_12_presets.py` garde l'affectation bleue (Mi-8, CH-47) et retire l'exclusion rouge. L'OT Mariannes réécrivait tout `presets.yaml` sans ces sections, ce qui a perdu au passage le jeu de radios du CH-47.
8. **Le catalogue livré de slots dynamiques contient le MB-339**, mod communautaire, que `list_unit_types` connaît pourtant (la base d'unités a dû être extraite d'une installation où il est installé).
   Le contrôle « type absent de la base = mod » ne l'attrape donc pas (il attrape A-4E-C, OV-10A, T-45, comme aux Mariannes). Retiré à la main (`tools/gen_14_slots_dynamiques.py`).
9. **`geocode` tombe sur des homonymes sans le signaler** (déjà vu aux Mariannes) : « Hajiabad, Hormozgan » → un quartier de Parsian ; « Liwa Oasis » → un immeuble de Dubaï ; « Masafi » → une station-service de Dubaï ; « Kerman » → la province.
   Remplacés par les coordonnées géographiques réelles dans `tools/lib.py`, convertis par `latlon_to_xy`.
10. **`describe_known_limitations` rend 72 000 caractères**, au-delà de ce qu'un client MCP affiche : la réponse a été versée dans un fichier, à relire par morceaux.
    Un mode résumé (id, titre, contournement) suffirait pour la lecture de départ.
11. **`veaf-tools dcs inject-bridge` attend « Appuyez sur Entrée pour quitter... » même lancé par un script**, sans console.
    Vu dans la sortie de `tools/make_test_mission.py` ; le processus finit quand même (entrée standard fermée), mais un appel depuis un terminal interactif resterait bloqué.
12. **Une variante `clearsky` est identique à sa jumelle réelle quand le METAR n'a pas de nuage**, ce qui est le cas courant dans le Golfe.
    Le 12/10/2026, OMAA donnait `NSC` : les quatre paires réel / réel-dégagé sont sorties identiques dans les champs que DCS lit (`tools/verify.py`). Ce n'est pas un défaut du build, mais le prompt exige des variantes différentes : le build pourrait signaler une variante `clearsky` sans effet, et le prompt dire de ne pas en prévoir sur un théâtre au ciel souvent clair.
13. **`add_group` ne cale pas un convoi sur la route, et la règle « points 2+ On Road » laisse le premier tronçon à travers champs.**
    Sonde en jeu du 12/10/2026 : départs à 7 km (Minab) et 3 km (Jask) de la route la plus proche, chef de file hors route après 99 s, 2,4 m/s au lieu de 5,5. Corrigé par `tools/fix_convoys_on_road.py` avec les points que DCS donne (`land.getClosestPointOnRoads`, par le pont) et tous les points en « On Road » ; à la seconde sonde, les trois convois étaient sur la route dès la première minute. Le prompt est corrigé (VMCT `b8f342c4`). Une option `snap_to_road` de `add_group` / `create_combat_zone`, appuyée sur un relevé du réseau routier, éviterait le passage par DCS.
14. **Aucune action ne déplace ensemble une zone de combat, ses groupes et leurs routes.** `set_group_properties` déplace l'ancre d'un groupe, `edit_zone` le cercle, `edit_route set` un point à la fois : recaler un convoi demande trois actions et un calcul de décalage, d'où le script ci-dessus.
15. **Les scripts de sonde en jeu de GermanyCW (`test_en_jeu.py`) supposent ses noms** : CAP nommées « CAP … » et missions « /good/2 », alors que `create_cap_mission` et VEAF donnent « CAP-… » et « /Good/2 ». Le premier passage a rendu « 0 sur 0 CAP » sans erreur. Et `statics` lu juste après `activate` déclare 48 statiques manquantes : elles apparaissent en différé. Ces sondes mériteraient d'entrer dans VMCT (`veaf-tools dcs probe …`), avec les attentes et les noms lus dans la mission.
