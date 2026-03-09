// ============================================================================
// WeaponXSoldier.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T039
// Purpose: Standard infantry AI
// FR Mapping: FR-09
// HR Mapping: HR-07 (predator optional - fear response)
// NFR Mapping: NFR-04 (event-driven AI)
// Dependencies: T001, T005
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "IWolverineDamageInterface.h"
#include "WeaponXSoldier.generated.h"

// TODO (T039.1): Define AWeaponXSoldier class (ACharacter)
// TODO (T039.2): Declare FearLevel (float, 0-100)
// TODO (T039.3): Declare BehaviorTree reference
// TODO (T039.4): Declare OnFearEscalated delegate - HR-07

UCLASS()
class WOLVERINE_API AWeaponXSoldier : public ACharacter, public IWolverineDamageInterface
{
    GENERATED_BODY()

public:
    AWeaponXSoldier();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement AI behavior (fear response, suppression)
};
