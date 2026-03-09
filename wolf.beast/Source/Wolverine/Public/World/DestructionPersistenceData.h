// ============================================================================
// DestructionPersistenceData.h
// ============================================================================
// Build Level: L4 (AI + World)
// Task Ref: T053
// Purpose: Destruction records (survives save/load)
// FR Mapping: FR-13
// HR Mapping: HR-05 (persistent destruction)
// NFR Mapping: NFR-06 (save/load cycle)
// Dependencies: T001, T007
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "WolverineDataStructures.h"
#include "DestructionPersistenceData.generated.h"

// TODO (T053.1): Define UDestructionPersistenceData class (UDataAsset)
// TODO (T053.2): Declare DestructionRecords map (GUID → FDestructionRecord) - HR-05
// TODO (T053.3): Declare AddRecord(FDestructionRecord) function
// TODO (T053.4): Declare GetRecord(FGuid) function - O(1) lookup

UCLASS()
class WOLVERINE_API UDestructionPersistenceData : public UDataAsset
{
    GENERATED_BODY()

public:
    UDestructionPersistenceData();

public:
    // TODO: Implement destruction record storage (GUID-based)
};
