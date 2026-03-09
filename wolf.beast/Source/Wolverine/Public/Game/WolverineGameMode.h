// ============================================================================
// WolverineGameMode.h
// ============================================================================
// Build Level: L5 (Game Flow)
// Task Ref: T075
// Purpose: 72-hour narrative, mission flow
// FR Mapping: FR-17
// Dependencies: T001, T049
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameMode.h"
#include "WolverineCoreTypes.h"
#include "WolverineGameMode.generated.h"

// TODO (T075.1): Define AWolverineGameMode class (AGameMode)
// TODO (T075.2): Declare GameTimeHours (float, 0-72)
// TODO (T075.3): Declare CurrentMission (string)
// TODO (T075.4): Declare AdvanceTime(float Hours) function

UCLASS()
class WOLVERINE_API AWolverineGameMode : public AGameMode
{
    GENERATED_BODY()

public:
    AWolverineGameMode();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement 72-hour narrative timeline
};
