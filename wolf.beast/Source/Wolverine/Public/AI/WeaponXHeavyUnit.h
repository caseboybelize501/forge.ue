// ============================================================================
// WeaponXHeavyUnit.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T041
// Purpose: Powered armor — claw pry required
// FR Mapping: FR-09
// Dependencies: T039
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AI/WeaponXSoldier.h"
#include "WeaponXHeavyUnit.generated.h"

// TODO (T041.1): Define AWeaponXHeavyUnit class (AWeaponXSoldier)
// TODO (T041.2): Declare ArmorHealth (float)
// TODO (T041.3): Declare PryArmor() function (claw interaction)

UCLASS()
class WOLVERINE_API AWeaponXHeavyUnit : public AWeaponXSoldier
{
    GENERATED_BODY()

public:
    AWeaponXHeavyUnit();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement armor breach mechanic
};
