// IForgeInventory.h — Level 0 Foundation
// Inventory system interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IForgeInventory.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeInventory : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeInventory Interface
 * 
 * Standard inventory system interface for item management,
 * weight limits, and inventory UI integration.
 */
class FORGE_API IIForgeInventory
{
    GENERATED_BODY()

public:
    /** Add item to inventory */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    bool AddItem(class UForgeItemBase* Item, int32 Quantity);

    /** Remove item from inventory */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    bool RemoveItem(class UForgeItemBase* Item, int32 Quantity);

    /** Get item quantity */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    int32 GetItemQuantity(class UForgeItemBase* Item) const;

    /** Get total inventory weight */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    float GetTotalWeight() const;

    /** Get max inventory weight */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    float GetMaxWeight() const;

    /** Check if inventory is full */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    bool IsInventoryFull() const;

    /** Get all inventory items */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    TArray<class UForgeItemBase*> GetAllItems() const;

    /** Clear entire inventory */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Inventory")
    void ClearInventory();
};
