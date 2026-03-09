// ============================================================================
// EnvironmentalDestructible.cpp
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T060
// Purpose: GUID assignment, destruction state
// FR Mapping: FR-13
// HR Mapping: HR-05 (persistent destruction)
// Dependencies: T059
// ============================================================================
#include "World/EnvironmentalDestructible.h"

// TODO (T060.1): Implement constructor (generate GUID)
// TODO (T060.2): Implement GetDestructionState (serialize Chaos state)
// TODO (T060.3): Add destruction callback (notify persistence) - HR-05

AEnvironmentalDestructible::AEnvironmentalDestructible()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AEnvironmentalDestructible::BeginPlay()
{
    Super::BeginPlay();
}
