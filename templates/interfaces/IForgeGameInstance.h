// IForgeGameInstance.h — Level 0 Foundation
// Persistent state and save/load interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "IForgeGameInstance.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeGameInstance : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeGameInstance Interface
 * 
 * Interface for persistent game state, save/load functionality,
 * and cross-level data persistence.
 */
class FORGE_API IIForgeGameInstance
{
    GENERATED_BODY()

public:
    /** Save current game state */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameInstance")
    bool SaveGame(const FString& SlotName, int32 UserIndex);

    /** Load game state from slot */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameInstance")
    bool LoadGame(const FString& SlotName, int32 UserIndex);

    /** Check if save exists */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameInstance")
    bool DoesSaveGameExist(const FString& SlotName, int32 UserIndex);

    /** Delete save game */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameInstance")
    bool DeleteGame(const FString& SlotName, int32 UserIndex);

    /** Get persistent data value */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameInstance")
    TArray<uint8> GetPersistentData(const FString& Key) const;

    /** Set persistent data value */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|GameInstance")
    void SetPersistentData(const FString& Key, const TArray<uint8>& Value);
};
