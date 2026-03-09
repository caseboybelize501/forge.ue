// ============================================================================
// WolverineGameState.h
// ============================================================================
// Build Level: L5 (Game Flow)
// Task Ref: T077
// Purpose: Replicated game state
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameState.h"
#include "WolverineGameState.generated.h"

// TODO (T077.1): Define AWolverineGameState class (AGameState)
// TODO (T077.2): Declare replicated properties (time, weather, district)

UCLASS()
class WOLVERINE_API AWolverineGameState : public AGameState
{
    GENERATED_BODY()

public:
    AWolverineGameState();

protected:
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

public:
    // TODO: Add replicated state properties
};
