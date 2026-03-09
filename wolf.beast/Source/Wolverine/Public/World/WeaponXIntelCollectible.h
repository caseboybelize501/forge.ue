// ============================================================================
// WeaponXIntelCollectible.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T063
// Purpose: Weapon X collectible (audio log/photo)
// FR Mapping: FR-15
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WolverineDataStructures.h"
#include "WeaponXIntelCollectible.generated.h"

// TODO (T063.1): Define AWeaponXIntelCollectible class (AActor)
// TODO (T063.2): Declare IntelData (FIntelItem) - Layer 3 content slot
// TODO (T063.3): Declare OnCollect delegate
// TODO (T063.4): NO map markers - FR-15

UCLASS()
class WOLVERINE_API AWeaponXIntelCollectible : public AActor
{
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement collectible trigger (no map markers)
};
