// IForgeOnlineSubsystem.h — Level 0 Foundation
// Online/multiplayer interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IForgeOnlineSubsystem.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeOnlineSubsystem : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeOnlineSubsystem Interface
 * 
 * Interface for online subsystem integration including EOS, Steam,
 * and platform-specific online services.
 */
class FORGE_API IIForgeOnlineSubsystem
{
    GENERATED_BODY()

public:
    /** Initialize online subsystem */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    bool Initialize();

    /** Shutdown online subsystem */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    void Shutdown();

    /** Check if online subsystem is available */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    bool IsAvailable() const;

    /** Get local player unique net ID */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    FUniqueNetIdRepl GetLocalPlayerNetId() const;

    /** Get local player name */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    FString GetLocalPlayerName() const;

    /** Create online session */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    void CreateSession(int32 MaxPlayers, bool bIsLAN);

    /** Destroy online session */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    void DestroySession();

    /** Find online sessions */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    void FindSessions(bool bIsLAN);

    /** Join online session */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    void JoinSession(const FOnlineSessionSearchResult& SearchResult);

    /** Get session state */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    FString GetSessionState() const;

    /** Get number of connected players */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Online")
    int32 GetNumConnectedPlayers() const;
};
