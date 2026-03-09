// ============================================================================
// WolverineWoundSystemComponent.h
// ============================================================================
// Build Level: L1 (Systems)
// Task Ref: T011
// Purpose: Mesh deformation, healing, wound state management
// FR Mapping: FR-06
// HR Mapping: HR-02 (real-time mesh deformation)
// NFR Mapping: NFR-01 (60fps), NFR-03 (10Hz healing tick)
// Dependencies: T001, T005, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWolverineDamageInterface.h"
#include "WolverineDataStructures.h"
#include "WolverineWoundSystemComponent.generated.h"

// TODO (T011.1): Define UWolverineWoundSystemComponent class (UActorComponent)
// TODO (T011.2): Declare WoundState array (FWoundData)
// TODO (T011.3): Declare HealingTickRate (default 10Hz)
// TODO (T011.4): Declare ApplyWound(FWoundData) function
// TODO (T011.5): Declare HealWound(float DeltaTime) function
// TODO (T011.6): Declare GetWoundSeverity() function
// TODO (T011.7): Declare morph target references (UPROPERTY)

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineWoundSystemComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineWoundSystemComponent();
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement wound application and healing
};
