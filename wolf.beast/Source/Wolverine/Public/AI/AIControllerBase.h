// ============================================================================
// AIControllerBase.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T069
// Purpose: Base AI controller
// FR Mapping: FR-09
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "AIControllerBase.generated.h"

// TODO (T069.1): Define AWolverineAIController class (AAIController)
// TODO (T069.2): Declare Blackboard reference
// TODO (T069.3): Declare BehaviorTree reference

UCLASS()
class WOLVERINE_API AWolverineAIController : public AAIController
{
    GENERATED_BODY()

public:
    AWolverineAIController();

protected:
    virtual void OnPossess(APawn* InPawn) override;

public:
    // TODO: Implement common AI logic
};
