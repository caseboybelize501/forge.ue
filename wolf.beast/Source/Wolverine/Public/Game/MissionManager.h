// ============================================================================
// MissionManager.h
// ============================================================================
// Build Level: L5 (Game Flow)
// Task Ref: T083
// Purpose: Mission state machine
// FR Mapping: FR-17
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "MissionManager.generated.h"

// TODO (T083.1): Define UMissionManager class (UActorComponent)
// TODO (T083.2): Declare CurrentMission (string)
// TODO (T083.3): Declare MissionState enum
// TODO (T083.4): Declare CompleteMission() function

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UMissionManager : public UActorComponent
{
    GENERATED_BODY()

public:
    UMissionManager();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement mission state machine
};
