// ============================================================================
// SafeHouse.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T061
// Purpose: Safe house location (4 total)
// FR Mapping: FR-16
// Dependencies: T001
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SafeHouse.generated.h"

// TODO (T061.1): Define ASafeHouse class (AActor)
// TODO (T061.2): Declare SafeHouseID (int, 1-4)
// TODO (T061.3): Declare JournalEntry (FText) - Layer 3 content slot
// TODO (T061.4): Declare OnEnterSafeHouse delegate - FR-16

UCLASS()
class WOLVERINE_API ASafeHouse : public AActor
{
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement safe house trigger (heal player, show journal)
};
