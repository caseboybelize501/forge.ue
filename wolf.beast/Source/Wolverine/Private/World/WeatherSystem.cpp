// ============================================================================
// WeatherSystem.cpp
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T052
// Purpose: Weather state machine, Niagara particles
// FR Mapping: FR-12
// Dependencies: T051
// ============================================================================
#include "World/WeatherSystem.h"

// TODO (T052.1): Implement TransitionWeather (lerp parameters)
// TODO (T052.2): Implement Niagara particle activation
// TODO (T052.3): Add weather state machine

AWeatherSystem::AWeatherSystem()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AWeatherSystem::BeginPlay()
{
    Super::BeginPlay();
}
