# WOLVERINE: UNBOUNDED — Architecture Specification

## GOVERNANCE
**Parent Document:** critic_final.md (Layer 1 Phase 9)
**Status:** READ-ONLY — Layer 1 frozen. Modifications require return to source phase.
**Layer:** L1 | **Phase:** P2

## SUMMARY
Complete UE5 architecture for Wolverine: Unbounded. Defines GameMode hierarchy, character components (Claw, Wound, Rage, Movement, Trauma), AI systems (Weapon X soldiers, fear escalation), world architecture (Port Ashford districts, persistent destruction), audio (MetaSounds reactive graph), and HUD (minimal, wound-driven). All components map to FR/NFR/HR requirements from wolf.beastprompt.md.

---

## 1. GAME MODE HIERARCHY

### 1.1 UWolverineGameMode
```
Parent: AGameMode
Purpose: Manages 72-hour narrative timeline, district state, mission flow
Key Properties:
  - CurrentDistrict: EDistrictType (Basin, Midtown, Ridge)
  - GameTimeHours: float (0-72 hour story clock)
  - WeatherState: EWeatherType (Clear, Rain, Storm)
  - WeaponXEscalationLevel: int (0-5 city-wide threat)
  - MutantUndergroundTrust: float (0-1 faction reputation)
Key Functions:
  - StartGame() → void
  - AdvanceTime(float Hours) → void
  - TriggerDistrictTransition(EDistrictType) → void
  - GetEscalationManager() → AEscalationManager*
BlueprintCallable: Yes (game flow events)
```

### 1.2 UWolverineGameState
```
Parent: AGameState
Purpose: Replicates game state to all clients (future multiplayer-ready)
Key Properties:
  - ReplicatedCurrentTime: float (server-authoritative)
  - ReplicatedWeather: EWeatherType
  - ActiveRagePlayers: TArray<AWolverineCharacter*> (debug)
Replication: All properties replicated
```

### 1.3 UWolverinePlayerState
```
Parent: APlayerState
Purpose: Player-specific persistent data (no XP/skills per HR-08)
Key Properties:
  - MemoriesUnlocked: TArray<FMemoryFragment>
  - WeaponXIntelCollected: TArray<FIntelItem>
  - TotalDamageTaken: float (session stat)
  - TotalKills: int32 (session stat)
  - LongestCombo: int32 (session stat)
Note: NO level, NO skill points, NO XP — HR-08 compliance
```

---

## 2. CHARACTER COMPONENT ARCHITECTURE

### 2.1 UWolverineClawComponent
```
Parent: UActorComponent
Purpose: Claw deployment, material detection, impact response
Dependencies: IWolverineMaterialResponse, UGameplayStatics
Key Properties:
  - LeftClawDeployed: bool
  - RightClawDeployed: bool
  - ClawDeployTime: float (target: <200ms NFR-02)
  - MaterialTraceInterval: float (per-frame at 60fps)
  - CurrentLeftMaterial: EClawMaterialType
  - CurrentRightMaterial: EClawMaterialType
  - OnClawImpact: FMulticastDelegate(FHitResult, EClawMaterialType, EClawSide)
Key Functions:
  - DeployClaws(EClawSide) → void (BlueprintCallable)
  - RetractClaws(EClawSide) → void (BlueprintCallable)
  - AreClawsDeployed() → bool (BlueprintPure)
  - GetClawMaterial(EClawSide) → EClawMaterialType (BlueprintPure)
  - PerformMaterialTrace(EClawSide) → EClawMaterialType
  - OnImpact(FHitResult, EClawMaterialType, EClawSide) → void
Tick: Yes (per-frame for material trace during combat)
TickGroup: TG_PrePhysics
NFR Mapping: NFR-02 (<200ms deploy), NFR-08 (audio never masked)
HR Mapping: HR-01 (deploy <10s), HR-06 (6 materials)
```

### 2.2 EClawMaterialType (Enum)
```
Values:
  Flesh = 0
  Bone = 1
  LightMetal = 2    (aluminum, thin steel)
  HeavyMetal = 3    (armor, reinforced)
  Concrete = 4
  Glass = 5
Count: Exactly 6 types (HR-06 compliance)
Usage: UWolverineClawComponent, UWolverineAudioComponent, UHapticFeedbackSystem
```

### 2.3 UWolverineWoundSystemComponent
```
Parent: UActorComponent
Purpose: Real-time mesh deformation, healing visualization, wound state
Dependencies: Chaos Physics, SkeletalMeshComponent
Key Properties:
  - ActiveWounds: TArray<FWoundData>
  - HealingRate: float (base 1.0, increases with rage)
  - MeshDeformationActive: bool
  - MaxSimultaneousWounds: int32 (performance cap)
  - VisualHealingDelay: float (500ms per NFR-03)
Key Structures:
  FWoundData:
    - Location: FVector (world space)
    - Severity: float (0-1)
    - Age: float (seconds since inflicted)
    - HealingProgress: float (0-1)
    - BoneName: FName (for deformation target)
    - DecalHandle: FDecalHandle (visual blood/damage)
Key Functions:
  - ApplyWound(FVector Location, float Severity) → void (BlueprintCallable)
  - GetTotalWoundSeverity() → float (BlueprintPure)
  - IsHealing() → bool (BlueprintPure)
  - SetHealingRate(float Rate) → void
  - TickHealing(float DeltaTime) → void
Tick: Yes (healing tick at 10Hz, not 60fps — performance optimization)
TickGroup: TG_PostUpdateWork
TickInterval: 0.1f (10 times per second)
NFR Mapping: NFR-03 (healing visual <500ms), NFR-01 (60fps budget)
HR Mapping: HR-02 (real-time mesh deformation)
Note: Nanite conflict resolution — Logan uses non-Nanite skeletal mesh.
      World geometry uses Nanite. Character mesh deforms via skeleton +
      morph targets, not Nanite geometry.
```

### 2.4 UWolverineRageComponent
```
Parent: UActorComponent
Purpose: Rage accumulation, Berserker Mode state machine, damage multiplier
Dependencies: UWolverineWoundSystemComponent, UWolverineClawComponent
Key Properties:
  - CurrentRage: float (0-100)
  - RageFillRate: float (from damage dealt/taken)
  - RageDrainRate: float (when idle >30s)
  - BerserkerActive: bool
  - BerserkerTimeRemaining: float
  - DamageMultiplier: float (1.0 normal, 3.0 berserker)
  - IdleTimer: float (tracks time since last combat action)
Key Functions:
  - AddRage(float Amount) → void (internal, from damage events)
  - ConsumeRage(float Amount) → void (for healing boost)
  - GetRageLevel() → ERageLevel (Low, Mid, Full) (BlueprintPure)
  - GetDamageMultiplier() → float (BlueprintPure)
  - IsBerserkerActive() → bool (BlueprintPure)
  - OnDamageDealt(float Amount, AActor* Target) → void (event handler)
  - OnDamageReceived(float Amount, AActor* Source) → void (event handler)
  - TickRage(float DeltaTime) → void
Tick: Yes (rage drain check, Berserker countdown)
TickGroup: TG_UpdateWork
CRITICAL HR-04 COMPLIANCE:
  - NO public ActivateRage() function exists
  - NO BlueprintCallable on rage-filling methods
  - Rage ONLY fills via OnDamageDealt/OnDamageReceived events
  - Berserker triggers automatically at 100 rage — no player input
NFR Mapping: NFR-01 (60fps), NFR-04 (AI response <100ms to rage state)
HR Mapping: HR-04 (event-driven only, no manual activation)
```

### 2.5 ERageLevel (Enum)
```
Values:
  Low = 0     (0-33 rage, normal combat)
  Mid = 1     (34-99 rage, claw trails, faster healing)
  Full = 2    (100 rage, Berserker Mode, 3x damage, 20s duration)
Usage: UWolverineRageComponent, UWolverineAudioComponent, UPostProcessManager
```

### 2.6 UWolverineMovementComponent
```
Parent: UCharacterMovementComponent
Purpose: Custom movement for predator-style traversal
Dependencies: Character, CollisionComponent
Key Properties:
  - SprintSpeed: float (base 800 units/s)
  - ClawSprintSpeed: float (700 units/s, combat-ready)
  - WallClimbSpeed: float (vertical 400 units/s)
  - ClawSwingLaunchForce: float (2000 units forward vector)
  - ClawLungeDistance: float (15-20m per prompt)
  - ClawLungeForce: float (3000 units toward target)
  - IsWallClimbing: bool
  - IsClawSwinging: bool
  - IsClawLunging: bool
  - CurrentTraversalState: ETraversalState
Key Functions:
  - StartSprint() → void (BlueprintCallable)
  - StartClawSprint() → void (BlueprintCallable)
  - StartWallClimb(FVector WallNormal) → void (BlueprintCallable)
  - StartClawSwing(FVector AnchorPoint) → void (BlueprintCallable)
  - PerformClawLunge(AActor* Target) → void (BlueprintCallable)
  - PerformDropAttack() → void (BlueprintCallable)
  - PerformClawBrake() → void (BlueprintCallable)
  - GetTraversalState() → ETraversalState (BlueprintPure)
Tick: Yes (movement state machine, surface detection)
TickGroup: TG_PrePhysics (must run before physics simulation)
NFR Mapping: NFR-01 (60fps movement), NFR-02 (claw lunge <200ms)
HR Mapping: HR-01 (claws deploy fast), HR-07 (predator optional)
```

### 2.7 ETraversalState (Enum)
```
Values:
  Grounded = 0
  Sprinting = 1
  ClawSprinting = 2
  WallClimbing = 3
  ClawSwinging = 4
  ClawLunging = 5
  Falling = 6
  ClawBraking = 7
  LedgeVaulting = 8
Usage: UWolverineMovementComponent, UWolverineAnimationInstance
```

### 2.8 UWolverineTraumaSystemComponent
```
Parent: UActorComponent
Purpose: Memory fragment unlocks, mechanical bonuses (no XP/skills)
Dependencies: UWolverinePlayerState
Key Properties:
  - UnlockedMemories: TArray<FMemoryFragment>
  - ComboWindowExtension: float (base 0.3s, max +0.2s)
  - RageFillRateBonus: float (base 1.0, max +0.5)
  - HealingEfficiencyBonus: float (base 1.0, max +0.3)
Key Structures:
  FMemoryFragment:
    - MemoryID: FName
    - Title: FText
    - Duration: float (30-60 seconds playable)
    - MechanicalBonus: ETraumaBonusType
    - BonusValue: float
    - IsUnlocked: bool
    - BlueprintData: UDataAsset (memory content)
Key Functions:
  - UnlockMemory(FName MemoryID) → void (BlueprintCallable)
  - GetComboWindow() → float (BlueprintPure)
  - GetRageFillRateMultiplier() → float (BlueprintPure)
  - GetHealingEfficiency() → float (BlueprintPure)
  - PlayMemoryFragment(FName MemoryID) → void
Tick: No (event-driven only)
HR Mapping: HR-08 (no skill trees — progression via memories only)
FR Mapping: FR-11 (Trauma System progression)
```

---

## 3. AI ARCHITECTURE

### 3.1 AWeaponXSoldier (AI Character)
```
Parent: ACharacter
Purpose: Standard Weapon X infantry — trained, coordinated, flanking
Key Properties:
  - SquadMember: AWeaponXSquadLeader* (null if independent)
  - FearLevel: float (0-1, increases with player rage)
  - CurrentTactic: ESoldierTactic (Flank, Suppress, Retreat, CallBackup)
  - HasLineOfSight: bool
  - LastKnownPlayerLocation: FVector
Key Functions:
  - EnterFearState(float FearLevel) → void
  - ExecuteTactic(ESoldierTactic) → void
  - ReportPlayerPosition(FVector Location) → void
  - CallForBackup() → void
Behavior Tree: BT_WeaponXSoldier
Blackboard: BB_WeaponXSoldier (keys: TargetActor, LastSeenPos, FearLevel, SquadStatus)
EQS Queries: EQS_FlankPosition, EQS_CoverSearch, EQS_RetreatPath
FR Mapping: FR-09 (soldier coordination, fear response, escalation)
```

### 3.2 ESoldierTactic (Enum)
```
Values:
  Advance = 0
  Flank = 1
  Suppress = 2
  Retreat = 3
  CallBackup = 4
  Freeze = 5      (high fear, no line of sight)
  Flee = 6        (maximum fear, Berserker Mode visible)
Usage: AWeaponXSoldier AI decision making
```

### 3.3 AWeaponXHeavyUnit (AI Character)
```
Parent: ACharacter
Purpose: Powered armor — requires claw pry to damage
Key Properties:
  - ArmorHealth: float (separate from Health)
  - IsArmorBreached: bool
  - ArmorMaterial: EClawMaterialType (HeavyMetal)
Key Functions:
  - AttemptClawPry() → bool (player must trigger via claw interaction)
  - BreachArmor() → void
  - GetEffectiveHealth() → float
FR Mapping: FR-09 (enemy types — Heavy Units)
```

### 3.4 AMutantHunter (AI Character)
```
Parent: ACharacter
Purpose: Counter-mutant specialist — can dampen healing factor
Key Properties:
  - DampeningFieldActive: bool
  - DampeningRadius: float (500 units)
  - HealingSuppressionFactor: float (0.5 = 50% healing reduction)
Key Functions:
  - ActivateDampeningField() → void
  - DeactivateDampeningField() → void
  - IsPlayerInDampeningField() → bool
FR Mapping: FR-09 (enemy types — Mutant Hunters)
```

### 3.5 AFeralMutant (AI Character)
```
Parent: ACharacter
Purpose: Fast, unpredictable, dodge-heavy enemy
Key Properties:
  - DodgeCooldown: float
  - AggressionLevel: float
  - CurrentCombo: int32 (feral mutants combo like player)
Key Functions:
  - PerformEvasiveDodge() → void
  - ChainAttack() → void
  - GetAggressionMultiplier() → float
FR Mapping: FR-09 (enemy types — Feral Mutants)
```

### 3.6 ASentinel (AI Character)
```
Parent: ACharacter
Purpose: Late-game large enemy, multi-phase, environmental destruction
Key Properties:
  - CurrentPhase: ESentinelPhase (1-3)
  - HealthThresholds: TArray<float> (phase transition points)
  - DestructionRadius: float (area damage in phase 3)
Key Functions:
  - TransitionToPhase(ESentinelPhase) → void
  - PerformAreaAttack(FVector Center, float Radius) → void
  - DestroyEnvironmentInRange() → void
FR Mapping: FR-09 (enemy types — Sentinels late game)
```

### 3.7 AEscalationManager
```
Parent: AActor
Purpose: City-wide AI state — tracks Logan's actions, escalates response
Key Properties:
  - CurrentEscalationLevel: int (0-5)
  - PlayerNotoriety: float (0-1, decays over time)
  - ActivePatrols: int
  - PolicePresence: float (0-1 per district)
  - WeaponXDeployment: float (0-1 per district)
Key Functions:
  - AddNotoriety(float Amount) → void (from kills, destruction)
  - UpdateEscalationLevel() → void
  - SpawnPatrolAtLocation(FVector Location) → void
  - GetDistrictAlertLevel(EDistrictType) → float
Tick: Yes (notoriety decay, patrol management)
TickInterval: 1.0f (once per second)
FR Mapping: FR-14 (mutant escalation system, city response)
```

---

## 4. WORLD ARCHITECTURE

### 4.1 APortAshfordWorldSettings
```
Parent: AWorldSettings
Purpose: District streaming, weather, time-of-day, destruction persistence
Key Properties:
  - CurrentDistrict: EDistrictType
  - TimeOfDay: float (0-24 hours, compressed 72-hour story)
  - WeatherType: EWeatherType
  - RainIntensity: float (0-1)
  - DestructionPersistence: UDestructionPersistenceData*
  - StreamingSubLevels: TMap<EDistrictType, FSoftObjectPath>
Key Functions:
  - TransitionToDistrict(EDistrictType) → void
  - SetTimeOfDay(float Hours) → void
  - SetWeatherType(EWeatherType) → void
  - GetDestructionStateAtLocation(FVector) → FDestructionState
  - SaveDestructionState() → void
  - LoadDestructionState() → void
HR Mapping: HR-03 (no loading screens), HR-05 (persistent destruction)
FR Mapping: FR-12 (dynamic weather), FR-13 (persistent destruction)
```

### 4.2 EDistrictType (Enum)
```
Values:
  Basin = 0     (starting area, industrial, rain-heavy)
  Midtown = 1   (downtown, civilian dense, police presence)
  Ridge = 2     (residential, campus, Weapon X HQ)
Usage: APortAshfordWorldSettings, UWolverineGameMode
```

### 4.3 EWeatherType (Enum)
```
Values:
  Clear = 0
  Overcast = 1
  Rain = 2
  Storm = 3
Usage: APortAshfordWorldSettings, UWolverineAudioComponent, UPostProcessManager
```

### 4.4 UDestructionPersistenceData
```
Parent: UDataAsset
Purpose: Survives save/load, level streaming — tracks all destruction
Key Properties:
  - DestroyedActors: TArray<FDestructionRecord>
  - DamagedActors: TArray<FDamageRecord>
  - LevelInstanceID: FGuid
Key Structures:
  FDestructionRecord:
    - ActorGUID: FGuid
    - ActorClass: TSubclassOf<AActor>
    - DestroyedLocation: FVector
    - DestroyedRotation: FRotator
    - DestructionTime: float (game time)
    - Cause: EDestructionCause (Claw, Explosion, Fall, Environmental)
  FDamageRecord:
    - ActorGUID: FGuid
    - DamageSeverity: float
    - DamageLocation: FVector
    - VisualState: EDamageVisual (Scratched, Dented, Cracked, Shattered)
HR Mapping: HR-05 (persistent destruction survives reload)
NFR Mapping: NFR-06 (destruction state survives save/load)
FR Mapping: FR-13 (persistent environmental destruction)
```

### 4.5 AWeatherSystem
```
Parent: AActor
Purpose: Dynamic weather transitions, rain effects, visibility impact
Key Properties:
  - CurrentWeather: EWeatherType
  - TransitionProgress: float (0-1 between weather states)
  - RainParticleSystem: UNiagaraComponent*
  - WindDirection: FVector
  - LightningTimer: float (storm-only)
Key Functions:
  - TransitionToWeather(EWeatherType, float TransitionTime) → void
  - GetVisibilityMultiplier() → float (affects AI sight)
  - GetSurfaceFrictionMultiplier() → float (affects movement)
  - TriggerLightning() → void
Tick: Yes (weather transitions, particle updates)
FR Mapping: FR-12 (dynamic weather system)
```

---

## 5. AUDIO ARCHITECTURE (MetaSounds)

### 5.1 UWolverineAudioComponent
```
Parent: UAudioComponent
Purpose: MetaSounds reactive graph, combat intensity → music intensity
Dependencies: MetaSound plugin, UWolverineRageComponent, UWolverineClawComponent
Key Properties:
  - CombatIntensity: float (0-1, from combo count + enemy count)
  - RageVignetteIntensity: float (from rage level)
  - CurrentMaterial: EClawMaterialType (last impact)
  - MetaSoundSource: UMetaSoundSource*
  - ReactiveParameters: FAudioReactiveParams
Key Structures:
  FAudioReactiveParams:
    - TempoBPM: float (60-140, scales with combat intensity)
    - PercussionLayer: float (0-1, full percussion at Berserker)
    - DistortionLayer: float (0-1, rage mode = max distortion)
    - ClawImpactEQ: FEqualizerSettings (per material type)
    - AmbientLayer: float (0-1, exploration vs combat)
Key Functions:
  - SetCombatIntensity(float Intensity) → void
  - SetRageLevel(ERageLevel) → void
  - PlayClawImpact(EClawMaterialType) → void
  - PlayHealingSound() → void
  - TriggerBerserkerMusic() → void
  - UpdateReactiveParameters() → void
NFR Mapping: NFR-08 (claw impact never masked by music)
FR Mapping: FR-18 (reactive audio score)
HR Mapping: HR-06 (6 material audio responses)
```

### 5.2 UHapticFeedbackSystem
```
Parent: UActorComponent
Purpose: Asymmetric haptic feedback per claw, per material
Dependencies: InputCore, Platform-specific haptic plugin
Key Properties:
  - LeftClawHapticStrength: float (0-1, per material)
  - RightClawHapticStrength: float (0-1, per material)
  - HapticDuration: float (material-dependent)
  - HapticFrequency: float (material-dependent)
Key Structures:
  FHapticFeedbackData:
    - Material: EClawMaterialType
    - LeftStrength: float
    - RightStrength: float
    - Duration: float
    - Frequency: float
    - Pattern: EHapticPattern (Steady, Pulse, Burst, Wave)
Key Functions:
  - TriggerClawImpact(EClawMaterialType, EClawSide) → void
  - TriggerRageActivation() → void (Berserker = strong asymmetric pulse)
  - TriggerDamageReceived(FVector Location, float Severity) → void
  - TriggerHealing() → void (subtle continuous vibration)
NFR Mapping: NFR-02 (haptic response <200ms from claw impact)
FR Mapping: FR-20 (haptic feedback system)
HR Mapping: HR-06 (per-material haptic response)
```

---

## 6. HUD ARCHITECTURE (Minimal)

### 6.1 UWolverineHUD
```
Parent: UUserWidget
Purpose: Minimal HUD — wound density, rage vignette, compass only
Key Properties:
  - CompassWidget: UCompassWidget*
  - RageVignette: UImage* (post-process overlay)
  - ObjectiveText: UTextBlock*
  - WoundIndicator: UWoundIndicatorWidget* (subtle, not a bar)
Key Functions:
  - UpdateCompassBearing(float Degrees) → void
  - SetRageVignetteIntensity(float Intensity) → void
  - SetObjectiveText(FText Text) → void
  - ShowClawDeploymentIndicator(bool bDeployed) → void
HR Mapping: HR-08 (no XP/level/skill UI — wound-driven health)
FR Mapping: FR-19 (minimal HUD)
```

### 6.2 UWoundIndicatorWidget
```
Parent: UUserWidget
Purpose: Visual wound feedback — not a health bar
Key Properties:
  - WoundOverlay: UImage* (red vignette, pulses with wound severity)
  - HealingIndicator: UImage* (green pulse when healing active)
Key Functions:
  - UpdateWoundSeverity(float Severity) → void
  - ShowHealingActive(bool bActive) → void
Note: This is NOT a health bar. It is a visual feedback layer
      that pulses based on wound state. Player reads Logan's
      body model for actual wound density.
HR Mapping: HR-08 (no traditional health bar)
FR Mapping: FR-19 (wound-based health visualization)
```

### 6.3 UCompassWidget
```
Parent: UUserWidget
Purpose: Compass bearing only — no waypoint beam
Key Properties:
  - CurrentBearing: float (degrees)
  - ObjectiveMarker: UImage* (subtle chevron, not a beam)
Key Functions:
  - UpdateBearing(float Degrees) → void
  - SetObjectiveDirection(float Degrees) → void
FR Mapping: FR-19 (compass bearing only, no waypoint beam)
```

---

## 7. ANIMATION ARCHITECTURE (Motion Matching)

### 7.1 UWolverineAnimationInstance
```
Parent: UAnimInstance
Purpose: Motion Matching for fluid traversal, procedural claw integration
Dependencies: Motion Matching plugin (UE5.3+)
Key Properties:
  - CurrentTraversalState: ETraversalState
  - MotionMatchingData: FMotionMatchingData
  - ClawBlendWeight: float (0-1, retracted → deployed)
  - RootMotionMode: ERootMotionMode
Key Structures:
  FMotionMatchingData:
    - DesiredVelocity: FVector
    - DesiredDirection: FVector
    - CurrentPose: FName
    - BlendSpaceInput: FVector2D
  FClawAnimationData:
    - LeftClawDeployBlend: float
    - RightClawDeployBlend: float
    - ClawImpactStun: float (micro-stutter on impact)
Key Functions:
  - UpdateMotionMatching(FVector Velocity, FVector Direction) → void
  - BlendClawDeployment(float LeftBlend, float RightBlend) → void
  - TriggerClawImpactStun(EClawSide) → void
  - TransitionToWallClimb() → void
  - TransitionToClawSwing() → void
  - TriggerLungeAnimation(AActor* Target) → void
NFR Mapping: NFR-01 (60fps animation), NFR-02 (claw lunge fluidity)
FR Mapping: FR-02 (seamless traversal), FR-03 (freeform combo)
```

### 7.2 Motion Matching Clip Database
```
Required Animation Clips:
  Locomotion:
    - Sprint_Forward (0°-360° directional)
    - Sprint_ClawDeployed (separate — claws affect posture)
    - Walk_Forward
    - Strafe_Left, Strafe_Right
    - Idle_CombatReady
    - Idle_Relaxed

  Wall Climbing:
    - WallClimb_Start (transition from ground)
    - WallClimb_Loop (vertical, horizontal, diagonal)
    - WallClimb_JumpOff (transition to air)
    - WallClimb_Grab (procedural hand placement)

  Claw Swing:
    - ClawSwing_Attach (throw claw, grab surface)
    - ClawSwing_Swing (pendulum arc)
    - ClawSwing_Release (launch)
    - ClawSwing_Landing (impact absorption)

  Claw Lunge:
    - ClawLunge_Start (windup)
    - ClawLunge_Airborne (mid-flight)
    - ClawLunge_Impact (contact)
    - ClawLunge_Recovery (reset stance)

  Combat:
    - LightAttack_01-05 (5 variants, directional)
    - HeavyAttack_01-03 (3 variants, slower)
    - Dodge_Forward, Dodge_Left, Dodge_Right, Dodge_Back
    - Grab_Standing, Grab_Wall, Grab_Ledge
    - ComboChain_01-10 (10 fluid chains)

  Predator/Stealth:
    - Stealth_Walk
    - Stealth_Takedown_Floor
    - Stealth_Takedown_Wall
    - Stealth_Takedown_Ledge
    - Vent_Crawl

  Damage/Healing:
    - Damage_Flesh_Impact (micro-stutter)
    - Damage_Heavy_Stagger
    - Healing_Active (visible recovery animation blend)
    - Death_Feral, Death_Heavy

Total Clips: ~50 minimum for fluid traversal
Blend Spaces: 8 (directional locomotion, wall climb, claw swing, lunge)
NFR Mapping: NFR-01 (60fps), NFR-07 (seamless <2s transitions)
FR Mapping: FR-02 (seamless traversal)
```

---

## 8. REQUIREMENT MAPPING MATRIX

| Component | FR | NFR | HR |
|-----------|----|-----|----|
| UWolverineClawComponent | FR-03, FR-04, FR-07 | NFR-02, NFR-08 | HR-01, HR-06 |
| UWolverineWoundSystemComponent | FR-06 | NFR-01, NFR-03 | HR-02 |
| UWolverineRageComponent | FR-05 | NFR-01, NFR-04 | HR-04 |
| UWolverineMovementComponent | FR-02 | NFR-01, NFR-02 | HR-01, HR-07 |
| UWolverineTraumaSystemComponent | FR-11 | - | HR-08 |
| AWeaponXSoldier | FR-09 | NFR-04 | HR-07 |
| AEscalationManager | FR-14 | NFR-05 | - |
| APortAshfordWorldSettings | FR-12, FR-13 | NFR-06 | HR-03, HR-05 |
| UWolverineAudioComponent | FR-18 | NFR-08 | HR-06 |
| UHapticFeedbackSystem | FR-20 | NFR-02 | HR-06 |
| UWolverineHUD | FR-19 | - | HR-08 |
| UWolverineAnimationInstance | FR-02, FR-03 | NFR-01, NFR-07 | - |

---

## 9. TECHNICAL RESOLUTIONS

### 9.1 Nanite + Mesh Deformation Conflict (HR-02)
**Problem:** Nanite does not support skeletal mesh deformation.
**Resolution:** Logan character uses non-Nanite skeletal mesh with:
  - High-poly base mesh (traditional LODs)
  - Morph targets for wound deformation
  - Skeleton-driven mesh distortion
  - Decal overlays for blood/damage visualization
World geometry uses Nanite for density without LOD pop.
**Trade-off:** Logan mesh has traditional LODs (acceptable — single character).

### 9.2 Persistent Destruction + Level Streaming (HR-05)
**Problem:** District streaming reloads level — destruction must persist.
**Resolution:** UDestructionPersistenceData is:
  - Saved to player save game (binary serialized)
  - Loaded on district entry
  - Applied via level instance references (GUID-based)
  - Actors tagged with persistent GUIDs at level design time
**Implementation:** FDestroyRecord stores ActorGUID → on load, find actor by GUID, apply destruction state.

### 9.3 Motion Matching + Claw Integration
**Problem:** Claws change posture — standard locomotion clips invalid.
**Resolution:** Dual motion matching databases:
  - DB_Retracted: all clips with claws retracted
  - DB_Deployed: all clips with claws deployed
  - Runtime blend based on UWolverineClawComponent state
  - Transition clips for deploy/retract mid-motion
**Cost:** 2x animation data (acceptable — traversal is core pillar).

### 9.4 Rage Event-Driven Enforcement (HR-04)
**Problem:** Prevent any manual rage activation path.
**Resolution:**
  - UWolverineRageComponent has NO public ActivateRage()
  - AddRage() is internal, called only by:
    - OnDamageReceived event (from UWolverineWoundSystemComponent)
    - OnDamageDealt event (from UWolverineClawComponent impact)
  - Berserker triggers automatically at 100 rage — no player input
  - Blueprint exposes GetRageLevel() (read-only), not SetRage()
**Enforcement:** Critic greps all Blueprint for ActivateRage → zero results required.

---

## 10. MODULE DEPENDENCIES (High-Level)

```
Level 0 (Core):
  WolverineCoreTypes.h      (enums, structs, interfaces)
  IWolverineMaterialResponse.h
  IWolverineDamageInterface.h

Level 1 (Systems):
  WolverineWoundSystemComponent.h
  WolverineMaterialResponseSystem.h

Level 2 (Character):
  WolverineClawComponent.h
  WolverineRageComponent.h
  WolverineTraumaSystemComponent.h

Level 3 (Player):
  WolverineCharacter.h
  WolverineMovementComponent.h
  WolverineAnimationInstance.h
  WolverinePlayerController.h

Level 4 (AI + World):
  WeaponXSoldier.h
  EscalationManager.h
  PortAshfordWorldSettings.h
  WeatherSystem.h

Level 5 (UI + Audio):
  WolverineHUD.h
  WolverineAudioComponent.h
  HapticFeedbackSystem.h
```

---

## 11. PLUGIN DEPENDENCIES

| Plugin | Type | Version | Purpose |
|--------|------|---------|---------|
| Chaos | Built-in | UE5.3+ | Physics, destruction, ragdoll |
| Nanite | Built-in | UE5.3+ | World geometry (not character) |
| Lumen | Built-in | UE5.3+ | Global illumination, wet surfaces |
| Motion Matching | Built-in | UE5.3+ | Traversal animation |
| MetaSounds | Built-in | UE5.3+ | Reactive audio score |
| Enhanced Input | Built-in | UE5.3+ | Claw deployment, movement input |
| DualSense Haptics | Built-in | UE5.3+ | Asymmetric trigger resistance |
| MassAI | Built-in | UE5.3+ | City population (civilians) |
| Niagara | Built-in | UE5.3+ | Weather particles, claw effects |

All plugins are UE5.3+ built-in — no marketplace dependencies.

---

## DECISION_HASH
```json
{
  "document": "wfarch.md",
  "project": "wolf.beast",
  "version": "1.0",
  "created": "2026-03-08",
  "derived_from": ["wolf.beastprompt.md", "quickstart.md", "wfreqs.md"],
  "key_decisions": [
    "Logan uses non-Nanite skeletal mesh for wound deformation (HR-02)",
    "UWolverineRageComponent has NO public ActivateRage() — HR-04 enforced",
    "Destruction persists via GUID-based UDestructionPersistenceData — HR-05",
    "Dual motion matching databases (Retracted/Deployed) for claw posture",
    "6 EClawMaterialType values exactly — HR-06",
    "No XP/level/skill in any component — HR-08",
    "WoundSystem ticks at 10Hz (not 60fps) for performance — NFR-01",
    "Motion Matching requires ~50 animation clips minimum"
  ],
  "constraints": [
    "All components must pass 60fps on PS5/Xbox Series X — NFR-01",
    "Claw deploy-to-impact <200ms — NFR-02",
    "Healing visual begins <500ms — NFR-03",
    "AI response to rage state <100ms — NFR-04",
    "40+ civilians visible in populated districts — NFR-05",
    "Destruction survives save/load — NFR-06",
    "Memory fragment load <2s — NFR-07",
    "Claw impact audio never masked — NFR-08"
  ],
  "component_count": 12,
  "ai_character_count": 5,
  "enum_count": 9,
  "fr_mapped": 20,
  "nfr_mapped": 8,
  "hr_mapped": 8
}
```

---

*WOLVERINE: UNBOUNDED — A FORGE Game*
*Private Repository — All Rights Reserved*
*Logan doesn't wait to be Wolverine. Neither does the game.*
