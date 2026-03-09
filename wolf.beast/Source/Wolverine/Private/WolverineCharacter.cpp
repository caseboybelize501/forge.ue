// ============================================================================
// WolverineCharacter.cpp
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T030
// Purpose: Component creation, input binding
// FR Mapping: All FR requirements
// HR Mapping: All HR requirements
// Dependencies: T029
// ============================================================================
#include "WolverineCharacter.h"

// TODO (T030.1): Implement constructor (create components, attach)
// TODO (T030.2): Implement SetupPlayerInputComponent
// TODO (T030.3): Bind input actions to functions - Q=ClawDeploy (DefaultInput.ini)
// TODO (T030.4): Implement input handlers (call component functions)
// TODO (T030.5): Add BeginPlay (initialize state)

AWolverineCharacter::AWolverineCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AWolverineCharacter::BeginPlay()
{
    Super::BeginPlay();
}

void AWolverineCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    // TODO: Bind input actions
}
