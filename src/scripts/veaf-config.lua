---------------------------------------------------------------------------------------------------------------------------------------------
-- Généré par veaf-tools build depuis mission.yaml
-- Ne pas éditer manuellement.
-- Relancez 'veaf-tools build' ou 'veaf-tools generate-config' pour régénérer.
---------------------------------------------------------------------------------------------------------------------------------------------

-- ── Mission identity ─────────────────────────────────────────────────────────
veaf.config.MISSION_NAME = "VEAF_OpenTraining_PersianGulf_ICAO_OMAA"
veaf.config.era = veaf.ERA.MODERN
veaf.silenceAtcOnAllAirbases()
veaf.HideNamesFromSpawnedGroups = true

veaf.config.language = "fr"

-- ── Airfield channels of the mission's radio plan (src/presets.yaml, `bases`) ──────
if veafAirbases then
    veafAirbases.MissionChannels = {
        [2] = { alias = "Base-Bandar Abbas Intl", title = "Bandar Abbas Intl / 78X", uhf = 251.0, vhf = 118.1, fm = 39.4 },
        [4] = { alias = "Base-Al Dhafra AFB", title = "Al Dhafra AFB / 96X", uhf = 251.1, vhf = 126.5, fm = 39.5 },
        [7] = { alias = "Base-Fujairah Intl", title = "Fujairah Intl", uhf = 251.25, vhf = 124.6, fm = 39.65 },
        [9] = { alias = "Base-Havadarya", title = "Havadarya / 47X", uhf = 251.3, vhf = 123.15, fm = 39.7 },
        [10] = { alias = "Base-Khasab", title = "Khasab", uhf = 250.0, vhf = 124.35, fm = 38.4 },
        [11] = { alias = "Base-Lar", title = "Lar", uhf = 250.05, vhf = 127.35, fm = 38.45 },
        [12] = { alias = "Base-Al Minhad AFB", title = "Al Minhad AFB / 99X", uhf = 250.1, vhf = 118.55, fm = 38.5 },
        [13] = { alias = "Base-Qeshm Island", title = "Qeshm Island", uhf = 250.15, vhf = 118.05, fm = 38.55 },
        [17] = { alias = "Base-Sir Abu Nuayr", title = "Sir Abu Nuayr", uhf = 250.8, vhf = 118.0, fm = 38.7 },
        [19] = { alias = "Base-Shiraz Intl", title = "Shiraz Intl / 94X", uhf = 250.35, vhf = 121.9, fm = 38.8 },
        [23] = { alias = "Base-Al-Bateen", title = "Al-Bateen", uhf = 250.6, vhf = 119.9, fm = 39.05 },
        [24] = { alias = "Base-Kish Intl", title = "Kish Intl / 112X", uhf = 250.65, vhf = 121.65, fm = 39.1 },
        [25] = { alias = "Base-Al Ain Intl", title = "Al Ain Intl", uhf = 250.7, vhf = 119.85, fm = 39.15 },
        [28] = { alias = "Base-Ras Al Khaimah Intl", title = "Ras Al Khaimah Intl", uhf = 250.9, vhf = 121.6, fm = 39.3 },
        [29] = { alias = "Base-Liwa AFB", title = "Liwa AFB / 121X", uhf = 250.95, vhf = 119.3, fm = 39.35 },
    }
end

-- ── Global log level ─────────────────────────────────────────────────────────
veaf.ForcedLogLevel = "info"

-- ── CTLD 2 ───────────────────────────────────────────────────────────────────
-- Configuration lives in ctld-config.yaml (edit it with ctld-tools); this only starts it.
veaf.config.manage_airbase_logistics = true
veaf.config.airbase_logistics_radius = 2500
veaf.config.airbase_occupation_radius = 2000
veaf.config.airbase_logistics_tick = 30
-- One module's initialisation error must not take the others down (FIX-DEMO-MISSION-FINDINGS 02).
local function veafGuardedInit(name, initialize)
    local ok, err = xpcall(initialize, function(e)
        if debug and debug.traceback then
            return debug.traceback(tostring(e), 2)
        end
        return tostring(e)
    end)
    if not ok then
        veaf.loggers.get(veaf.Id):error("%s init failed: %s", name, err)
    end
end

veafGuardedInit("CTLD", function()
if ctld then
    veaf.ctld_initialize()
end
end)

-- ── Module configuration + initialization ────────────────────────────────────

-- ── Core ──

veafGuardedInit("SECURITY", function()
if veafSecurity then
    veafSecurity.initialize()
end
end)

veafGuardedInit("RADIO", function()
if veafRadio then
    veafRadio.initialize(true)
end
end)

veafGuardedInit("SHORTCUTS", function()
if veafShortcuts then
    veafShortcuts.initialize()
end
end)

veafGuardedInit("NAMEDPOINTS", function()
if veafNamedPoints then
    veafNamedPoints.initialize({})
end
end)

veafGuardedInit("SPAWN", function()
if veafSpawn then
    veafSpawn.initialize()
end
end)

-- ── Combat ──

veafGuardedInit("CARRIER", function()
if veafCarrierOperations then
    veafCarrierOperations.initialize(true)
end
end)

veafGuardedInit("CASMISSION", function()
if veafCasMission then
    veafCasMission.initialize()
end
end)

veafGuardedInit("TRANSPORTMISSION", function()
if veafTransportMission then
    veafTransportMission.initialize()
end
end)

veafGuardedInit("COMBATMISSION", function()
if veafCombatMission then
    veafCombatMission.addCapMission("CAP-Qeshm-MiG29", "CAP rouge MiG-29 (Fox 1) — Qeshm — FL220", "Deux MiG-29A armés de R-27R et R-73 patrouillent au-dessus de l'île de Qeshm, au FL220. Emport : R-73*4,R-27R*2,Fuel-1500.", false, true)
    veafCombatMission.addCapMission("CAP-Lengeh-F4", "CAP rouge F-4E (Fox 1) — Bandar Lengeh — FL200", "Deux F-4E armés d'AIM-7 et d'AIM-9 patrouillent au-dessus de Bandar Lengeh et de Kong, au FL200. Emport : AIM-9*4,AIM-7*4,Fuel*2.", false, true)
    veafCombatMission.addCapMission("CAP-Lar-F14", "CAP rouge F-14A (intercepteur haut et rapide, AIM-54) — Lar — FL350", "Deux F-14A armés de Phoenix patrouillent haut et vite au-dessus de Lar, au FL350. Emport : AIM-54C*4,AIM-9*2,AIM-7*2.", false, true)
    veafCombatMission.addCapMission("Raid-Kish-Su24", "Raid rouge Su-24M à intercepter — Kish — FL150", "Deux Su-24M chargés de bombes tournent au-dessus de Kish, au FL150, prêts à frapper Sir Abu Nuayr : les intercepter. Emport : FAB-500*4,R-60M*2.", false, true)
    veafCombatMission.addCapMission("CAP-RAK-F16", "CAP bleue F-16 (Fox 3) — Ras Al Khaimah — FL220", "Deux F-16C patrouillent au-dessus de Ras Al Khaimah et de la base de Musandam, au FL220. Emport : AIM-120C*4, AIM-9M*2, Fuel.", false, true)
    veafCombatMission.addCapMission("CAP-AbuDhabi-M2000", "CAP bleue Mirage 2000-5 (Fox 3) — Abu Dhabi — FL250", "Deux Mirage 2000-5 émiriens couvrent la côte d'Abu Dhabi, au FL250. Emport : R 550*2,MICA AR*4,Fuel*3.", false, true)
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Defense-AlMinhad")
        :setFriendlyName("Défense — raid iranien sur Al Minhad")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Deux Su-24M armés de missiles antiradar ouvrent la route à quatre F-4E chargés de bombes, escortés de deux F-14A, partis de Qeshm vers Al Minhad. Abattez les bombardiers avant le largage.
Échec si la base est bombardée (constaté par vous : la mission ne le vérifie pas).]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("SEAD")
            :setGroups({"SC-Defense-AlMinhad-SEAD"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Bombardiers")
            :setGroups({"SC-Defense-AlMinhad-Bombers"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Defense-AlMinhad-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Interception-VIP")
        :setFriendlyName("Interception — transport VIP de Bandar Abbas à Shiraz")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Un IL-76 emmène l'état-major des Gardiens de la révolution de Bandar Abbas vers Shiraz, escorté par deux MiG-29A. Interceptez-le avant Shiraz : la fin de la route est dans le sanctuaire rouge de Shiraz, sous son SA-11.]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Transport")
            :setGroups({"SC-Intercept-VIP-Il76"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Intercept-VIP-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.initialize()
end
end)

veafGuardedInit("COMBATZONE", function()
if veafCombatZone then
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Berlin_Easy")
        :setFriendlyName("H1 Hélico Berlin — facile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères à 3 nm à l'ouest du FARP Berlin : cibles inertes (chars, blindés et camions immobiles, tir interdit).
Position : bullseye 212°/146 nm (N24°10.751' E053°54.423'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 32 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 47 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Berlin_Medium")
        :setFriendlyName("H2 Hélico Berlin — moyen")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de Berlin : de l'artillerie antiaérienne légère (ZU-23, parfois un Shilka) en plus des cibles du niveau facile.
Position : bullseye 212°/146 nm (N24°10.751' E053°54.423'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 32 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 47 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Berlin_Hard")
        :setFriendlyName("H3 Hélico Berlin — difficile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de Berlin, avec une défense courte portée réaliste : un SA-13 et une équipe de lance-missiles portatifs SA-18, à guidage infrarouge.
Position : bullseye 212°/146 nm (N24°10.751' E053°54.423'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 32 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 47 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Tarif_Easy")
        :setFriendlyName("A1 Attaque Tarif — facile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir air-sol au nord de Tarif, à 23 nm de Liwa : blindés et camions immobiles en tir interdit, dépôt de carburant et poste de commandement. Le drone Reaper 1 tourne au-dessus.
Position : bullseye 205°/156 nm (N23°53.372' E054°08.675'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 49 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 65 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Tarif_Medium")
        :setFriendlyName("A2 Attaque Tarif — moyen")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir de Tarif : une compagnie blindée active et de l'artillerie antiaérienne légère en plus des cibles du niveau facile.
Position : bullseye 205°/156 nm (N23°53.372' E054°08.675'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 49 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 65 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Tarif_Hard")
        :setFriendlyName("A3 Attaque Tarif — difficile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir de Tarif : un second groupe blindé et une défense courte portée à guidage infrarouge (SA-13 ou SA-9), avec un Shilka.
Position : bullseye 205°/156 nm (N23°53.372' E054°08.675'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 49 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 65 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_AlQua_Easy")
        :setFriendlyName("S1 SEAD Al Qua'a — facile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD dans le désert d'Al Qua'a, au sud d'Al Dhafra : une batterie sol-air moyenne portée, SA-6 ou SA-11 tirée au sort.
Position : bullseye 191°/163 nm (N23°35.050' E054°47.271'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 68 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 85 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_AlQua_Medium")
        :setFriendlyName("S2 SEAD Al Qua'a — moyen")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD d'Al Qua'a : la batterie moyenne portée est protégée par une défense courte portée (SA-15, SA-8).
Position : bullseye 191°/163 nm (N23°35.050' E054°47.271'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 68 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 85 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_AlQua_Hard")
        :setFriendlyName("S3 SEAD Al Qua'a — difficile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD d'Al Qua'a en réseau Skynet : un radar d'alerte avancée guide les batteries, qui restent éteintes jusqu'au dernier moment.
Position : bullseye 191°/163 nm (N23°35.050' E054°47.271'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 68 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 85 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Qeshm")
        :setFriendlyName("Z01 Front — brigade IRGC de Qeshm")
        :setRadioGroupName("Front")
        :setBriefing([[La brigade des Gardiens de la révolution qui tient l'île de Qeshm et le détroit d'Ormuz : chars, blindés et lance-roquettes multiples en position. Détruire les blindés et l'artillerie ; défense SA-15 possible et artillerie antiaérienne. Sous la couverture lointaine du SA-10 au nord de Bandar Abbas.
Position : bullseye 045°/50 nm (N26°51.371' E055°57.336'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 112 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 98 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_BandarLengeh")
        :setFriendlyName("Z02 Front — défense côtière de Bandar Lengeh")
        :setRadioGroupName("Front")
        :setBriefing([[La brigade de défense côtière de Bandar Lengeh, face à Abu Musa et aux Tunb : blindés et artillerie. Défense courte portée seulement (SA-13, Shilka) : le drone Reaper 2 la désigne au laser.
Position : bullseye 314°/31 nm (N26°36.972' E054°52.969'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 115 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 101 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Minab")
        :setFriendlyName("Z03 Front — base IRGC de Minab")
        :setRadioGroupName("Front")
        :setBriefing([[La base des Gardiens de la révolution de Minab, à l'est de Bandar Abbas : casernes, dépôts, lance-roquettes Smerch. Défendue par une batterie SA-11, un SA-15 et des ZU-23 : traiter le SA-11 d'abord.
Position : bullseye 061°/111 nm (N27°09.693' E057°06.429'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 116 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 110 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Lavan")
        :setFriendlyName("Z04 SEAD — site Hawk de Lavan")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site Hawk de l'île de Lavan, à l'ouest du Golfe, couvert par un radar d'alerte avancée en réseau Skynet. Détruire le radar de poursuite et les lanceurs.
Position : bullseye 288°/114 nm (N26°48.386' E053°16.551'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 133 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 115 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Jask")
        :setFriendlyName("Z05 SEAD — site sol-air de Jask")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site sol-air qui protège la base navale de Jask, sur la mer d'Oman : une batterie SA-2 ou SA-3 tirée au sort, son radar d'alerte avancée et un Shilka.
Position : bullseye 104°/138 nm (N25°42.556' E057°46.884'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 52 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 63 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiMinab")
        :setFriendlyName("Z06 Convoi — Bandar Abbas vers Minab")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi logistique quitte Bandar Abbas par la route côtière de l'est vers la base de Minab. L'arrêter avant Minab ; il porte sa propre artillerie antiaérienne (ZU-23).
Position : bullseye 052°/90 nm (N27°11.574' E056°37.733'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 119 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 110 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiLar")
        :setFriendlyName("Z07 Convoi — Lar vers Bandar Lengeh")
        :setRadioGroupName("Convois")
        :setBriefing([[Des renforts blindés descendent de Lar vers la côte par Bastak et Kong. Les arrêter avant la côte ; le convoi est escorté par un SA-13.
Position : bullseye 326°/92 nm (N27°31.037' E054°19.422'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 168 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 152 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiJask")
        :setFriendlyName("Z08 Convoi — Jask vers Sirik")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi de carburant remonte la côte de la mer d'Oman, de Jask vers Sirik et Minab. Le détruire avant Sirik ; il porte sa propre artillerie antiaérienne.
Position : bullseye 103°/136 nm (N25°44.750' E057°45.837'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 52 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 62 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_WeaponFactory")
        :setFriendlyName("Z09 Frappe — usine d'armement de Sirjan")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[L'usine d'armement de la région de Sirjan, loin dans les terres : ateliers, hangars, réservoirs chimiques. Tout détruire ; défense SA-6 et ZU-23. Long trajet : prévoir le ravitaillement.
Position : bullseye 001°/169 nm (N29°05.411' E055°19.804'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 248 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 235 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Missiles")
        :setFriendlyName("Z10 Frappe — base de missiles balistiques")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Une base de missiles balistiques des Gardiens de la révolution dans les montagnes au nord-est de Bandar Abbas : lanceurs Scud et leurs camions. Détruire les lanceurs ; défense SA-15 et Shilka, sous la couverture du SA-10 au nord de Bandar Abbas.
Position : bullseye 044°/104 nm (N27°31.660' E056°38.274'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 139 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 130 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortRajaee")
        :setFriendlyName("Z11 Frappe — port Shahid Rajaee")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Les dépôts logistiques militaires du port Shahid Rajaee, à l'ouest de Bandar Abbas : entrepôts, réservoirs, conteneurs. Tout détruire ; ZU-23 sur place, et les défenses permanentes de Bandar Abbas à moins de 15 nm.
Position : bullseye 040°/65 nm (N27°06.254' E056°03.789'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 123 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 110 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_CentraleLar")
        :setFriendlyName("Z12 Frappe — centrale électrique de Lar")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[La centrale électrique au sud de Lar. Détruire les bâtiments ; ZU-23 sur place, et le SA-10 et le SA-15 de Lar à 10 nm au nord.
Position : bullseye 325°/103 nm (N27°39.516' E054°11.357'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 177 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 161 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Kish")
        :setFriendlyName("Z13 OCA — base aérienne de Kish")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[La base aérienne de l'île de Kish : chasseurs au parking, hangars et carburant. Tout détruire au sol ; défense SA-15 et Shilka.
Position : bullseye 284°/73 nm (N26°31.959' E053°58.856'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 110 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 94 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Jiroft")
        :setFriendlyName("Z14 OCA — base aérienne de Jiroft")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[La base aérienne de Jiroft, au nord de Minab : chasseurs-bombardiers au parking, hangars. Tout détruire au sol ; défense SA-6 et ZU-23.
Position : bullseye 041°/194 nm (N28°43.409' E057°40.874'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 212 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 208 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Flottille")
        :setFriendlyName("Z15 Antinavire — flottille devant Bandar Abbas")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Une flottille de la marine iranienne en patrouille dans le détroit, entre Qeshm, Larak et Bandar Abbas : deux vedettes lance-missiles et une corvette. Les couler ; elles sont sous les défenses permanentes de Bandar Abbas.
Position : bullseye 050°/70 nm (N27°01.786' E056°17.200'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 114 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 102 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_AbuMusa")
        :setFriendlyName("Z16 Antinavire — vedettes et Silkworm d'Abu Musa")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Les Gardiens de la révolution tiennent Abu Musa : un essaim de vedettes rapides à l'est de l'île et une batterie de missiles antinavires (HY-2 Silkworm) sur l'île. Couler les vedettes, détruire les lanceurs et leur radar ; SA-15 permanent sur l'île.
Position : bullseye 212°/25 nm (N25°54.210' E055°03.646'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 75 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 64 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Mubarek")
        :setFriendlyName("Z17 Antinavire — champ pétrolier de Mubarek")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Le champ pétrolier offshore de Mubarek, au sud-est des Tunb, sert de base avancée aux vedettes des Gardiens de la révolution : plates-formes et vedettes en patrouille. Détruire les plates-formes et couler les vedettes.
Position : bullseye 096°/18 nm (N26°14.372' E055°37.848'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 95 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 78 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Persepolis")
        :setFriendlyName("Z18 Tourisme — Persépolis")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Persépolis, la capitale des rois achéménides, au pied du mont Rahmat : un vol touristique à basse altitude sur le plateau de Marvdasht, à 1 600 m. Les Gardiens de la révolution ont installé un détachement à 2 km au nord-est du site : blindés, camions et deux ZU-23. Le neutraliser sans toucher aux ruines. Le SA-11 de Shiraz porte jusqu'à 3 nm au sud-ouest du site : arriver par l'est. Les colonnes et l'escalier de l'Apadana sont modélisés dans DCS.
Position : bullseye 331°/254 nm (N29°56.110' E052°53.424'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 319 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 302 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.GetZone("combatZone_Berlin_Medium"):addZoneElementsFromZoneNamed("combatZone_Berlin_Easy")
    veafCombatZone.GetZone("combatZone_Berlin_Hard"):addZoneElementsFromZoneNamed("combatZone_Berlin_Medium")
    veafCombatZone.GetZone("combatZone_Berlin_Hard"):addZoneElementsFromZoneNamed("combatZone_Berlin_Easy")
    veafCombatZone.GetZone("combatZone_Tarif_Medium"):addZoneElementsFromZoneNamed("combatZone_Tarif_Easy")
    veafCombatZone.GetZone("combatZone_Tarif_Hard"):addZoneElementsFromZoneNamed("combatZone_Tarif_Medium")
    veafCombatZone.GetZone("combatZone_Tarif_Hard"):addZoneElementsFromZoneNamed("combatZone_Tarif_Easy")
    veafCombatZone.GetZone("combatZone_AlQua_Medium"):addZoneElementsFromZoneNamed("combatZone_AlQua_Easy")
    veafCombatZone.GetZone("combatZone_AlQua_Hard"):addZoneElementsFromZoneNamed("combatZone_AlQua_Medium")
    veafCombatZone.GetZone("combatZone_AlQua_Hard"):addZoneElementsFromZoneNamed("combatZone_AlQua_Easy")
    veafCombatZone.initialize()
end
end)

veafGuardedInit("QRA", function()
if veafQraManager then
    veafQraManager.initialize()
    local QRA_Bandar_Abbas = VeafQRA:new()
        :setName("QRA Bandar Abbas")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-BandarAbbas")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-BandarAbbas-MiG29", "QRA-BandarAbbas-F4"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-BandarAbbas-F14", "QRA-BandarAbbas-MiG29x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Bandar Abbas Intl")
        :start()
    local QRA_Lar = VeafQRA:new()
        :setName("QRA Lar")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Lar")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Lar-F4", "QRA-Lar-MiG29"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Lar-F14", "QRA-Lar-F4x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Lar")
        :start()
    local QRA_Al_Minhad = VeafQRA:new()
        :setName("QRA Al Minhad")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-AlMinhad")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-AlMinhad-F16", "QRA-AlMinhad-M2000"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-AlMinhad-F15", "QRA-AlMinhad-M2000x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Al Minhad AFB")
        :start()
    local QRA_Al_Dhafra = VeafQRA:new()
        :setName("QRA Al Dhafra")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-AlDhafra")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-AlDhafra-F15", "QRA-AlDhafra-F16"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-AlDhafra-F15x4", "QRA-AlDhafra-F16x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Al Dhafra AFB")
        :start()
end
end)

-- ── Features ──

veafGuardedInit("GRASS", function()
if veafGrass then
    veafGrass.initialize()
end
end)

veafGuardedInit("ASSETS", function()
if veafAssets then
    veafAssets.Assets = {
        {sort = 1, name = "Overlord 1", description = "Overlord 1 (E-3A) — AWACS ouest", information = "U282.0 — FL300 — orbite au sud d'Abu Dhabi et d'Al Ain", linked = "Overlord 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 2, name = "Magic 1", description = "Magic 1 (E-2C) — AWACS est", information = "U283.0 — FL280 — orbite au-dessus de la mer d'Oman, au sud de Fujairah", linked = "Magic 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 3, name = "Texaco 1", description = "Texaco 1 (KC-135, perche) — ouest", information = "TACAN 50Y TX1 — U290.0 — FL220 — piste nord-sud au large d'Abu Dhabi, à l'ouest de Sir Abu Nuayr", linked = "Texaco 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 4, name = "Arco 1", description = "Arco 1 (KC-135 MPRS, panier) — ouest", information = "TACAN 51Y AR1 — U291.0 — FL180 — piste nord-sud au large d'Abu Dhabi", linked = "Arco 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 5, name = "Texaco 2", description = "Texaco 2 (KC-135, perche) — est", information = "TACAN 52Y TX2 — U292.0 — FL240 — piste nord-sud en mer d'Oman, à l'est de Fujairah", linked = "Texaco 2 - Escort", coalition = coalition.side.BLUE},
        {sort = 6, name = "Arco 2", description = "Arco 2 (KC-135 MPRS, panier) — est", information = "TACAN 53Y AR2 — U293.0 — FL200 — piste nord-sud en mer d'Oman, près du Roosevelt", linked = "Arco 2 - Escort", coalition = coalition.side.BLUE},
        {sort = 7, name = "CSG-74 Stennis", description = "CVN-74 Stennis — Golfe", information = "TACAN 74X STN — ICLS 11 — Link 4 336.0 — ACLS — U305.0", coalition = coalition.side.BLUE},
        {sort = 8, name = "CSG-71 Roosevelt", description = "CVN-71 Roosevelt — mer d'Oman", information = "TACAN 71X RSV — ICLS 12 — Link 4 337.0 — ACLS — U306.0", coalition = coalition.side.BLUE},
        {sort = 9, name = "ARG-1 Tarawa", description = "LHA-1 Tarawa — Golfe", information = "TACAN 73X TRW — ICLS 13 — U307.0", coalition = coalition.side.BLUE},
        {sort = 10, name = "CSG-74 Stennis S3B-Tanker", description = "S-3B du Stennis (ravitailleur embarqué)", information = "TACAN 56Y S74 — U296.0", coalition = coalition.side.BLUE},
        {sort = 11, name = "CSG-71 Roosevelt S3B-Tanker", description = "S-3B du Roosevelt (ravitailleur embarqué)", information = "TACAN 57Y S71 — U297.0", coalition = coalition.side.BLUE},
        {sort = 12, name = "Darkstar 1", description = "Darkstar 1 (E-3A) — AWACS bleu de l'arène", information = "U285.0 — FL300", coalition = coalition.side.BLUE},
        {sort = 13, name = "Wizard 1", description = "Wizard 1 (A-50) — AWACS rouge", information = "U284.0 — FL300 — orbite au sud de Sirjan", linked = "Wizard 1 - Escort", coalition = coalition.side.RED},
        {sort = 14, name = "Shell 1", description = "Shell 1 (IL-78M) — ravitailleur rouge", information = "U294.0 — FL200 — orbite à l'est de Lar", linked = "Shell 1 - Escort", coalition = coalition.side.RED},
        {sort = 15, name = "Focus 1", description = "Focus 1 (A-50) — AWACS rouge de l'arène", information = "U286.0 — FL300", coalition = coalition.side.RED},
        {sort = 16, name = "Reaper 1", description = "Reaper 1 (drone laser) — champ de tir de Tarif", information = "Laser 1511 — FM 35.55. 3 000 m sol au-dessus du champ de tir attaque (zone A).", jtac = 1511, freq = "35.55", mod = "FM", coalition = coalition.side.BLUE},
        {sort = 17, name = "Reaper 2", description = "Reaper 2 (drone laser) — Bandar Lengeh", information = "Laser 1512 — FM 35.6. 3 000 m sol au-dessus de la défense côtière de Bandar Lengeh (Z02).", jtac = 1512, freq = "35.6", mod = "FM", coalition = coalition.side.BLUE},
    }
    veafAssets.initialize()
end
end)

veafGuardedInit("MOVE", function()
if veafMove then
    veafMove.initialize()
end
end)

veafGuardedInit("SANCTUARY", function()
if veafSanctuary then
    veafSanctuary.initialize()
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-AlDhafra")
        if zone then
            zone:setName("Sanctuaire Al Dhafra")
                :setCoalition(coalition.side.BLUE)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Lar")
        if zone then
            zone:setName("Sanctuaire Lar")
                :setCoalition(coalition.side.RED)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Shiraz")
        if zone then
            zone:setName("Sanctuaire Shiraz")
                :setCoalition(coalition.side.RED)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
end
end)

veafGuardedInit("WEATHER", function()
if veafWeather then
    veafWeather.initialize()
end
end)

veafGuardedInit("REMOTE", function()
if veafRemote then
    veafRemote.initialize()
end
end)

veafGuardedInit("AIRBASES", function()
if veafAirbases then
    veafAirbases.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("MARKERS", function()
if veafMarkers then
    veafMarkers.initialize()
end
end)

veafGuardedInit("TIME", function()
if veafTime then
    veafTime.initialize()
end
end)

veafGuardedInit("UNITS", function()
if veafUnits then
    veafUnits.initialize()
end
end)

veafGuardedInit("CACHE", function()
if veafCacheManager then
    veafCacheManager.initialize()
end
end)

veafGuardedInit("EVENTS", function()
if veafEventHandler then
    veafEventHandler.initialize()
end
end)

-- ── Core ──

veafGuardedInit("GROUNDAI", function()
if veafGroundAI then
    veafGroundAI.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("COMMANDS", function()
if veafCommands then
    veafCommands.initialize()
end
end)

-- ── Features ──

veafGuardedInit("INTERPRETER", function()
if veafInterpreter then
    veafInterpreter.initialize()
end
end)

-- ── Community scripts disabled (VEAF leaves their globals alone) ──────────────
veaf.setConfig("tum", "enable", false)

-- ── Skynet-IADS ──────────────────────────────────────────────────────────────
veafGuardedInit("SKYNET", function()
if veafSkynet then
    veafSkynet.SpotterNetwork = true
    veafSkynet.SpotterView = "off"
    veafSkynet.initialize(false, false, false, false)
end
end)

-- ── CSAR configuration ───────────────────────────────────────────────────────
-- Note: CSAR.lua must be loaded by mission-script.lua before this block.
veafGuardedInit("CSAR", function()
if csar then
    csar.initialize()
end
end)
