// ============================================================================
// WeaponXSquadLeader.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T067
// Purpose: Squad coordination
// FR Mapping: FR-09
// Dependencies: T039
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AI/WeaponXSoldier.h"
#include "WeaponXSquadLeader.generated.h"

// TODO (T067.1): Define AWeaponXSquadLeader class (AWeaponXSoldier)
// TODO (T067.2): Declare SquadMembers array
// TODO (T067.3): Declare OrderSquad(FString Command) function

UCLASS()
class WOLVERINE_API AWeaponXSquadLeader : public AWeaponXSoldier
{
    GENERATED_BODY()

public:
    AWeaponXSquadLeader();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement squad tactics, backup calls
};
