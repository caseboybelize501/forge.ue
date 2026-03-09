// ============================================================================
// WolverineMovementComponent.h
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T027
// Purpose: Custom traversal (sprint, wall climb, claw swing, lunge)
// FR Mapping: FR-02
// HR Mapping: HR-01 (claws <10s), HR-07 (predator optional)
// NFR Mapping: NFR-01 (60fps), NFR-02 (<200ms response)
// Dependencies: T001, T017
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineMovementComponent.generated.h"

// TODO (T027.1): Define UWolverineMovementComponent class (UActorComponent)
// TODO (T027.2): Declare CurrentTraversalState (ETraversalState)
// TODO (T027.3): Declare Sprint(), WallClimb(), ClawSwing(), ClawLunge() functions
// TODO (T027.4): Declare ClawBrake() function (stealth) - HR-07
// TODO (T027.5): Declare movement parameters (speed, acceleration, lunge distance)

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineMovementComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineMovementComponent();
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement traversal state machine
};
