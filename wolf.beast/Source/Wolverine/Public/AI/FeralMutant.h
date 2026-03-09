// ============================================================================
// FeralMutant.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T045
// Purpose: Fast, dodge-heavy enemy
// FR Mapping: FR-09
// Dependencies: T039
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AI/WeaponXSoldier.h"
#include "FeralMutant.generated.h"

// TODO (T045.1): Define AFeralMutant class (AWeaponXSoldier)
// TODO (T045.2): Declare DodgeChance (float)
// TODO (T045.3): Declare ChainAttackCombo() function

UCLASS()
class WOLVERINE_API AFeralMutant : public AWeaponXSoldier
{
    GENERATED_BODY()

public:
    AFeralMutant();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement evasive dodge, chain attacks
};
