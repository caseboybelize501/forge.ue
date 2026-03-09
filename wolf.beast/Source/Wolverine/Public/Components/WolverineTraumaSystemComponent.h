// ============================================================================
// WolverineTraumaSystemComponent.h
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T021
// Purpose: Memory unlocks, mechanical bonuses
// FR Mapping: FR-11
// HR Mapping: HR-08 (no skill trees)
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineDataStructures.h"
#include "WolverineTraumaSystemComponent.generated.h"

// TODO (T021.1): Define UWolverineTraumaSystemComponent class (UActorComponent)
// TODO (T021.2): Declare UnlockedMemories array (FMemoryFragment)
// TODO (T021.3): Declare UnlockMemory(FMemoryFragment) function
// TODO (T021.4): Declare GetMechanicalBonus() function
// TODO (T021.5): Declare OnMemoryUnlocked delegate - HR-08

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineTraumaSystemComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineTraumaSystemComponent();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement memory-based progression (NO XP/levels)
};
