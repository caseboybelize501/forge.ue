// ============================================================================
// WolverineTraumaSystemComponent.cpp
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T022
// Purpose: Bonus calculation from memories
// FR Mapping: FR-11
// HR Mapping: HR-08 (no skill trees)
// Dependencies: T021
// ============================================================================
#include "Components/WolverineTraumaSystemComponent.h"

// TODO (T022.1): Implement UnlockMemory (add to array, broadcast)
// TODO (T022.2): Implement GetMechanicalBonus (aggregate from memories)
// TODO (T022.3): Define bonus types (healing rate, rage gain, damage resist)
// TODO (T022.4): Ensure NO XP/level/skill references - HR-08

UWolverineTraumaSystemComponent::UWolverineTraumaSystemComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UWolverineTraumaSystemComponent::BeginPlay()
{
    Super::BeginPlay();
}
