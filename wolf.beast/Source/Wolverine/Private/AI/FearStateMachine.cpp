// ============================================================================
// FearStateMachine.cpp
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T072
// Purpose: Fear level calculation, response
// FR Mapping: FR-09
// HR Mapping: HR-07 (predator optional)
// Dependencies: T071
// ============================================================================
#include "AI/FearStateMachine.h"

// TODO (T072.1): Implement AddFear (from claw sightings, damage)
// TODO (T072.2): Implement fear response (trembling, missed shots, retreat) - HR-07
// TODO (T072.3): Add fear decay over time

UFearStateMachine::UFearStateMachine()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UFearStateMachine::BeginPlay()
{
    Super::BeginPlay();
}
