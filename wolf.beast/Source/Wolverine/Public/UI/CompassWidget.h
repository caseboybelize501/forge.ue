// ============================================================================
// CompassWidget.h
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T037
// Purpose: Compass bearing only
// FR Mapping: FR-19
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "CompassWidget.generated.h"

// TODO (T037.1): Define UCompassWidget class (UUserWidget)
// TODO (T037.2): Declare CompassArrow reference
// TODO (T037.3): Declare SetBearing(float Degrees) function
// TODO (T037.4): Declare ObjectiveChevron reference

UCLASS()
class WOLVERINE_API UCompassWidget : public UUserWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeConstruct() override;

public:
    // TODO: Add compass arrow reference
    // TODO: Add bearing update function
};
