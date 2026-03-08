// IForgePlatformLayer.h — Level 0 Foundation
// Platform abstraction interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IForgePlatformLayer.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgePlatformLayer : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgePlatformLayer Interface
 * 
 * Platform abstraction layer for cross-platform compatibility.
 * All platform-specific code must go through this interface.
 */
class FORGE_API IIForgePlatformLayer
{
    GENERATED_BODY()

public:
    /** Get current platform name */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    FString GetPlatformName() const;

    /** Check if running on console */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    bool IsConsolePlatform() const;

    /** Get platform SDK version */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    FString GetSDKVersion() const;

    /** Get user language */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    FString GetUserLanguage() const;

    /** Get user country */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    FString GetUserCountry() const;

    /** Open external URL */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    void OpenExternalURL(const FString& URL);

    /** Copy text to clipboard */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    void CopyToClipboard(const FString& Text);

    /** Get clipboard text */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    FString GetFromClipboard() const;

    /** Trigger platform haptic feedback */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    void TriggerHaptic(float Intensity, float Duration);

    /** Get platform-specific save path */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Platform")
    FString GetSaveGamePath() const;
};
