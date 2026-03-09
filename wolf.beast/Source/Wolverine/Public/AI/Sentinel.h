// ============================================================================
// Sentinel.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T047
// Purpose: Late-game boss — multi-phase
// FR Mapping: FR-09
// Dependencies: T039
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AI/WeaponXSoldier.h"
#include "Sentinel.generated.h"

// TODO (T047.1): Define ASentinel class (AWeaponXSoldier)
// TODO (T047.2): Declare CurrentPhase (enum, 3 phases)
// TODO (T047.3): Declare PhaseTransition() function
// TODO (T047.4): Declare AreaDestructionAttack() function

UCLASS()
class WOLVERINE_API ASentinel : public AWeaponXSoldier
{
    GENERATED_BODY()

public:
    ASentinel();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement multi-phase boss behavior
};
