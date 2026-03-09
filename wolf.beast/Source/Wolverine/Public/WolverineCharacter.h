// ============================================================================
// WolverineCharacter.h
// ============================================================================
// Build Level: L3 (Character)
// Task Ref: T029
// Purpose: Player character — aggregates all components
// FR Mapping: All FR requirements
// HR Mapping: All HR requirements
// Dependencies: T011, T017, T019, T021, T023, T027
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "WolverineCoreTypes.h"
#include "WolverineCharacter.generated.h"

// Forward declarations
class UWolverineClawComponent;
class UWolverineRageComponent;
class UWolverineWoundSystemComponent;
class UWolverineTraumaSystemComponent;
class UWolverineAudioComponent;
class UWolverineMovementComponent;

// TODO (T029.1): Define AWolverineCharacter class (ACharacter)
// TODO (T029.2): Declare component references (Claw, Rage, Wound, Trauma, Audio, Movement)
// TODO (T029.3): Declare Input_DeployClaws(), Input_RetractClaws() functions - HR-01
// TODO (T029.4): Declare Input_Sprint(), Input_ClawLunge() functions
// TODO (T029.5): Declare Input_LightAttack(), Input_HeavyAttack() functions
// TODO (T029.6): Declare Input_Dodge() function

UCLASS()
class WOLVERINE_API AWolverineCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AWolverineCharacter();
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Add component references
    // TODO: Add input handlers
};
