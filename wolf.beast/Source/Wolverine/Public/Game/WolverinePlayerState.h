// ============================================================================
// WolverinePlayerState.h
// ============================================================================
// Build Level: L5 (Game Flow)
// Task Ref: T079
// Purpose: Persistent player data (NO XP/levels)
// FR Mapping: FR-11, FR-15
// HR Mapping: HR-08 (no skill trees)
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "WolverineDataStructures.h"
#include "WolverinePlayerState.generated.h"

// TODO (T079.1): Define AWolverinePlayerState class (APlayerState)
// TODO (T079.2): Declare UnlockedMemories array
// TODO (T079.3): Declare CollectedIntel array
// TODO (T079.4): NO XP, NO Level, NO SkillPoints - HR-08

UCLASS()
class WOLVERINE_API AWolverinePlayerState : public APlayerState
{
    GENERATED_BODY()

public:
    AWolverinePlayerState();

public:
    // TODO: Add memory/intel persistence (NO XP/levels)
};
