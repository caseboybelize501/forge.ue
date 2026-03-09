// ============================================================================
// PortAshfordWorldSettings.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T049
// Purpose: District streaming, weather, destruction persistence
// FR Mapping: FR-12, FR-13
// HR Mapping: HR-03 (no loading screens), HR-05 (persistent destruction)
// NFR Mapping: NFR-06 (save/load cycle)
// Dependencies: T001, T007, T015
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/WorldSettings.h"
#include "WolverineCoreTypes.h"
#include "WolverineDataStructures.h"
#include "PortAshfordWorldSettings.generated.h"

// TODO (T049.1): Define APortAshfordWorldSettings class (AWorldSettings)
// TODO (T049.2): Declare CurrentDistrict (EDistrictType)
// TODO (T049.3): Declare CurrentWeather (EWeatherState)
// TODO (T049.4): Declare GameTimeHours (float, 0-72)
// TODO (T049.5): Declare SaveDestructionState() function - HR-05
// TODO (T049.6): Declare LoadDestructionState() function - HR-05

UCLASS()
class WOLVERINE_API APortAshfordWorldSettings : public AWorldSettings
{
    GENERATED_BODY()

public:
    APortAshfordWorldSettings();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement district streaming, destruction persistence
};
