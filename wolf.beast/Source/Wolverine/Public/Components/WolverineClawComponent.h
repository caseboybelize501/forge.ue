// ============================================================================
// WolverineClawComponent.h
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T017
// Purpose: Claw deployment, material tracing, impact events
// FR Mapping: FR-03, FR-04, FR-07
// HR Mapping: HR-01 (claws <10s), HR-06 (6 material types)
// NFR Mapping: NFR-02 (<200ms deploy), NFR-08 (audio never masked)
// Dependencies: T001, T003, T009
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWolverineMaterialResponse.h"
#include "WolverineCoreTypes.h"
#include "WolverineClawComponent.generated.h"

// TODO (T017.1): Define UWolverineClawComponent class (UActorComponent)
// TODO (T017.2): Declare ClawState enum (Retracted, Deploying, Deployed, Retracting)
// TODO (T017.3): Declare DeployClaws() function (BlueprintCallable) - HR-01
// TODO (T017.4): Declare RetractClaws() function
// TODO (T017.5): Declare ClawDeployTime (default 0.15f) - NFR-02
// TODO (T017.6): Declare OnClawImpact delegate (EClawMaterialType)
// TODO (T017.7): Declare MaterialTraceHandle (60fps trace)

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineClawComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineClawComponent();
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement claw deployment and material tracing
};
