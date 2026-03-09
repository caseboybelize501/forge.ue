// ============================================================================
// WolverineAudioComponent.h
// ============================================================================
// Build Level: L2 (Components)
// Task Ref: T023
// Purpose: MetaSounds reactive graph
// FR Mapping: FR-18
// HR Mapping: HR-06 (material-specific audio)
// NFR Mapping: NFR-08 (audio never masked)
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "WolverineCoreTypes.h"
#include "WolverineAudioComponent.generated.h"

// TODO (T023.1): Define UWolverineAudioComponent class (UActorComponent)
// TODO (T023.2): Declare CombatIntensity (float, 0-1)
// TODO (T023.3): Declare PlayClawImpactSound(EClawMaterialType) function
// TODO (T023.4): Declare UpdateMusicIntensity(float Intensity) function
// TODO (T023.5): Declare MetaSound references (UPROPERTY)

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineAudioComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UWolverineAudioComponent();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement reactive audio system
};
