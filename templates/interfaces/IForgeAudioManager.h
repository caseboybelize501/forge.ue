// IForgeAudioManager.h — Level 0 Foundation
// Audio system interface
// Immutable after Step 0 human review

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "IForgeAudioManager.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UIForgeAudioManager : public UInterface
{
    GENERATED_BODY()
};

/**
 * IForgeAudioManager Interface
 * 
 * Interface for audio playback, music control, and SFX management.
 */
class FORGE_API IIForgeAudioManager
{
    GENERATED_BODY()

public:
    /** Play sound effect */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void PlaySFX(class USoundBase* Sound, float VolumeMultiplier = 1.0f);

    /** Stop all sound effects */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void StopAllSFX();

    /** Play background music */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void PlayMusic(class USoundBase* Music, bool bLoop = true);

    /** Stop background music */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void StopMusic();

    /** Fade music in/out */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void FadeMusic(float TargetVolume, float Duration);

    /** Set master volume */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void SetMasterVolume(float Volume);

    /** Set SFX volume */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void SetSFXVolume(float Volume);

    /** Set music volume */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void SetMusicVolume(float Volume);

    /** Pause all audio */
    UFUNCTION(BlueprintNativeEvent, Category = "Forge|Audio")
    void PauseAllAudio(bool bPaused);
};
