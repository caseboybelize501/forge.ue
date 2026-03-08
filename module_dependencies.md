# FORGE — Module Dependencies Specification

## 1. OVERVIEW

This document specifies the **exact Python import statements** required for each module in the FORGE pipeline. Each module's dependencies are derived from Graph A in `dependency_graph.md`.

---

## 2. LEVEL 0 — CONTRACTS (No Dependencies)

### 2.1 contracts/models/game_brief.py
```python
# No internal dependencies — foundation module
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# External only: pydantic
```

### 2.2 contracts/models/project_spec.py
```python
# No internal dependencies — foundation module
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# External only: pydantic
```

### 2.3 contracts/models/code_artifact.py
```python
# No internal dependencies — foundation module
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# External only: pydantic
```

### 2.4 contracts/models/build_result.py
```python
# No internal dependencies — foundation module
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# External only: pydantic
```

### 2.5 contracts/models/agent_message.py
```python
# No internal dependencies — foundation module
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# External only: pydantic
```

### 2.6 contracts/models/platform_spec.py
```python
# No internal dependencies — foundation module
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# External only: pydantic
```

### 2.7 contracts/models/store_spec.py
```python
# No internal dependencies — foundation module
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# External only: pydantic
```

### 2.8 contracts/api.yaml
```yaml
# No dependencies — OpenAPI specification
openapi: 3.0.3
info:
  title: FORGE API
  version: 1.0.0
```

### 2.9 templates/interfaces/*.h (10 files)
```cpp
// No internal dependencies — UE5 interface headers
// External only: Unreal Engine headers
#pragma once
#include "CoreMinimal.h"
#include "UObject/Interface.h"
// ... UE5 includes only
```

---

## 3. LEVEL 1 — CORE AGENTS + SCANNERS

### 3.1 ai/architect_agent.py
```python
"""
Level 1 — Depends on: C0, C1, C8-C17
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief, Genre, Platform, MechanicSpec
from contracts.models.project_spec import (
    ProjectSpec,
    ModuleSpec,
    SubsystemRef,
    ModuleType,
)
from contracts.models.code_artifact import HeaderFile
from contracts.models.agent_message import AgentTask, AgentResult

# External dependencies
from typing import List, Dict, Optional
from pathlib import Path


class ArchitectAgent:
    """Transforms GameBrief → ProjectSpec + UBT Module Graph."""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.interface_headers = self._load_interface_headers()
    
    def design_architecture(self, brief: GameBrief) -> ProjectSpec:
        """Generate full project architecture from game brief."""
        pass
    
    def _load_interface_headers(self) -> Dict[str, HeaderFile]:
        """Load immutable interface headers from templates/."""
        pass
```

### 3.2 ai/test_agent.py
```python
"""
Level 1 — Depends on: C0, C3
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult, TestSpec

# External dependencies
from typing import List, Dict
from pathlib import Path


class TestAgent:
    """Generates test specifications per generated system."""
    
    def generate_test_specs(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """Create test specs for all systems in project."""
        pass
```

### 3.3 ai/repair_loop.py
```python
"""
Level 1 — Depends on: C0, C3
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, ErrorReport, RepairContext

# External dependencies
from typing import List, Optional, Dict
from pathlib import Path


class RepairLoop:
    """Parse UBT/UHT errors → Targeted file repair → Recompile."""
    
    MAX_REPAIR_ATTEMPTS = 3
    
    def repair_file(self, context: RepairContext) -> Optional[str]:
        """Attempt to repair a failing file."""
        pass
    
    def classify_error(self, error_text: str) -> str:
        """Classify UE5 build error type."""
        pass
```

### 3.4 engine/ue5_scanner.py
```python
"""
Level 1 — Depends on: C0
"""
# Internal dependencies
from contracts.models.game_brief import Platform

# External dependencies
from typing import Dict, Optional, List
from pathlib import Path
import subprocess
import re


class UE5Scanner:
    """Scan UE5 install, verify version, detect platform SDKs."""
    
    MIN_UE5_VERSION = (5, 3)
    
    def __init__(self):
        self.ue_root: Optional[Path] = None
        self.ue_version: Optional[tuple] = None
        self.platform_sdks: Dict[str, Path] = {}
    
    def scan_ue5_install(self) -> bool:
        """Find and verify UE5 installation."""
        pass
    
    def detect_platform_sdks(self) -> Dict[str, bool]:
        """Detect available platform SDKs."""
        pass
```

### 3.5 engine/learning_store.py
```python
"""
Level 1 — Depends on: C0, C1
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief, Genre
from contracts.models.project_spec import ProjectSpec, ModuleSpec, Pattern

# External dependencies
from typing import Dict, List, Optional
from pathlib import Path
import json


class LearningStore:
    """Pattern library per genre + subsystem."""
    
    def __init__(self, store_path: Path):
        self.store_path = store_path
        self.patterns: Dict[str, Pattern] = {}
    
    def store_pattern(self, genre: Genre, system: str, pattern: Pattern) -> None:
        """Store pattern for future reuse."""
        pass
    
    def get_patterns(self, genre: Genre) -> List[Pattern]:
        """Retrieve patterns for genre."""
        pass
    
    def find_similar_project(self, brief: GameBrief) -> Optional[ProjectSpec]:
        """Find most similar past project."""
        pass
```

---

## 4. LEVEL 2 — TEST GENERATION + BRIEF PARSING

### 4.1 ai/test_generation/cpp_test_generator.py
```python
"""
Level 2 — Depends on: C0, C1, AI1
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.build_result import TestSpec, AssertionSpec
from ai.test_agent import TestAgent

# External dependencies
from typing import List, Dict
from pathlib import Path


class CppTestGenerator:
    """Generate UE5 Automation Tests (C++)."""
    
    def generate_test_file(self, test_spec: TestSpec) -> str:
        """Generate C++ test file content."""
        pass
    
    def _generate_assertion(self, assertion: AssertionSpec) -> str:
        """Generate single assertion code."""
        pass
```

### 4.2 ai/test_generation/blueprint_test_validator.py
```python
"""
Level 2 — Depends on: C0, C1, AI1
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TestSpec, ValidationResult
from ai.test_agent import TestAgent

# External dependencies
from typing import List, Dict
from pathlib import Path
import json


class BlueprintTestValidator:
    """Validate Blueprint JSON graphs."""
    
    def validate_blueprint(self, bp_json: Dict) -> ValidationResult:
        """Validate Blueprint graph structure."""
        pass
    
    def _check_node_connections(self, nodes: List[Dict]) -> List[str]:
        """Verify all node connections are valid."""
        pass
```

### 4.3 ai/test_generation/test_harness.py
```python
"""
Level 2 — Depends on: C0, C1, AI1
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TestSpec, TestResult
from ai.test_agent import TestAgent

# External dependencies
from typing import List, Dict
from pathlib import Path
import subprocess


class TestHarness:
    """Orchestrate UE5 test runner."""
    
    def run_tests(self, test_specs: List[TestSpec], project_path: Path) -> TestResult:
        """Execute all tests and aggregate results."""
        pass
    
    def _run_ue5_automation(self, project_path: Path) -> subprocess.CompletedProcess:
        """Run UE5 Automation Test runner."""
        pass
```

### 4.4 engine/brief_parser.py
```python
"""
Level 2 — Depends on: C0, C1, AI0
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief, Genre, Platform, MechanicSpec
from contracts.models.project_spec import ProjectSpec
from ai.architect_agent import ArchitectAgent

# External dependencies
from typing import Optional, Dict, Any
from pathlib import Path


class BriefParser:
    """Parse raw brief → GameBrief schema via LLM."""
    
    def __init__(self, architect: ArchitectAgent):
        self.architect = architect
    
    def parse_brief(self, raw_brief: str) -> GameBrief:
        """Extract structured GameBrief from raw text."""
        pass
    
    def validate_brief(self, brief: GameBrief) -> bool:
        """Validate brief completeness."""
        pass
```

---

## 5. LEVEL 3 — PROJECT SCAFFOLDING

### 5.1 engine/project_scaffolder.py
```python
"""
Level 3 — Depends on: C0, C1, C8-C17, E1
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief, Platform
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.code_artifact import HeaderFile
from engine.brief_parser import BriefParser

# External dependencies
from typing import List, Dict
from pathlib import Path
import shutil


class ProjectScaffolder:
    """Create UE5 project folder structure + configs."""
    
    def __init__(self, brief_parser: BriefParser):
        self.brief_parser = brief_parser
    
    def scaffold_project(self, brief: GameBrief, spec: ProjectSpec) -> Path:
        """Create complete project directory structure."""
        pass
    
    def _generate_uproject(self, spec: ProjectSpec) -> str:
        """Generate .uproject descriptor file."""
        pass
    
    def _generate_build_cs(self, module: ModuleSpec) -> str:
        """Generate Build.cs module file."""
        pass
    
    def _generate_target_cs(self, spec: ProjectSpec) -> str:
        """Generate Target.cs file."""
        pass
    
    def _generate_ini_configs(self, spec: ProjectSpec) -> Dict[str, str]:
        """Generate platform .ini configuration files."""
        pass
```

---

## 6. LEVEL 4 — CODE GENERATION

### 6.1 engine/cpp_generator.py
```python
"""
Level 4 — Depends on: C0, C1, C2, C8-C17, E2
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief, Genre
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.code_artifact import CppFile, HeaderFile
from engine.project_scaffolder import ProjectScaffolder

# External dependencies
from typing import List, Dict, Optional
from pathlib import Path


class CppGenerator:
    """Generate C++ .h + .cpp files from ModuleSpec."""
    
    def __init__(self, scaffolder: ProjectScaffolder):
        self.scaffolder = scaffolder
        self.interface_headers = self._load_interface_headers()
    
    def generate_module(self, module: ModuleSpec) -> List[CppFile]:
        """Generate all C++ files for a module."""
        pass
    
    def _generate_header(self, module: ModuleSpec, class_name: str) -> HeaderFile:
        """Generate UCLASS header file."""
        pass
    
    def _generate_cpp(self, module: ModuleSpec, header: HeaderFile) -> CppFile:
        """Generate implementation .cpp file."""
        pass
    
    def _load_interface_headers(self) -> Dict[str, HeaderFile]:
        """Load immutable interface headers from templates/."""
        pass
```

### 6.2 engine/blueprint_generator.py
```python
"""
Level 4 — Depends on: C0, C1, E2
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.code_artifact import BlueprintGraph
from engine.project_scaffolder import ProjectScaffolder

# External dependencies
from typing import List, Dict
from pathlib import Path
import json


class BlueprintGenerator:
    """Generate Blueprint graphs as structured JSON."""
    
    def __init__(self, scaffolder: ProjectScaffolder):
        self.scaffolder = scaffolder
    
    def generate_blueprint(self, spec: ProjectSpec, system: str) -> BlueprintGraph:
        """Generate Blueprint graph for system."""
        pass
    
    def _generate_node_graph(self, blueprint_type: str) -> Dict:
        """Generate node graph structure."""
        pass
```

### 6.3 engine/platform_guards.py
```python
"""
Level 4 — Depends on: C0, C5
"""
# Internal dependencies
from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget, SDKStatus

# External dependencies
from typing import List, Dict, Optional
from pathlib import Path
import re


class PlatformGuards:
    """Inject and validate platform guard macros."""
    
    PLATFORM_GUARDS = {
        "PS5": "#if PLATFORM_PS5",
        "XBOX": "#if PLATFORM_XBOXONE",
        "SWITCH": "#if PLATFORM_SWITCH",
        "ANDROID": "#if PLATFORM_ANDROID",
        "IOS": "#if PLATFORM_IOS",
    }
    
    def wrap_code(self, code: str, platform: Platform) -> str:
        """Wrap code in platform guard macros."""
        pass
    
    def validate_guards(self, file_content: str) -> List[str]:
        """Validate all platform-specific code is guarded."""
        pass
    
    def _check_guard_coverage(self, content: str, line_num: int) -> bool:
        """Check if line is covered by platform guard."""
        pass
```

---

## 7. LEVEL 5 — BUILD EXECUTION

### 7.1 engine/build_runner.py
```python
"""
Level 5 — Depends on: C0, C3, E3, AI1
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult, ErrorReport
from contracts.models.code_artifact import CppFile
from engine.cpp_generator import CppGenerator
from ai.test_agent import TestAgent

# External dependencies
from typing import List, Dict, Optional
from pathlib import Path
import subprocess
import re


class BuildRunner:
    """Invoke UHT → UBT, capture errors."""
    
    def __init__(self, cpp_generator: CppGenerator, test_agent: TestAgent):
        self.cpp_generator = cpp_generator
        self.test_agent = test_agent
    
    def run_uht(self, project_path: Path) -> CompileResult:
        """Run UnrealHeaderTool dry-run."""
        pass
    
    def run_ubt(self, project_path: Path, configuration: str = "Development") -> CompileResult:
        """Run UnrealBuildTool compile."""
        pass
    
    def parse_ubt_errors(self, stderr: str) -> List[ErrorReport]:
        """Parse UBT stderr into structured errors."""
        pass
    
    def run_tests(self, project_path: Path) -> TestResult:
        """Run UE5 Automation Tests."""
        pass
```

---

## 8. LEVEL 6 — PACKAGING + STORE

### 8.1 engine/package_agent.py
```python
"""
Level 6 — Depends on: C0, C5, E5
"""
# Internal dependencies
from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget, PackageConfig, SDKStatus
from contracts.models.build_result import CompileResult, PackageResult
from engine.build_runner import BuildRunner

# External dependencies
from typing import List, Dict, Optional
from pathlib import Path
import subprocess


class PackageAgent:
    """Cook + pak for each platform target."""
    
    def __init__(self, build_runner: BuildRunner):
        self.build_runner = build_runner
    
    def package_project(
        self,
        project_path: Path,
        platforms: List[PlatformTarget],
    ) -> PackageResult:
        """Package project for all target platforms."""
        pass
    
    def _cook_platform(self, project_path: Path, platform: PlatformTarget) -> bool:
        """Cook content for single platform."""
        pass
    
    def _pak_binaries(self, project_path: Path, platform: PlatformTarget) -> Path:
        """Create .pak file for platform."""
        pass
    
    def _validate_sdk(self, platform: PlatformTarget) -> bool:
        """Validate platform SDK availability."""
        pass
```

### 8.2 engine/store_agent.py
```python
"""
Level 6 — Depends on: C0, C6, E6
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.store_spec import StoreSubmission, StoreAssets, RatingConfig
from contracts.models.platform_spec import PackageResult
from engine.package_agent import PackageAgent

# External dependencies
from typing import List, Dict, Optional
from pathlib import Path
import json


class StoreAgent:
    """Generate Steam/EGS submission config + assets."""
    
    def __init__(self, package_agent: PackageAgent):
        self.package_agent = package_agent
    
    def generate_submission(
        self,
        brief: GameBrief,
        package_result: PackageResult,
    ) -> StoreSubmission:
        """Generate store submission package."""
        pass
    
    def _generate_steam_config(self, brief: GameBrief) -> Dict:
        """Generate Steamworks configuration."""
        pass
    
    def _generate_egs_config(self, brief: GameBrief) -> Dict:
        """Generate Epic Games Store configuration."""
        pass
    
    def _generate_rating_config(self, brief: GameBrief) -> RatingConfig:
        """Generate ESRB/PEGI rating configuration."""
        pass
```

---

## 9. LEVEL 7 — SERVER + DASHBOARD

### 9.1 server/api/projects.py
```python
"""
Level 7 — Depends on: C0, C1, C7, E1, E2
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief, GameBriefRequest
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import ProjectResponse
from engine.brief_parser import BriefParser
from engine.project_scaffolder import ProjectScaffolder

# External dependencies
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse)
async def create_project(brief: GameBriefRequest):
    """Create project from GameBrief."""
    pass


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get project details."""
    pass
```

### 9.2 server/api/architecture.py
```python
"""
Level 7 — Depends on: C0, C1, C7, AI0
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from ai.architect_agent import ArchitectAgent

# External dependencies
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/projects/{project_id}/architecture", tags=["architecture"])


@router.get("", response_model=ProjectSpec)
async def get_architecture(project_id: str):
    """Get architect plan for human review (GATE-1)."""
    pass
```

### 9.3 server/api/generation.py
```python
"""
Level 7 — Depends on: C0, C1, C7, E3, E4, E5
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TaskResponse, ProgressResponse, FileTreeResponse
from engine.cpp_generator import CppGenerator
from engine.blueprint_generator import BlueprintGenerator
from engine.build_runner import BuildRunner

# External dependencies
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional

router = APIRouter(prefix="/api/projects/{project_id}/generate", tags=["generation"])


@router.post("", response_model=TaskResponse)
async def trigger_generation(project_id: str, background_tasks: BackgroundTasks):
    """Trigger full generation pipeline."""
    pass


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(project_id: str):
    """Get topo level + critic status."""
    pass


@router.get("/files", response_model=FileTreeResponse)
async def get_file_tree(project_id: str):
    """Get generated file tree."""
    pass
```

### 9.4 server/api/builds.py
```python
"""
Level 7 — Depends on: C0, C3, C7, E5
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult, BuildStatusResponse
from engine.build_runner import BuildRunner

# External dependencies
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/projects/{project_id}/build", tags=["builds"])


@router.get("", response_model=BuildStatusResponse)
async def get_build_status(project_id: str):
    """Get compilation status."""
    pass
```

### 9.5 server/api/packages.py
```python
"""
Level 7 — Depends on: C0, C5, C7, E6
"""
# Internal dependencies
from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget, PackageResult
from contracts.models.build_result import TaskResponse
from engine.package_agent import PackageAgent

# External dependencies
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List

router = APIRouter(prefix="/api/projects/{project_id}/package", tags=["packages"])


@router.post("", response_model=TaskResponse)
async def trigger_packaging(project_id: str, platforms: List[str], background_tasks: BackgroundTasks):
    """Trigger platform packaging."""
    pass


@router.get("/{platform}", response_model=FileResponse)
async def download_package(project_id: str, platform: str):
    """Download packaged binary."""
    pass
```

### 9.6 server/api/store.py
```python
"""
Level 7 — Depends on: C0, C6, C7, E7
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.store_spec import StoreSubmission, StoreAssets
from engine.store_agent import StoreAgent

# External dependencies
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/projects/{project_id}/store", tags=["store"])


@router.get("", response_model=StoreSubmission)
async def get_store_submission(project_id: str):
    """Get store submission assets."""
    pass
```

### 9.7 server/api/auth.py
```python
"""
Level 7 — Depends on: C0, C7
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief

# External dependencies
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/token")
async def get_token(username: str, password: str):
    """Get JWT token."""
    pass


@router.post("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    pass
```

### 9.8 server/workers/generation_worker.py
```python
"""
Level 7 — Depends on: C0, C1, E1, E2, E3, E4
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from engine.brief_parser import BriefParser
from engine.project_scaffolder import ProjectScaffolder
from engine.cpp_generator import CppGenerator
from engine.blueprint_generator import BlueprintGenerator

# External dependencies
from celery import Celery, chain, chord, group
from pathlib import Path

app = Celery("forge", broker="redis://localhost:6379/0")


@app.task(bind=True, max_retries=3)
def run_generation_pipeline(self, project_id: str):
    """Execute full generation pipeline via Celery chain."""
    pass


@app.task
def generate_level_0(project_id: str):
    """Generate Level 0 files (contracts already exist)."""
    pass


@app.task
def generate_level_1(project_id: str):
    """Generate Level 1 files."""
    pass
```

### 9.9 server/workers/build_worker.py
```python
"""
Level 7 — Depends on: C0, C3, E5
"""
# Internal dependencies
from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult
from engine.build_runner import BuildRunner

# External dependencies
from celery import Celery
from pathlib import Path

app = Celery("forge", broker="redis://localhost:6379/0")


@app.task
def run_ubt_compile(project_id: str, configuration: str = "Development"):
    """Run UBT compile via Celery."""
    pass


@app.task
def run_tests(project_id: str):
    """Run UE5 Automation Tests."""
    pass
```

### 9.10 server/workers/package_worker.py
```python
"""
Level 7 — Depends on: C0, C5, E6
"""
# Internal dependencies
from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget, PackageResult
from engine.package_agent import PackageAgent

# External dependencies
from celery import Celery
from pathlib import Path

app = Celery("forge", broker="redis://localhost:6379/0")


@app.task
def package_platform(project_id: str, platform: str):
    """Package project for single platform."""
    pass
```

### 9.11 dashboard/src/pages/ProjectBrief.jsx
```jsx
/*
Level 7 — Depends on: C0, C7
*/
// Internal dependencies
// (References API spec from contracts/api.yaml)

// External dependencies
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

const ProjectBrief = () => {
    const { register, handleSubmit } = useForm();
    const [brief, setBrief] = useState('');
    
    const onSubmit = async (data) => {
        const response = await axios.post('/api/projects', { brief: data.brief });
        // Handle response
    };
    
    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            {/* Form fields */}
        </form>
    );
};

export default ProjectBrief;
```

### 9.12 dashboard/src/pages/GenerationProgress.jsx
```jsx
/*
Level 7 — Depends on: C0, C7
*/
// Internal dependencies
// (References API spec from contracts/api.yaml)

// External dependencies
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GenerationProgress = ({ projectId }) => {
    const [progress, setProgress] = useState(null);
    
    useEffect(() => {
        const fetchProgress = async () => {
            const response = await axios.get(`/api/projects/${projectId}/generate/progress`);
            setProgress(response.data);
        };
        fetchProgress();
    }, [projectId]);
    
    return (
        <div>
            {/* Progress display */}
        </div>
    );
};

export default GenerationProgress;
```

### 9.13 dashboard/src/pages/FileTree.jsx
```jsx
/*
Level 7 — Depends on: C0, C7
*/
// Internal dependencies
// (References API spec from contracts/api.yaml)

// External dependencies
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileTree = ({ projectId }) => {
    const [files, setFiles] = useState([]);
    
    useEffect(() => {
        const fetchFiles = async () => {
            const response = await axios.get(`/api/projects/${projectId}/generate/files`);
            setFiles(response.data.files);
        };
        fetchFiles();
    }, [projectId]);
    
    return (
        <div>
            {/* File tree display */}
        </div>
    );
};

export default FileTree;
```

### 9.14 dashboard/src/pages/BuildConsole.jsx
```jsx
/*
Level 7 — Depends on: C0, C7
*/
// Internal dependencies
// (References API spec from contracts/api.yaml)

// External dependencies
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BuildConsole = ({ projectId }) => {
    const [buildStatus, setBuildStatus] = useState(null);
    
    useEffect(() => {
        const fetchBuild = async () => {
            const response = await axios.get(`/api/projects/${projectId}/build`);
            setBuildStatus(response.data);
        };
        fetchBuild();
    }, [projectId]);
    
    return (
        <div>
            {/* Build console display */}
        </div>
    );
};

export default BuildConsole;
```

### 9.15 dashboard/src/pages/PlatformPackages.jsx
```jsx
/*
Level 7 — Depends on: C0, C7
*/
// Internal dependencies
// (References API spec from contracts/api.yaml)

// External dependencies
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PlatformPackages = ({ projectId }) => {
    const [packages, setPackages] = useState([]);
    
    useEffect(() => {
        const fetchPackages = async () => {
            const response = await axios.get(`/api/projects/${projectId}/package`);
            setPackages(response.data);
        };
        fetchPackages();
    }, [projectId]);
    
    return (
        <div>
            {/* Platform packages display */}
        </div>
    );
};

export default PlatformPackages;
```

### 9.16 dashboard/src/pages/LearningStore.jsx
```jsx
/*
Level 7 — Depends on: C0, C7
*/
// Internal dependencies
// (References API spec from contracts/api.yaml)

// External dependencies
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const LearningStore = () => {
    const [patterns, setPatterns] = useState([]);
    
    useEffect(() => {
        const fetchPatterns = async () => {
            const response = await axios.get('/api/learning-store/patterns');
            setPatterns(response.data);
        };
        fetchPatterns();
    }, []);
    
    return (
        <div>
            {/* Learning store display */}
        </div>
    );
};

export default LearningStore;
```

---

## 10. LEVEL 8 — SERVER ENTRY POINT

### 10.1 server/main.py
```python
"""
Level 8 — Depends on: S0, S1, S2, S3, S4, S5, S6, S7, S8, S9
"""
# Internal dependencies
from server.api.projects import router as projects_router
from server.api.architecture import router as architecture_router
from server.api.generation import router as generation_router
from server.api.builds import router as builds_router
from server.api.packages import router as packages_router
from server.api.store import router as store_router
from server.api.auth import router as auth_router
from server.workers.generation_worker import app as celery_app

# External dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup + shutdown lifecycle."""
    # Startup
    os.environ.setdefault("UNREAL_ENGINE_ROOT", os.getenv("UNREAL_ENGINE_ROOT", ""))
    yield
    # Shutdown
    celery_app.close()


app = FastAPI(
    title="FORGE API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router)
app.include_router(architecture_router)
app.include_router(generation_router)
app.include_router(builds_router)
app.include_router(packages_router)
app.include_router(store_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 11. DEPENDENCY SUMMARY TABLE

| Module | Level | Direct Deps | Transitive Deps | Import Count |
|--------|-------|-------------|-----------------|--------------|
| **L0** | 0 | 0 | 0 | 0 internal |
| ai/architect_agent.py | 1 | 4 | 0 | 4 |
| ai/test_agent.py | 1 | 2 | 0 | 2 |
| ai/repair_loop.py | 1 | 2 | 0 | 2 |
| engine/ue5_scanner.py | 1 | 1 | 0 | 1 |
| engine/learning_store.py | 1 | 2 | 0 | 2 |
| ai/test_generation/*.py | 2 | 3-4 | 2-3 | 3-4 |
| engine/brief_parser.py | 2 | 3 | 4 | 3 |
| engine/project_scaffolder.py | 3 | 4 | 6 | 4 |
| engine/cpp_generator.py | 4 | 4 | 10 | 4 |
| engine/blueprint_generator.py | 4 | 3 | 9 | 3 |
| engine/platform_guards.py | 4 | 2 | 0 | 2 |
| engine/build_runner.py | 5 | 4 | 14 | 4 |
| engine/package_agent.py | 6 | 3 | 18 | 3 |
| engine/store_agent.py | 6 | 3 | 21 | 3 |
| server/api/*.py | 7 | 3-5 | 14-21 | 3-5 |
| server/workers/*.py | 7 | 3-4 | 14-18 | 3-4 |
| dashboard/src/pages/*.jsx | 7 | 0 | 0 | 0 (API refs only) |
| server/main.py | 8 | 10 | 58 | 10 |

---

## 12. CIRCULAR DEPENDENCY PREVENTION

### 12.1 Rules

1. **Lower levels cannot depend on higher levels** — L1 cannot import from L2+
2. **Same-level imports must be acyclic** — Use dependency injection if needed
3. **L0 is always safe** — Contracts have no internal dependencies
4. **Agents cannot import engine modules** — ai/ can only depend on contracts/ + templates/
5. **Server cannot import ai/ directly** — Must go through engine/ abstractions

### 12.2 Allowed Import Patterns

```
✓ contracts → (nothing internal)
✓ ai → contracts, templates
✓ engine → contracts, ai (limited), engine (lower levels only)
✓ server → contracts, engine
✓ dashboard → (API calls only, no Python imports)
```

### 12.3 Forbidden Import Patterns

```
✗ engine → server (higher level)
✗ ai → engine (wrong direction)
✗ server → ai (must use engine abstraction)
✗ Same-level circular: E3 ↔ E4
```

### 12.4 Dependency Injection for Same-Level Dependencies

```python
# WRONG — circular import risk
# engine/cpp_generator.py
from engine.blueprint_generator import BlueprintGenerator

# CORRECT — dependency injection
# engine/cpp_generator.py
class CppGenerator:
    def __init__(self, blueprint_generator: Optional['BlueprintGenerator'] = None):
        self.bp_generator = blueprint_generator
```

---

## 13. IMPORT VALIDATION SCRIPT

```python
# tests/test_module_dependencies.py
import pytest
import ast
from pathlib import Path

class TestModuleDependencies:
    """Validate actual imports match declared dependencies."""
    
    @pytest.fixture
    def declared_deps(self):
        """Load declared dependencies from module_dependencies.md."""
        return self.parse_dependency_table()
    
    def test_no_circular_dependencies(self):
        """Verify no circular imports exist."""
        from engine.dependency_validator import DependencyValidator
        validator = DependencyValidator()
        
        has_cycle, cycles = validator.detect_cycles(GRAPH_A)
        assert not has_cycle, f"Circular dependencies detected: {cycles}"
    
    def test_imports_match_declarations(self, declared_deps):
        """Verify actual Python imports match declared graph."""
        for module_path, expected_deps in declared_deps.items():
            actual_deps = self.extract_imports(module_path)
            
            for dep in expected_deps:
                assert self.is_imported(dep, actual_deps), \
                    f"{module_path} missing declared dependency: {dep}"
    
    def test_no_forbidden_imports(self):
        """Verify no forbidden import patterns exist."""
        forbidden_patterns = [
            ("engine/", "server/"),
            ("ai/", "engine/"),
            ("server/", "ai/"),
        ]
        
        for module_path in self.all_python_files():
            imports = self.extract_imports(module_path)
            
            for source, target in forbidden_patterns:
                if module_path.startswith(source):
                    for imp in imports:
                        assert not imp.startswith(target), \
                            f"Forbidden import: {module_path} → {imp}"
    
    def extract_imports(self, module_path: str) -> List[str]:
        """Extract actual import statements from Python file."""
        with open(module_path) as f:
            tree = ast.parse(f.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return imports
```

---

*End of Module Dependencies Specification*
