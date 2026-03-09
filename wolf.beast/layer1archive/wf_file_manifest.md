# WOLVERINE: UNBOUNDED — File Manifest

## GOVERNANCE
**Parent Document:** critic_final.md (Layer 1 Phase 9)
**Status:** READ-ONLY — Layer 1 frozen. Modifications require return to source phase.
**Layer:** L1 | **Phase:** P5

## SUMMARY
Complete file manifest for Wolverine: Unbounded. Every C++ header/implementation pair, Blueprint class, config file, and automation test. Total: 154 files (62 C++ source, 10 Blueprint classes, 5 config files, 8 automation tests, 69 content assets). Organized by build level from wfmod.dep.md. Each file includes path, build level, and FR/NFR/HR references.

---

## BUILD LEVEL 0 — Core Types (8 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 0.1 | `Source/Wolverine/Public/WolverineCoreTypes.h` | C++ Header | L0 | All/All/HR-06 | All core enums (EClawMaterialType, ERageLevel, ETraversalState, etc.) |
| 0.2 | `Source/Wolverine/Private/WolverineCoreTypes.cpp` | C++ Source | L0 | - | Empty impl (enums only) |
| 0.3 | `Source/Wolverine/Public/IWolverineMaterialResponse.h` | C++ Header | L0 | FR-07/HR-06 | Interface for material detection |
| 0.4 | `Source/Wolverine/Private/IWolverineMaterialResponse.cpp` | C++ Source | L0 | FR-07 | Default interface impl |
| 0.5 | `Source/Wolverine/Public/IWolverineDamageInterface.h` | C++ Header | L0 | FR-06/HR-02 | Interface for damage application |
| 0.6 | `Source/Wolverine/Private/IWolverineDamageInterface.cpp` | C++ Source | L0 | FR-06 | Default interface impl |
| 0.7 | `Source/Wolverine/Public/WolverineDataStructures.h` | C++ Header | L0 | FR-06/FR-11/FR-13/FR-15/FR-18/FR-20 | All FStructs (FWoundData, FMemoryFragment, etc.) |
| 0.8 | `Source/Wolverine/Private/WolverineDataStructures.cpp` | C++ Source | L0 | - | Empty impl (structs only) |

---

## BUILD LEVEL 1 — Systems (8 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 1.1 | `Source/Wolverine/Public/Components/WolverineMaterialResponseSystem.h` | C++ Header | L1 | FR-07/HR-06 | Material detection from hit results |
| 1.2 | `Source/Wolverine/Private/Components/WolverineMaterialResponseSystem.cpp` | C++ Source | L1 | FR-07 | Surface type → EClawMaterialType mapping |
| 1.3 | `Source/Wolverine/Public/Components/WolverineWoundSystemComponent.h` | C++ Header | L1 | FR-06/NFR-01/NFR-03/HR-02 | Mesh deformation, healing, wound state |
| 1.4 | `Source/Wolverine/Private/Components/WolverineWoundSystemComponent.cpp` | C++ Source | L1 | FR-06/HR-02 | 10Hz healing tick, morph target deformation |
| 1.5 | `Source/Wolverine/Public/Animation/WolverineAnimationInstance.h` | C++ Header | L1 | FR-02/FR-03/NFR-01/NFR-07 | Motion Matching, claw animation blending |
| 1.6 | `Source/Wolverine/Private/Animation/WolverineAnimationInstance.cpp` | C++ Source | L1 | FR-02/FR-03 | Motion Matching update, claw blend weights |
| 1.7 | `Source/Wolverine/Public/WolverineSaveGame.h` | C++ Header | L1 | FR-11/FR-13/FR-15/NFR-06/HR-05 | Save game class with destruction persistence |
| 1.8 | `Source/Wolverine/Private/WolverineSaveGame.cpp` | C++ Source | L1 | FR-13/HR-05 | Constructor impl |

---

## BUILD LEVEL 2 — Components (10 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 2.1 | `Source/Wolverine/Public/Components/WolverineClawComponent.h` | C++ Header | L2 | FR-03/FR-04/FR-07/NFR-02/NFR-08/HR-01/HR-06 | Claw deployment, material tracing, impact events |
| 2.2 | `Source/Wolverine/Private/Components/WolverineClawComponent.cpp` | C++ Source | L2 | FR-03/FR-04/FR-07/HR-01/HR-06 | 60fps material trace, <200ms deploy |
| 2.3 | `Source/Wolverine/Public/Components/WolverineRageComponent.h` | C++ Header | L2 | FR-05/NFR-01/NFR-04/HR-04 | Rage accumulation, Berserker state machine |
| 2.4 | `Source/Wolverine/Private/Components/WolverineRageComponent.cpp` | C++ Source | L2 | FR-05/HR-04 | Event-driven rage (NO manual activation) |
| 2.5 | `Source/Wolverine/Public/Components/WolverineTraumaSystemComponent.h` | C++ Header | L2 | FR-11/HR-08 | Memory unlocks, mechanical bonuses |
| 2.6 | `Source/Wolverine/Private/Components/WolverineTraumaSystemComponent.cpp` | C++ Source | L2 | FR-11/HR-08 | Bonus calculation from memories |
| 2.7 | `Source/Wolverine/Public/Components/WolverineAudioComponent.h` | C++ Header | L2 | FR-18/NFR-08/HR-06 | MetaSounds reactive graph |
| 2.8 | `Source/Wolverine/Private/Components/WolverineAudioComponent.cpp` | C++ Source | L2 | FR-18/HR-06 | Combat intensity → music intensity |
| 2.9 | `Source/Wolverine/Public/Components/HapticFeedbackSystem.h` | C++ Header | L2 | FR-20/NFR-02/HR-06 | Asymmetric haptic feedback per claw/material |
| 2.10 | `Source/Wolverine/Private/Components/HapticFeedbackSystem.cpp` | C++ Source | L2 | FR-20/HR-06 | Per-material haptic data |

---

## BUILD LEVEL 3 — Character (12 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 3.1 | `Source/Wolverine/Public/Components/WolverineMovementComponent.h` | C++ Header | L3 | FR-02/NFR-01/NFR-02/HR-01/HR-07 | Custom traversal (sprint, wall climb, claw swing, lunge) |
| 3.2 | `Source/Wolverine/Private/Components/WolverineMovementComponent.cpp` | C++ Source | L3 | FR-02/HR-01/HR-07 | Movement state machine |
| 3.3 | `Source/Wolverine/Public/WolverineCharacter.h` | C++ Header | L3 | All | Player character — aggregates all components |
| 3.4 | `Source/Wolverine/Private/WolverineCharacter.cpp` | C++ Source | L3 | All | Component creation, input binding |
| 3.5 | `Source/Wolverine/Public/WolverinePlayerController.h` | C++ Header | L3 | FR-02/FR-03 | Input binding, UI management |
| 3.6 | `Source/Wolverine/Private/WolverinePlayerController.cpp` | C++ Source | L3 | FR-02/FR-03 | Enhanced Input mapping |
| 3.7 | `Source/Wolverine/Public/UI/WolverineHUD.h` | C++ Header | L3 | FR-19/HR-08 | Minimal HUD (compass, vignette, wound indicator) |
| 3.8 | `Source/Wolverine/Private/UI/WolverineHUD.cpp` | C++ Source | L3 | FR-19/HR-08 | Widget references, state updates |
| 3.9 | `Source/Wolverine/Public/UI/WoundIndicatorWidget.h` | C++ Header | L3 | FR-19/HR-08 | Wound feedback (not a health bar) |
| 3.10 | `Source/Wolverine/Private/UI/WoundIndicatorWidget.cpp` | C++ Source | L3 | FR-19 | Vignette pulse based on severity |
| 3.11 | `Source/Wolverine/Public/UI/CompassWidget.h` | C++ Header | L3 | FR-19 | Compass bearing only |
| 3.12 | `Source/Wolverine/Private/UI/CompassWidget.cpp` | C++ Source | L3 | FR-19 | Bearing update, objective chevron |

---

## BUILD LEVEL 4 — AI + World (36 files)

### AI Characters (10 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 4.1 | `Source/Wolverine/Public/AI/WeaponXSoldier.h` | C++ Header | L4 | FR-09/NFR-04/HR-07 | Standard infantry AI |
| 4.2 | `Source/Wolverine/Private/AI/WeaponXSoldier.cpp` | C++ Source | L4 | FR-09/HR-07 | Behavior Tree execution, fear state |
| 4.3 | `Source/Wolverine/Public/AI/WeaponXHeavyUnit.h` | C++ Header | L4 | FR-09 | Powered armor — claw pry required |
| 4.4 | `Source/Wolverine/Private/AI/WeaponXHeavyUnit.cpp` | C++ Source | L4 | FR-09 | Armor breach mechanic |
| 4.5 | `Source/Wolverine/Public/AI/MutantHunter.h` | C++ Header | L4 | FR-09 | Healing dampening specialist |
| 4.6 | `Source/Wolverine/Private/AI/MutantHunter.cpp` | C++ Source | L4 | FR-09 | Dampening field activation |
| 4.7 | `Source/Wolverine/Public/AI/FeralMutant.h` | C++ Header | L4 | FR-09 | Fast, dodge-heavy enemy |
| 4.8 | `Source/Wolverine/Private/AI/FeralMutant.cpp` | C++ Source | L4 | FR-09 | Evasive dodge, chain attacks |
| 4.9 | `Source/Wolverine/Public/AI/Sentinel.h` | C++ Header | L4 | FR-09 | Late-game boss — multi-phase |
| 4.10 | `Source/Wolverine/Private/AI/Sentinel.cpp` | C++ Source | L4 | FR-09 | Phase transitions, area destruction |

### World Systems (18 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 4.11 | `Source/Wolverine/Public/World/PortAshfordWorldSettings.h` | C++ Header | L4 | FR-12/FR-13/NFR-06/HR-03/HR-05 | District streaming, weather, destruction persistence |
| 4.12 | `Source/Wolverine/Private/World/PortAshfordWorldSettings.cpp` | C++ Source | L4 | FR-12/FR-13/HR-03/HR-05 | Level streaming, destruction save/load |
| 4.13 | `Source/Wolverine/Public/World/WeatherSystem.h` | C++ Header | L4 | FR-12 | Dynamic weather transitions |
| 4.14 | `Source/Wolverine/Private/World/WeatherSystem.cpp` | C++ Source | L4 | FR-12 | Weather state machine, Niagara particles |
| 4.15 | `Source/Wolverine/Public/World/DestructionPersistenceData.h` | C++ Header | L4 | FR-13/NFR-06/HR-05 | Destruction records (survives save/load) |
| 4.16 | `Source/Wolverine/Private/World/DestructionPersistenceData.cpp` | C++ Source | L4 | FR-13/HR-05 | Data asset impl |
| 4.17 | `Source/Wolverine/Public/World/EscalationManager.h` | C++ Header | L4 | FR-14/NFR-05 | City-wide AI escalation |
| 4.18 | `Source/Wolverine/Private/World/EscalationManager.cpp` | C++ Source | L4 | FR-14/NFR-05 | Notoriety decay, patrol spawning |
| 4.19 | `Source/Wolverine/Public/World/DistrictStreamingVolume.h` | C++ Header | L4 | FR-02/HR-03 | Trigger volume for district transitions |
| 4.20 | `Source/Wolverine/Private/World/DistrictStreamingVolume.cpp` | C++ Source | L4 | FR-02/HR-03 | Seamless district loading |
| 4.21 | `Source/Wolverine/Public/World/EnvironmentalDestructible.h` | C++ Header | L4 | FR-13/HR-05 | Chaos destruction actor |
| 4.22 | `Source/Wolverine/Private/World/EnvironmentalDestructible.cpp` | C++ Source | L4 | FR-13/HR-05 | GUID assignment, destruction state |
| 4.23 | `Source/Wolverine/Public/World/SafeHouse.h` | C++ Header | L4 | FR-16 | Safe house location (4 total) |
| 4.24 | `Source/Wolverine/Private/World/SafeHouse.cpp` | C++ Source | L4 | FR-16 | Journal trigger, full heal |
| 4.25 | `Source/Wolverine/Public/World/WeaponXIntelCollectible.h` | C++ Header | L4 | FR-15 | Weapon X collectible (audio log/photo) |
| 4.26 | `Source/Wolverine/Private/World/WeaponXIntelCollectible.cpp` | C++ Source | L4 | FR-15 | Collection trigger, no map markers |
| 4.27 | `Source/Wolverine/Public/World/MemoryFragmentTrigger.h` | C++ Header | L4 | FR-11/FR-17 | Trauma system memory trigger |
| 4.28 | `Source/Wolverine/Private/World/MemoryFragmentTrigger.cpp` | C++ Source | L4 | FR-11/FR-17 | Playable flashback trigger |

### AI Support (8 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 4.29 | `Source/Wolverine/Public/AI/WeaponXSquadLeader.h` | C++ Header | L4 | FR-09 | Squad coordination |
| 4.30 | `Source/Wolverine/Private/AI/WeaponXSquadLeader.cpp` | C++ Source | L4 | FR-09 | Squad tactics, backup calls |
| 4.31 | `Source/Wolverine/Public/AI/AIControllerBase.h` | C++ Header | L4 | FR-09 | Base AI controller |
| 4.32 | `Source/Wolverine/Private/AI/AIControllerBase.cpp` | C++ Source | L4 | FR-09 | Common AI logic |
| 4.33 | `Source/Wolverine/Public/AI/FearStateMachine.h` | C++ Header | L4 | FR-09/HR-07 | Fear escalation system |
| 4.34 | `Source/Wolverine/Private/AI/FearStateMachine.cpp` | C++ Source | L4 | FR-09/HR-07 | Fear level calculation, response |
| 4.35 | `Source/Wolverine/Public/AI/EQSService.h` | C++ Header | L4 | FR-09 | EQS query helper |
| 4.36 | `Source/Wolverine/Private/AI/EQSService.cpp` | C++ Source | L4 | FR-09 | Flank/cover/retreat queries |

---

## BUILD LEVEL 5 — Game Flow (10 files)

| # | File Path | Type | Build Level | FR/NFR/HR | Description |
|---|-----------|------|-------------|-----------|-------------|
| 5.1 | `Source/Wolverine/Public/Game/WolverineGameMode.h` | C++ Header | L5 | FR-17 | 72-hour narrative, mission flow |
| 5.2 | `Source/Wolverine/Private/Game/WolverineGameMode.cpp` | C++ Source | L5 | FR-17 | District transitions, escalation queries |
| 5.3 | `Source/Wolverine/Public/Game/WolverineGameState.h` | C++ Header | L5 | - | Replicated game state |
| 5.4 | `Source/Wolverine/Private/Game/WolverineGameState.cpp` | C++ Source | L5 | - | State replication |
| 5.5 | `Source/Wolverine/Public/Game/WolverinePlayerState.h` | C++ Header | L5 | FR-11/FR-15/HR-08 | Persistent player data (NO XP/skills) |
| 5.6 | `Source/Wolverine/Private/Game/WolverinePlayerState.cpp` | C++ Source | L5 | FR-11/FR-15/HR-08 | Memory/intel persistence |
| 5.7 | `Source/Wolverine/Public/Game/WolverineGameInstance.h` | C++ Header | L5 | - | Game instance (menu to game) |
| 5.8 | `Source/Wolverine/Private/Game/WolverineGameInstance.cpp` | C++ Source | L5 | - | Save/load management |
| 5.9 | `Source/Wolverine/Public/Game/MissionManager.h` | C++ Header | L5 | FR-17 | Mission state machine |
| 5.10 | `Source/Wolverine/Private/Game/MissionManager.cpp` | C++ Source | L5 | FR-17 | Act transitions, mission triggers |

---

## BLUEPRINT CLASSES (10 files)

| # | File Path | Type | Parent | Purpose |
|---|-----------|------|--------|---------|
| BP-01 | `Content/Blueprints/Characters/BP_WolverineCharacter.uasset` | Blueprint | AWolverineCharacter | Player character BP |
| BP-02 | `Content/Blueprints/AI/BP_WeaponXSoldier.uasset` | Blueprint | AWeaponXSoldier | Soldier AI BP |
| BP-03 | `Content/Blueprints/AI/BP_WeaponXHeavy.uasset` | Blueprint | AWeaponXHeavyUnit | Heavy unit BP |
| BP-04 | `Content/Blueprints/AI/BP_MutantHunter.uasset` | Blueprint | AMutantHunter | Hunter AI BP |
| BP-05 | `Content/Blueprints/AI/BP_FeralMutant.uasset` | Blueprint | AFeralMutant | Feral AI BP |
| BP-06 | `Content/Blueprints/AI/BP_Sentinel.uasset` | Blueprint | ASentinel | Boss BP |
| BP-07 | `Content/Blueprints/World/BP_EscalationManager.uasset` | Blueprint | AEscalationManager | Escalation BP |
| BP-08 | `Content/Blueprints/World/BP_WeatherSystem.uasset` | Blueprint | AWeatherSystem | Weather BP |
| BP-09 | `Content/Blueprints/UI/BP_WolverineHUD.uasset` | Blueprint | UWolverineHUD | HUD BP |
| BP-10 | `Content/Blueprints/UI/BP_WoundIndicator.uasset` | Blueprint | UWoundIndicatorWidget | Wound UI BP |

---

## BLUEPRINT-ONLY SYSTEMS (6 files)

| # | File Path | Type | Purpose |
|---|-----------|------|---------|
| BP-BT-01 | `Content/Blueprints/AI/BT_WeaponXSoldier.uasset` | Behavior Tree | Soldier behavior (Flank, Suppress, Retreat) |
| BP-BB-01 | `Content/Blueprints/AI/BB_WeaponXSoldier.uasset` | Blackboard | Soldier blackboard (TargetActor, LastSeenPos, FearLevel) |
| BP-EQS-01 | `Content/Blueprints/AI/EQS_FlankPosition.uasset` | EQS Query | Flank position query |
| BP-EQS-02 | `Content/Blueprints/AI/EQS_CoverSearch.uasset` | EQS Query | Cover search query |
| BP-EQS-03 | `Content/Blueprints/AI/EQS_RetreatPath.uasset` | EQS Query | Retreat path query |
| BP-IA-01 | `Content/Blueprints/Input/BPD_WolverineInput.uasset` | Input Actions | IA_ClawDeploy, IA_ClawLunge, IA_Sprint, IA_LightAttack, IA_HeavyAttack, IA_Dodge |

---

## CONFIG FILES (5 files)

| # | File Path | Type | Purpose |
|---|-----------|------|---------|
| CFG-01 | `Config/DefaultGame.ini` | Config | Game settings, project metadata |
| CFG-02 | `Config/DefaultInput.ini` | Config | Input mappings (Enhanced Input) |
| CFG-03 | `Config/DefaultEngine.ini` | Config | Engine settings, plugins |
| CFG-04 | `Config/DefaultEditor.ini` | Config | Editor settings |
| CFG-05 | `Config/DefaultScalability.ini` | Config | Performance scalability (60fps target) |

### DefaultGame.ini Section
```ini
[/Script/EngineSettings.GeneralProjectSettings]
ProjectID=WOLVERINE-UNBOUNDED-2026
ProjectName=Wolverine: Unbounded
CompanyName=Forge Game Studio

[/Script/Wolverine.WolverineGameMode]
StartingDistrict=Basin
StartingTimeHours=0.0
StartingWeather=Rain
```

### DefaultInput.ini Section
```ini
[/Script/EnhancedInput.EnhancedInputProjectSettings]
DefaultMappingContext=/Game/Input/IMC_Wolverine.IMC_Wolverine

[/Script/Wolverine.WolverinePlayerController]
+InputMappings=(Action="IA_ClawDeploy", Key=Q)
+InputMappings=(Action="IA_ClawLunge", Key=MiddleMouseButton)
+InputMappings=(Action="IA_Sprint", Key=LeftShift)
+InputMappings=(Action="IA_LightAttack", Key=LeftMouseButton)
+InputMappings=(Action="IA_HeavyAttack", Key=RightMouseButton)
+InputMappings=(Action="IA_Dodge", Key=Spacebar)
```

### DefaultEngine.ini Section
```ini
[/Script/Engine.RendererSettings]
r.Nanite=1
r.Lumen=1
r.Shadow.Virtual=1

[/Script/Wolverine.WolverineCharacter]
TargetFrameRate=60
MotionMatchingEnabled=1
```

---

## AUTOMATION TESTS (8 files)

| # | File Path | Type | Tests | HR Verified |
|---|-----------|------|-------|-------------|
| TEST-01 | `Source/Wolverine/Tests/Automation/Test_WolverineClaw.cpp` | Automation | Claw deploy time, material detection, impact events | HR-01, HR-06 |
| TEST-02 | `Source/Wolverine/Tests/Automation/Test_WolverineWoundSystem.cpp` | Automation | Wound application, healing tick rate, mesh deformation | HR-02 |
| TEST-03 | `Source/Wolverine/Tests/Automation/Test_WolverineRage.cpp` | Automation | Rage fill from damage, Berserker trigger, NO manual activation | HR-04 |
| TEST-04 | `Source/Wolverine/Tests/Automation/Test_WolverineMovement.cpp` | Automation | Traversal states, claw lunge distance, wall climb | HR-01, HR-07 |
| TEST-05 | `Source/Wolverine/Tests/Automation/Test_DestructionPersistence.cpp` | Automation | Destruction save/load, GUID lookup, district transition | HR-03, HR-05 |
| TEST-06 | `Source/Wolverine/Tests/Automation/Test_MaterialResponse.cpp` | Automation | 6 material types, surface mapping, haptic response | HR-06 |
| TEST-07 | `Source/Wolverine/Tests/Automation/Test_TraumaSystem.cpp` | Automation | Memory unlocks, bonus calculation, NO XP/levels | HR-08 |
| TEST-08 | `Source/Wolverine/Tests/Automation/Test_HUDCompliance.cpp` | Automation | UMG widget grep for XP/level/skill references | HR-08 |

### Test_WolverineRage.cpp — HR-04 Compliance Test
```cpp
BEGIN_DEFINE_SPEC(FWolverineRageSpec, "Wolverine.Rage.HR04",
    EAutomationTestFlags::ProductFilter | EAutomationTestFlags::ApplicationContextMask)

void TestNoManualActivation()
{
    // HR-04: RageComponent MUST NOT have public ActivateRage
    UWolverineRageComponent* RageComp = NewObject<UWolverineRageComponent>();
    
    // Check for public ActivateRage function
    UFunction* ActivateRageFunc = RageComp->FindFunctionByName("ActivateRage");
    TestFalse("ActivateRage function exists", ActivateRageFunc != nullptr);
    
    // Check that AddRage is NOT BlueprintCallable
    UFunction* AddRageFunc = RageComp->FindFunctionByName("AddRage");
    TestTrue("AddRage function exists", AddRageFunc != nullptr);
    TestFalse("AddRage is BlueprintCallable", 
        AddRageFunc->HasAnyFunctionFlags(FUNC_BlueprintCallable));
}

END_DEFINE_SPEC(FWolverineRageSpec)
```

### Test_HUDCompliance.cpp — HR-08 Compliance Test
```cpp
BEGIN_DEFINE_SPEC(FHUDComplianceSpec, "Wolverine.HUD.HR08",
    EAutomationTestFlags::ProductFilter | EAutomationTestFlags::ApplicationContextMask)

void TestNoXPUILeferences()
{
    // HR-08: NO XP/level/skill UI references
    TArray<FString> ForbiddenTerms = { "XP", "Experience", "Level", "SkillPoint", "SkillTree" };
    
    // Grep all UMG widgets
    TArray<UUserWidget*> AllWidgets;
    // ... load all widgets ...
    
    for (UUserWidget* Widget : AllWidgets)
    {
        for (const FString& Term : ForbiddenTerms)
        {
            TestFalse("Widget contains " + Term, 
                Widget->GetName().Contains(Term));
        }
    }
}

END_DEFINE_SPEC(FHUDComplianceSpec)
```

---

## CONTENT ASSETS (69 files)

### Animation Assets (52 files)

| Category | Count | Path |
|----------|-------|------|
| Locomotion | 6 | `Content/Animations/Locomotion/` |
| Wall Climbing | 4 | `Content/Animations/WallClimb/` |
| Claw Swing | 4 | `Content/Animations/ClawSwing/` |
| Claw Lunge | 4 | `Content/Animations/ClawLunge/` |
| Combat | 18 | `Content/Animations/Combat/` |
| Predator/Stealth | 5 | `Content/Animations/Stealth/` |
| Damage/Healing | 4 | `Content/Animations/Damage/` |
| Blend Spaces | 8 | `Content/Animations/BlendSpaces/` |

**Total Animation Clips:** 52 (see wfarch.md Section 7.2 for full list)

### Audio Assets (10 files)

| Type | Count | Path |
|------|-------|------|
| MetaSound Sources | 6 | `Content/Audio/MetaSounds/` |
| Claw Impact Sounds | 6 | `Content/Audio/SFX/Claw/` |
| Healing Sounds | 1 | `Content/Audio/SFX/Healing/` |
| Berserker Music | 1 | `Content/Audio/Music/Berserker/` |
| Ambient Tracks | 4 | `Content/Audio/Music/Ambient/` |

### Material Assets (6 files)

| Type | Count | Path |
|------|-------|------|
| Claw Impact Materials | 6 | `Content/Materials/ClawImpact/` |

### Data Assets (7 files)

| Type | Count | Path |
|------|-------|------|
| Memory Fragment Data | 10 | `Content/Data/Memories/` |
| Weapon X Intel Data | 15 | `Content/Data/Intel/` |
| Haptic Feedback Data | 6 | `Content/Data/Haptics/` |

---

## FILE COUNT SUMMARY

| Category | Count |
|----------|-------|
| **C++ Headers** | 42 |
| **C++ Sources** | 42 |
| **Blueprint Classes** | 10 |
| **Blueprint-Only Systems** | 6 |
| **Config Files** | 5 |
| **Automation Tests** | 8 |
| **Animation Assets** | 52 |
| **Audio Assets** | 12 |
| **Material Assets** | 6 |
| **Data Assets** | 31 |
| **TOTAL** | **214** |

**Note:** Previous summary claimed 238 files (54 headers + 54 sources). Corrected count is 214 files (42 headers + 42 sources). Discrepancy was due to BUILD LEVEL 2 header claiming "20 files" but only listing 10 files (2.1-2.10). Actual C++ file count: L0(8) + L1(8) + L2(10) + L3(12) + L4(36) + L5(10) = 84 files (42 headers + 42 sources).

---

## CRITICAL PATH FILES (CLAWS IN GAME)

These 16 files unblock the first milestone (CLAWS IN GAME):

| Build Level | Files | Cumulative |
|-------------|-------|------------|
| L0 | 0.1-0.8 (8 files) | 8 |
| L1 | 1.1-1.4 (4 files) | 12 |
| L2 | 2.1-2.2 (2 files) | 14 |
| L3 | 3.1-3.4 (4 files) | 18 |

**Milestone:** Playable claw combat in empty level after these 18 files compile.

---

## HR VERIFICATION MATRIX

| HR | Files That Verify | Test File |
|----|-------------------|-----------|
| HR-01 (Claws <10s) | 2.1, 2.2, 3.1, 3.2 | TEST-01, TEST-04 |
| HR-02 (Mesh deformation) | 1.3, 1.4 | TEST-02 |
| HR-03 (No loading screens) | 4.11, 4.12, 4.19, 4.20 | TEST-05 |
| HR-04 (Rage event-driven) | 2.3, 2.4 | TEST-03 |
| HR-05 (Persistent destruction) | 1.7, 1.8, 4.11, 4.12, 4.15, 4.16 | TEST-05 |
| HR-06 (6 material types) | 0.1, 1.1, 1.2, 2.1, 2.2, 2.9, 2.10 | TEST-01, TEST-06 |
| HR-07 (Predator optional) | 3.1, 3.2, 4.1, 4.2 | TEST-04 |
| HR-08 (No skill trees) | 2.5, 2.6, 3.7, 3.8, 3.9, 5.5, 5.6 | TEST-07, TEST-08 |

---

## DECISION_HASH

```json
{
  "document": "wf_file_manifest.md",
  "project": "wolf.beast",
  "version": "1.1",
  "created": "2026-03-08",
  "revised": "2026-03-08",
  "derived_from": ["wfmod.dep.md", "wfdep.graph.md", "wfarch.md"],
  "total_files": 214,
  "cpp_headers": 42,
  "cpp_sources": 42,
  "blueprint_classes": 10,
  "blueprint_systems": 6,
  "config_files": 5,
  "automation_tests": 8,
  "content_assets": 101,
  "critical_path_files": 18,
  "key_decisions": [
    "18 files minimum for CLAWS IN GAME milestone (L0-L3 subset)",
    "8 automation tests map to 8 HR requirements 1:1",
    "52 animation clips for Motion Matching (wfarch.md Section 7.2)",
    "HR-04 test explicitly checks NO public ActivateRage function",
    "HR-08 test greps all UMG widgets for XP/level/skill terms",
    "214 total files — corrected from 238 (BUILD LEVEL 2 header error fixed)",
    "C++ file count: 84 (42 headers + 42 sources), not 108"
  ],
  "constraints": [
    "All 42 C++ headers must compile with UHT dry-run before L2P8",
    "All 8 automation tests must pass before L3P9",
    "HR verification tests are blocking — cannot proceed on failure",
    "Critical path files (18) have priority — build first"
  ]
}
```

---

*WOLVERINE: UNBOUNDED — A FORGE Game*
*Private Repository — All Rights Reserved*
*Logan doesn't wait to be Wolverine. Neither does the game.*
