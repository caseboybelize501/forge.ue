// IForgeUIManager.h — Level 0 Foundation
// HUD and widget manager interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IForgeUIManager.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeUIManager : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeUIManager Interface
 * 
 * Interface for HUD management, widget spawning, and UI state control.
 */
class FORGE_API IIForgeUIManager
{
    GENERATED_BODY()

public:
    /** Show HUD */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    void ShowHUD();

    /** Hide HUD */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    void HideHUD();

    /** Toggle HUD visibility */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    void ToggleHUD();

    /** Open widget by class */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    class UUserWidget* OpenWidget(TSubclassOf<class UUserWidget> WidgetClass);

    /** Close widget by class */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    void CloseWidget(TSubclassOf<class UUserWidget> WidgetClass);

    /** Get active widget */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    class UUserWidget* GetWidget(TSubclassOf<class UUserWidget> WidgetClass) const;

    /** Set UI enabled state */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    void SetUIEnabled(bool bEnabled);

    /** Check if UI is enabled */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|UI")
    bool IsUIEnabled() const;
};
