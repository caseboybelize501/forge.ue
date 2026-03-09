// ============================================================================
// WeaponXSoldier.cpp
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T040
// Purpose: Behavior Tree execution, fear state
// FR Mapping: FR-09
// HR Mapping: HR-07 (predator optional)
// Dependencies: T039
// ============================================================================
#include "AI/WeaponXSoldier.h"

// TODO (T040.1): Implement BehaviorTree execution
// TODO (T040.2): Implement fear response (trembling, retreat at high fear) - HR-07
// TODO (T040.3): Add suppression behavior

AWeaponXSoldier::AWeaponXSoldier()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AWeaponXSoldier::BeginPlay()
{
    Super::BeginPlay();
}
