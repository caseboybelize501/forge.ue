// IForgeAchievement.h — Level 0 Foundation
// Achievement/trophy interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IForgeAchievement.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeAchievement : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeAchievement Interface
 * 
 * Interface for achievement/trophy tracking and unlocking.
 * Integrates with platform-specific achievement systems.
 */
class FORGE_API IIForgeAchievement
{
    GENERATED_BODY()

public:
    /** Unlock achievement by ID */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    void UnlockAchievement(const FString& AchievementId);

    /** Check if achievement is unlocked */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    bool IsAchievementUnlocked(const FString& AchievementId) const;

    /** Get achievement progress */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    float GetAchievementProgress(const FString& AchievementId) const;

    /** Update achievement progress */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    void UpdateAchievementProgress(const FString& AchievementId, float Progress, float MaxProgress);

    /** Get all achievement IDs */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    TArray<FString> GetAllAchievementIds() const;

    /** Get achievement name */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    FString GetAchievementName(const FString& AchievementId) const;

    /** Get achievement description */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Achievement")
    FString GetAchievementDescription(const FString& AchievementId) const;
};
