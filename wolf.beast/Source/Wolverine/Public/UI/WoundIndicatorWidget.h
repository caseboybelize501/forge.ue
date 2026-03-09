// ============================================================================
// WoundIndicatorWidget.h
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T035
// Purpose: Wound feedback (not a health bar)
// FR Mapping: FR-19
// HR Mapping: HR-08 (no skill trees)
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "WolverineCoreTypes.h"
#include "WoundIndicatorWidget.generated.h"

// TODO (T035.1): Define UWoundIndicatorWidget class (UUserWidget)
// TODO (T035.2): Declare VignetteImage reference
// TODO (T035.3): Declare SetSeverity(EWoundSeverity) function
// TODO (T035.4): NOT a health bar - visual feedback only - HR-08

UCLASS()
class WOLVERINE_API UWoundIndicatorWidget : public UUserWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeConstruct() override;

public:
    // TODO: Add vignette visual reference
    // TODO: Add wound severity update function
};
