# WOLVERINE: UNBOUNDED — Task Schedule (Phase 7)

## GOVERNANCE
**Parent Document:** critic_final.md (Layer 1 Phase 9)
**Status:** READ-ONLY — Layer 1 frozen. Modifications require return to source phase.
**Layer:** L1 | **Phase:** P7

## SUMMARY
Atomic task breakdown with dependencies for all 214 files. Organized by build level (L0-L5) and milestone gates. Each task includes ID, description, input files, output artifacts, dependencies, and estimated complexity.

**Total Tasks:** 220 (84 C++ tasks, 16 Blueprint tasks, 5 config tasks, 8 automation test tasks, 107 content asset tasks)

---

## TASK NOTATION

| Field | Format | Description |
|-------|--------|-------------|
| **Task ID** | `T###` | Unique identifier (e.g., T001, T105) |
| **File Ref** | `Manifest#` | Reference to wf_file_manifest.md entry (e.g., 0.1, 2.3) |
| **Type** | `Header` / `Source` / `BP` / `Config` / `Test` / `Content` | Artifact type |
| **Complexity** | `S` / `M` / `L` / `XL` | Small (<2h), Medium (2-4h), Large (4-8h), XL (>8h) |
| **Dependencies** | `T###` | List of task IDs that must complete first |
| **Output** | `Compile` / `Test` / `Asset` / `Config` | Verification artifact |

---

## MILESTONE GATES

| Gate | ID | Name | Blocking Tasks | Entry Criteria |
|------|----|------|----------------|----------------|
| G1 | `MG-L0-COMPLETE` | Core Types Compiled | T001-T008 | All L0 headers compile with UHT |
| G2 | `MG-L1-COMPLETE` | Systems Functional | T009-T016 | L0 + L1 compile, interfaces verified |
| G3 | `MG-L2-COMPLETE` | Components Ready | T017-T026 | L0-L2 compile, component tests pass |
| G4 | `MG-CLAWS-IN-GAME` | **CRITICAL MILESTONE** | T001-T018 | 18 files compiled, playable claw demo |
| G5 | `MG-L3-COMPLETE` | Character Complete | T027-T038 | Full character functional |
| G6 | `MG-L4-COMPLETE` | AI + World Integrated | T039-T074 | AI behaviors, world systems active |
| G7 | `MG-L5-COMPLETE` | Game Flow Complete | T075-T084 | 72-hour narrative flow |
| G8 | `MG-BP-COMPLETE` | Blueprints Integrated | T085-T099 | All BPs functional |
| G9 | `MG-TESTS-PASS` | Automation Tests Pass | T100-T107 | All 8 HR tests pass |
| G10 | `MG-CONTENT-READY` | Content Assets Complete | T108-T214 | All animations, audio, materials |

---

## BUILD LEVEL 0 — Core Types (8 files)

### Task T001 — WolverineCoreTypes.h
| Field | Value |
|-------|-------|
| **File Ref** | 0.1 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | None |
| **Output** | Compile |

**Description:** Define all core enums and foundational structs.

**Subtasks:**
- T001.1: Define EClawMaterialType (6 values: Flesh, Bone, LightMetal, HeavyMetal, Concrete, Glass) — **HR-06**
- T001.2: Define ERageLevel (3 values: Calm, Agitated, Berserker)
- T001.3: Define ETraversalState (5 values: Grounded, Sprinting, WallClimbing, ClawSwinging, Lunging)
- T001.4: Define EDistrictType (3 values: Basin, Midtown, Ridge)
- T001.5: Define EWeatherState (4 values: Clear, Rain, Overcast, Storm)
- T001.6: Define EWoundSeverity (4 values: Minor, Moderate, Severe, Critical)
- T001.7: Define FWoundData, FMemoryFragment, FIntelItem, FDestructionRecord structs
- T001.8: Add UHT macros (UENUM, USTRUCT, BlueprintType, etc.)

---

### Task T002 — WolverineCoreTypes.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 0.2 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Empty implementation file (enums/structs only, no logic).

**Subtasks:**
- T002.1: Include WolverineCoreTypes.h
- T002.2: Add module export macros

---

### Task T003 — IWolverineMaterialResponse.h
| Field | Value |
|-------|-------|
| **File Ref** | 0.3 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Interface for material detection from hit results.

**Subtasks:**
- T003.1: Define IWolverineMaterialResponse interface class
- T003.2: Declare GetMaterialType(FHitResult) pure virtual function
- T003.3: Add UINTERFACE and IInterface macros

---

### Task T004 — IWolverineMaterialResponse.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 0.4 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T003 |
| **Output** | Compile |

**Description:** Default interface implementation (surface type mapping).

**Subtasks:**
- T004.1: Implement default GetMaterialType (returns LightMetal)
- T004.2: Add PhysicalSurface → EClawMaterialType mapping table

---

### Task T005 — IWolverineDamageInterface.h
| Field | Value |
|-------|-------|
| **File Ref** | 0.5 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Interface for damage application to actors.

**Subtasks:**
- T005.1: Define IWolverineDamageInterface interface class
- T005.2: Declare ApplyDamage(FWoundData) pure virtual function
- T005.3: Declare GetWoundSeverity() const pure virtual function

---

### Task T006 — IWolverineDamageInterface.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 0.6 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T005 |
| **Output** | Compile |

**Description:** Default interface implementation (no-op).

**Subtasks:**
- T006.1: Implement default ApplyDamage (no-op)
- T006.2: Implement default GetWoundSeverity (returns Minor)

---

### Task T007 — WolverineDataStructures.h
| Field | Value |
|-------|-------|
| **File Ref** | 0.7 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** All data structs for wounds, memories, intel, destruction, haptics.

**Subtasks:**
- T007.1: Define FWoundData (BoneName, Severity, DecalHandle, Timestamp)
- T007.2: Define FMemoryFragment (MemoryID, Title, Duration, MechanicalBonus, BonusValue, BlueprintData) — **Layer 3 content slot**
- T007.3: Define FIntelItem (IntelID, Title, Description, AudioLog, IsCollected) — **Layer 3 content slot**
- T007.4: Define FDestructionRecord (ActorGUID, DestructionState, Timestamp, District)
- T007.5: Define FHapticFeedbackData (MaterialType, Strength, Duration, Pattern)
- T007.6: Add USTRUCT and BlueprintType macros

---

### Task T008 — WolverineDataStructures.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 0.8 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T007 |
| **Output** | Compile |

**Description:** Empty implementation file (structs only).

**Subtasks:**
- T008.1: Include WolverineDataStructures.h
- T008.2: Add module export macros

---

## BUILD LEVEL 1 — Systems (8 files)

### Task T009 — WolverineMaterialResponseSystem.h
| Field | Value |
|-------|-------|
| **File Ref** | 1.1 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T003 |
| **Output** | Compile |

**Description:** Material detection system from hit results.

**Subtasks:**
- T009.1: Define UWolverineMaterialResponseSystem class (UObject)
- T009.2: Declare SurfaceMaterialMap (UPROPERTY)
- T009.3: Declare GetMaterialFromHit(FHitResult) function
- T009.4: Declare GetMaterialFromSurface(UPhysicalMaterial) function

---

### Task T010 — WolverineMaterialResponseSystem.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 1.2 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T009, T004 |
| **Output** | Compile |

**Description:** Surface type to EClawMaterialType mapping implementation.

**Subtasks:**
- T010.1: Initialize SurfaceMaterialMap in constructor
- T010.2: Implement GetMaterialFromHit (trace PhysicalMaterial)
- T010.3: Implement GetMaterialFromSurface (lookup table)
- T010.4: Add default mappings for 6 material types — **HR-06**

---

### Task T011 — WolverineWoundSystemComponent.h
| Field | Value |
|-------|-------|
| **File Ref** | 1.3 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T001, T005, T007 |
| **Output** | Compile |

**Description:** Mesh deformation, healing, wound state management.

**Subtasks:**
- T011.1: Define UWolverineWoundSystemComponent class (UActorComponent)
- T011.2: Declare WoundState array (FWoundData)
- T011.3: Declare HealingTickRate (default 10Hz) — **Performance optimization**
- T011.4: Declare ApplyWound(FWoundData) function
- T011.5: Declare HealWound(float DeltaTime) function
- T011.6: Declare GetWoundSeverity() function
- T011.7: Declare morph target references (UPROPERTY) — **HR-02**

---

### Task T012 — WolverineWoundSystemComponent.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 1.4 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T011, T006 |
| **Output** | Compile, Test (HR-02) |

**Description:** 10Hz healing tick, morph target deformation.

**Subtasks:**
- T012.1: Implement TickComponent (10Hz interval)
- T012.2: Implement ApplyWound (add to WoundState, update morph targets)
- T012.3: Implement HealWound (reduce severity over time)
- T012.4: Implement GetWoundSeverity (aggregate calculation)
- T012.5: Add morph target weight calculation — **HR-02**

---

### Task T013 — WolverineAnimationInstance.h
| Field | Value |
|-------|-------|
| **File Ref** | 1.5 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Motion Matching, claw animation blending.

**Subtasks:**
- T013.1: Define UWolverineAnimationInstance class (UAnimInstance)
- T013.2: Declare ClawBlendWeight (float, 0-1)
- T013.3: Declare CurrentTraversalState (ETraversalState)
- T013.4: Declare MotionMatchingDatabase (retracted/deployed)
- T013.5: Declare UpdateClawBlend(float Weight) function

---

### Task T014 — WolverineAnimationInstance.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 1.6 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T013 |
| **Output** | Compile |

**Description:** Motion Matching update, claw blend weights.

**Subtasks:**
- T014.1: Implement NativeUpdateAnimation
- T014.2: Implement UpdateClawBlend (lerp between states)
- T014.3: Add Motion Matching query logic
- T014.4: Add transition clips for claw deploy/retract

---

### Task T015 — WolverineSaveGame.h
| Field | Value |
|-------|-------|
| **File Ref** | 1.7 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Save game class with destruction persistence.

**Subtasks:**
- T015.1: Define UWolverineSaveGame class (USaveGame)
- T015.2: Declare DestructionRecords map (GUID → FDestructionRecord) — **HR-05**
- T015.3: Declare PlayerState (location, health, memories, intel)
- T015.4: Declare GameTimeHours (0-72)
- T015.5: Declare CurrentDistrict, CurrentWeather

---

### Task T016 — WolverineSaveGame.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 1.8 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T015 |
| **Output** | Compile |

**Description:** Constructor implementation.

**Subtasks:**
- T016.1: Implement constructor (initialize default values)
- T016.2: Set SaveGameName, UserIndex, Version

---

## BUILD LEVEL 2 — Components (10 files)

### Task T017 — WolverineClawComponent.h
| Field | Value |
|-------|-------|
| **File Ref** | 2.1 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T001, T003, T009 |
| **Output** | Compile |

**Description:** Claw deployment, material tracing, impact events.

**Subtasks:**
- T017.1: Define UWolverineClawComponent class (UActorComponent)
- T017.2: Declare ClawState enum (Retracted, Deploying, Deployed, Retracting)
- T017.3: Declare DeployClaws() function (BlueprintCallable) — **HR-01**
- T017.4: Declare RetractClaws() function
- T017.5: Declare ClawDeployTime (default 0.15f) — **NFR-02: <200ms**
- T017.6: Declare OnClawImpact delegate (EClawMaterialType)
- T017.7: Declare MaterialTraceHandle (60fps trace)

---

### Task T018 — WolverineClawComponent.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 2.2 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T017, T010 |
| **Output** | Compile, Test (HR-01, HR-06) |

**Description:** 60fps material trace, <200ms deploy.

**Subtasks:**
- T018.1: Implement DeployClaws (timeline, <200ms) — **HR-01 performance test**
- T018.2: Implement RetractClaws
- T018.3: Implement TickComponent (60fps material trace)
- T018.4: Implement OnClawImpact broadcast
- T018.5: Add haptic feedback integration — **HR-06**

---

### Task T019 — WolverineRageComponent.h
| Field | Value |
|-------|-------|
| **File Ref** | 2.3 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Rage accumulation, Berserker state machine.

**Subtasks:**
- T019.1: Define UWolverineRageComponent class (UActorComponent)
- T019.2: Declare CurrentRage (float, 0-100)
- T019.3: Declare CurrentRageLevel (ERageLevel)
- T019.4: Declare OnDamageDealt(float Damage) function (BlueprintCallable) — **HR-04**
- T019.5: Declare OnDamageReceived(float Damage) function (BlueprintCallable) — **HR-04**
- T019.6: Declare AddRage(float Amount) function (**NOT BlueprintCallable**) — **HR-04**
- T019.7: Declare OnBerserkerActivated delegate

---

### Task T020 — WolverineRageComponent.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 2.4 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T019 |
| **Output** | Compile, Test (HR-04) |

**Description:** Event-driven rage (NO manual activation).

**Subtasks:**
- T020.1: Implement OnDamageDealt (add rage from damage dealt)
- T020.2: Implement OnDamageReceived (add rage from damage taken)
- T020.3: Implement AddRage (internal, clamp 0-100) — **NOT BlueprintCallable**
- T020.4: Implement CheckBerserker (auto-trigger at 100) — **HR-04**
- T020.5: Implement rage decay over time

---

### Task T021 — WolverineTraumaSystemComponent.h
| Field | Value |
|-------|-------|
| **File Ref** | 2.5 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Memory unlocks, mechanical bonuses.

**Subtasks:**
- T021.1: Define UWolverineTraumaSystemComponent class (UActorComponent)
- T021.2: Declare UnlockedMemories array (FMemoryFragment)
- T021.3: Declare UnlockMemory(FMemoryFragment) function
- T021.4: Declare GetMechanicalBonus() function
- T021.5: Declare OnMemoryUnlocked delegate — **HR-08**

---

### Task T022 — WolverineTraumaSystemComponent.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 2.6 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T021 |
| **Output** | Compile, Test (HR-08) |

**Description:** Bonus calculation from memories.

**Subtasks:**
- T022.1: Implement UnlockMemory (add to array, broadcast)
- T022.2: Implement GetMechanicalBonus (aggregate from memories)
- T022.3: Define bonus types (healing rate, rage gain, damage resist)
- T022.4: Ensure NO XP/level/skill references — **HR-08**

---

### Task T023 — WolverineAudioComponent.h
| Field | Value |
|-------|-------|
| **File Ref** | 2.7 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** MetaSounds reactive graph.

**Subtasks:**
- T023.1: Define UWolverineAudioComponent class (UActorComponent)
- T023.2: Declare CombatIntensity (float, 0-1)
- T023.3: Declare PlayClawImpactSound(EClawMaterialType) function
- T023.4: Declare UpdateMusicIntensity(float Intensity) function
- T023.5: Declare MetaSound references (UPROPERTY)

---

### Task T024 — WolverineAudioComponent.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 2.8 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T023 |
| **Output** | Compile |

**Description:** Combat intensity → music intensity.

**Subtasks:**
- T024.1: Implement PlayClawImpactSound (per-material audio) — **HR-06**
- T024.2: Implement UpdateMusicIntensity (MetaSound parameter)
- T024.3: Add combat intensity calculation (damage frequency)

---

### Task T025 — HapticFeedbackSystem.h
| Field | Value |
|-------|-------|
| **File Ref** | 2.9 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Asymmetric haptic feedback per claw/material.

**Subtasks:**
- T025.1: Define UHapticFeedbackSystem class (UObject)
- T025.2: Declare HapticDataMap (EClawMaterialType → FHapticFeedbackData)
- T025.3: Declare PlayHaptic(EClawMaterialType, EControllerHand) function
- T025.4: Declare HapticStrength, HapticDuration properties

---

### Task T026 — HapticFeedbackSystem.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 2.10 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T025 |
| **Output** | Compile, Test (HR-06) |

**Description:** Per-material haptic data.

**Subtasks:**
- T026.1: Initialize HapticDataMap in constructor
- T026.2: Implement PlayHaptic (lookup data, trigger controller vibration)
- T026.3: Define per-material patterns (flesh=soft, metal=sharp, etc.) — **HR-06**

---

## BUILD LEVEL 3 — Character (12 files)

### Task T027 — WolverineMovementComponent.h
| Field | Value |
|-------|-------|
| **File Ref** | 3.1 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T001, T017 |
| **Output** | Compile |

**Description:** Custom traversal (sprint, wall climb, claw swing, lunge).

**Subtasks:**
- T027.1: Define UWolverineMovementComponent class (UActorComponent)
- T027.2: Declare CurrentTraversalState (ETraversalState)
- T027.3: Declare Sprint(), WallClimb(), ClawSwing(), ClawLunge() functions
- T027.4: Declare ClawBrake() function (stealth) — **HR-07**
- T027.5: Declare movement parameters (speed, acceleration, lunge distance)

---

### Task T028 — WolverineMovementComponent.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 3.2 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T027 |
| **Output** | Compile, Test (HR-01, HR-07) |

**Description:** Movement state machine.

**Subtasks:**
- T028.1: Implement Sprint (increase speed, stamina drain)
- T028.2: Implement WallClimb (gravity override, stamina drain)
- T028.3: Implement ClawSwing (anchor point, pendulum motion)
- T028.4: Implement ClawLunge (forward burst, claw check) — **HR-01**
- T028.5: Implement ClawBrake (instant stop, stealth) — **HR-07**
- T028.6: Add state transitions and validation

---

### Task T029 — WolverineCharacter.h
| Field | Value |
|-------|-------|
| **File Ref** | 3.3 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T011, T017, T019, T021, T023, T027 |
| **Output** | Compile |

**Description:** Player character — aggregates all components.

**Subtasks:**
- T029.1: Define AWolverineCharacter class (ACharacter)
- T029.2: Declare component references (Claw, Rage, Wound, Trauma, Audio, Movement)
- T029.3: Declare Input_DeployClaws(), Input_RetractClaws() functions — **HR-01**
- T029.4: Declare Input_Sprint(), Input_ClawLunge() functions
- T029.5: Declare Input_LightAttack(), Input_HeavyAttack() functions
- T029.6: Declare Input_Dodge() function

---

### Task T030 — WolverineCharacter.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 3.4 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T029 |
| **Output** | Compile |

**Description:** Component creation, input binding.

**Subtasks:**
- T030.1: Implement constructor (create components, attach)
- T030.2: Implement SetupPlayerInputComponent
- T030.3: Bind input actions to functions — **Q=ClawDeploy (DefaultInput.ini)**
- T030.4: Implement input handlers (call component functions)
- T030.5: Add BeginPlay (initialize state)

---

### Task T031 — WolverinePlayerController.h
| Field | Value |
|-------|-------|
| **File Ref** | 3.5 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T029 |
| **Output** | Compile |

**Description:** Input binding, UI management.

**Subtasks:**
- T031.1: Define AWolverinePlayerController class (APlayerController)
- T031.2: Declare HUDClass reference
- T031.3: Declare InputMappingContext (UPROPERTY)
- T031.4: Declare ShowHUD(), HideHUD() functions

---

### Task T032 — WolverinePlayerController.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 3.6 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T031 |
| **Output** | Compile |

**Description:** Enhanced Input mapping.

**Subtasks:**
- T032.1: Implement BeginPlay (set input mapping)
- T032.2: Implement ShowHUD (create widget)
- T032.3: Implement HideHUD (remove widget)

---

### Task T033 — WolverineHUD.h
| Field | Value |
|-------|-------|
| **File Ref** | 3.7 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Minimal HUD (compass, vignette, wound indicator).

**Subtasks:**
- T033.1: Define UWolverineHUD class (UUserWidget)
- T033.2: Declare CompassWidget reference
- T033.3: Declare WoundIndicatorWidget reference
- T033.4: Declare UpdateWoundIndicator(EWoundSeverity) function
- T033.5: Declare UpdateCompassBearing(float Degrees) function
- T033.6: **NO XP/level/skill references** — **HR-08**

---

### Task T034 — WolverineHUD.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 3.8 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T033 |
| **Output** | Compile, Test (HR-08) |

**Description:** Widget references, state updates.

**Subtasks:**
- T034.1: Implement UpdateWoundIndicator (update vignette)
- T034.2: Implement UpdateCompassBearing (rotate chevron)

---

### Task T035 — WoundIndicatorWidget.h
| Field | Value |
|-------|-------|
| **File Ref** | 3.9 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Wound feedback (not a health bar).

**Subtasks:**
- T035.1: Define UWoundIndicatorWidget class (UUserWidget)
- T035.2: Declare VignetteImage reference
- T035.3: Declare SetSeverity(EWoundSeverity) function
- T035.4: **NOT a health bar** — visual feedback only — **HR-08**

---

### Task T036 — WoundIndicatorWidget.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 3.10 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T035 |
| **Output** | Compile |

**Description:** Vignette pulse based on severity.

**Subtasks:**
- T036.1: Implement SetSeverity (change vignette color/intensity)
- T036.2: Add pulse animation for severe wounds

---

### Task T037 — CompassWidget.h
| Field | Value |
|-------|-------|
| **File Ref** | 3.11 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Compass bearing only.

**Subtasks:**
- T037.1: Define UCompassWidget class (UUserWidget)
- T037.2: Declare CompassArrow reference
- T037.3: Declare SetBearing(float Degrees) function
- T037.4: Declare ObjectiveChevron reference

---

### Task T038 — CompassWidget.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 3.12 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T037 |
| **Output** | Compile |

**Description:** Bearing update, objective chevron.

**Subtasks:**
- T038.1: Implement SetBearing (rotate arrow)
- T038.2: Implement objective chevron direction

---

## BUILD LEVEL 4 — AI + World (36 files)

### Task T039 — WeaponXSoldier.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.1 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T005 |
| **Output** | Compile |

**Description:** Standard infantry AI.

**Subtasks:**
- T039.1: Define AWeaponXSoldier class (ACharacter)
- T039.2: Declare FearLevel (float, 0-100)
- T039.3: Declare BehaviorTree reference
- T039.4: Declare OnFearEscalated delegate — **HR-07**

---

### Task T040 — WeaponXSoldier.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.2 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T039 |
| **Output** | Compile, Test (HR-07) |

**Description:** Behavior Tree execution, fear state.

**Subtasks:**
- T040.1: Implement BehaviorTree execution
- T040.2: Implement fear response (trembling, retreat at high fear) — **HR-07**
- T040.3: Add suppression behavior

---

### Task T041 — WeaponXHeavyUnit.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.3 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T039 |
| **Output** | Compile |

**Description:** Powered armor — claw pry required.

**Subtasks:**
- T041.1: Define AWeaponXHeavyUnit class (AWeaponXSoldier)
- T041.2: Declare ArmorHealth (float)
- T041.3: Declare PryArmor() function (claw interaction)

---

### Task T042 — WeaponXHeavyUnit.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.4 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T041 |
| **Output** | Compile |

**Description:** Armor breach mechanic.

**Subtasks:**
- T042.1: Implement PryArmor (reduce ArmorHealth)
- T042.2: Add breach state (vulnerable after pry)

---

### Task T043 — MutantHunter.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.5 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T039 |
| **Output** | Compile |

**Description:** Healing dampening specialist.

**Subtasks:**
- T043.1: Define AMutantHunter class (AWeaponXSoldier)
- T043.2: Declare DampeningFieldActive (bool)
- T043.3: Declare ActivateDampeningField() function

---

### Task T044 — MutantHunter.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.6 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T043 |
| **Output** | Compile |

**Description:** Dampening field activation.

**Subtasks:**
- T044.1: Implement ActivateDampeningField (reduce player healing)
- T044.2: Add field duration and cooldown

---

### Task T045 — FeralMutant.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.7 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T039 |
| **Output** | Compile |

**Description:** Fast, dodge-heavy enemy.

**Subtasks:**
- T045.1: Define AFeralMutant class (AWeaponXSoldier)
- T045.2: Declare DodgeChance (float)
- T045.3: Declare ChainAttackCombo() function

---

### Task T046 — FeralMutant.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.8 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T045 |
| **Output** | Compile |

**Description:** Evasive dodge, chain attacks.

**Subtasks:**
- T046.1: Implement dodge behavior (random chance)
- T046.2: Implement chain attack combo

---

### Task T047 — Sentinel.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.9 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T039 |
| **Output** | Compile |

**Description:** Late-game boss — multi-phase.

**Subtasks:**
- T047.1: Define ASentinel class (AWeaponXSoldier)
- T047.2: Declare CurrentPhase (enum, 3 phases)
- T047.3: Declare PhaseTransition() function
- T047.4: Declare AreaDestructionAttack() function

---

### Task T048 — Sentinel.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.10 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T047 |
| **Output** | Compile |

**Description:** Phase transitions, area destruction.

**Subtasks:**
- T048.1: Implement phase transitions (health thresholds)
- T048.2: Implement area destruction attacks
- T048.3: Add phase-specific behaviors

---

### Task T049 — PortAshfordWorldSettings.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.11 |
| **Type** | C++ Header |
| **Complexity** | L |
| **Dependencies** | T001, T007, T015 |
| **Output** | Compile |

**Description:** District streaming, weather, destruction persistence.

**Subtasks:**
- T049.1: Define APortAshfordWorldSettings class (AWorldSettings)
- T049.2: Declare CurrentDistrict (EDistrictType)
- T049.3: Declare CurrentWeather (EWeatherState)
- T049.4: Declare GameTimeHours (float, 0-72)
- T049.5: Declare SaveDestructionState() function — **HR-05**
- T049.6: Declare LoadDestructionState() function — **HR-05**

---

### Task T050 — PortAshfordWorldSettings.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.12 |
| **Type** | C++ Source |
| **Complexity** | L |
| **Dependencies** | T049 |
| **Output** | Compile, Test (HR-03, HR-05) |

**Description:** Level streaming, destruction save/load.

**Subtasks:**
- T050.1: Implement SaveDestructionState (serialize to UWolverineSaveGame) — **HR-05**
- T050.2: Implement LoadDestructionState (apply from save) — **HR-05**
- T050.3: Add district streaming logic — **HR-03**
- T050.4: Add weather transition logic

---

### Task T051 — WeatherSystem.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.13 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Dynamic weather transitions.

**Subtasks:**
- T051.1: Define AWeatherSystem class (AActor)
- T051.2: Declare CurrentWeather (EWeatherState)
- T051.3: Declare TransitionWeather(EWeatherState, float Duration) function
- T051.4: Declare NiagaraParticle references

---

### Task T052 — WeatherSystem.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.14 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T051 |
| **Output** | Compile |

**Description:** Weather state machine, Niagara particles.

**Subtasks:**
- T052.1: Implement TransitionWeather (lerp parameters)
- T052.2: Implement Niagara particle activation
- T052.3: Add weather state machine

---

### Task T053 — DestructionPersistenceData.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.15 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Destruction records (survives save/load).

**Subtasks:**
- T053.1: Define UDestructionPersistenceData class (UDataAsset)
- T053.2: Declare DestructionRecords map (GUID → FDestructionRecord) — **HR-05**
- T053.3: Declare AddRecord(FDestructionRecord) function
- T053.4: Declare GetRecord(FGuid) function — **O(1) lookup**

---

### Task T054 — DestructionPersistenceData.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.16 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T053 |
| **Output** | Compile, Test (HR-05) |

**Description:** Data asset implementation.

**Subtasks:**
- T054.1: Implement AddRecord (add to map)
- T054.2: Implement GetRecord (lookup by GUID) — **HR-05**

---

### Task T055 — EscalationManager.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.17 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** City-wide AI escalation.

**Subtasks:**
- T055.1: Define AEscalationManager class (AActor)
- T055.2: Declare NotorietyLevel (float, 0-100)
- T055.3: Declare AddNotoriety(float Amount) function
- T055.4: Declare SpawnPatrol() function

---

### Task T056 — EscalationManager.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.18 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T055 |
| **Output** | Compile |

**Description:** Notoriety decay, patrol spawning.

**Subtasks:**
- T056.1: Implement AddNotoriety (increase level)
- T056.2: Implement notoriety decay over time
- T056.3: Implement SpawnPatrol (based on notoriety)

---

### Task T057 — DistrictStreamingVolume.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.19 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Trigger volume for district transitions.

**Subtasks:**
- T057.1: Define ADistrictStreamingVolume class (AVolume)
- T057.2: Declare TargetDistrict (EDistrictType)
- T057.3: Declare OnPlayerEnter delegate — **HR-03**

---

### Task T058 — DistrictStreamingVolume.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.20 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T057 |
| **Output** | Compile, Test (HR-03) |

**Description:** Seamless district loading.

**Subtasks:**
- T058.1: Implement OnOverlapBegin (trigger streaming)
- T058.2: Add fade transition (no loading screen) — **HR-03**

---

### Task T059 — EnvironmentalDestructible.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.21 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Chaos destruction actor.

**Subtasks:**
- T059.1: Define AEnvironmentalDestructible class (AActor)
- T059.2: Declare ActorGUID (FGuid) — **HR-05**
- T059.3: Declare ChaosDestructionComponent (UPROPERTY)
- T059.4: Declare GetDestructionState() function

---

### Task T060 — EnvironmentalDestructible.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.22 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T059 |
| **Output** | Compile |

**Description:** GUID assignment, destruction state.

**Subtasks:**
- T060.1: Implement constructor (generate GUID)
- T060.2: Implement GetDestructionState (serialize Chaos state)
- T060.3: Add destruction callback (notify persistence) — **HR-05**

---

### Task T061 — SafeHouse.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.23 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Safe house location (4 total).

**Subtasks:**
- T061.1: Define ASafeHouse class (AActor)
- T061.2: Declare SafeHouseID (int, 1-4)
- T061.3: Declare JournalEntry (FText) — **Layer 3 content slot**
- T061.4: Declare OnEnterSafeHouse delegate — **FR-16**

---

### Task T062 — SafeHouse.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.24 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T061 |
| **Output** | Compile |

**Description:** Journal trigger, full heal.

**Subtasks:**
- T062.1: Implement OnOverlapBegin (heal player, show journal) — **FR-16**
- T062.2: Add journal UI trigger — **Layer 3 content**

---

### Task T063 — WeaponXIntelCollectible.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.25 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Weapon X collectible (audio log/photo).

**Subtasks:**
- T063.1: Define AWeaponXIntelCollectible class (AActor)
- T063.2: Declare IntelData (FIntelItem) — **Layer 3 content slot**
- T063.3: Declare OnCollect delegate
- T063.4: **NO map markers** — **FR-15**

---

### Task T064 — WeaponXIntelCollectible.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.26 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T063 |
| **Output** | Compile |

**Description:** Collection trigger, no map markers.

**Subtasks:**
- T064.1: Implement OnOverlapBegin (add to player state, play audio)
- T064.2: Add collectible hide/destroy

---

### Task T065 — MemoryFragmentTrigger.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.27 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Trauma system memory trigger.

**Subtasks:**
- T065.1: Define AMemoryFragmentTrigger class (AActor)
- T065.2: Declare MemoryData (FMemoryFragment) — **Layer 3 content slot**
- T065.3: Declare FlashbackLevel (string path)
- T065.4: Declare OnCollect delegate

---

### Task T066 — MemoryFragmentTrigger.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.28 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T065 |
| **Output** | Compile |

**Description:** Playable flashback trigger.

**Subtasks:**
- T066.1: Implement OnOverlapBegin (unlock memory, start flashback)
- T066.2: Add flashback level streaming

---

### Task T067 — WeaponXSquadLeader.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.29 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T039 |
| **Output** | Compile |

**Description:** Squad coordination.

**Subtasks:**
- T067.1: Define AWeaponXSquadLeader class (AWeaponXSoldier)
- T067.2: Declare SquadMembers array
- T067.3: Declare OrderSquad(FString Command) function

---

### Task T068 — WeaponXSquadLeader.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.30 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T067 |
| **Output** | Compile |

**Description:** Squad tactics, backup calls.

**Subtasks:**
- T068.1: Implement OrderSquad (flank, suppress, retreat)
- T068.2: Add backup call behavior

---

### Task T069 — AIControllerBase.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.31 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Base AI controller.

**Subtasks:**
- T069.1: Define AWolverineAIController class (AAIController)
- T069.2: Declare Blackboard reference
- T069.3: Declare BehaviorTree reference

---

### Task T070 — AIControllerBase.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.32 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T069 |
| **Output** | Compile |

**Description:** Common AI logic.

**Subtasks:**
- T070.1: Implement OnPossess (run BehaviorTree)
- T070.2: Initialize Blackboard

---

### Task T071 — FearStateMachine.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.33 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Fear escalation system.

**Subtasks:**
- T071.1: Define UFearStateMachine class (UActorComponent)
- T071.2: Declare FearLevel (float, 0-100)
- T071.3: Declare AddFear(float Amount) function
- T071.4: Declare OnFearThresholdCrossed delegate — **HR-07**

---

### Task T072 — FearStateMachine.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.34 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T071 |
| **Output** | Compile, Test (HR-07) |

**Description:** Fear level calculation, response.

**Subtasks:**
- T072.1: Implement AddFear (from claw sightings, damage)
- T072.2: Implement fear response (trembling, missed shots, retreat) — **HR-07**
- T072.3: Add fear decay over time

---

### Task T073 — EQSService.h
| Field | Value |
|-------|-------|
| **File Ref** | 4.35 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** EQS query helper.

**Subtasks:**
- T073.1: Define UEQSService class (UObject)
- T073.2: Declare FindFlankPosition() function
- T073.3: Declare FindCover() function
- T073.4: Declare FindRetreatPath() function

---

### Task T074 — EQSService.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 4.36 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T073 |
| **Output** | Compile |

**Description:** Flank/cover/retreat queries.

**Subtasks:**
- T074.1: Implement FindFlankPosition (EQS query)
- T074.2: Implement FindCover (EQS query)
- T074.3: Implement FindRetreatPath (EQS query)

---

## BUILD LEVEL 5 — Game Flow (10 files)

### Task T075 — WolverineGameMode.h
| Field | Value |
|-------|-------|
| **File Ref** | 5.1 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T049 |
| **Output** | Compile |

**Description:** 72-hour narrative, mission flow.

**Subtasks:**
- T075.1: Define AWolverineGameMode class (AGameMode)
- T075.2: Declare GameTimeHours (float, 0-72)
- T075.3: Declare CurrentMission (string)
- T075.4: Declare AdvanceTime(float Hours) function

---

### Task T076 — WolverineGameMode.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 5.2 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T075 |
| **Output** | Compile |

**Description:** District transitions, escalation queries.

**Subtasks:**
- T076.1: Implement AdvanceTime (update GameTimeHours)
- T076.2: Implement mission triggers (time-based)
- T076.3: Add district transition logic

---

### Task T077 — WolverineGameState.h
| Field | Value |
|-------|-------|
| **File Ref** | 5.3 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Replicated game state.

**Subtasks:**
- T077.1: Define AWolverineGameState class (AGameState)
- T077.2: Declare replicated properties (time, weather, district)

---

### Task T078 — WolverineGameState.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 5.4 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T077 |
| **Output** | Compile |

**Description:** State replication.

**Subtasks:**
- T078.1: Implement GetLifetimeReplicatedProps
- T078.2: Add replication notifications

---

### Task T079 — WolverinePlayerState.h
| Field | Value |
|-------|-------|
| **File Ref** | 5.5 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001, T007 |
| **Output** | Compile |

**Description:** Persistent player data (NO XP/levels).

**Subtasks:**
- T079.1: Define AWolverinePlayerState class (APlayerState)
- T079.2: Declare UnlockedMemories array
- T079.3: Declare CollectedIntel array
- T079.4: **NO XP, NO Level, NO SkillPoints** — **HR-08**

---

### Task T080 — WolverinePlayerState.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 5.6 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T079 |
| **Output** | Compile, Test (HR-08) |

**Description:** Memory/intel persistence.

**Subtasks:**
- T080.1: Implement AddMemory(FMemoryFragment)
- T080.2: Implement AddIntel(FIntelItem)
- T080.3: **Ensure NO XP/level/skill code** — **HR-08**

---

### Task T081 — WolverineGameInstance.h
| Field | Value |
|-------|-------|
| **File Ref** | 5.7 |
| **Type** | C++ Header |
| **Complexity** | S |
| **Dependencies** | T015 |
| **Output** | Compile |

**Description:** Game instance (menu to game).

**Subtasks:**
- T081.1: Define UWolverineGameInstance class (UGameInstance)
- T081.2: Declare CurrentSaveGame (UWolverineSaveGame)
- T081.3: Declare LoadGame() function
- T081.4: Declare SaveGame() function

---

### Task T082 — WolverineGameInstance.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 5.8 |
| **Type** | C++ Source |
| **Complexity** | S |
| **Dependencies** | T081 |
| **Output** | Compile |

**Description:** Save/load management.

**Subtasks:**
- T082.1: Implement LoadGame (UGameplayStatics::LoadGameFromSlot)
- T082.2: Implement SaveGame (UGameplayStatics::SaveGameToSlot)

---

### Task T083 — MissionManager.h
| Field | Value |
|-------|-------|
| **File Ref** | 5.9 |
| **Type** | C++ Header |
| **Complexity** | M |
| **Dependencies** | T001 |
| **Output** | Compile |

**Description:** Mission state machine.

**Subtasks:**
- T083.1: Define UMissionManager class (UActorComponent)
- T083.2: Declare CurrentMission (string)
- T083.3: Declare MissionState enum
- T083.4: Declare CompleteMission() function

---

### Task T084 — MissionManager.cpp
| Field | Value |
|-------|-------|
| **File Ref** | 5.10 |
| **Type** | C++ Source |
| **Complexity** | M |
| **Dependencies** | T083 |
| **Output** | Compile |

**Description:** Act transitions, mission triggers.

**Subtasks:**
- T084.1: Implement CompleteMission (transition to next)
- T084.2: Add mission triggers (time, location, kills)

---

## BLUEPRINT CLASSES (10 files)

### Task T085 — BP_WolverineCharacter
| Field | Value |
|-------|-------|
| **File Ref** | BP-01 |
| **Type** | Blueprint |
| **Complexity** | M |
| **Dependencies** | T030 |
| **Output** | Asset |

**Description:** Player character BP.

**Subtasks:**
- T085.1: Create BP from AWolverineCharacter
- T085.2: Assign mesh, components
- T085.3: Configure input mappings

---

### Task T086 — BP_WeaponXSoldier
| Field | Value |
|-------|-------|
| **File Ref** | BP-02 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T040 |
| **Output** | Asset |

**Description:** Soldier AI BP.

**Subtasks:**
- T086.1: Create BP from AWeaponXSoldier
- T086.2: Assign BehaviorTree, Blackboard

---

### Task T087 — BP_WeaponXHeavy
| Field | Value |
|-------|-------|
| **File Ref** | BP-03 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T042 |
| **Output** | Asset |

**Description:** Heavy unit BP.

**Subtasks:**
- T087.1: Create BP from AWeaponXHeavyUnit
- T087.2: Assign armor mesh, behavior

---

### Task T088 — BP_MutantHunter
| Field | Value |
|-------|-------|
| **File Ref** | BP-04 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T044 |
| **Output** | Asset |

**Description:** Hunter AI BP.

**Subtasks:**
- T088.1: Create BP from AMutantHunter
- T088.2: Configure dampening field

---

### Task T089 — BP_FeralMutant
| Field | Value |
|-------|-------|
| **File Ref** | BP-05 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T046 |
| **Output** | Asset |

**Description:** Feral AI BP.

**Subtasks:**
- T089.1: Create BP from AFeralMutant
- T089.2: Configure dodge behavior

---

### Task T090 — BP_Sentinel
| Field | Value |
|-------|-------|
| **File Ref** | BP-06 |
| **Type** | Blueprint |
| **Complexity** | M |
| **Dependencies** | T048 |
| **Output** | Asset |

**Description:** Boss BP.

**Subtasks:**
- T090.1: Create BP from ASentinel
- T090.2: Configure phase transitions

---

### Task T091 — BP_EscalationManager
| Field | Value |
|-------|-------|
| **File Ref** | BP-07 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T056 |
| **Output** | Asset |

**Description:** Escalation BP.

**Subtasks:**
- T091.1: Create BP from AEscalationManager
- T091.2: Configure notoriety parameters

---

### Task T092 — BP_WeatherSystem
| Field | Value |
|-------|-------|
| **File Ref** | BP-08 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T052 |
| **Output** | Asset |

**Description:** Weather BP.

**Subtasks:**
- T092.1: Create BP from AWeatherSystem
- T092.2: Assign Niagara systems

---

### Task T093 — BP_WolverineHUD
| Field | Value |
|-------|-------|
| **File Ref** | BP-09 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T034 |
| **Output** | Asset, Test (HR-08) |

**Description:** HUD BP.

**Subtasks:**
- T093.1: Create BP from UWolverineHUD
- T093.2: Design widget layout (compass, vignette)
- T093.3: **NO XP/level/skill widgets** — **HR-08**

---

### Task T094 — BP_WoundIndicator
| Field | Value |
|-------|-------|
| **File Ref** | BP-10 |
| **Type** | Blueprint |
| **Complexity** | S |
| **Dependencies** | T036 |
| **Output** | Asset |

**Description:** Wound UI BP.

**Subtasks:**
- T094.1: Create BP from UWoundIndicatorWidget
- T094.2: Design vignette visual

---

## BLUEPRINT-ONLY SYSTEMS (6 files)

### Task T095 — BT_WeaponXSoldier + BB_WeaponXSoldier
| Field | Value |
|-------|-------|
| **File Ref** | BP-BT-01, BP-BB-01 |
| **Type** | Behavior Tree + Blackboard |
| **Complexity** | M |
| **Dependencies** | T086 |
| **Output** | Asset |

**Description:** Soldier behavior (Flank, Suppress, Retreat).

**Subtasks:**
- T095.1: Create Blackboard (TargetActor, LastSeenPos, FearLevel)
- T095.2: Create Behavior Tree with tasks (Flank, Suppress, Retreat)
- T095.3: Add EQS query nodes

---

### Task T096 — EQS_FlankPosition
| Field | Value |
|-------|-------|
| **File Ref** | BP-EQS-01 |
| **Type** | EQS Query |
| **Complexity** | S |
| **Dependencies** | T074 |
| **Output** | Asset |

**Description:** Flank position query.

**Subtasks:**
- T096.1: Create EQS query (distance from player, angle)
- T096.2: Add cover test

---

### Task T097 — EQS_CoverSearch
| Field | Value |
|-------|-------|
| **File Ref** | BP-EQS-02 |
| **Type** | EQS Query |
| **Complexity** | S |
| **Dependencies** | T074 |
| **Output** | Asset |

**Description:** Cover search query.

**Subtasks:**
- T097.1: Create EQS query (cover actors, distance to player)
- T097.2: Add line-of-sight test

---

### Task T098 — EQS_RetreatPath
| Field | Value |
|-------|-------|
| **File Ref** | BP-EQS-03 |
| **Type** | EQS Query |
| **Complexity** | S |
| **Dependencies** | T074 |
| **Output** | Asset |

**Description:** Retreat path query.

**Subtasks:**
- T098.1: Create EQS query (safe locations, distance from player)
- T098.2: Add navigation test

---

### Task T099 — BPD_WolverineInput
| Field | Value |
|-------|-------|
| **File Ref** | BP-IA-01 |
| **Type** | Input Actions |
| **Complexity** | S |
| **Dependencies** | T030 |
| **Output** | Asset, Config |

**Description:** Input actions/mappings.

**Subtasks:**
- T099.1: Create Input Actions (IA_ClawDeploy, IA_ClawLunge, IA_Sprint, IA_LightAttack, IA_HeavyAttack, IA_Dodge)
- T099.2: Create Input Mapping Context
- T099.3: Assign key bindings (Q=ClawDeploy, MMB=ClawLunge, LShift=Sprint, LMB=LightAttack, RMB=HeavyAttack, Space=Dodge) — **HR-01**

---

## CONFIG FILES (5 files)

### Task T100 — DefaultGame.ini
| Field | Value |
|-------|-------|
| **File Ref** | CFG-01 |
| **Type** | Config |
| **Complexity** | S |
| **Dependencies** | T075 |
| **Output** | Config |

**Description:** Game settings, project metadata.

**Subtasks:**
- T100.1: Set ProjectID, ProjectName, CompanyName
- T100.2: Configure WolverineGameMode defaults (StartingDistrict=Basin, StartingTimeHours=0.0, StartingWeather=Rain)

---

### Task T101 — DefaultInput.ini
| Field | Value |
|-------|-------|
| **File Ref** | CFG-02 |
| **Type** | Config |
| **Complexity** | S |
| **Dependencies** | T099 |
| **Output** | Config |

**Description:** Input mappings (Enhanced Input).

**Subtasks:**
- T101.1: Set DefaultMappingContext
- T101.2: Configure input bindings (Q=ClawDeploy, MMB=ClawLunge, LShift=Sprint, LMB=LightAttack, RMB=HeavyAttack, Space=Dodge) — **HR-01**

---

### Task T102 — DefaultEngine.ini
| Field | Value |
|-------|-------|
| **File Ref** | CFG-03 |
| **Type** | Config |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Config |

**Description:** Engine settings, plugins.

**Subtasks:**
- T102.1: Enable Nanite, Lumen, Virtual Shadows
- T102.2: Set TargetFrameRate=60 — **NFR-01**
- T102.3: Enable Motion Matching plugin

---

### Task T103 — DefaultEditor.ini
| Field | Value |
|-------|-------|
| **File Ref** | CFG-04 |
| **Type** | Config |
| **Complexity** | S |
| **Dependencies** | None |
| **Output** | Config |

**Description:** Editor settings.

**Subtasks:**
- T103.1: Configure editor preferences
- T103.2: Set play-in-editor defaults

---

### Task T104 — DefaultScalability.ini
| Field | Value |
|-------|-------|
| **File Ref** | CFG-05 |
| **Type** | Config |
| **Complexity** | S |
| **Dependencies** | T001 |
| **Output** | Config |

**Description:** Performance scalability (60fps target).

**Subtasks:**
- T104.1: Define scalability profiles (Low, Medium, High, Epic)
- T104.2: Set resolution scale, shadow quality, post-process — **NFR-01**

---

## AUTOMATION TESTS (8 files)

### Task T105 — Test_WolverineClaw
| Field | Value |
|-------|-------|
| **File Ref** | TEST-01 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T018 |
| **Output** | Test (HR-01, HR-06) |

**Description:** Claw deploy time, material detection, impact events.

**Subtasks:**
- T105.1: Implement ClawDeployTime test (<200ms) — **HR-01**
- T105.2: Implement MaterialDetection test (6 types) — **HR-06**
- T105.3: Implement ImpactEvent test (delegate fires)

---

### Task T106 — Test_WolverineWoundSystem
| Field | Value |
|-------|-------|
| **File Ref** | TEST-02 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T012 |
| **Output** | Test (HR-02) |

**Description:** Wound application, healing tick rate, mesh deformation.

**Subtasks:**
- T106.1: Implement WoundApplication test — **HR-02**
- T106.2: Implement HealingTickRate test (10Hz) — **HR-02**
- T106.3: Implement MeshDeformation test (morph targets) — **HR-02**

---

### Task T107 — Test_WolverineRage
| Field | Value |
|-------|-------|
| **File Ref** | TEST-03 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T020 |
| **Output** | Test (HR-04) |

**Description:** Rage fill from damage, Berserker trigger, NO manual activation.

**Subtasks:**
- T107.1: Implement NoManualActivation test (NO ActivateRage function) — **HR-04**
- T107.2: Implement AddRageNotBlueprintCallable test — **HR-04**
- T107.3: Implement BerserkerTrigger test (at 100 rage) — **HR-04**

---

### Task T108 — Test_WolverineMovement
| Field | Value |
|-------|-------|
| **File Ref** | TEST-04 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T028 |
| **Output** | Test (HR-01, HR-07) |

**Description:** Traversal states, claw lunge distance, wall climb.

**Subtasks:**
- T108.1: Implement TraversalStates test (all 5 states)
- T108.2: Implement ClawLungeDistance test — **HR-01**
- T108.3: Implement WallClimb test
- T108.4: Implement StealthLoudOptions test (HR-07) — **HR-07**

---

### Task T109 — Test_DestructionPersistence
| Field | Value |
|-------|-------|
| **File Ref** | TEST-05 |
| **Type** | Automation |
| **Complexity** | L |
| **Dependencies** | T050, T054 |
| **Output** | Test (HR-03, HR-05) |

**Description:** Destruction save/load, GUID lookup, district transition.

**Subtasks:**
- T109.1: Implement DestructionSaveLoad test — **HR-05**
- T109.2: Implement GUIDLookup test (O(1)) — **HR-05**
- T109.3: Implement DistrictTransition test (no loading screen) — **HR-03**

---

### Task T110 — Test_MaterialResponse
| Field | Value |
|-------|-------|
| **File Ref** | TEST-06 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T010, T026 |
| **Output** | Test (HR-06) |

**Description:** 6 material types, surface mapping, haptic response.

**Subtasks:**
- T110.1: Implement SixMaterialTypes test — **HR-06**
- T110.2: Implement SurfaceMapping test — **HR-06**
- T110.3: Implement HapticResponse test (per-material) — **HR-06**

---

### Task T111 — Test_TraumaSystem
| Field | Value |
|-------|-------|
| **File Ref** | TEST-07 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T022 |
| **Output** | Test (HR-08) |

**Description:** Memory unlocks, bonus calculation, NO XP/levels.

**Subtasks:**
- T111.1: Implement MemoryUnlocks test — **HR-08**
- T111.2: Implement BonusCalculation test — **HR-08**
- T111.3: Implement NoXPLevels test (verify NO XP/skill code) — **HR-08**

---

### Task T112 — Test_HUDCompliance
| Field | Value |
|-------|-------|
| **File Ref** | TEST-08 |
| **Type** | Automation |
| **Complexity** | M |
| **Dependencies** | T034, T093 |
| **Output** | Test (HR-08) |

**Description:** UMG widget grep for XP/level/skill references.

**Subtasks:**
- T112.1: Implement NoXPUILeferences test (grep "XP", "Experience", "Level", "SkillPoint", "SkillTree") — **HR-08**
- T112.2: Implement MinimalHUD test (compass, vignette only) — **HR-08**

---

## CONTENT ASSETS (101 files)

### Animation Assets (52 files) — T113 to T164

| Task Range | Category | Count | Dependencies | Complexity |
|------------|----------|-------|--------------|------------|
| T113-T118 | Locomotion | 6 | T014 | M each |
| T119-T122 | Wall Climbing | 4 | T014 | M each |
| T123-T126 | Claw Swing | 4 | T014 | M each |
| T127-T130 | Claw Lunge | 4 | T014 | M each |
| T131-T148 | Combat | 18 | T014 | M each |
| T149-T153 | Predator/Stealth | 5 | T014 | M each |
| T154-T157 | Damage/Healing | 4 | T014 | M each |
| T158-T164 | Blend Spaces | 7 | T014 | M each |

**Note:** 52 animation clips for Motion Matching (wfarch.md Section 7.2)

---

### Audio Assets (12 files) — T165 to T176

| Task Range | Type | Count | Dependencies | Complexity |
|------------|------|-------|--------------|------------|
| T165-T170 | MetaSound Sources | 6 | T024 | S each |
| T171-T176 | Claw Impact Sounds | 6 | T024 | S each |
| T177 | Healing Sounds | 1 | T024 | S |
| T178 | Berserker Music | 1 | T024 | S |
| T179-T182 | Ambient Tracks | 4 | T024 | S each |

---

### Material Assets (6 files) — T183 to T188

| Task Range | Type | Count | Dependencies | Complexity |
|------------|------|-------|--------------|------------|
| T183-T188 | Claw Impact Materials | 6 | T010 | S each |

---

### Data Assets (31 files) — T189 to T219

| Task Range | Type | Count | Dependencies | Complexity | Notes |
|------------|------|-------|--------------|------------|-------|
| T189-T198 | Memory Fragment Data | 10 | T022 | S each | **Layer 3 content** — titles, descriptions, bonuses |
| T199-T213 | Weapon X Intel Data | 15 | T022 | S each | **Layer 3 content** — audio logs, photos |
| T214-T219 | Haptic Feedback Data | 6 | T026 | S each | Per-material haptic patterns |

---

## TASK DEPENDENCY GRAPH

### Critical Path (CLAWS IN GAME — 18 files)
```
T001 → T002 (L0 Core Types)
T001 → T003 → T004 (Material Interface)
T001 → T005 → T006 (Damage Interface)
T001 → T007 → T008 (Data Structures)
T001,T003 → T009 → T010 (Material System)
T001,T005,T007 → T011 → T012 (Wound System)
T001 → T013 → T014 (Animation Instance)
T001,T007 → T015 → T016 (Save Game)
T001,T003,T009 → T017 → T018 (Claw Component) ← HR-01, HR-06
T017 → T027 → T028 (Movement Component) ← HR-01, HR-07
T011,T017,T019,T021,T023,T027 → T029 → T030 (Character)
```

**Milestone MG-CLAWS-IN-GAME:** T001-T018 complete (18 files)

---

## MILESTONE SCHEDULE

| Milestone | Tasks | Entry Criteria | Exit Criteria |
|-----------|-------|----------------|---------------|
| MG-L0-COMPLETE | T001-T008 | None | All L0 headers compile |
| MG-L1-COMPLETE | T009-T016 | MG-L0-COMPLETE | L0+L1 compile, interfaces work |
| MG-L2-COMPLETE | T017-T026 | MG-L1-COMPLETE | Components functional |
| **MG-CLAWS-IN-GAME** | T001-T018 | MG-L2-COMPLETE | **Playable claw demo** |
| MG-L3-COMPLETE | T027-T038 | MG-CLAWS-IN-GAME | Full character ready |
| MG-L4-COMPLETE | T039-T074 | MG-L3-COMPLETE | AI + World integrated |
| MG-L5-COMPLETE | T075-T084 | MG-L4-COMPLETE | Game flow complete |
| MG-BP-COMPLETE | T085-T099 | MG-L5-COMPLETE | All BPs functional |
| MG-TESTS-PASS | T100-T107 | MG-BP-COMPLETE | All 8 HR tests pass |
| MG-CONTENT-READY | T108-T219 | MG-TESTS-PASS | All content assets ready |

---

## TASK COUNT SUMMARY

| Category | Task Count | Task IDs |
|----------|------------|----------|
| **L0 Core Types** | 8 | T001-T008 |
| **L1 Systems** | 8 | T009-T016 |
| **L2 Components** | 10 | T017-T026 |
| **L3 Character** | 12 | T027-T038 |
| **L4 AI + World** | 36 | T039-T074 |
| **L5 Game Flow** | 10 | T075-T084 |
| **Blueprint Classes** | 10 | T085-T094 |
| **Blueprint-Only Systems** | 5 | T095-T099 |
| **Config Files** | 5 | T100-T104 |
| **Automation Tests** | 8 | T105-T112 |
| **Animation Assets** | 52 | T113-T164 |
| **Audio Assets** | 12 | T165-T182 |
| **Material Assets** | 6 | T183-T188 |
| **Data Assets** | 31 | T189-T219 |
| **TOTAL** | **213 tasks** | |

---

## HR VERIFICATION TASKS

| HR | Verifying Tasks | Milestone |
|----|-----------------|-----------|
| HR-01 (Claws <10s) | T018, T028, T099, T101, T105, T108 | MG-CLAWS-IN-GAME |
| HR-02 (Mesh deformation) | T012, T106 | MG-L1-COMPLETE |
| HR-03 (No loading screens) | T050, T058, T109 | MG-L4-COMPLETE |
| HR-04 (Rage event-driven) | T020, T107 | MG-L2-COMPLETE |
| HR-05 (Persistent destruction) | T050, T054, T109 | MG-L4-COMPLETE |
| HR-06 (6 material types) | T001, T010, T018, T026, T105, T110 | MG-L2-COMPLETE |
| HR-07 (Predator optional) | T028, T040, T072, T108 | MG-L4-COMPLETE |
| HR-08 (No skill trees) | T022, T034, T080, T093, T111, T112 | MG-L5-COMPLETE |

---

## LAYER 1 GAP RESOLUTIONS

The following gaps identified in the Layer 1 audit have been resolved:

| Gap | Resolution | Task Reference |
|-----|------------|----------------|
| Opening sequence design | HR-01 enforced via DeployClaws() <200ms + input binding (Q key). No tutorial system. Opening = first 10 seconds of gameplay. | T017, T018, T099, T101 |
| Memory fragment content | FMemoryFragment struct fully defined. 10 data asset slots allocated (T189-T198). Content creation is Layer 3. | T007, T189-T198 |
| Weapon X Intel content | FIntelItem struct fully defined. 15 data asset slots allocated (T199-T213). Content creation is Layer 3. | T007, T199-T213 |
| Safe house journal system | ASafeHouse class complete with JournalEntry property. 4 safe houses defined. Content is Layer 3. | T061, T062 |

---

## DECISION_HASH

```json
{
  "document": "task_schedule.md",
  "project": "wolf.beast",
  "version": "1.0",
  "created": "2026-03-09",
  "derived_from": ["wf_file_manifest.md", "wfcritic_prebuild.md", "wfmod.dep.md", "wfdep.graph.md"],
  "total_tasks": 213,
  "cpp_tasks": 84,
  "blueprint_tasks": 16,
  "config_tasks": 5,
  "automation_test_tasks": 8,
  "content_asset_tasks": 100,
  "critical_path_tasks": 18,
  "milestone_gates": 10,
  "hr_verification_tasks": {
    "HR-01": ["T018", "T028", "T099", "T101", "T105", "T108"],
    "HR-02": ["T012", "T106"],
    "HR-03": ["T050", "T058", "T109"],
    "HR-04": ["T020", "T107"],
    "HR-05": ["T050", "T054", "T109"],
    "HR-06": ["T001", "T010", "T018", "T026", "T105", "T110"],
    "HR-07": ["T028", "T040", "T072", "T108"],
    "HR-08": ["T022", "T034", "T080", "T093", "T111", "T112"]
  },
  "layer1_gaps_resolved": [
    "Opening sequence: DeployClaws() <200ms + Q key binding (no tutorial)",
    "Memory fragments: FMemoryFragment struct complete, 10 data slots (Layer 3 content)",
    "Weapon X Intel: FIntelItem struct complete, 15 data slots (Layer 3 content)",
    "Safe house journal: ASafeHouse class complete, JournalEntry property (Layer 3 narrative)"
  ],
  "key_decisions": [
    "213 atomic tasks defined for 214 files (some files combined)",
    "18 critical path tasks for CLAWS IN GAME milestone (T001-T018)",
    "10 milestone gates from L0 to content complete",
    "Each HR requirement has explicit verification tasks",
    "Task dependencies mirror build levels from wfmod.dep.md",
    "Content assets (101 files) scheduled after code complete",
    "Automation tests (8) block final milestone",
    "Layer 1 gaps resolved — content creation deferred to Layer 3"
  ],
  "constraints": [
    "T018 (ClawComponent) must complete in <200ms (HR-01)",
    "T020 (RageComponent) must NOT have BlueprintCallable AddRage (HR-04)",
    "T034, T080, T093 must NOT reference XP/levels/skills (HR-08)",
    "T050, T058 must have seamless district transitions (HR-03)",
    "T105-T112 (automation tests) must pass before MG-TESTS-PASS"
  ]
}
```

---

*WOLVERINE: UNBOUNDED — A FORGE Game*
*Private Repository — All Rights Reserved*
*Logan doesn't wait to be Wolverine. Neither does the game.*
