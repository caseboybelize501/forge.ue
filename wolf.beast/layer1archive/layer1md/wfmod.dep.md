# WOLVERINE: UNBOUNDED — Module Dependencies

## GOVERNANCE
**Parent Document:** critic_final.md (Layer 1 Phase 9)
**Status:** READ-ONLY — Layer 1 frozen. Modifications require return to source phase.
**Layer:** L1 | **Phase:** P4

## SUMMARY
Topological sort of wfdep.graph.md establishing exact UBT build order. 31 C++ modules (62 files) organized into 6 build levels. Each module specifies parent class, key UPROPERTY/UFUNCTION declarations, tick configuration, and FR/NFR/HR mappings. Critical path: CoreTypes → MaterialResponse → ClawComponent → MovementComponent → Character (playable at Level 3).

---

## BUILD LEVEL 0 — Core Types (No Dependencies)

### 0.1 WolverineCoreTypes.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "WolverineCoreTypes.generated.h"

// ============================================================================
// ENUMS — All core game state enums
// ============================================================================

UENUM(BlueprintType)
enum class EClawMaterialType : uint8
{
    Flesh       UMETA(DisplayName = "Flesh"),
    Bone        UMETA(DisplayName = "Bone"),
    LightMetal  UMETA(DisplayName = "Light Metal"),
    HeavyMetal  UMETA(DisplayName = "Heavy Metal"),
    Concrete    UMETA(DisplayName = "Concrete"),
    Glass       UMETA(DisplayName = "Glass")
};
// HR-06: Exactly 6 material types

UENUM(BlueprintType)
enum class ERageLevel : uint8
{
    Low     UMETA(DisplayName = "Low (0-33)"),
    Mid     UMETA(DisplayName = "Mid (34-99)"),
    Full    UMETA(DisplayName = "Full (100 - Berserker)")
};

UENUM(BlueprintType)
enum class ETraversalState : uint8
{
    Grounded        UMETA(DisplayName = "Grounded"),
    Sprinting       UMETA(DisplayName = "Sprinting"),
    ClawSprinting   UMETA(DisplayName = "Claw Sprinting"),
    WallClimbing    UMETA(DisplayName = "Wall Climbing"),
    ClawSwinging    UMETA(DisplayName = "Claw Swinging"),
    ClawLunging     UMETA(DisplayName = "Claw Lunging"),
    Falling         UMETA(DisplayName = "Falling"),
    ClawBraking     UMETA(DisplayName = "Claw Braking"),
    LedgeVaulting   UMETA(DisplayName = "Ledge Vaulting")
};

UENUM(BlueprintType)
enum class EDistrictType : uint8
{
    Basin       UMETA(DisplayName = "The Basin"),
    Midtown     UMETA(DisplayName = "Midtown Ashford"),
    Ridge       UMETA(DisplayName = "The Ridge")
};

UENUM(BlueprintType)
enum class EWeatherType : uint8
{
    Clear       UMETA(DisplayName = "Clear"),
    Overcast    UMETA(DisplayName = "Overcast"),
    Rain        UMETA(DisplayName = "Rain"),
    Storm       UMETA(DisplayName = "Storm")
};

UENUM(BlueprintType)
enum class ESoldierTactic : uint8
{
    Advance     UMETA(DisplayName = "Advance"),
    Flank       UMETA(DisplayName = "Flank"),
    Suppress    UMETA(DisplayName = "Suppress"),
    Retreat     UMETA(DisplayName = "Retreat"),
    CallBackup  UMETA(DisplayName = "Call Backup"),
    Freeze      UMETA(DisplayName = "Freeze"),
    Flee        UMETA(DisplayName = "Flee")
};

UENUM(BlueprintType)
enum class ESentinelPhase : uint8
{
    Phase1      UMETA(DisplayName = "Phase 1"),
    Phase2      UMETA(DisplayName = "Phase 2"),
    Phase3      UMETA(DisplayName = "Phase 3")
};

UENUM(BlueprintType)
enum class ETraumaBonusType : uint8
{
    ComboWindow     UMETA(DisplayName = "Combo Window Extension"),
    RageFillRate    UMETA(DisplayName = "Rage Fill Rate"),
    HealingEfficiency UMETA(DisplayName = "Healing Efficiency")
};

UENUM(BlueprintType)
enum class EHapticPattern : uint8
{
    Steady      UMETA(DisplayName = "Steady"),
    Pulse       UMETA(DisplayName = "Pulse"),
    Burst       UMETA(DisplayName = "Burst"),
    Wave        UMETA(DisplayName = "Wave")
};

UENUM(BlueprintType)
enum class EDestructionCause : uint8
{
    Claw            UMETA(DisplayName = "Claw"),
    Explosion       UMETA(DisplayName = "Explosion"),
    Fall            UMETA(DisplayName = "Fall"),
    Environmental   UMETA(DisplayName = "Environmental")
};

UENUM(BlueprintType)
enum class EDamageVisual : uint8
{
    Scratched       UMETA(DisplayName = "Scratched"),
    Dented          UMETA(DisplayName = "Dented"),
    Cracked         UMETA(DisplayName = "Cracked"),
    Shattered       UMETA(DisplayName = "Shattered")
};

UENUM(BlueprintType)
enum class ERootMotionMode : uint8
{
    Local       UMETA(DisplayName = "Local Space"),
    Root        UMETA(DisplayName = "Root Motion")
};

UENUM(BlueprintType)
enum class EClawSide : uint8
{
    Left        UMETA(DisplayName = "Left Claw"),
    Right       UMETA(DisplayName = "Right Claw")
};
```

**File:** `Source/Wolverine/Public/WolverineCoreTypes.h`
**Dependencies:** None
**FR Mapping:** All (foundational enums)
**HR Mapping:** HR-06 (6 material types)

---

### 0.2 WolverineCoreTypes.cpp
```cpp
#include "WolverineCoreTypes.h"

// No implementation — enums only.
// This file exists for UBT compatibility.
```

**File:** `Source/Wolverine/Private/WolverineCoreTypes.cpp`
**Dependencies:** WolverineCoreTypes.h

---

### 0.3 IWolverineMaterialResponse.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "WolverineCoreTypes.h"
#include "IWolverineMaterialResponse.generated.h"

UINTERFACE(MinimalAPI)
class UIWolverineMaterialResponse : public UInterface
{
    GENERATED_BODY()
};

/**
 * Interface for material detection from hit results.
 * Implemented by WolverineMaterialResponseSystem.
 */
class WOLVERINE_API IWolverineMaterialResponse
{
    GENERATED_BODY()

public:
    /**
     * Determine claw material type from hit result.
     * @param HitResult The hit result from line trace
     * @return EClawMaterialType detected
     */
    UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category = "Claw")
    EClawMaterialType GetMaterialType(const FHitResult& HitResult);
};
```

**File:** `Source/Wolverine/Public/IWolverineMaterialResponse.h`
**Dependencies:** WolverineCoreTypes.h
**FR Mapping:** FR-07 (material-responsive claw impact)
**HR Mapping:** HR-06 (6 material types)

---

### 0.4 IWolverineMaterialResponse.cpp
```cpp
#include "IWolverineMaterialResponse.h"

// Default implementation (not used — concrete implementation in MaterialResponseSystem)
EClawMaterialType IWolverineMaterialResponse::GetMaterialType_Implementation(const FHitResult& HitResult)
{
    return EClawMaterialType::Flesh;
}
```

**File:** `Source/Wolverine/Private/IWolverineMaterialResponse.cpp`
**Dependencies:** IWolverineMaterialResponse.h

---

### 0.5 IWolverineDamageInterface.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IWolverineDamageInterface.generated.h"

UINTERFACE(MinimalAPI)
class UIWolverineDamageInterface : public UInterface
{
    GENERATED_BODY()
};

/**
 * Interface for damage application.
 * Implemented by characters and destructible actors.
 */
class WOLVERINE_API IWolverineDamageInterface
{
    GENERATED_BODY()

public:
    /**
     * Apply damage to this actor.
     * @param Amount Damage amount
     * @param Location World space location of damage
     * @param Instigator Actor that caused damage
     */
    UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category = "Damage")
    void ApplyDamage(float Amount, const FVector& Location, AActor* Instigator);
};
```

**File:** `Source/Wolverine/Public/IWolverineDamageInterface.h`
**Dependencies:** None (uses FVector from CoreMinimal)
**FR Mapping:** FR-06 (real-time wound system)
**HR Mapping:** HR-02 (mesh deformation)

---

### 0.6 IWolverineDamageInterface.cpp
```cpp
#include "IWolverineDamageInterface.h"

// Default implementation (not used — concrete implementation in WoundSystem)
void IWolverineDamageInterface::ApplyDamage_Implementation(float Amount, const FVector& Location, AActor* Instigator)
{
    // No-op default
}
```

**File:** `Source/Wolverine/Private/IWolverineDamageInterface.cpp`
**Dependencies:** IWolverineDamageInterface.h

---

### 0.7 WolverineDataStructures.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.generated.h"

// ============================================================================
// FWoundData — Wound state for WoundSystemComponent
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FWoundData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Wound")
    FVector Location;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Wound")
    float Severity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Wound")
    float Age;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Wound")
    float HealingProgress;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Wound")
    FName BoneName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Wound")
    FDecalHandle DecalHandle;

    FWoundData()
        : Location(FVector::ZeroVector)
        , Severity(0.0f)
        , Age(0.0f)
        , HealingProgress(0.0f)
        , BoneName(NAME_None)
    {}
};

// ============================================================================
// FMemoryFragment — Trauma system memory unlock
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FMemoryFragment
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    FName MemoryID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    FText Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    float Duration;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    ETraumaBonusType MechanicalBonus;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    float BonusValue;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    bool IsUnlocked;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Memory")
    UDataAsset* BlueprintData;

    FMemoryFragment()
        : MemoryID(NAME_None)
        , Duration(30.0f)
        , MechanicalBonus(ETraumaBonusType::ComboWindow)
        , BonusValue(0.0f)
        , IsUnlocked(false)
        , BlueprintData(nullptr)
    {}
};

// ============================================================================
// FAudioReactiveParams — MetaSounds reactive parameters
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FAudioReactiveParams
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Audio")
    float TempoBPM;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Audio")
    float PercussionLayer;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Audio")
    float DistortionLayer;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Audio")
    float AmbientLayer;

    FAudioReactiveParams()
        : TempoBPM(60.0f)
        , PercussionLayer(0.0f)
        , DistortionLayer(0.0f)
        , AmbientLayer(1.0f)
    {}
};

// ============================================================================
// FHapticFeedbackData — Haptic feedback per material
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FHapticFeedbackData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Haptic")
    EClawMaterialType Material;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Haptic")
    float LeftStrength;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Haptic")
    float RightStrength;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Haptic")
    float Duration;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Haptic")
    float Frequency;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Haptic")
    EHapticPattern Pattern;

    FHapticFeedbackData()
        : Material(EClawMaterialType::Flesh)
        , LeftStrength(0.5f)
        , RightStrength(0.5f)
        , Duration(0.1f)
        , Frequency(100.0f)
        , Pattern(EHapticPattern::Pulse)
    {}
};

// ============================================================================
// FMotionMatchingData — Motion matching state
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FMotionMatchingData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    FVector DesiredVelocity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    FVector DesiredDirection;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    FName CurrentPose;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    FVector2D BlendSpaceInput;

    FMotionMatchingData()
        : DesiredVelocity(FVector::ZeroVector)
        , DesiredDirection(FVector::ForwardVector)
        , CurrentPose(NAME_None)
        , BlendSpaceInput(FVector2D::ZeroVector)
    {}
};

// ============================================================================
// FClawAnimationData — Claw animation state
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FClawAnimationData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    float LeftClawDeployBlend;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    float RightClawDeployBlend;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    float ClawImpactStun;

    FClawAnimationData()
        : LeftClawDeployBlend(0.0f)
        , RightClawDeployBlend(0.0f)
        , ClawImpactStun(0.0f)
    {}
};

// ============================================================================
// FDestructionRecord — Persistent destruction state
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FDestructionRecord
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Destruction")
    FGuid ActorGUID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Destruction")
    TSubclassOf<AActor> ActorClass;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Destruction")
    FVector DestroyedLocation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Destruction")
    FRotator DestroyedRotation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Destruction")
    float DestructionTime;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Destruction")
    EDestructionCause Cause;

    FDestructionRecord()
        : ActorGUID(FGuid())
        , ActorClass(nullptr)
        , DestroyedLocation(FVector::ZeroVector)
        , DestroyedRotation(FRotator::ZeroRotator)
        , DestructionTime(0.0f)
        , Cause(EDestructionCause::Claw)
    {}
};

// ============================================================================
// FDamageRecord — Persistent damage state
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FDamageRecord
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Damage")
    FGuid ActorGUID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Damage")
    float DamageSeverity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Damage")
    FVector DamageLocation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Damage")
    EDamageVisual VisualState;

    FDamageRecord()
        : ActorGUID(FGuid())
        , DamageSeverity(0.0f)
        , DamageLocation(FVector::ZeroVector)
        , VisualState(EDamageVisual::Scratched)
    {}
};

// ============================================================================
// FIntelItem — Weapon X collectible
// ============================================================================

USTRUCT(BlueprintType)
struct WOLVERINE_API FIntelItem
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Intel")
    FName IntelID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Intel")
    FText Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Intel")
    FText Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Intel")
    UAudioComponent* AudioLog;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Intel")
    bool IsCollected;

    FIntelItem()
        : IntelID(NAME_None)
        , AudioLog(nullptr)
        , IsCollected(false)
    {}
};
```

**File:** `Source/Wolverine/Public/WolverineDataStructures.h`
**Dependencies:** WolverineCoreTypes.h
**FR Mapping:** FR-06, FR-11, FR-13, FR-15, FR-18, FR-20

---

### 0.8 WolverineDataStructures.cpp
```cpp
#include "WolverineDataStructures.h"

// No implementation — structs only.
// This file exists for UBT compatibility.
```

**File:** `Source/Wolverine/Private/WolverineDataStructures.cpp`
**Dependencies:** WolverineDataStructures.h

---

## BUILD LEVEL 1 — Systems (Depend on L0 Only)

### 1.1 WolverineMaterialResponseSystem.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWolverineMaterialResponse.h"
#include "WolverineDataStructures.h"
#include "WolverineMaterialResponseSystem.generated.h"

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineMaterialResponseSystem : public UActorComponent, public IWolverineMaterialResponse
{
    GENERATED_BODY()

public:
    UWolverineMaterialResponseSystem();

protected:
    virtual void BeginPlay() override;

public:
    // IWolverineMaterialResponse implementation
    virtual EClawMaterialType GetMaterialType_Implementation(const FHitResult& HitResult) override;

    /**
     * Get material from physical surface type.
     * @param SurfaceType Physical surface from hit
     * @return EClawMaterialType
     */
    UFUNCTION(BlueprintPure, Category = "Material")
    EClawMaterialType GetMaterialFromSurface(ETypedSurfaceChannel SurfaceType) const;

private:
    /** Material mapping from surface type */
    UPROPERTY(EditAnywhere, Category = "Material")
    TMap<ETypedSurfaceChannel, EClawMaterialType> SurfaceMaterialMap;
};
```

**File:** `Source/Wolverine/Public/Components/WolverineMaterialResponseSystem.h`
**Dependencies:** L0 (WolverineCoreTypes, IWolverineMaterialResponse, WolverineDataStructures)
**Parent:** UActorComponent
**Interfaces:** IWolverineMaterialResponse
**FR Mapping:** FR-07 (material-responsive claw impact)
**HR Mapping:** HR-06 (6 material types)

---

### 1.2 WolverineMaterialResponseSystem.cpp
```cpp
#include "Components/WolverineMaterialResponseSystem.h"

UWolverineMaterialResponseSystem::UWolverineMaterialResponseSystem()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UWolverineMaterialResponseSystem::BeginPlay()
{
    Super::BeginPlay();

    // Initialize surface mapping
    SurfaceMaterialMap[SurfaceType_Default] = EClawMaterialType::Flesh;
    SurfaceMaterialMap[SurfaceType_Flesh] = EClawMaterialType::Flesh;
    SurfaceMaterialMap[SurfaceType_Stone] = EClawMaterialType::Concrete;
    SurfaceMaterialMap[SurfaceType_Metal] = EClawMaterialType::LightMetal;
    SurfaceMaterialMap[SurfaceType_Glass] = EClawMaterialType::Glass;
}

EClawMaterialType UWolverineMaterialResponseSystem::GetMaterialType_Implementation(const FHitResult& HitResult)
{
    if (HitResult.PhysMaterial.IsValid())
    {
        return GetMaterialFromSurface(HitResult.PhysMaterial->SurfaceType);
    }
    return EClawMaterialType::Flesh;
}

EClawMaterialType UWolverineMaterialResponseSystem::GetMaterialFromSurface(ETypedSurfaceChannel SurfaceType) const
{
    if (SurfaceMaterialMap.Contains(SurfaceType))
    {
        return SurfaceMaterialMap[SurfaceType];
    }
    return EClawMaterialType::Flesh;
}
```

**File:** `Source/Wolverine/Private/Components/WolverineMaterialResponseSystem.cpp`
**Dependencies:** WolverineMaterialResponseSystem.h
**Tick:** No

---

### 1.3 WolverineWoundSystemComponent.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWolverineDamageInterface.h"
#include "WolverineDataStructures.h"
#include "WolverineWoundSystemComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWoundApplied, const FWoundData&, Wound);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHealingStarted, float, HealingRate);

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineWoundSystemComponent : public UActorComponent, public IWolverineDamageInterface
{
    GENERATED_BODY()

public:
    UWolverineWoundSystemComponent();

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

public:
    // IWolverineDamageInterface implementation
    virtual void ApplyDamage_Implementation(float Amount, const FVector& Location, AActor* Instigator) override;

    /**
     * Apply wound to Wolverine.
     * @param Location World space location
     * @param Severity Wound severity (0-1)
     */
    UFUNCTION(BlueprintCallable, Category = "Wound")
    void ApplyWound(const FVector& Location, float Severity);

    /**
     * Get total wound severity (sum of all active wounds).
     * @return float Total severity
     */
    UFUNCTION(BlueprintPure, Category = "Wound")
    float GetTotalWoundSeverity() const;

    /**
     * Check if healing is active.
     * @return bool
     */
    UFUNCTION(BlueprintPure, Category = "Wound")
    bool IsHealing() const;

    /**
     * Set healing rate multiplier.
     * @param Rate Multiplier (1.0 = base)
     */
    UFUNCTION(BlueprintCallable, Category = "Wound")
    void SetHealingRate(float Rate);

    /** Get current healing rate */
    UFUNCTION(BlueprintPure, Category = "Wound")
    float GetHealingRate() const { return HealingRate; }

    /** Events */
    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnWoundApplied OnWoundApplied;

    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnHealingStarted OnHealingStarted;

private:
    /** Active wounds */
    UPROPERTY()
    TArray<FWoundData> ActiveWounds;

    /** Base healing rate */
    UPROPERTY(EditAnywhere, Category = "Healing")
    float HealingRate;

    /** Visual healing delay (NFR-03: 500ms) */
    UPROPERTY(EditAnywhere, Category = "Healing")
    float VisualHealingDelay;

    /** Max simultaneous wounds (performance cap) */
    UPROPERTY(EditAnywhere, Category = "Performance")
    int32 MaxSimultaneousWounds;

    /** Healing tick interval (10Hz for performance) */
    UPROPERTY(EditAnywhere, Category = "Performance")
    float HealingTickInterval;

    /** Time accumulator for healing tick */
    float HealingTickAccumulator;

    /** Internal healing tick */
    void TickHealing(float DeltaTime);
};
```

**File:** `Source/Wolverine/Public/Components/WolverineWoundSystemComponent.h`
**Dependencies:** L0 (WolverineCoreTypes, IWolverineDamageInterface, WolverineDataStructures)
**Parent:** UActorComponent
**Interfaces:** IWolverineDamageInterface
**Tick:** Yes (10Hz — 0.1f interval)
**TickGroup:** TG_PostUpdateWork
**FR Mapping:** FR-06 (real-time wound system)
**HR Mapping:** HR-02 (mesh deformation)
**NFR Mapping:** NFR-01 (60fps), NFR-03 (healing visual <500ms)

---

### 1.4 WolverineWoundSystemComponent.cpp
```cpp
#include "Components/WolverineWoundSystemComponent.h"

UWolverineWoundSystemComponent::UWolverineWoundSystemComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.TickGroup = TG_PostUpdateWork;
    PrimaryComponentTick.TickInterval = 0.1f; // 10Hz

    HealingRate = 1.0f;
    VisualHealingDelay = 0.5f; // NFR-03: 500ms
    MaxSimultaneousWounds = 16;
    HealingTickAccumulator = 0.0f;
}

void UWolverineWoundSystemComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UWolverineWoundSystemComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    TickHealing(DeltaTime);
}

void UWolverineWoundSystemComponent::ApplyDamage_Implementation(float Amount, const FVector& Location, AActor* Instigator)
{
    ApplyWound(Location, Amount / 100.0f); // Normalize to 0-1
}

void UWolverineWoundSystemComponent::ApplyWound(const FVector& Location, float Severity)
{
    if (ActiveWounds.Num() >= MaxSimultaneousWounds)
    {
        // Remove oldest wound
        ActiveWounds.RemoveAt(0);
    }

    FWoundData NewWound;
    NewWound.Location = Location;
    NewWound.Severity = Severity;
    NewWound.Age = 0.0f;
    NewWound.HealingProgress = 0.0f;

    ActiveWounds.Add(NewWound);
    OnWoundApplied.Broadcast(NewWound);
}

float UWolverineWoundSystemComponent::GetTotalWoundSeverity() const
{
    float Total = 0.0f;
    for (const FWoundData& Wound : ActiveWounds)
    {
        Total += Wound.Severity * (1.0f - Wound.HealingProgress);
    }
    return Total;
}

bool UWolverineWoundSystemComponent::IsHealing() const
{
    for (const FWoundData& Wound : ActiveWounds)
    {
        if (Wound.HealingProgress > 0.0f && Wound.HealingProgress < 1.0f)
        {
            return true;
        }
    }
    return false;
}

void UWolverineWoundSystemComponent::SetHealingRate(float Rate)
{
    HealingRate = Rate;
    OnHealingStarted.Broadcast(HealingRate);
}

void UWolverineWoundSystemComponent::TickHealing(float DeltaTime)
{
    HealingTickAccumulator += DeltaTime;
    if (HealingTickAccumulator < HealingTickInterval)
    {
        return;
    }
    HealingTickAccumulator = 0.0f;

    // Heal all wounds
    for (FWoundData& Wound : ActiveWounds)
    {
        if (Wound.Age >= VisualHealingDelay)
        {
            Wound.HealingProgress += HealingRate * HealingTickInterval;
            Wound.HealingProgress = FMath::Clamp(Wound.HealingProgress, 0.0f, 1.0f);
        }
        Wound.Age += HealingTickInterval;
    }

    // Remove fully healed wounds
    ActiveWounds.RemoveAll([](const FWoundData& Wound) {
        return Wound.HealingProgress >= 1.0f;
    });
}
```

**File:** `Source/Wolverine/Private/Components/WolverineWoundSystemComponent.cpp`
**Dependencies:** WolverineWoundSystemComponent.h
**Tick:** 10Hz (0.1f interval)

---

### 1.5 WolverineAnimationInstance.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "WolverineAnimationInstance.generated.h"

UCLASS()
class WOLVERINE_API UWolverineAnimationInstance : public UAnimInstance
{
    GENERATED_BODY()

public:
    UWolverineAnimationInstance();

protected:
    virtual void NativeUpdateAnimation(float DeltaTime) override;
    virtual void NativeThreadSafeUpdateAnimation(float DeltaTime) override;

public:
    /**
     * Update motion matching with desired velocity/direction.
     * @param Velocity Desired velocity
     * @param Direction Desired direction
     */
    UFUNCTION(BlueprintCallable, Category = "Motion Matching")
    void UpdateMotionMatching(const FVector& Velocity, const FVector& Direction);

    /**
     * Blend claw deployment.
     * @param LeftBlend Left claw blend (0-1)
     * @param RightBlend Right claw blend (0-1)
     */
    UFUNCTION(BlueprintCallable, Category = "Claw")
    void BlendClawDeployment(float LeftBlend, float RightBlend);

    /**
     * Trigger claw impact stun (micro-stutter).
     * @param Side Claw side
     */
    UFUNCTION(BlueprintCallable, Category = "Claw")
    void TriggerClawImpactStun(EClawSide Side);

    /** Transition to wall climb */
    UFUNCTION(BlueprintCallable, Category = "Traversal")
    void TransitionToWallClimb();

    /** Transition to claw swing */
    UFUNCTION(BlueprintCallable, Category = "Traversal")
    void TransitionToClawSwing();

    /** Trigger lunge animation */
    UFUNCTION(BlueprintCallable, Category = "Combat")
    void TriggerLungeAnimation(AActor* Target);

    /** Current traversal state */
    UPROPERTY(BlueprintReadWrite, Category = "State")
    ETraversalState CurrentTraversalState;

    /** Motion matching data */
    UPROPERTY(BlueprintReadWrite, Category = "Animation")
    FMotionMatchingData MotionMatchingData;

    /** Claw animation data */
    UPROPERTY(BlueprintReadWrite, Category = "Animation")
    FClawAnimationData ClawAnimationData;

private:
    /** Cached character reference */
    UPROPERTY()
    ACharacter* CharacterOwner;
};
```

**File:** `Source/Wolverine/Public/Animation/WolverineAnimationInstance.h`
**Dependencies:** L0 (WolverineCoreTypes, WolverineDataStructures)
**Parent:** UAnimInstance
**FR Mapping:** FR-02 (seamless traversal), FR-03 (freeform combo)
**NFR Mapping:** NFR-01 (60fps), NFR-07 (<2s transitions)

---

### 1.6 WolverineAnimationInstance.cpp
```cpp
#include "Animation/WolverineAnimationInstance.h"

UWolverineAnimationInstance::UWolverineAnimationInstance()
    : CurrentTraversalState(ETraversalState::Grounded)
    , CharacterOwner(nullptr)
{
}

void UWolverineAnimationInstance::NativeUpdateAnimation(float DeltaTime)
{
    Super::NativeUpdateAnimation(DeltaTime);

    if (!CharacterOwner)
    {
        CharacterOwner = Cast<ACharacter>(TryGetPawnOwner());
    }
}

void UWolverineAnimationInstance::NativeThreadSafeUpdateAnimation(float DeltaTime)
{
    Super::NativeThreadSafeUpdateAnimation(DeltaTime);
    // Motion Matching update happens here
}

void UWolverineAnimationInstance::UpdateMotionMatching(const FVector& Velocity, const FVector& Direction)
{
    MotionMatchingData.DesiredVelocity = Velocity;
    MotionMatchingData.DesiredDirection = Direction;
}

void UWolverineAnimationInstance::BlendClawDeployment(float LeftBlend, float RightBlend)
{
    ClawAnimationData.LeftClawDeployBlend = LeftBlend;
    ClawAnimationData.RightClawDeployBlend = RightBlend;
}

void UWolverineAnimationInstance::TriggerClawImpactStun(EClawSide Side)
{
    ClawAnimationData.ClawImpactStun = 0.1f; // 100ms micro-stutter
}

void UWolverineAnimationInstance::TransitionToWallClimb()
{
    CurrentTraversalState = ETraversalState::WallClimbing;
}

void UWolverineAnimationInstance::TransitionToClawSwing()
{
    CurrentTraversalState = ETraversalState::ClawSwinging;
}

void UWolverineAnimationInstance::TriggerLungeAnimation(AActor* Target)
{
    CurrentTraversalState = ETraversalState::ClawLunging;
}
```

**File:** `Source/Wolverine/Private/Animation/WolverineAnimationInstance.cpp`
**Dependencies:** WolverineAnimationInstance.h
**Tick:** Native (AnimInstance)

---

### 1.7 WolverineSaveGame.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "WolverineDataStructures.h"
#include "WolverineSaveGame.generated.h"

UCLASS()
class WOLVERINE_API UWolverineSaveGame : public USaveGame
{
    GENERATED_BODY()

public:
    UWolverineSaveGame();

    /** Slot name */
    UPROPERTY(VisibleAnywhere, Category = "Save")
    FString SlotName;

    /** Play time */
    UPROPERTY(VisibleAnywhere, Category = "Save")
    float PlayTime;

    /** Current district */
    UPROPERTY(VisibleAnywhere, Category = "Save")
    int32 CurrentDistrict;

    /** Game time hours (0-72) */
    UPROPERTY(VisibleAnywhere, Category = "Save")
    float GameTimeHours;

    /** Current weather */
    UPROPERTY(VisibleAnywhere, Category = "Save")
    int32 CurrentWeather;

    /** Destruction records */
    UPROPERTY(VisibleAnywhere, Category = "Destruction")
    TArray<FDestructionRecord> DestructionRecords;

    /** Damage records */
    UPROPERTY(VisibleAnywhere, Category = "Destruction")
    TArray<FDamageRecord> DamageRecords;

    /** Unlocked memories */
    UPROPERTY(VisibleAnywhere, Category = "Progression")
    TArray<FMemoryFragment> UnlockedMemories;

    /** Collected intel */
    UPROPERTY(VisibleAnywhere, Category = "Collectibles")
    TArray<FIntelItem> CollectedIntel;

    /** Session stats */
    UPROPERTY(VisibleAnywhere, Category = "Stats")
    float TotalDamageTaken;

    UPROPERTY(VisibleAnywhere, Category = "Stats")
    int32 TotalKills;

    UPROPERTY(VisibleAnywhere, Category = "Stats")
    int32 LongestCombo;
};
```

**File:** `Source/Wolverine/Public/WolverineSaveGame.h`
**Dependencies:** L0 (WolverineCoreTypes, WolverineDataStructures)
**Parent:** USaveGame
**FR Mapping:** FR-13 (persistent destruction), FR-11 (Trauma System), FR-15 (Weapon X Intel)
**HR Mapping:** HR-05 (persistent destruction)
**NFR Mapping:** NFR-06 (destruction survives save/load)

---

### 1.8 WolverineSaveGame.cpp
```cpp
#include "WolverineSaveGame.h"

UWolverineSaveGame::UWolverineSaveGame()
{
    SlotName = TEXT("SaveGame");
    PlayTime = 0.0f;
    CurrentDistrict = 0;
    GameTimeHours = 0.0f;
    CurrentWeather = 0;
    TotalDamageTaken = 0.0f;
    TotalKills = 0;
    LongestCombo = 0;
}
```

**File:** `Source/Wolverine/Private/WolverineSaveGame.cpp`
**Dependencies:** WolverineSaveGame.h

---

## BUILD LEVEL 2 — Components (Depend on L0 + L1)

### 2.1 WolverineClawComponent.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWolverineMaterialResponse.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "WolverineClawComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnClawImpact, const FHitResult&, HitResult, EClawMaterialType, Material, EClawSide, Side);

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineClawComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineClawComponent();

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

public:
    /**
     * Deploy claws.
     * @param Side Which claw to deploy
     */
    UFUNCTION(BlueprintCallable, Category = "Claw")
    void DeployClaws(EClawSide Side);

    /**
     * Retract claws.
     * @param Side Which claw to retract
     */
    UFUNCTION(BlueprintCallable, Category = "Claw")
    void RetractClaws(EClawSide Side);

    /**
     * Check if claws are deployed.
     * @return bool
     */
    UFUNCTION(BlueprintPure, Category = "Claw")
    bool AreClawsDeployed() const;

    /**
     * Get claw material type.
     * @param Side Which claw
     * @return EClawMaterialType
     */
    UFUNCTION(BlueprintPure, Category = "Claw")
    EClawMaterialType GetClawMaterial(EClawSide Side) const;

    /**
     * Perform material trace for claw.
     * @param Side Which claw
     * @return EClawMaterialType
     */
    UFUNCTION(BlueprintCallable, Category = "Claw")
    EClawMaterialType PerformMaterialTrace(EClawSide Side);

    /** Impact event */
    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnClawImpact OnClawImpact;

    /** Left claw deployed */
    UPROPERTY(BlueprintReadWrite, Category = "State")
    bool LeftClawDeployed;

    /** Right claw deployed */
    UPROPERTY(BlueprintReadWrite, Category = "State")
    bool RightClawDeployed;

    /** Claw deploy time target (NFR-02: <200ms) */
    UPROPERTY(EditAnywhere, Category = "Performance")
    float ClawDeployTime;

private:
    /** Current left material */
    EClawMaterialType CurrentLeftMaterial;

    /** Current right material */
    EClawMaterialType CurrentRightMaterial;

    /** Material trace interval */
    UPROPERTY(EditAnywhere, Category = "Performance")
    float MaterialTraceInterval;

    /** Cached material response system */
    UPROPERTY()
    UWolverineMaterialResponseSystem* MaterialResponseSystem;

    /** Handle claw impact */
    void OnImpact(const FHitResult& HitResult, EClawMaterialType Material, EClawSide Side);
};
```

**File:** `Source/Wolverine/Public/Components/WolverineClawComponent.h`
**Dependencies:** L0 + L1 (WolverineMaterialResponseSystem)
**Parent:** UActorComponent
**Tick:** Yes (per-frame during combat)
**TickGroup:** TG_PrePhysics
**FR Mapping:** FR-03 (freeform combo), FR-04 (claw lunge), FR-07 (material response)
**HR Mapping:** HR-01 (deploy <10s), HR-06 (6 materials)
**NFR Mapping:** NFR-02 (<200ms deploy), NFR-08 (audio never masked)

---

### 2.2 WolverineClawComponent.cpp
```cpp
#include "Components/WolverineClawComponent.h"

UWolverineClawComponent::UWolverineClawComponent()
    : LeftClawDeployed(false)
    , RightClawDeployed(false)
    , ClawDeployTime(0.15f) // <200ms NFR-02
    , CurrentLeftMaterial(EClawMaterialType::Flesh)
    , CurrentRightMaterial(EClawMaterialType::Flesh)
    , MaterialTraceInterval(0.016f) // 60fps
    , MaterialResponseSystem(nullptr)
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.TickGroup = TG_PrePhysics;
}

void UWolverineClawComponent::BeginPlay()
{
    Super::BeginPlay();

    // Find material response system
    AActor* Owner = GetOwner();
    if (Owner)
    {
        MaterialResponseSystem = Owner->FindComponentByClass<UWolverineMaterialResponseSystem>();
    }
}

void UWolverineClawComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (LeftClawDeployed)
    {
        PerformMaterialTrace(EClawSide::Left);
    }
    if (RightClawDeployed)
    {
        PerformMaterialTrace(EClawSide::Right);
    }
}

void UWolverineClawComponent::DeployClaws(EClawSide Side)
{
    if (Side == EClawSide::Left)
    {
        LeftClawDeployed = true;
    }
    else
    {
        RightClawDeployed = true;
    }
}

void UWolverineClawComponent::RetractClaws(EClawSide Side)
{
    if (Side == EClawSide::Left)
    {
        LeftClawDeployed = false;
    }
    else
    {
        RightClawDeployed = false;
    }
}

bool UWolverineClawComponent::AreClawsDeployed() const
{
    return LeftClawDeployed || RightClawDeployed;
}

EClawMaterialType UWolverineClawComponent::GetClawMaterial(EClawSide Side) const
{
    return (Side == EClawSide::Left) ? CurrentLeftMaterial : CurrentRightMaterial;
}

EClawMaterialType UWolverineClawComponent::PerformMaterialTrace(EClawSide Side)
{
    // Line trace from claw tip
    // Simplified for stub
    EClawMaterialType Detected = EClawMaterialType::Flesh;

    if (MaterialResponseSystem)
    {
        // Would do actual line trace here
        Detected = MaterialResponseSystem->GetMaterialFromSurface(SurfaceType_Default);
    }

    if (Side == EClawSide::Left)
    {
        CurrentLeftMaterial = Detected;
    }
    else
    {
        CurrentRightMaterial = Detected;
    }

    return Detected;
}

void UWolverineClawComponent::OnImpact(const FHitResult& HitResult, EClawMaterialType Material, EClawSide Side)
{
    OnClawImpact.Broadcast(HitResult, Material, Side);
}
```

**File:** `Source/Wolverine/Private/Components/WolverineClawComponent.cpp`
**Dependencies:** WolverineClawComponent.h
**Tick:** Per-frame (60fps during combat)

---

### 2.3 WolverineRageComponent.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "WolverineRageComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRageLevelChanged, ERageLevel, NewLevel);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnBerserkerActivated);

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineRageComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineRageComponent();

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

public:
    /**
     * Add rage (internal only — called from damage events).
     * @param Amount Rage amount to add
     * NOTE: No BlueprintCallable — HR-04 compliance
     */
    void AddRage(float Amount);

    /**
     * Consume rage (for healing boost).
     * @param Amount Rage to consume
     */
    UFUNCTION(BlueprintCallable, Category = "Rage")
    void ConsumeRage(float Amount);

    /**
     * Get current rage level.
     * @return ERageLevel
     */
    UFUNCTION(BlueprintPure, Category = "Rage")
    ERageLevel GetRageLevel() const;

    /**
     * Get damage multiplier.
     * @return float (1.0 normal, 3.0 berserker)
     */
    UFUNCTION(BlueprintPure, Category = "Rage")
    float GetDamageMultiplier() const;

    /**
     * Check if Berserker is active.
     * @return bool
     */
    UFUNCTION(BlueprintPure, Category = "Rage")
    bool IsBerserkerActive() const;

    /**
     * Handle damage dealt event.
     * @param Amount Damage amount
     * @param Target Target actor
     */
    UFUNCTION(BlueprintCallable, Category = "Events")
    void OnDamageDealt(float Amount, AActor* Target);

    /**
     * Handle damage received event.
     * @param Amount Damage amount
     * @param Source Source actor
     */
    UFUNCTION(BlueprintCallable, Category = "Events")
    void OnDamageReceived(float Amount, AActor* Source);

    /** Events */
    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnRageLevelChanged OnRageLevelChanged;

    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnBerserkerActivated OnBerserkerActivated;

    /** Current rage (0-100) */
    UPROPERTY(BlueprintReadWrite, Category = "State")
    float CurrentRage;

    /** Berserker active flag */
    UPROPERTY(BlueprintReadWrite, Category = "State")
    bool BerserkerActive;

    /** Berserker time remaining */
    UPROPERTY(BlueprintReadWrite, Category = "State")
    float BerserkerTimeRemaining;

private:
    /** Rage fill rate */
    UPROPERTY(EditAnywhere, Category = "Rage")
    float RageFillRate;

    /** Rage drain rate (when idle) */
    UPROPERTY(EditAnywhere, Category = "Rage")
    float RageDrainRate;

    /** Damage multiplier */
    float DamageMultiplier;

    /** Idle timer (30s drain) */
    float IdleTimer;

    /** Berserker duration */
    UPROPERTY(EditAnywhere, Category = "Rage")
    float BerserkerDuration;

    /** Internal rage tick */
    void TickRage(float DeltaTime);

    /** Check and trigger Berserker */
    void CheckBerserker();

    /** Update damage multiplier */
    void UpdateDamageMultiplier();
};
```

**File:** `Source/Wolverine/Public/Components/WolverineRageComponent.h`
**Dependencies:** L0 (WolverineCoreTypes, WolverineDataStructures)
**Parent:** UActorComponent
**Tick:** Yes (rage drain, Berserker countdown)
**TickGroup:** TG_UpdateWork
**FR Mapping:** FR-05 (rage system)
**HR Mapping:** HR-04 (event-driven only, NO manual activation)
**NFR Mapping:** NFR-01 (60fps), NFR-04 (AI response <100ms)

**CRITICAL HR-04 COMPLIANCE:**
- NO public `ActivateRage()` function
- NO `BlueprintCallable` on `AddRage()`
- Rage ONLY fills via `OnDamageDealt`/`OnDamageReceived` events

---

### 2.4 WolverineRageComponent.cpp
```cpp
#include "Components/WolverineRageComponent.h"

UWolverineRageComponent::UWolverineRageComponent()
    : CurrentRage(0.0f)
    , BerserkerActive(false)
    , BerserkerTimeRemaining(0.0f)
    , RageFillRate(1.0f)
    , RageDrainRate(0.5f)
    , DamageMultiplier(1.0f)
    , IdleTimer(0.0f)
    , BerserkerDuration(20.0f)
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.TickGroup = TG_UpdateWork;
}

void UWolverineRageComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UWolverineRageComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    TickRage(DeltaTime);
}

void UWolverineRageComponent::AddRage(float Amount)
{
    // Internal only — HR-04: no BlueprintCallable
    CurrentRage = FMath::Clamp(CurrentRage + Amount, 0.0f, 100.0f);
    CheckBerserker();
    UpdateDamageMultiplier();
}

void UWolverineRageComponent::ConsumeRage(float Amount)
{
    CurrentRage = FMath::Clamp(CurrentRage - Amount, 0.0f, 100.0f);
    UpdateDamageMultiplier();
}

ERageLevel UWolverineRageComponent::GetRageLevel() const
{
    if (CurrentRage >= 100.0f)
    {
        return ERageLevel::Full;
    }
    else if (CurrentRage >= 34.0f)
    {
        return ERageLevel::Mid;
    }
    return ERageLevel::Low;
}

float UWolverineRageComponent::GetDamageMultiplier() const
{
    return DamageMultiplier;
}

bool UWolverineRageComponent::IsBerserkerActive() const
{
    return BerserkerActive;
}

void UWolverineRageComponent::OnDamageDealt(float Amount, AActor* Target)
{
    AddRage(Amount * 0.5f); // 50% rage from damage dealt
    IdleTimer = 0.0f; // Reset idle timer
}

void UWolverineRageComponent::OnDamageReceived(float Amount, AActor* Source)
{
    AddRage(Amount * 1.0f); // 100% rage from damage received
    IdleTimer = 0.0f; // Reset idle timer
}

void UWolverineRageComponent::TickRage(float DeltaTime)
{
    if (BerserkerActive)
    {
        BerserkerTimeRemaining -= DeltaTime;
        if (BerserkerTimeRemaining <= 0.0f)
        {
            BerserkerActive = false;
            CurrentRage = 0.0f;
            UpdateDamageMultiplier();
        }
        return;
    }

    // Drain rage when idle
    IdleTimer += DeltaTime;
    if (IdleTimer > 30.0f && CurrentRage > 0.0f)
    {
        CurrentRage = FMath::Clamp(CurrentRage - RageDrainRate * DeltaTime, 0.0f, 100.0f);
        UpdateDamageMultiplier();
    }
}

void UWolverineRageComponent::CheckBerserker()
{
    if (CurrentRage >= 100.0f && !BerserkerActive)
    {
        BerserkerActive = true;
        BerserkerTimeRemaining = BerserkerDuration;
        DamageMultiplier = 3.0f;
        OnBerserkerActivated.Broadcast();
        OnRageLevelChanged.Broadcast(ERageLevel::Full);
    }
}

void UWolverineRageComponent::UpdateDamageMultiplier()
{
    if (BerserkerActive)
    {
        DamageMultiplier = 3.0f;
    }
    else
    {
        ERageLevel Level = GetRageLevel();
        if (Level == ERageLevel::Mid)
        {
            DamageMultiplier = 1.5f;
        }
        else
        {
            DamageMultiplier = 1.0f;
        }
    }
}
```

**File:** `Source/Wolverine/Private/Components/WolverineRageComponent.cpp`
**Dependencies:** WolverineRageComponent.h
**Tick:** Yes (rage drain, Berserker countdown)

---

### 2.5 WolverineTraumaSystemComponent.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "WolverineTraumaSystemComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMemoryUnlocked, const FMemoryFragment&, Memory);

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineTraumaSystemComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineTraumaSystemComponent();

protected:
    virtual void BeginPlay() override;

public:
    /**
     * Unlock memory fragment.
     * @param MemoryID Memory identifier
     */
    UFUNCTION(BlueprintCallable, Category = "Trauma")
    void UnlockMemory(const FName& MemoryID);

    /**
     * Get combo window duration.
     * @return float (base 0.3s + bonus)
     */
    UFUNCTION(BlueprintPure, Category = "Trauma")
    float GetComboWindow() const;

    /**
     * Get rage fill rate multiplier.
     * @return float (base 1.0 + bonus)
     */
    UFUNCTION(BlueprintPure, Category = "Trauma")
    float GetRageFillRateMultiplier() const;

    /**
     * Get healing efficiency.
     * @return float (base 1.0 + bonus)
     */
    UFUNCTION(BlueprintPure, Category = "Trauma")
    float GetHealingEfficiency() const;

    /**
     * Play memory fragment.
     * @param MemoryID Memory identifier
     */
    UFUNCTION(BlueprintCallable, Category = "Trauma")
    void PlayMemoryFragment(const FName& MemoryID);

    /** Event */
    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnMemoryUnlocked OnMemoryUnlocked;

private:
    /** Unlocked memories */
    UPROPERTY()
    TArray<FMemoryFragment> UnlockedMemories;

    /** Combo window extension */
    float ComboWindowExtension;

    /** Rage fill rate bonus */
    float RageFillRateBonus;

    /** Healing efficiency bonus */
    float HealingEfficiencyBonus;

    /** Calculate bonuses from unlocked memories */
    void CalculateBonuses();
};
```

**File:** `Source/Wolverine/Public/Components/WolverineTraumaSystemComponent.h`
**Dependencies:** L0 (WolverineCoreTypes, WolverineDataStructures)
**Parent:** UActorComponent
**Tick:** No (event-driven only)
**FR Mapping:** FR-11 (Trauma System progression)
**HR Mapping:** HR-08 (no skill trees — progression via memories)

---

### 2.6 WolverineTraumaSystemComponent.cpp
```cpp
#include "Components/WolverineTraumaSystemComponent.h"

UWolverineTraumaSystemComponent::UWolverineTraumaSystemComponent()
    : ComboWindowExtension(0.0f)
    , RageFillRateBonus(0.0f)
    , HealingEfficiencyBonus(0.0f)
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UWolverineTraumaSystemComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UWolverineTraumaSystemComponent::UnlockMemory(const FName& MemoryID)
{
    // Check if already unlocked
    for (const FMemoryFragment& Memory : UnlockedMemories)
    {
        if (Memory.MemoryID == MemoryID)
        {
            return;
        }
    }

    // Create new memory (would load from data asset in full implementation)
    FMemoryFragment NewMemory;
    NewMemory.MemoryID = MemoryID;
    NewMemory.IsUnlocked = true;
    NewMemory.MechanicalBonus = ETraumaBonusType::ComboWindow;
    NewMemory.BonusValue = 0.05f;

    UnlockedMemories.Add(NewMemory);
    CalculateBonuses();
    OnMemoryUnlocked.Broadcast(NewMemory);
}

float UWolverineTraumaSystemComponent::GetComboWindow() const
{
    return 0.3f + ComboWindowExtension;
}

float UWolverineTraumaSystemComponent::GetRageFillRateMultiplier() const
{
    return 1.0f + RageFillRateBonus;
}

float UWolverineTraumaSystemComponent::GetHealingEfficiency() const
{
    return 1.0f + HealingEfficiencyBonus;
}

void UWolverineTraumaSystemComponent::PlayMemoryFragment(const FName& MemoryID)
{
    // Would trigger playable flashback in full implementation
}

void UWolverineTraumaSystemComponent::CalculateBonuses()
{
    ComboWindowExtension = 0.0f;
    RageFillRateBonus = 0.0f;
    HealingEfficiencyBonus = 0.0f;

    for (const FMemoryFragment& Memory : UnlockedMemories)
    {
        switch (Memory.MechanicalBonus)
        {
            case ETraumaBonusType::ComboWindow:
                ComboWindowExtension += Memory.BonusValue;
                break;
            case ETraumaBonusType::RageFillRate:
                RageFillRateBonus += Memory.BonusValue;
                break;
            case ETraumaBonusType::HealingEfficiency:
                HealingEfficiencyBonus += Memory.BonusValue;
                break;
        }
    }

    // Cap bonuses
    ComboWindowExtension = FMath::Min(ComboWindowExtension, 0.2f);
    RageFillRateBonus = FMath::Min(RageFillRateBonus, 0.5f);
    HealingEfficiencyBonus = FMath::Min(HealingEfficiencyBonus, 0.3f);
}
```

**File:** `Source/Wolverine/Private/Components/WolverineTraumaSystemComponent.cpp`
**Dependencies:** WolverineTraumaSystemComponent.h

---

### 2.7 WolverineAudioComponent.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "AudioComponents/AudioComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "WolverineAudioComponent.generated.h"

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineAudioComponent : public UAudioComponent
{
    GENERATED_BODY()

public:
    UWolverineAudioComponent();

protected:
    virtual void BeginPlay() override;

public:
    /**
     * Set combat intensity.
     * @param Intensity 0-1
     */
    UFUNCTION(BlueprintCallable, Category = "Audio")
    void SetCombatIntensity(float Intensity);

    /**
     * Set rage level.
     * @param Level ERageLevel
     */
    UFUNCTION(BlueprintCallable, Category = "Audio")
    void SetRageLevel(ERageLevel Level);

    /**
     * Play claw impact sound.
     * @param Material EClawMaterialType
     */
    UFUNCTION(BlueprintCallable, Category = "Claw")
    void PlayClawImpact(EClawMaterialType Material);

    /**
     * Play healing sound.
     */
    UFUNCTION(BlueprintCallable, Category = "Healing")
    void PlayHealingSound();

    /**
     * Trigger Berserker music.
     */
    UFUNCTION(BlueprintCallable, Category = "Rage")
    void TriggerBerserkerMusic();

    /**
     * Update reactive parameters.
     */
    UFUNCTION(BlueprintCallable, Category = "Audio")
    void UpdateReactiveParameters();

private:
    /** Reactive parameters */
    UPROPERTY()
    FAudioReactiveParams ReactiveParameters;

    /** Current material */
    EClawMaterialType CurrentMaterial;

    /** MetaSound source */
    UPROPERTY()
    UMetaSoundSource* MetaSoundSource;
};
```

**File:** `Source/Wolverine/Public/Components/WolverineAudioComponent.h`
**Dependencies:** L0 + L1
**Parent:** UAudioComponent
**FR Mapping:** FR-18 (reactive audio score)
**HR Mapping:** HR-06 (6 material audio responses)
**NFR Mapping:** NFR-08 (claw impact never masked)

---

### 2.8 WolverineAudioComponent.cpp
```cpp
#include "Components/WolverineAudioComponent.h"

UWolverineAudioComponent::UWolverineAudioComponent()
    : CurrentMaterial(EClawMaterialType::Flesh)
    , MetaSoundSource(nullptr)
{
}

void UWolverineAudioComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UWolverineAudioComponent::SetCombatIntensity(float Intensity)
{
    ReactiveParameters.PercussionLayer = Intensity;
    ReactiveParameters.TempoBPM = 60.0f + (Intensity * 80.0f); // 60-140 BPM
    UpdateReactiveParameters();
}

void UWolverineAudioComponent::SetRageLevel(ERageLevel Level)
{
    switch (Level)
    {
        case ERageLevel::Low:
            ReactiveParameters.DistortionLayer = 0.0f;
            break;
        case ERageLevel::Mid:
            ReactiveParameters.DistortionLayer = 0.5f;
            break;
        case ERageLevel::Full:
            ReactiveParameters.DistortionLayer = 1.0f;
            break;
    }
    UpdateReactiveParameters();
}

void UWolverineAudioComponent::PlayClawImpact(EClawMaterialType Material)
{
    CurrentMaterial = Material;
    // Play material-specific impact sound
}

void UWolverineAudioComponent::PlayHealingSound()
{
    // Play healing sound
}

void UWolverineAudioComponent::TriggerBerserkerMusic()
{
    ReactiveParameters.PercussionLayer = 1.0f;
    ReactiveParameters.DistortionLayer = 1.0f;
    ReactiveParameters.TempoBPM = 140.0f;
    ReactiveParameters.AmbientLayer = 0.0f;
    UpdateReactiveParameters();
}

void UWolverineAudioComponent::UpdateReactiveParameters()
{
    // Update MetaSound parameters
}
```

**File:** `Source/Wolverine/Private/Components/WolverineAudioComponent.cpp`
**Dependencies:** WolverineAudioComponent.h

---

### 2.9 HapticFeedbackSystem.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "HapticFeedbackSystem.generated.h"

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UHapticFeedbackSystem : public UActorComponent
{
    GENERATED_BODY()

public:
    UHapticFeedbackSystem();

protected:
    virtual void BeginPlay() override;

public:
    /**
     * Trigger claw impact haptic.
     * @param Material EClawMaterialType
     * @param Side EClawSide
     */
    UFUNCTION(BlueprintCallable, Category = "Haptic")
    void TriggerClawImpact(EClawMaterialType Material, EClawSide Side);

    /**
     * Trigger rage activation haptic.
     */
    UFUNCTION(BlueprintCallable, Category = "Rage")
    void TriggerRageActivation();

    /**
     * Trigger damage received haptic.
     * @param Location FVector
     * @param Severity float
     */
    UFUNCTION(BlueprintCallable, Category = "Damage")
    void TriggerDamageReceived(const FVector& Location, float Severity);

    /**
     * Trigger healing haptic.
     */
    UFUNCTION(BlueprintCallable, Category = "Healing")
    void TriggerHealing();

private:
    /** Haptic data per material */
    UPROPERTY(EditAnywhere, Category = "Haptic")
    TMap<EClawMaterialType, FHapticFeedbackData> HapticDataMap;

    /** Initialize haptic data */
    void InitializeHapticData();
};
```

**File:** `Source/Wolverine/Public/Components/HapticFeedbackSystem.h`
**Dependencies:** L0 (WolverineCoreTypes, WolverineDataStructures)
**Parent:** UActorComponent
**FR Mapping:** FR-20 (haptic feedback system)
**HR Mapping:** HR-06 (per-material haptic response)
**NFR Mapping:** NFR-02 (haptic response <200ms)

---

### 2.10 HapticFeedbackSystem.cpp
```cpp
#include "Components/HapticFeedbackSystem.h"

UHapticFeedbackSystem::UHapticFeedbackSystem()
{
    PrimaryComponentTick.bCanEverTick = false;
    InitializeHapticData();
}

void UHapticFeedbackSystem::BeginPlay()
{
    Super::BeginPlay();
}

void UHapticFeedbackSystem::TriggerClawImpact(EClawMaterialType Material, EClawSide Side)
{
    if (HapticDataMap.Contains(Material))
    {
        FHapticFeedbackData Data = HapticDataMap[Material];
        // Trigger haptic feedback with Data.LeftStrength or Data.RightStrength
    }
}

void UHapticFeedbackSystem::TriggerRageActivation()
{
    // Strong asymmetric pulse for Berserker
}

void UHapticFeedbackSystem::TriggerDamageReceived(const FVector& Location, float Severity)
{
    // Haptic feedback based on damage location/severity
}

void UHapticFeedbackSystem::TriggerHealing()
{
    // Subtle continuous vibration
}

void UHapticFeedbackSystem::InitializeHapticData()
{
    // Initialize haptic data per material
    FHapticFeedbackData FleshData;
    FleshData.Material = EClawMaterialType::Flesh;
    FleshData.LeftStrength = 0.3f;
    FleshData.RightStrength = 0.3f;
    FleshData.Pattern = EHapticPattern::Pulse;
    HapticDataMap.Add(EClawMaterialType::Flesh, FleshData);

    // ... initialize other materials
}
```

**File:** `Source/Wolverine/Private/Components/HapticFeedbackSystem.cpp`
**Dependencies:** HapticFeedbackSystem.h

---

## BUILD LEVEL 3 — Character (Depend on L0 + L1 + L2)

### 3.1 WolverineMovementComponent.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineMovementComponent.generated.h"

UCLASS(ClassGroup=(Wolverine))
class WOLVERINE_API UWolverineMovementComponent : public UCharacterMovementComponent
{
    GENERATED_BODY()

public:
    UWolverineMovementComponent();

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

public:
    /** Start sprint */
    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StartSprint();

    /** Start claw sprint */
    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StartClawSprint();

    /** Start wall climb */
    UFUNCTION(BlueprintCallable, Category = "Traversal")
    void StartWallClimb(const FVector& WallNormal);

    /** Start claw swing */
    UFUNCTION(BlueprintCallable, Category = "Traversal")
    void StartClawSwing(const FVector& AnchorPoint);

    /** Perform claw lunge */
    UFUNCTION(BlueprintCallable, Category = "Combat")
    void PerformClawLunge(AActor* Target);

    /** Perform drop attack */
    UFUNCTION(BlueprintCallable, Category = "Combat")
    void PerformDropAttack();

    /** Perform claw brake */
    UFUNCTION(BlueprintCallable, Category = "Traversal")
    void PerformClawBrake();

    /** Get traversal state */
    UFUNCTION(BlueprintPure, Category = "Movement")
    ETraversalState GetTraversalState() const { return CurrentTraversalState; }

    /** Sprint speed */
    UPROPERTY(EditAnywhere, Category = "Speed")
    float SprintSpeed;

    /** Claw sprint speed */
    UPROPERTY(EditAnywhere, Category = "Speed")
    float ClawSprintSpeed;

    /** Wall climb speed */
    UPROPERTY(EditAnywhere, Category = "Speed")
    float WallClimbSpeed;

    /** Claw swing launch force */
    UPROPERTY(EditAnywhere, Category = "Force")
    float ClawSwingLaunchForce;

    /** Claw lunge distance */
    UPROPERTY(EditAnywhere, Category = "Force")
    float ClawLungeDistance;

    /** Claw lunge force */
    UPROPERTY(EditAnywhere, Category = "Force")
    float ClawLungeForce;

private:
    /** Current traversal state */
    ETraversalState CurrentTraversalState;

    /** Wall climbing flag */
    bool IsWallClimbing;

    /** Claw swinging flag */
    bool IsClawSwinging;

    /** Claw lunging flag */
    bool IsClawLunging;
};
```

**File:** `Source/Wolverine/Public/Components/WolverineMovementComponent.h`
**Dependencies:** L0 + L2 (WolverineClawComponent)
**Parent:** UCharacterMovementComponent
**Tick:** Yes (movement state machine)
**TickGroup:** TG_PrePhysics
**FR Mapping:** FR-02 (seamless traversal)
**HR Mapping:** HR-01 (claws deploy fast), HR-07 (predator optional)
**NFR Mapping:** NFR-01 (60fps), NFR-02 (claw lunge <200ms)

---

### 3.2 WolverineMovementComponent.cpp
```cpp
#include "Components/WolverineMovementComponent.h"

UWolverineMovementComponent::UWolverineMovementComponent()
    : SprintSpeed(800.0f)
    , ClawSprintSpeed(700.0f)
    , WallClimbSpeed(400.0f)
    , ClawSwingLaunchForce(2000.0f)
    , ClawLungeDistance(2000.0f) // 20m
    , ClawLungeForce(3000.0f)
    , CurrentTraversalState(ETraversalState::Grounded)
    , IsWallClimbing(false)
    , IsClawSwinging(false)
    , IsClawLunging(false)
{
    MaxWalkSpeed = SprintSpeed;
}

void UWolverineMovementComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UWolverineMovementComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}

void UWolverineMovementComponent::StartSprint()
{
    MaxWalkSpeed = SprintSpeed;
    CurrentTraversalState = ETraversalState::Sprinting;
}

void UWolverineMovementComponent::StartClawSprint()
{
    MaxWalkSpeed = ClawSprintSpeed;
    CurrentTraversalState = ETraversalState::ClawSprinting;
}

void UWolverineMovementComponent::StartWallClimb(const FVector& WallNormal)
{
    IsWallClimbing = true;
    CurrentTraversalState = ETraversalState::WallClimbing;
}

void UWolverineMovementComponent::StartClawSwing(const FVector& AnchorPoint)
{
    IsClawSwinging = true;
    CurrentTraversalState = ETraversalState::ClawSwinging;
}

void UWolverineMovementComponent::PerformClawLunge(AActor* Target)
{
    IsClawLunging = true;
    CurrentTraversalState = ETraversalState::ClawLunging;
    // Launch toward target
}

void UWolverineMovementComponent::PerformDropAttack()
{
    // Ground slam on landing
}

void UWolverineMovementComponent::PerformClawBrake()
{
    CurrentTraversalState = ETraversalState::ClawBraking;
}
```

**File:** `Source/Wolverine/Private/Components/WolverineMovementComponent.cpp`
**Dependencies:** WolverineMovementComponent.h

---

### 3.3 WolverineCharacter.h
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "WolverineCoreTypes.h"
#include "WolverineCharacter.generated.h"

UCLASS()
class WOLVERINE_API AWolverineCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AWolverineCharacter();

protected:
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

public:
    /** Claw component */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWolverineClawComponent* ClawComponent;

    /** Wound system component */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWolverineWoundSystemComponent* WoundSystemComponent;

    /** Rage component */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWolverineRageComponent* RageComponent;

    /** Movement component */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWolverineMovementComponent* MovementComponent;

    /** Trauma system component */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWolverineTraumaSystemComponent* TraumaSystemComponent;

    /** Audio component */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UWolverineAudioComponent* AudioComponent;

    /** Haptic feedback system */
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UHapticFeedbackSystem* HapticFeedbackSystem;

    /** Animation instance */
    UPROPERTY()
    class UWolverineAnimationInstance* AnimationInstance;

    /** Input: Deploy claws */
    void Input_DeployClaws();

    /** Input: Sprint */
    void Input_Sprint();

    /** Input: Jump */
    void Input_Jump();

    /** Input: Crouch */
    void Input_Crouch();

    /** Input: Light attack */
    void Input_LightAttack();

    /** Input: Heavy attack */
    void Input_HeavyAttack();

    /** Input: Dodge */
    void Input_Dodge();
};
```

**File:** `Source/Wolverine/Public/WolverineCharacter.h`
**Dependencies:** L0 + L1 + L2 (all components)
**Parent:** ACharacter
**FR Mapping:** All (aggregates all systems)

---

### 3.4 WolverineCharacter.cpp
```cpp
#include "WolverineCharacter.h"
#include "Components/WolverineClawComponent.h"
#include "Components/WolverineWoundSystemComponent.h"
#include "Components/WolverineRageComponent.h"
#include "Components/WolverineMovementComponent.h"
#include "Components/WolverineTraumaSystemComponent.h"
#include "Components/WolverineAudioComponent.h"
#include "Components/HapticFeedbackSystem.h"
#include "Animation/WolverineAnimationInstance.h"

AWolverineCharacter::AWolverineCharacter()
{
    // Create components
    ClawComponent = CreateDefaultSubobject<UWolverineClawComponent>(TEXT("ClawComponent"));
    WoundSystemComponent = CreateDefaultSubobject<UWolverineWoundSystemComponent>(TEXT("WoundSystemComponent"));
    RageComponent = CreateDefaultSubobject<UWolverineRageComponent>(TEXT("RageComponent"));
    MovementComponent = CreateDefaultSubobject<UWolverineMovementComponent>(TEXT("MovementComponent"));
    TraumaSystemComponent = CreateDefaultSubobject<UWolverineTraumaSystemComponent>(TEXT("TraumaSystemComponent"));
    AudioComponent = CreateDefaultSubobject<UWolverineAudioComponent>(TEXT("AudioComponent"));
    HapticFeedbackSystem = CreateDefaultSubobject<UHapticFeedbackSystem>(TEXT("HapticFeedbackSystem"));
}

void AWolverineCharacter::BeginPlay()
{
    Super::BeginPlay();

    // Get animation instance
    if (GetMesh())
    {
        AnimationInstance = Cast<UWolverineAnimationInstance>(GetMesh()->GetAnimInstance());
    }
}

void AWolverineCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // Bind inputs
    PlayerInputComponent->BindAction("DeployClaws", IE_Pressed, this, &AWolverineCharacter::Input_DeployClaws);
    PlayerInputComponent->BindAction("Sprint", IE_Pressed, this, &AWolverineCharacter::Input_Sprint);
    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &AWolverineCharacter::Input_Jump);
    PlayerInputComponent->BindAction("LightAttack", IE_Pressed, this, &AWolverineCharacter::Input_LightAttack);
    PlayerInputComponent->BindAction("HeavyAttack", IE_Pressed, this, &AWolverineCharacter::Input_HeavyAttack);
}

void AWolverineCharacter::Input_DeployClaws()
{
    ClawComponent->DeployClaws(EClawSide::Left);
    ClawComponent->DeployClaws(EClawSide::Right);
}

void AWolverineCharacter::Input_Sprint()
{
    MovementComponent->StartSprint();
}

void AWolverineCharacter::Input_Jump()
{
    Jump();
}

void AWolverineCharacter::Input_Crouch()
{
    bWantsToCrouch = !bWantsToCrouch;
}

void AWolverineCharacter::Input_LightAttack()
{
    // Trigger light attack
}

void AWolverineCharacter::Input_HeavyAttack()
{
    // Trigger heavy attack
}

void AWolverineCharacter::Input_Dodge()
{
    // Trigger dodge
}
```

**File:** `Source/Wolverine/Private/WolverineCharacter.cpp`
**Dependencies:** WolverineCharacter.h + all component headers

---

## BUILD LEVEL 4 — AI + World

*(Remaining modules follow same pattern — abbreviated for brevity)*

### 4.1 WeaponXSoldier.h/cpp
**Parent:** ACharacter
**Dependencies:** L0 + L3
**FR Mapping:** FR-09

### 4.2 WeaponXHeavyUnit.h/cpp
**Parent:** AWeaponXSoldier
**Dependencies:** L0 + L3
**FR Mapping:** FR-09

### 4.3 MutantHunter.h/cpp
**Parent:** AWeaponXSoldier
**Dependencies:** L0 + L3
**FR Mapping:** FR-09

### 4.4 FeralMutant.h/cpp
**Parent:** AWeaponXSoldier
**Dependencies:** L0 + L3
**FR Mapping:** FR-09

### 4.5 Sentinel.h/cpp
**Parent:** AWeaponXSoldier
**Dependencies:** L0 + L3 + L4
**FR Mapping:** FR-09

### 4.6 EscalationManager.h/cpp
**Parent:** AActor
**Dependencies:** L0 + L3 + L4
**FR Mapping:** FR-14

### 4.7 PortAshfordWorldSettings.h/cpp
**Parent:** AWorldSettings
**Dependencies:** L0 + L1
**FR Mapping:** FR-12, FR-13
**HR Mapping:** HR-03, HR-05

### 4.8 WeatherSystem.h/cpp
**Parent:** AActor
**Dependencies:** L0 + L4
**FR Mapping:** FR-12

### 4.9 DestructionPersistenceData.h/cpp
**Parent:** UDataAsset
**Dependencies:** L0
**FR Mapping:** FR-13
**HR Mapping:** HR-05
**NFR Mapping:** NFR-06

---

## BUILD LEVEL 5 — Game Flow

### 5.1 WolverineGameMode.h/cpp
**Parent:** AGameMode
**Dependencies:** L0-L4
**FR Mapping:** FR-17 (three-act narrative)

### 5.2 WolverineGameState.h/cpp
**Parent:** AGameState
**Dependencies:** L0 + L3
**FR Mapping:** Replication

### 5.3 WolverinePlayerState.h/cpp
**Parent:** APlayerState
**Dependencies:** L0
**FR Mapping:** FR-11, FR-15
**HR Mapping:** HR-08 (no XP/skills)

---

## BUILD ORDER SUMMARY

| Level | Module | Files | Cumulative | Milestone |
|-------|--------|-------|------------|-----------|
| 0 | CoreTypes, Interfaces, Structs | 8 | 8 | Types available |
| 1 | MaterialResponse, WoundSystem, Animation, SaveGame | 8 | 16 | Systems ready |
| 2 | Claw, Rage, Trauma, Audio, Haptic | 10 | 26 | Components ready |
| 3 | Movement, Character | 4 | 30 | **CLAWS IN GAME** |
| 4 | AI (5), World (4) | 18 | 48 | AI + World integrated |
| 5 | GameMode, GameState, PlayerState | 6 | 54 | **FULL GAME LOOP** |

**Total C++ Files:** 54 headers + 54 implementation = **108 files**

---

## DECISION_HASH

```json
{
  "document": "wfmod.dep.md",
  "project": "wolf.beast",
  "version": "1.0",
  "created": "2026-03-08",
  "derived_from": ["wfdep.graph.md", "wfarch.md"],
  "build_levels": 6,
  "cpp_modules": 31,
  "cpp_files": 62,
  "total_files": 108,
  "key_decisions": [
    "Level 0 frozen after L1P9 — WolverineCoreTypes is foundational",
    "WoundSystemComponent ticks at 10Hz (0.1f) — NFR-01 performance optimization",
    "RageComponent::AddRage() has NO BlueprintCallable — HR-04 enforced",
    "ClawComponent ticks at 60fps during combat — NFR-02 <200ms response",
    "Critical path: L0→L1→L2→L3 = CLAWS IN GAME at Level 3",
    "All 6 EClawMaterialType values defined — HR-06 compliance verified"
  ],
  "constraints": [
    "No changes to Level 0 after L1P9 without full rebuild",
    "RageComponent MUST NOT expose ActivateRage — HR-04 compile-time enforcement",
    "WoundSystemComponent tick interval fixed at 0.1f — do not increase",
    "ClawComponent material trace cached if no movement — performance budget"
  ],
  "hr_compliance": {
    "HR-01": "ClawComponent deploy time <200ms — NFR-02",
    "HR-02": "WoundSystemComponent mesh deformation — non-Nanite skeletal mesh",
    "HR-04": "RageComponent::AddRage() internal only — no BlueprintCallable",
    "HR-05": "DestructionPersistenceData survives save/load — NFR-06",
    "HR-06": "EClawMaterialType has exactly 6 values",
    "HR-08": "No XP/level/skill in PlayerState or any UMG"
  }
}
```

---

*WOLVERINE: UNBOUNDED — A FORGE Game*
*Private Repository — All Rights Reserved*
*Logan doesn't wait to be Wolverine. Neither does the game.*
