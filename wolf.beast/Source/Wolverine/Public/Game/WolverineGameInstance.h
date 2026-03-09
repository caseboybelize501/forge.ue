// ============================================================================
// WolverineGameInstance.h
// ============================================================================
// Build Level: L5 (Game Flow)
// Task Ref: T081
// Purpose: Game instance (menu to game)
// Dependencies: T015
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "WolverineSaveGame.h"
#include "WolverineGameInstance.generated.h"

// TODO (T081.1): Define UWolverineGameInstance class (UGameInstance)
// TODO (T081.2): Declare CurrentSaveGame (UWolverineSaveGame)
// TODO (T081.3): Declare LoadGame() function
// TODO (T081.4): Declare SaveGame() function

UCLASS()
class WOLVERINE_API UWolverineGameInstance : public UGameInstance
{
    GENERATED_BODY()

public:
    UWolverineGameInstance();

public:
    // TODO: Implement save/load management
};
