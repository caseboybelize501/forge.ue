// ============================================================================
// WolverineHUD.h
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T033
// Purpose: Minimal HUD (compass, vignette, wound indicator)
// FR Mapping: FR-19
// HR Mapping: HR-08 (no skill trees)
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "WolverineHUD.generated.h"

// Forward declarations
class UWoundIndicatorWidget;
class UCompassWidget;

// TODO (T033.1): Define UWolverineHUD class (UUserWidget)
// TODO (T033.2): Declare CompassWidget reference
// TODO (T033.3): Declare WoundIndicatorWidget reference
// TODO (T033.4): Declare UpdateWoundIndicator(EWoundSeverity) function
// TODO (T033.5): Declare UpdateCompassBearing(float Degrees) function
// TODO (T033.6): NO XP/level/skill references - HR-08

UCLASS()
class WOLVERINE_API UWolverineHUD : public UUserWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeConstruct() override;

public:
    // TODO: Add widget references
    // TODO: Add HUD update functions (minimal - wound-driven only)
};
