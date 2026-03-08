// IForgeCharacter.h — Level 0 Foundation
// Base Character interface for all FORGE projects
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "IForgeCharacter.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeCharacter : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeCharacter Interface
 * 
 * Base Character interface defining common character functionality
 * across all FORGE-generated projects.
 */
class FORGE_API IIForgeCharacter
{
    GENERATED_BODY()

public:
    /** Get character health */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Character")
    float GetHealth() const;

    /** Apply damage to character */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Character")
    void ApplyDamage(float Damage, class AController* InstigatedBy, class AActor* DamageCauser);

    /** Check if character is alive */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Character")
    bool IsAlive() const;

    /** Get character movement speed */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Character")
    float GetMovementSpeed() const;

    /** Set character movement speed */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Character")
    void SetMovementSpeed(float Speed);
};
