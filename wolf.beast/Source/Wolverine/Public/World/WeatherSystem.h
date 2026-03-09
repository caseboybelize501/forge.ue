// ============================================================================
// WeatherSystem.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T051
// Purpose: Dynamic weather transitions
// FR Mapping: FR-12
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WolverineCoreTypes.h"
#include "WeatherSystem.generated.h"

// TODO (T051.1): Define AWeatherSystem class (AActor)
// TODO (T051.2): Declare CurrentWeather (EWeatherState)
// TODO (T051.3): Declare TransitionWeather(EWeatherState, float Duration) function
// TODO (T051.4): Declare NiagaraParticle references

UCLASS()
class WOLVERINE_API AWeatherSystem : public AActor
{
    GENERATED_BODY()

public:
    AWeatherSystem();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement dynamic weather transitions
};
