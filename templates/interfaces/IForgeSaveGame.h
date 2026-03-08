// IForgeSaveGame.h — Level 0 Foundation
// Save game base class interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "IForgeSaveGame.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeSaveGame : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeSaveGame Interface
 * 
 * Interface for save game serialization and deserialization.
 * All FORGE save games implement this interface.
 */
class FORGE_API IIForgeSaveGame
{
    GENERATED_BODY()

public:
    /** Get save slot name */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|SaveGame")
    FString GetSlotName() const;

    /** Get user index */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|SaveGame")
    int32 GetUserIndex() const;

    /** Get play time in seconds */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|SaveGame")
    float GetPlayTime() const;

    /** Get save timestamp */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|SaveGame")
    FDateTime GetTimestamp() const;

    /** Serialize save data to bytes */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|SaveGame")
    TArray<uint8> Serialize() const;

    /** Deserialize save data from bytes */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|SaveGame")
    bool Deserialize(const TArray<uint8>& Data);
};
