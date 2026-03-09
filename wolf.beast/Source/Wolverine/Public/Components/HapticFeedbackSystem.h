// ============================================================================
// HapticFeedbackSystem.h
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T025
// Purpose: Asymmetric haptic feedback per claw/material
// FR Mapping: FR-20
// HR Mapping: HR-06 (6 material types)
// NFR Mapping: NFR-02 (<200ms response)
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "WolverineDataStructures.h"
#include "HapticFeedbackSystem.generated.h"

// TODO (T025.1): Define UHapticFeedbackSystem class (UObject)
// TODO (T025.2): Declare HapticDataMap (EClawMaterialType → FHapticFeedbackData)
// TODO (T025.3): Declare PlayHaptic(EClawMaterialType, EControllerHand) function
// TODO (T025.4): Declare HapticStrength, HapticDuration properties

UCLASS()
class WOLVERINE_API UHapticFeedbackSystem : public UObject
{
    GENERATED_BODY()

public:
    UHapticFeedbackSystem();

public:
    // TODO: Implement per-material haptic feedback
};
