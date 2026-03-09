"""
CPP Generator — Level 4 Engine Module

Generate C++ .h + .cpp files from ModuleSpec.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.code_artifact (L0-003)
- templates/interfaces/*.h (L0-009 to L0-018)
- engine.project_scaffolder (L3-001)
"""
from typing import List, Dict, Optional
from pathlib import Path
import re

from contracts.models.game_brief import GameBrief, Genre
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.code_artifact import CppFile, HeaderFile
from engine.project_scaffolder import ProjectScaffolder


class CppGenerator:
    """
    C++ Code Generator for FORGE pipeline.

    Generates UE5 C++ source files:
    - UCLASS headers with proper macros
    - Implementation .cpp files
    - Follows UE5 coding standards
    - Implements interface headers

    Attributes:
        scaffolder: Project scaffolder reference
        interface_headers: Loaded interface headers
    """

    # UE5 coding standard templates
    HEADER_TEMPLATE = """#pragma once

#include "CoreMinimal.h"
{includes}
#include "{class_name}.generated.h"

UCLASS({class_flags})
class {module_name}_API A{class_name} : public A{parent_class}
{{
    GENERATED_BODY()

{properties}

{functions}
}};
"""

    # CPP implementation template
    CPP_TEMPLATE = """#include "{class_name}.h"

{constructor}

{implementations}
"""

    # Default constructor template
    CONSTRUCTOR_TEMPLATE = """
A{class_name}::A{class_name}()
{{
    // Set default values
    PrimaryActorTick.bCanEverTick = {can_tick};
}}
"""

    def __init__(self, scaffolder: Optional['ProjectScaffolder'] = None):
        """
        Initialize C++ generator.

        Args:
            scaffolder: Project scaffolder reference
        """
        self.scaffolder = scaffolder
        self.interface_headers: Dict[str, HeaderFile] = {}
        self._load_interface_headers()

    def generate_module(self, module: ModuleSpec) -> List[CppFile]:
        """
        Generate all C++ files for a module.

        Args:
            module: Module specification

        Returns:
            List of generated C++ files
        """
        files = []

        # Generate header file
        header = self._generate_header(module)
        files.append(header)

        # Generate cpp file
        cpp = self._generate_cpp(module, header)
        files.append(cpp)

        return files

    def generate_from_spec(self, spec: ProjectSpec) -> List[CppFile]:
        """
        Generate all C++ files from project spec.

        Args:
            spec: Project specification

        Returns:
            List of all generated C++ files
        """
        all_files = []

        for module in spec.modules:
            module_files = self.generate_module(module)
            all_files.extend(module_files)

        return all_files

    def _generate_header(self, module: ModuleSpec, class_name: Optional[str] = None) -> HeaderFile:
        """
        Generate UCLASS header file.

        Args:
            module: Module specification
            class_name: Optional class name (defaults to module name)

        Returns:
            Generated header file
        """
        if class_name is None:
            class_name = module.module_name

        # Determine parent class based on module type
        parent_class = self._get_parent_class(module)

        # Generate includes
        includes = self._generate_includes(module.dependencies)

        # Generate properties
        properties = self._generate_properties(module)

        # Generate functions
        functions = self._generate_functions(module)

        # Build class flags
        class_flags = self._get_class_flags(module)

        # Render template
        header_content = self.HEADER_TEMPLATE.format(
            includes=includes,
            class_name=class_name,
            module_name=module.module_name,
            class_flags=class_flags,
            parent_class=parent_class,
            properties=properties,
            functions=functions
        )

        return HeaderFile(
            path=f"Source/{module.module_name}/{class_name}.h",
            content=header_content,
            module=module.module_name,
            node_id=f"header_{class_name}",
            node_type="header"
        )

    def _generate_cpp(self, module: ModuleSpec, header: HeaderFile) -> CppFile:
        """
        Generate implementation .cpp file.

        Args:
            module: Module specification
            header: Corresponding header file

        Returns:
            Generated cpp file
        """
        class_name = header.node_id.replace("header_", "")

        # Generate constructor
        can_tick = "true" if module.module_type.value in ["GameFramework", "GenreSystem"] else "false"
        constructor = self.CONSTRUCTOR_TEMPLATE.format(
            class_name=class_name,
            can_tick=can_tick
        )

        # Generate function implementations
        implementations = self._generate_implementations(module)

        # Render template
        cpp_content = self.CPP_TEMPLATE.format(
            class_name=class_name,
            constructor=constructor,
            implementations=implementations
        )

        return CppFile(
            path=f"Source/{module.module_name}/{class_name}.cpp",
            content=cpp_content,
            module=module.module_name,
            node_id=f"cpp_{class_name}",
            node_type="cpp"
        )

    def _load_interface_headers(self) -> Dict[str, HeaderFile]:
        """
        Load immutable interface headers from templates/.

        Returns:
            Dictionary of interface headers
        """
        if self.scaffolder is None:
            return self.interface_headers

        templates_dir = Path("templates/interfaces")
        if not templates_dir.exists():
            return self.interface_headers

        for header_file in templates_dir.glob("*.h"):
            try:
                with open(header_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.interface_headers[header_file.stem] = HeaderFile(
                        path=str(header_file),
                        content=content,
                        module="Interfaces",
                        node_id=header_file.stem,
                        node_type="interface_header",
                        is_interface=True
                    )
            except (IOError, OSError):
                continue

        return self.interface_headers

    def _generate_includes(self, dependencies: List[str]) -> str:
        """
        Generate #include statements.

        Args:
            dependencies: List of header dependencies

        Returns:
            Formatted include statements
        """
        if not dependencies:
            return ""

        includes = []
        for dep in dependencies:
            # Sanitize dependency name for include path
            dep_clean = re.sub(r'[^a-zA-Z0-9_]', '', dep)
            includes.append(f'#include "{dep_clean}.h"')

        return "\n".join(includes)

    def _get_parent_class(self, module: ModuleSpec) -> str:
        """
        Get parent class based on module type.

        Args:
            module: Module specification

        Returns:
            Parent class name
        """
        parent_map = {
            "Core": "Actor",
            "GameFramework": "GameModeBase",
            "GenreSystem": "Actor",
            "UI": "UserWidget",
            "Platform": "Actor",
        }
        return parent_map.get(module.module_type.value, "Actor")

    def _get_class_flags(self, module: ModuleSpec) -> str:
        """
        Get UCLASS decorator flags.

        Args:
            module: Module specification

        Returns:
            Class flags string
        """
        flags = []

        # Add blueprint spawnable flag for game-related modules
        if module.module_type.value in ["GameFramework", "GenreSystem"]:
            flags.append("Blueprintable")
            flags.append("BlueprintType")

        # Add not placeable for non-actor classes
        if module.module_type.value == "Core":
            flags.append("NotPlaceable")

        return ", ".join(flags) if flags else "Blueprintable"

    def _generate_properties(self, module: ModuleSpec) -> str:
        """
        Generate UPROPERTY declarations.

        Args:
            module: Module specification

        Returns:
            Formatted property declarations
        """
        properties = []

        # Add default properties based on module type
        if module.module_type.value in ["GameFramework", "GenreSystem"]:
            properties.append("""    // Default properties
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Health = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 MaxHealth = 100;""")

        if module.module_type.value == "UI":
            properties.append("""    // UI Properties
    UPROPERTY(BlueprintReadWrite, meta = (BindWidget))
    class UButton* ActionButton;

    UPROPERTY(BlueprintReadWrite, meta = (BindWidget))
    class UTextBlock* StatusText;""")

        return "\n\n".join(properties) if properties else "    // Add properties here"

    def _generate_functions(self, module: ModuleSpec) -> str:
        """
        Generate UFUNCTION declarations.

        Args:
            module: Module specification

        Returns:
            Formatted function declarations
        """
        functions = []

        # Add default functions based on module type
        if module.module_type.value in ["GameFramework", "GenreSystem"]:
            functions.append("""    // Called when the game starts or when spawned
    UFUNCTION(BlueprintCallable, Category = "Game")
    virtual void BeginPlay();

    // Called every frame
    UFUNCTION(BlueprintCallable, Category = "Game")
    virtual void Tick(float DeltaTime);

    // Take damage function
    UFUNCTION(BlueprintCallable, Category = "Combat")
    virtual void TakeDamage(int32 DamageAmount);""")

        if module.module_type.value == "UI":
            functions.append("""    // Button click handler
    UFUNCTION()
    void OnActionButtonClicked();

    // Update status text
    UFUNCTION(BlueprintCallable, Category = "UI")
    void UpdateStatus(const FString& NewStatus);""")

        return "\n\n".join(functions) if functions else "    // Add functions here"

    def _generate_implementations(self, module: ModuleSpec) -> str:
        """
        Generate function implementations.

        Args:
            module: Module specification

        Returns:
            Formatted function implementations
        """
        implementations = []

        if module.module_type.value in ["GameFramework", "GenreSystem"]:
            implementations.append("""void A{class_name}::BeginPlay()
{{
    Super::BeginPlay();

    // Initialization code
}}

void A{class_name}::Tick(float DeltaTime)
{{
    Super::Tick(DeltaTime);

    // Tick logic
}}

void A{class_name}::TakeDamage(int32 DamageAmount)
{{
    Health = FMath::Clamp(Health - DamageAmount, 0, MaxHealth);

    if (Health <= 0)
    {{
        // Handle death
    }}
}}""".format(class_name=module.module_name))

        if module.module_type.value == "UI":
            implementations.append("""void U{class_name}::OnActionButtonClicked()
{{
    // Button click handler
}}

void U{class_name}::UpdateStatus(const FString& NewStatus)
{{
    if (StatusText)
    {{
        StatusText->SetText(FText::FromString(NewStatus));
    }}
}}""".format(class_name=module.module_name))

        return "\n\n".join(implementations) if implementations else "// Add implementations here"

    def validate_generated_code(self, files: List[CppFile]) -> List[str]:
        """
        Validate generated C++ code for UE5 compliance.

        Args:
            files: List of generated files

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        for file in files:
            content = file.content

            # Check for GENERATED_BODY() in headers
            if file.node_type == "header":
                if "GENERATED_BODY()" not in content:
                    errors.append(f"{file.path}: Missing GENERATED_BODY() macro")

                # Check for UCLASS macro
                if "UCLASS(" not in content:
                    errors.append(f"{file.path}: Missing UCLASS macro")

            # Check for proper includes
            if file.node_type == "cpp":
                header_name = file.path.replace(".cpp", ".h")
                if f'#include "{header_name}"' not in content and header_name not in content:
                    # More lenient check
                    if not any(header_name.split("/")[-1] in line for line in content.split("\n")):
                        errors.append(f"{file.path}: Missing header include")

        return errors
