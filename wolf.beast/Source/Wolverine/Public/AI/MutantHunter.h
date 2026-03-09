// ============================================================================
// MutantHunter.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T043
// Purpose: Healing dampening specialist
// FR Mapping: FR-09
// Dependencies: T039
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AI/WeaponXSoldier.h"
#include "MutantHunter.generated.h"

// TODO (T043.1): Define AMutantHunter class (AWeaponXSoldier)
// TODO (T043.2): Declare DampeningFieldActive (bool)
// TODO (T043.3): Declare ActivateDampeningField() function

UCLASS()
class WOLVERINE_API AMutantHunter : public AWeaponXSoldier
{
    GENERATED_BODY()

public:
    AMutantHunter();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement healing dampening field
};
