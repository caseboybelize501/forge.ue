// IForgeGameMode.h — Level 0 Foundation
// Base GameMode interface for all FORGE projects
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "IForgeGameMode.h"
#include "IForgeGameMode.generated.h"

/**
 * IForgeGameMode
 * 
 * Base GameMode interface that all FORGE-generated projects inherit from.
 * Defines common game state management, scoring, and match lifecycle hooks.
 */
UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeGameMode : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeGameMode Interface
 */
class FORGE_API IIForgeGameMode
{
    GENERATED_BODY()

public:
    /** Initialize game state for new match */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameMode")
    void InitializeGame();

    /** Handle match start */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameMode")
    void OnMatchStart();

    /** Handle match end */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameMode")
    void OnMatchEnd();

    /** Get current game state */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameMode")
    class AForgeGameState* GetForgeGameState() const;
};
