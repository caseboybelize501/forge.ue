// ============================================================================
// WolverineAnimationInstance.h
// ============================================================================
// Build Level: L1 (Systems)
// Task Ref: T013
// Purpose: Motion Matching, claw animation blending
// FR Mapping: FR-02, FR-03
// NFR Mapping: NFR-01 (60fps), NFR-07 (Motion Matching)
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "WolverineCoreTypes.h"
#include "WolverineAnimationInstance.generated.h"

// TODO (T013.1): Define UWolverineAnimationInstance class (UAnimInstance)
// TODO (T013.2): Declare ClawBlendWeight (float, 0-1)
// TODO (T013.3): Declare CurrentTraversalState (ETraversalState)
// TODO (T013.4): Declare MotionMatchingDatabase (retracted/deployed)
// TODO (T013.5): Declare UpdateClawBlend(float Weight) function

UCLASS()
class WOLVERINE_API UWolverineAnimationInstance : public UAnimInstance
{
    GENERATED_BODY()

public:
    virtual void NativeUpdateAnimation(float DeltaSeconds) override;

protected:
    // TODO: Add motion matching properties
    // TODO: Add claw blend weight properties
};
