// ============================================================================
// WolverinePlayerController.h
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T031
// Purpose: Input binding, UI management
// FR Mapping: FR-02, FR-03
// Dependencies: T029
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "WolverinePlayerController.generated.h"

// TODO (T031.1): Define AWolverinePlayerController class (APlayerController)
// TODO (T031.2): Declare HUDClass reference
// TODO (T031.3): Declare InputMappingContext (UPROPERTY)
// TODO (T031.4): Declare ShowHUD(), HideHUD() functions

UCLASS()
class WOLVERINE_API AWolverinePlayerController : public APlayerController
{
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Add HUD management functions
};
