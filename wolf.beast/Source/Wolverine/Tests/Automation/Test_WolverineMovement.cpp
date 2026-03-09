// ============================================================================
// Test_WolverineMovement.cpp
// ============================================================================
// Build Level: Automation Tests
// Task Ref: T108
// Purpose: Traversal states, claw lunge distance, wall climb
// HR Verified: HR-01 (claws <10s), HR-07 (predator optional)
// Dependencies: T028 (WolverineMovementComponent)
// ============================================================================
#include "CoreMinimal.h"
#include "AutomationTest.h"
#include "Components/WolverineMovementComponent.h"

// TODO (T108.1): Implement TraversalStates test (all 5 states)
// TODO (T108.2): Implement ClawLungeDistance test - HR-01
// TODO (T108.3): Implement WallClimb test
// TODO (T108.4): Implement StealthLoudOptions test (HR-07) - HR-07

BEGIN_DEFINE_SPEC(FWolverineMovementSpec, "Wolverine.Movement.HR01_HR07",
    EAutomationTestFlags::ProductFilter | EAutomationTestFlags::ApplicationContextMask)

void TestTraversalStates();
void TestClawLungeDistance();
void TestWallClimb();
void TestStealthLoudOptions();

END_DEFINE_SPEC(FWolverineMovementSpec)
