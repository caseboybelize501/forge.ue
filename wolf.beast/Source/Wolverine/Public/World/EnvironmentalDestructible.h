// ============================================================================
// EnvironmentalDestructible.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T059
// Purpose: Chaos destruction actor
// FR Mapping: FR-13
// HR Mapping: HR-05 (persistent destruction)
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WolverineDataStructures.h"
#include "EnvironmentalDestructible.generated.h"

// TODO (T059.1): Define AEnvironmentalDestructible class (AActor)
// TODO (T059.2): Declare ActorGUID (FGuid) - HR-05
// TODO (T059.3): Declare ChaosDestructionComponent (UPROPERTY)
// TODO (T059.4): Declare GetDestructionState() function

UCLASS()
class WOLVERINE_API AEnvironmentalDestructible : public AActor
{
    GENERATED_BODY()

public:
    AEnvironmentalDestructible();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement Chaos destruction with GUID tracking
};
