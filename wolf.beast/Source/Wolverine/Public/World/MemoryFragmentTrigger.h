// ============================================================================
// MemoryFragmentTrigger.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T065
// Purpose: Trauma system memory trigger
// FR Mapping: FR-11
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WolverineDataStructures.h"
#include "MemoryFragmentTrigger.generated.h"

// TODO (T065.1): Define AMemoryFragmentTrigger class (AActor)
// TODO (T065.2): Declare MemoryData (FMemoryFragment) - Layer 3 content slot
// TODO (T065.3): Declare FlashbackLevel (string path)
// TODO (T065.4): Declare OnCollect delegate

UCLASS()
class WOLVERINE_API AMemoryFragmentTrigger : public AActor
{
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement memory trigger (unlock, start flashback)
};
