// ============================================================================
// AIControllerBase.cpp
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T070
// Purpose: Common AI logic
// FR Mapping: FR-09
// Dependencies: T069
// ============================================================================
#include "AI/AIControllerBase.h"

// TODO (T070.1): Implement OnPossess (run BehaviorTree)
// TODO (T070.2): Initialize Blackboard

AWolverineAIController::AWolverineAIController()
{
}

void AWolverineAIController::OnPossess(APawn* InPawn)
{
    Super::OnPossess(InPawn);
    // TODO: Run BehaviorTree
}
