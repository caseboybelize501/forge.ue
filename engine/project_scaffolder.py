"""
Project Scaffolder — Level 3 Engine Module

Create UE5 project folder structure + configs.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.code_artifact (L0-003)
- templates/interfaces/*.h (L0-009 to L0-018)
- engine.brief_parser (L2-004)
"""
from typing import List, Dict, Optional
from pathlib import Path
import shutil
import json
import re

from contracts.models.game_brief import GameBrief, Platform
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.code_artifact import HeaderFile


class ProjectScaffolder:
    """
    UE5 Project Scaffolder.

    Creates complete project directory structure:
    - Source/ with module folders
    - Content/ with Blueprint directories
    - Config/ with .ini files
    - .uproject descriptor
    - Build.cs and Target.cs files

    Attributes:
        output_base: Base output directory for projects
    """

    # Project folder structure template
    PROJECT_STRUCTURE = [
        'Source/{Project}',
        'Source/{Project}/Public',
        'Source/{Project}/Private',
        'Source/{Project}/Private/Core',
        'Source/{Project}/Private/Game',
        'Source/{Project}/Private/UI',
        'Content/Blueprints',
        'Content/Blueprints/Core',
        'Content/Blueprints/Game',
        'Content/Blueprints/UI',
        'Content/Materials',
        'Content/Maps',
        'Config',
    ]

    def __init__(self, output_base: Path):
        """
        Initialize project scaffolder.

        Args:
            output_base: Base directory for generated projects
        """
        self.output_base = output_base
        self.output_base.mkdir(parents=True, exist_ok=True)

    def scaffold_project(self, brief: GameBrief, spec: ProjectSpec) -> Path:
        """
        Create complete project directory structure.

        Args:
            brief: Game brief
            spec: Project specification

        Returns:
            Path to created project directory
        """
        # Sanitize project name for file system
        project_name = self._sanitize_name(spec.project_name)
        project_path = self.output_base / project_name

        # Remove existing directory if it exists
        if project_path.exists():
            shutil.rmtree(project_path)

        # Create directory structure
        self._create_directories(project_path, spec)

        # Generate .uproject file
        uproject_content = self._generate_uproject(spec)
        uproject_path = project_path / f"{project_name}.uproject"
        with open(uproject_path, 'w', encoding='utf-8') as f:
            f.write(uproject_content)

        # Generate Target.cs files
        target_cs_content = self._generate_target_cs(spec)
        target_cs_path = project_path / "Source" / project_name / f"{project_name}Target.cs"
        with open(target_cs_path, 'w', encoding='utf-8') as f:
            f.write(target_cs_content)

        # Generate Build.cs for each module
        for module in spec.modules:
            build_cs_content = self._generate_build_cs(module)
            module_name = self._sanitize_name(module.module_name)
            build_cs_path = project_path / "Source" / module_name / f"{module_name}.Build.cs"
            with open(build_cs_path, 'w', encoding='utf-8') as f:
                f.write(build_cs_content)

        # Generate .ini config files
        ini_configs = self._generate_ini_configs(spec)
        config_dir = project_path / "Config"
        config_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in ini_configs.items():
            config_path = config_dir / filename
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return project_path

    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize name for file system and UE5 conventions.

        Args:
            name: Original name

        Returns:
            Sanitized name (alphanumeric, no spaces)
        """
        # Remove special characters, replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '', name)
        # Ensure it starts with a letter
        if sanitized and sanitized[0].isdigit():
            sanitized = '_' + sanitized
        return sanitized or 'Untitled'

    def _generate_uproject(self, spec: ProjectSpec) -> str:
        """
        Generate .uproject descriptor file.

        Args:
            spec: Project specification

        Returns:
            .uproject file content
        """
        project_name = self._sanitize_name(spec.project_name)

        # Build modules array
        modules_json = []
        for module in spec.modules:
            module_name = self._sanitize_name(module.module_name)
            modules_json.append(f'        {{\n            "Name": "{module_name}",\n            "Type": "Runtime",\n            "LoadingPhase": "Default"\n        }}')

        # Build plugins array based on platform targets
        plugins = []
        if any(p in spec.platform_targets for p in ['Android', 'iOS']):
            plugins.append('        { "Name": "MobilePatching", "Enabled": true }')

        uproject = {
            "FileVersion": 3,
            "EngineAssociation": "5.3",
            "Category": "",
            "Description": f"Generated FORGE project: {spec.project_name}",
            "Modules": [
                {
                    "Name": self._sanitize_name(m.module_name),
                    "Type": "Runtime",
                    "LoadingPhase": "Default"
                } for m in spec.modules
            ],
            "Plugins": []
        }

        return json.dumps(uproject, indent=4)

    def _generate_build_cs(self, module: ModuleSpec) -> str:
        """
        Generate Build.cs module file.

        Args:
            module: Module specification

        Returns:
            Build.cs file content
        """
        module_name = self._sanitize_name(module.module_name)

        # Core dependencies for all modules
        public_deps = ['Core', 'CoreUObject', 'Engine', 'InputCore']

        # Add additional dependencies based on module type
        private_deps = []

        # Add module dependencies
        for dep in module.dependencies:
            dep_name = self._sanitize_name(dep)
            if dep_name != module_name:
                private_deps.append(dep_name)

        # Build private dependencies string
        private_deps_str = ',\n            '.join([f'"{dep}"' for dep in private_deps]) if private_deps else ''

        # Platform guards
        platform_guards = []
        if module.platform_guards:
            for platform in module.platform_guards:
                platform_guards.append(f'#if PLATFORM_{platform}')
                platform_guards.append(f'    // Platform-specific code for {platform}')
                platform_guards.append('#endif')

        build_cs = f"""using UnrealBuildTool;

public class {module_name} : ModuleRules
{{
    public {module_name}(ReadOnlyTargetRules Target) : base(Target)
    {{
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[] {{
            {', '.join([f'"{dep}"' for dep in public_deps])}
        }});

        PrivateDependencyModuleNames.AddRange(new string[] {{
            {private_deps_str if private_deps_str else '// No private dependencies'}
        }});

        // Uncomment if module uses Slate/SlateCore
        // PublicDependencyModuleNames.AddRange(new string[] {{ "Slate", "SlateCore" }});

        {chr(10).join(platform_guards) if platform_guards else '// No platform guards'}
    }}
}}
"""
        return build_cs

    def _generate_target_cs(self, spec: ProjectSpec) -> str:
        """
        Generate Target.cs file.

        Args:
            spec: Project specification

        Returns:
            Target.cs file content
        """
        project_name = self._sanitize_name(spec.project_name)

        target_cs = f"""using UnrealBuildTool;
using System.Collections.Generic;
using System.IO;

public class {project_name}Target : TargetRules
{{
    public {project_name}Target(TargetInfo Target) : base(Target)
    {{
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V4;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_3;
        ExtraModuleNames.Add("{project_name}");
    }}
}}
"""
        return target_cs

    def _generate_ini_configs(self, spec: ProjectSpec) -> Dict[str, str]:
        """
        Generate platform .ini configuration files.

        Args:
            spec: Project specification

        Returns:
            Dictionary of config filename → content
        """
        project_name = self._sanitize_name(spec.project_name)
        project_name_lower = project_name.lower()

        configs = {}

        # DefaultEngine.ini
        default_engine = f"""[/Script/EngineSettings.GameMapsSettings]
GameDefaultMap=/Game/Maps/MainMap.MainMap
EditorStartupMap=/Game/Maps/MainMap.MainMap
GlobalDefaultGameMode=/Script/{project_name}.{project_name}GameMode
GlobalDefaultServerGameMode=/Script/{project_name}.{project_name}GameMode

[/Script/Engine.RendererSettings]
r.Mobile.ShadingPath=0
r.Mobile.AllowDeferredShadingOpenGL=False
r.Mobile.SupportGPUScene=True
r.Mobile.AntiAliasing=1
r.Mobile.FloatPrecisionMode=0
r.Mobile.AllowDitheredLODTransition=False
r.Mobile.VirtualTextures=False
r.DiscardUnusedQuality=False
r.AllowOcclusionQueries=True
r.MinScreenRadiusForLights=0.030000
r.MinScreenRadiusForDepthPrepass=0.030000
r.PrecomputedVisibilityWarning=False
r.TextureStreaming=True
Compat.UseDXT5NormalMaps=False
r.AllowStaticLighting=True
r.NormalMapsForStaticLighting=False
r.GBuffer=False
r.GenerateMeshDistanceFields=True
r.Deferred.SupportGlobalLightFunction=False
r.Shadow.DistanceFieldPenumbraSize=0.050000
r.TessellationAdaptivePixelsPerTriangle=48.000000
r.SeparateTranslucency=True
r.TranslucentSortPolicy=0
TranslucentSortAxis=(X=0.000000,Y=-1.000000,Z=0.000000)
r.CustomDepth=1
r.CustomDepthTemporalAAJitter=True
r.PostProcessing.PropagateAlpha=False
r.DefaultFeature.Bloom=True
r.DefaultFeature.AmbientOcclusion=True
r.DefaultFeature.AmbientOcclusionStaticFraction=True
r.DefaultFeature.AutoExposure=False
r.DefaultFeature.AutoExposure.Method=0
r.DefaultFeature.AutoExposure.Bias=1.000000
r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange=False
r.DefaultFeature.MotionBlur=False
r.DefaultFeature.LensFlare=False
r.TemporalAA.Upsampling=True
r.AntiAliasingMethod=0
r.MSAACount=4
r.DefaultFeature.LightUnits=1
r.DefaultBackBufferPixelFormat=4
r.Shadow.UnbuiltPreviewInGame=True
r.StencilForLODDither=False
r.EarlyZPass=3
r.EarlyZPassOnlyMaterialMasking=False
r.DBuffer=True
r.ClearSceneMethod=1
r.VelocityOutputPass=1
r.Velocity.EnableVertexDeformation=2
r.SelectiveBasePassOutputs=False
bDefaultParticleCutouts=False
fx.GPUSimulationTextureSizeX=1024
fx.GPUSimulationTextureSizeY=1024
r.AllowGlobalClipPlane=False
r.GBufferFormat=1
r.MorphTarget.Mode=True
r.GPUCrashDebugging=False
vr.InstancedStereo=False
r.MobileHDR=True
vr.MobileMultiView=False
r.Mobile.UseHWsRGBEncoding=False
vr.RoundRobinOcclusion=False
r.MeshStreaming=False
r.HeterogeneousVolumes=True
r.WireframeCullThreshold=5.000000
r.SupportStationarySkylight=True
r.SupportLowQualityLightmaps=True
r.SupportPointLightWholeSceneShadows=True
r.SupportSkyAtmosphere=True
r.SupportSkyAtmosphereAffectsHeightFog=True
r.SupportExpFogMatchesVolumetricFog=False
r.SupportLocalFogVolumes=True
r.SupportAtmosphericFog=True
r.SkinCache.CompileShaders=False
r.Mobile.EnableMovableLightCSMShaderCulling=True
r.Mobile.Forward.EnableLocalLights=True
r.Mobile.Forward.EnableClusteredReflections=False
r.Mobile.AllowDistanceFieldShadows=True
r.Mobile.EnableMovableSpotlightsShadow=False
r.GPUResidentShader.Enable=False
r.Nanite.ProjectEnabled=False
r.RayTracing=False
r.Lumen.ProjectEnabled=False
r.VirtualTextures=False

[/Script/WindowsTargetPlatform.WindowsTargetSettings]
DefaultGraphicsRHI=DefaultGraphicsRHI_DX12
-D3D12TargetedShaderFormats=PCD3D_SM5
+D3D12TargetedShaderFormats=PCD3D_SM6
-D3D11TargetedShaderFormats=PCD3D_SM5
+D3D11TargetedShaderFormats=PCD3D_SM5
Compiler=Default
AudioSampleRate=48000
AudioCallbackBufferFrameSize=1024
AudioNumBuffersToEnqueue=1
AudioMaxChannels=0
AudioNumSourceWorkers=4
SpatializationPlugin=
SourceDataOverridePlugin=
ReverbPlugin=
OcclusionPlugin=
CompressionOverrides=(bOverrideCompressionTimes=False,DurationThreshold=5.000000,MaxNumRandomBranches=0,SoundCueQualityIndex=0,CacheSizeKB=65536,MaxChunkSizeOverrideKB=0)
bUseAudioStreamCaching=False
CacheSizeKB=32768
MaxChunkSizeOverrideKB=0
bResampleForDevice=False
MaxSampleRate=48000.000000
HighSampleRate=32000.000000
MedSampleRate=24000.000000
LowSampleRate=12000.000000
MinSampleRate=8000.000000
CompressionQualityModifier=1.000000
AutoStreamingThreshold=0.000000
SoundCueCookQualityIndex=-1
"""
        configs['DefaultEngine.ini'] = default_engine

        # DefaultGame.ini
        default_game = f"""[/Script/EngineSettings.GeneralProjectSettings]
ProjectID={self._generate_project_id()}
ProjectName={spec.project_name}
CompanyName=FORGE Generated
CompanyDistinguishedName=FORGE
Homepage=
Description=Generated using FORGE pipeline
"""
        configs['DefaultGame.ini'] = default_game

        # DefaultInput.ini (minimal)
        default_input = """[/Script/Engine.InputSettings]
bEnableLegacyInputSensitivity=False
DefaultPlayerInputClass=/Script/EnhancedInput.EnhancedPlayerInput
DefaultInputComponentClass=/Script/EnhancedInput.EnhancedInputComponent
"""
        configs['DefaultInput.ini'] = default_input

        return configs

    def _generate_project_id(self) -> str:
        """
        Generate a unique project ID.

        Returns:
            UUID-like string
        """
        import uuid
        return str(uuid.uuid4()).upper()

    def _create_directories(self, project_path: Path, spec: ProjectSpec) -> None:
        """
        Create project directory structure.

        Args:
            project_path: Project root path
            spec: Project specification
        """
        project_name = self._sanitize_name(spec.project_name)

        # Create base structure
        for dir_template in self.PROJECT_STRUCTURE:
            dir_name = dir_template.replace('{Project}', project_name)
            full_path = project_path / dir_name
            full_path.mkdir(parents=True, exist_ok=True)

        # Create module-specific directories
        for module in spec.modules:
            module_name = self._sanitize_name(module.module_name)
            module_source = project_path / "Source" / module_name
            module_source.mkdir(parents=True, exist_ok=True)
            (module_source / "Public").mkdir(exist_ok=True)
            (module_source / "Private").mkdir(exist_ok=True)

    def validate_structure(self, project_path: Path) -> bool:
        """
        Validate created project structure.

        Args:
            project_path: Path to project directory

        Returns:
            True if structure is valid
        """
        # Check for .uproject file
        uproject_files = list(project_path.glob('*.uproject'))
        if not uproject_files:
            return False

        # Check for Source directory
        source_dir = project_path / "Source"
        if not source_dir.exists():
            return False

        # Check for Content directory
        content_dir = project_path / "Content"
        if not content_dir.exists():
            return False

        # Check for Config directory
        config_dir = project_path / "Config"
        if not config_dir.exists():
            return False

        return True

    def get_project_info(self, project_path: Path) -> Dict[str, str]:
        """
        Get project information from .uproject file.

        Args:
            project_path: Path to project directory

        Returns:
            Dictionary with project info
        """
        uproject_files = list(project_path.glob('*.uproject'))
        if not uproject_files:
            return {}

        try:
            with open(uproject_files[0], 'r', encoding='utf-8') as f:
                uproject = json.load(f)
            return {
                'name': uproject.get('Description', 'Unknown'),
                'engine': uproject.get('EngineAssociation', 'Unknown'),
                'modules': len(uproject.get('Modules', [])),
                'path': str(project_path)
            }
        except (json.JSONDecodeError, IOError):
            return {}
