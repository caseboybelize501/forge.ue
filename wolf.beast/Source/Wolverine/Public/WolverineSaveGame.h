// ============================================================================
// WolverineSaveGame.h
// ============================================================================
// Build Level: L1 (Systems)
// Task Ref: T015
// Purpose: Save game class with destruction persistence
// FR Mapping: FR-11, FR-13, FR-15
// HR Mapping: HR-05 (persistent destruction)
// NFR Mapping: NFR-06 (save/load cycle)
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "WolverineDataStructures.h"
#include "WolverineSaveGame.generated.h"

// TODO (T015.1): Define UWolverineSaveGame class (USaveGame)
// TODO (T015.2): Declare DestructionRecords map (GUID → FDestructionRecord)
// TODO (T015.3): Declare PlayerState (location, health, memories, intel)
// TODO (T015.4): Declare GameTimeHours (0-72)
// TODO (T015.5): Declare CurrentDistrict, CurrentWeather

UCLASS()
class WOLVERINE_API UWolverineSaveGame : public USaveGame
{
    GENERATED_BODY()

public:
    UWolverineSaveGame();

    // TODO: Add save game properties
};
