// ============================================================================
// WolverineRageComponent.cpp
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T020
// Purpose: Event-driven rage (NO manual activation)
// FR Mapping: FR-05
// HR Mapping: HR-04 (rage cannot be manually activated)
// Dependencies: T019
// ============================================================================
#include "Components/WolverineRageComponent.h"

// TODO (T020.1): Implement OnDamageDealt (add rage from damage dealt)
// TODO (T020.2): Implement OnDamageReceived (add rage from damage taken)
// TODO (T020.3): Implement AddRage (internal, clamp 0-100) - NOT BlueprintCallable
// TODO (T020.4): Implement CheckBerserker (auto-trigger at 100) - HR-04
// TODO (T020.5): Implement rage decay over time

UWolverineRageComponent::UWolverineRageComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UWolverineRageComponent::BeginPlay()
{
    Super::BeginPlay();
}
