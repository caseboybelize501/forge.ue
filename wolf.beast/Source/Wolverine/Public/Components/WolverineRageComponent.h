// ============================================================================
// WolverineRageComponent.h
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T019
// Purpose: Rage accumulation, Berserker state machine
// FR Mapping: FR-05
// HR Mapping: HR-04 (rage cannot be manually activated)
// NFR Mapping: NFR-01 (60fps), NFR-04 (event-driven)
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineRageComponent.generated.h"

// TODO (T019.1): Define UWolverineRageComponent class (UActorComponent)
// TODO (T019.2): Declare CurrentRage (float, 0-100)
// TODO (T019.3): Declare CurrentRageLevel (ERageLevel)
// TODO (T019.4): Declare OnDamageDealt(float Damage) function (BlueprintCallable) - HR-04
// TODO (T019.5): Declare OnDamageReceived(float Damage) function (BlueprintCallable) - HR-04
// TODO (T019.6): Declare AddRage(float Amount) function (NOT BlueprintCallable) - HR-04
// TODO (T019.7): Declare OnBerserkerActivated delegate

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineRageComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineRageComponent();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement rage accumulation (event-driven only)
};
