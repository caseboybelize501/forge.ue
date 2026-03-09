// ============================================================================
// FearStateMachine.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T071
// Purpose: Fear escalation system
// FR Mapping: FR-09
// HR Mapping: HR-07 (predator optional)
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "FearStateMachine.generated.h"

// TODO (T071.1): Define UFearStateMachine class (UActorComponent)
// TODO (T071.2): Declare FearLevel (float, 0-100)
// TODO (T071.3): Declare AddFear(float Amount) function
// TODO (T071.4): Declare OnFearThresholdCrossed delegate - HR-07

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UFearStateMachine : public UActorComponent
{
    GENERATED_BODY()

public:
    UFearStateMachine();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement fear escalation (claw sightings, damage)
};
