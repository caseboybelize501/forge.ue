// ============================================================================
// WolverineMaterialResponseSystem.h
// ============================================================================
// Build Level: L1 (Systems)
// Task Ref: T009
// Purpose: Material detection system from hit results
// FR Mapping: FR-07
// HR Mapping: HR-06 (6 material types)
// Dependencies: T001, T003
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWolverineMaterialResponse.h"
#include "WolverineMaterialResponseSystem.generated.h"

// TODO (T009.1): Define UWolverineMaterialResponseSystem class (UObject)
// TODO (T009.2): Declare SurfaceMaterialMap (UPROPERTY)
// TODO (T009.3): Declare GetMaterialFromHit(FHitResult) function
// TODO (T009.4): Declare GetMaterialFromSurface(UPhysicalMaterial) function

UCLASS(ClassGroup=(Wolverine), meta=(BlueprintSpawnableComponent))
class WOLVERINE_API UWolverineMaterialResponseSystem : public UActorComponent, public IWolverineMaterialResponse
{
    GENERATED_BODY()

public:
    UWolverineMaterialResponseSystem();

protected:
    virtual void BeginPlay() override;

public:
    // TODO: Implement IWolverineMaterialResponse interface
    // TODO: Implement material detection from hit results
};
