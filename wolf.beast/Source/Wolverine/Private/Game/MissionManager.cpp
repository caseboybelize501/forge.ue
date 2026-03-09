// ============================================================================
// MissionManager.cpp
// ============================================================================
// Build Level: L5 (Game Flow)
// Task Ref: T084
// Purpose: Act transitions, mission triggers
// FR Mapping: FR-17
// Dependencies: T083
// ============================================================================
#include "Game/MissionManager.h"

// TODO (T084.1): Implement CompleteMission (transition to next)
// TODO (T084.2): Add mission triggers (time, location, kills)

UMissionManager::UMissionManager()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UMissionManager::BeginPlay()
{
    Super::BeginPlay();
}
