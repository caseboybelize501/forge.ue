# FORGE — Code Generation Architecture (architecture2.md)

## 1. OVERVIEW

This document specifies the **code generation architecture** for implementing all 112 stub files with working code. Based on `requirements2.md` and the complete folder structure.

**Prerequisites:**
- All 9 planning phases complete (critic_final.md: APPROVED)
- All 112 stub files in place
- requirements2.md defines generation rules

---

## 2. GENERATION ARCHITECTURE

### 2.1 Layered Implementation Model

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CODE GENERATION PIPELINE                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 0: Contracts (Foundation)                                    │
│  - Pydantic schemas                                                 │
│  - Enum definitions                                                 │
│  - API request/response models                                      │
│  - Immutable after generation                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 1: Core Agents (Intelligence)                                │
│  - architect_agent: brief → ProjectSpec                             │
│  - test_agent: generate test specs                                  │
│  - repair_loop: fix UBT/UHT errors                                  │
│  - ue5_scanner: detect UE5 install + SDKs                           │
│  - learning_store: pattern library                                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 2: Test Generation + Parsing                                 │
│  - cpp_test_generator: UE5 automation tests                         │
│  - blueprint_test_validator: BP JSON validation                     │
│  - test_harness: orchestrate test runner                            │
│  - brief_parser: LLM brief → GameBrief                              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: Project Scaffolding                                       │
│  - project_scaffolder: folder structure + configs                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 4: Code Generation                                           │
│  - cpp_generator: ModuleSpec → .h + .cpp                            │
│  - blueprint_generator: ModuleSpec → BP JSON                        │
│  - platform_guards: inject + validate macros                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 5: Build Execution                                           │
│  - build_runner: UHT → UBT → test                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 6: Packaging + Store                                         │
│  - package_agent: cook + pak per platform                           │
│  - store_agent: Steam/EGS submission                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 7: Server + Dashboard                                        │
│  - FastAPI endpoints (7)                                            │
│  - Celery workers (3)                                               │
│  - React pages (6) + components (8)                                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 8: Server Entry Point                                        │
│  - server/main.py: FastAPI app + routers                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. IMPLEMENTATION DEPENDENCY GRAPH

### 3.1 File Generation Order (Topological)

```
LEVEL 0 (10 files)
├── contracts/models/game_brief.py         [no deps]
├── contracts/models/platform_spec.py      [no deps]
├── contracts/models/store_spec.py         [no deps]
├── contracts/models/code_artifact.py      [no deps]
├── contracts/models/build_result.py       [deps: code_artifact]
├── contracts/models/agent_message.py      [no deps]
├── contracts/models/project_spec.py       [deps: game_brief, build_result]
├── contracts/models/__init__.py           [deps: all above]
├── contracts/__init__.py                  [deps: models/__init__]
└── contracts/api.yaml                     [already complete]

LEVEL 1 (7 files)
├── engine/ue5_scanner.py                  [deps: L0]
├── engine/learning_store.py               [deps: L0]
├── ai/test_agent.py                       [deps: L0]
├── ai/repair_loop.py                      [deps: L0]
├── ai/architect_agent.py                  [deps: L0, templates/]
├── ai/__init__.py                         [deps: ai/*]
└── engine/__init__.py                     [deps: engine/*]

LEVEL 2 (5 files)
├── ai/test_generation/cpp_test_generator.py   [deps: L0, L1]
├── ai/test_generation/blueprint_test_validator.py [deps: L0, L1]
├── ai/test_generation/test_harness.py     [deps: L0, L1]
├── ai/test_generation/__init__.py         [deps: test_generation/*]
└── engine/brief_parser.py                 [deps: L0, L1]

LEVEL 3 (2 files)
├── engine/project_scaffolder.py           [deps: L0, L2]
└── templates/__init__.py                  [no deps]

LEVEL 4 (4 files)
├── engine/cpp_generator.py                [deps: L0, L3]
├── engine/blueprint_generator.py          [deps: L0, L3]
├── engine/platform_guards.py              [deps: L0]
└── engine/ (update __init__.py)           [deps: engine/*]

LEVEL 5 (2 files)
├── engine/build_runner.py                 [deps: L0, L4, L1]
└── engine/ (update __init__.py)           [deps: engine/*]

LEVEL 6 (3 files)
├── engine/package_agent.py                [deps: L0, L5]
├── engine/store_agent.py                  [deps: L0, L6]
└── engine/ (update __init__.py)           [deps: engine/*]

LEVEL 7 (44 files)
├── server/api/projects.py                 [deps: L0, L2, L3]
├── server/api/architecture.py             [deps: L0, L1]
├── server/api/generation.py               [deps: L0, L4, L5]
├── server/api/builds.py                   [deps: L0, L5]
├── server/api/packages.py                 [deps: L0, L6]
├── server/api/store.py                    [deps: L0, L6]
├── server/api/auth.py                     [deps: L0]
├── server/api/__init__.py                 [deps: api/*]
├── server/workers/generation_worker.py    [deps: L0, L2, L3, L4]
├── server/workers/build_worker.py         [deps: L0, L5]
├── server/workers/package_worker.py       [deps: L0, L6]
├── server/workers/__init__.py             [deps: workers/*]
├── server/models/database.py              [deps: external]
├── server/models/project.py               [deps: database]
├── server/models/build.py                 [deps: database]
├── server/models/__init__.py              [deps: models/*]
├── dashboard/package.json                 [no deps]
├── dashboard/vite.config.js               [no deps]
├── dashboard/index.html                   [no deps]
├── dashboard/src/main.jsx                 [deps: App]
├── dashboard/src/index.css                [deps: styles]
├── dashboard/src/App.jsx                  [deps: pages, components]
├── dashboard/src/api/client.js            [deps: external]
├── dashboard/src/api/endpoints.js         [deps: external]
├── dashboard/src/api/index.js             [deps: client, endpoints]
├── dashboard/src/components/* (8 files)   [deps: external]
├── dashboard/src/components/index.js      [deps: components/*]
├── dashboard/src/hooks/useProject.js      [deps: api]
├── dashboard/src/hooks/useBuild.js        [deps: api]
├── dashboard/src/hooks/index.js           [deps: hooks/*]
├── dashboard/src/styles/variables.css     [no deps]
├── dashboard/src/styles/main.css          [deps: variables]
├── dashboard/src/pages/ProjectBrief.jsx   [deps: api]
├── dashboard/src/pages/GenerationProgress.jsx [deps: api]
├── dashboard/src/pages/FileTree.jsx       [deps: api, components]
├── dashboard/src/pages/BuildConsole.jsx   [deps: api, components]
├── dashboard/src/pages/PlatformPackages.jsx [deps: api, components]
├── dashboard/src/pages/LearningStore.jsx  [deps: api]
└── dashboard/src/ (update as needed)

LEVEL 8 (2 files)
├── server/main.py                         [deps: L7 api/*, workers/*]
└── server/__init__.py                     [deps: main]

LEVEL 9 (12 files)
├── tests/__init__.py                      [no deps]
├── tests/conftest.py                      [deps: external]
├── tests/test_platform_guards.py          [deps: L4]
├── tests/test_architect_agent.py          [deps: L1]
├── tests/test_cpp_generator.py            [deps: L4]
├── tests/test_blueprint_generator.py      [deps: L4]
├── tests/test_build_runner.py             [deps: L5]
├── tests/test_repair_loop.py              [deps: L1]
├── tests/test_dependency_graph.py         [deps: external]
├── tests/test_module_dependencies.py      [deps: all]
├── tests/integration/__init__.py          [no deps]
└── tests/integration/test_full_pipeline.py [deps: all]

LEVEL 10 (10 files)
├── docker-compose.yml                     [already complete]
├── .env.example                           [already complete]
├── .gitignore                             [already complete]
├── .python-version                        [already complete]
├── pyproject.toml                         [already complete]
├── requirements.txt                       [already complete]
├── requirements-dev.txt                   [already complete]
├── PRIVATE_LICENSE.md                     [already complete]
├── README.md                              [already complete]
└── tasks.md                               [already complete]
```

---

## 4. CODE GENERATION STRATEGY

### 4.1 Per-File Generation Process

```
┌─────────────────────────────────────────────────────────────────────┐
│  FOR EACH FILE (in topological order):                              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  1. READ STUB                                                       │
│     - Extract class/function signatures                             │
│     - Extract docstrings                                            │
│     - Extract import statements                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. READ DEPENDENCIES                                               │
│     - Load all dependency files                                     │
│     - Verify type hints match                                       │
│     - Verify import paths valid                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. GENERATE IMPLEMENTATION                                         │
│     - Replace `pass` with working code                              │
│     - Add error handling                                            │
│     - Add logging                                                   │
│     - Maintain type hints                                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. VALIDATE                                                        │
│     - Python: import + type check                                   │
│     - JavaScript: eslint + build                                    │
│     - C++: clang-format + UHT dry-run                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. CHECK AGAINST forgeue.md                                        │
│     - Verify requirements covered                                   │
│     - Verify API compliance                                         │
│     - Verify UE5 standards                                          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  IF VALID: Mark complete, proceed to next file                     │
│  IF INVALID: HALT, return to root cause phase                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Implementation Templates

**Pydantic Model Template:**
```python
class {ModelName}(BaseModel):
    """
    {Description from stub docstring}.
    
    Attributes:
        {field1}: {description}
        {field2}: {description}
    """
    {field1}: {type}
    {field2}: {type} = {default}
    
    @field_validator('{field1}')
    @classmethod
    def validate_{field1}(cls, v: str) -> str:
        """Validate {field1} is non-empty."""
        if not v or not v.strip():
            raise ValueError('{field1} cannot be empty')
        return v.strip()
```

**Agent Class Template:**
```python
class {AgentName}:
    """
    {Agent description from stub}.
    
    Attributes:
        {attr1}: {description}
        {attr2}: {description}
    """
    
    def __init__(self, {params}):
        """Initialize {agent_name}."""
        {initialization}
    
    def {method_name}(self, {params}) -> {return_type}:
        """
        {Method description}.
        
        Args:
            {arg}: {description}
            
        Returns:
            {description}
        """
        try:
            {implementation}
        except {Exception} as e:
            logger.error("Error in {method_name}: {e}")
            raise
```

**FastAPI Router Template:**
```python
router = APIRouter(prefix="/api/{resource}", tags=["{tag}"])


@router.get("/{resource_id}", response_model={ResponseModel})
async def {operation}(
    {resource_id}: str,
    db: Session = Depends(get_db)
) -> {ResponseModel}:
    """
    {Operation description}.
    
    Args:
        {resource_id}: Resource identifier
        db: Database session
        
    Returns:
        {ResponseModel}
    """
    try:
        {implementation}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in {operation}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**React Component Template:**
```jsx
/**
 * {Component} Component
 * 
 * {Description from stub}.
 */
import React, {{ useState, useEffect }} from 'react';
import apiClient from '../api/client';
import {{ endpoints }} from '../api/endpoints';

function {ComponentName}({{ {props} }}) {{
  const [{state}, setState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {{
    const fetchData = async () => {{
      try {{
        const response = await apiClient.get(endpoints.{endpoint});
        setState(response.data);
        setError(null);
      }} catch (err) {{
        setError(err.message);
      }} finally {{
        setLoading(false);
      }}
    }};

    fetchData();
  }}, [{dependencies}]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {{error}}</div>;

  return (
    <div className="{component-class}">
      {/* Component content */}
    </div>
  );
}}

export default {ComponentName};
```

---

## 5. VALIDATION GATES

### 5.1 Per-Level Validation

| Level | Validation Type | Tools | Pass Criteria |
|-------|----------------|-------|---------------|
| L0 (Contracts) | Pydantic validate | `pytest contracts/` | All models validate test data |
| L1 (Agents) | Import + type check | `mypy ai/ engine/` | No type errors |
| L2 (Test Gen) | Import + unit test | `pytest ai/test_generation/` | Tests generate valid specs |
| L3 (Scaffold) | Import + integration | `pytest engine/project_scaffolder.py` | Creates valid structure |
| L4 (Code Gen) | Import + UHT check | `mypy engine/` + UHT | No type/UHT errors |
| L5 (Build) | Import + mock UBT | `pytest engine/build_runner.py` | Parses errors correctly |
| L6 (Package) | Import + mock cook | `pytest engine/package_agent.py` | Validates SDK paths |
| L7 (Server) | Import + API test | `pytest server/` + `npm run build` | All endpoints respond |
| L8 (Main) | Import + health check | `curl /health` | Returns `{"status": "healthy"}` |
| L9 (Tests) | Run all tests | `pytest tests/ -v` | All tests pass |

### 5.2 Drift Detection Points

After each level completes:

```python
def check_drift(level: int) -> DriftReport:
    """
    Check for drift from forgeue.md after level completion.
    
    Args:
        level: Completed level number
        
    Returns:
        DriftReport with any detected issues
    """
    report = DriftReport()
    
    # Check requirements coverage
    for req in get_requirements_for_level(level):
        if not is_requirement_satisfied(req):
            report.add_drift(f"Requirement {req.id} not satisfied")
    
    # Check API compliance
    for endpoint in API_ENDPOINTS:
        if not endpoint_matches_spec(endpoint):
            report.add_drift(f"API endpoint {endpoint} drift detected")
    
    # Check UE5 standards
    for cpp_file in get_cpp_files(level):
        if not follows_ue5_standards(cpp_file):
            report.add_drift(f"C++ file {cpp_file} violates UE5 standards")
    
    # Check dependency graph
    if has_cycle(current_dependency_graph):
        report.add_drift("Dependency cycle detected")
    
    return report
```

---

## 6. ERROR RECOVERY STRATEGY

### 6.1 Root Cause Analysis

When drift is detected:

```
┌─────────────────────────────────────────────────────────────────────┐
│  DRIFT DETECTED                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CLASSIFY ERROR TYPE:                                               │
│  - Import error → Phase 4 (Module Dependencies)                     │
│  - Schema error → Phase 1 (Requirements)                            │
│  - API mismatch → Phase 1 (Requirements)                            │
│  - UE5 violation → Phase 6 (Pre-Build Critic)                       │
│  - Cycle detected → Phase 3 (Dependency Graph)                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  RETURN TO ROOT CAUSE PHASE                                         │
│  - Do not patch forward                                             │
│  - Regenerate from that phase                                       │
│  - Re-run critic gate                                               │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Recovery Examples

**Example 1: Import Error**
```
File: engine/cpp_generator.py
Error: cannot import name 'ModuleSpec' from 'contracts.models.project_spec'

Root Cause: ModuleSpec not exported in contracts/models/__init__.py
Return To: Phase 4 (Module Dependencies)
Fix: Update contracts/models/__init__.py exports
Regenerate: All files depending on ModuleSpec
```

**Example 2: API Mismatch**
```
File: server/api/projects.py
Error: POST /api/projects returns wrong response schema

Root Cause: ProjectResponse model missing fields
Return To: Phase 1 (Requirements)
Fix: Update contracts/models/build_result.py ProjectResponse
Regenerate: All API endpoints using ProjectResponse
```

**Example 3: UE5 Violation**
```
File: templates/interfaces/IForgeCharacter.h
Error: UHT error - GENERATED_BODY() missing

Root Cause: Interface header template incorrect
Return To: Phase 6 (Pre-Build Critic)
Fix: Update interface header template
Regenerate: All C++ files using this interface
```

---

## 7. PROGRESS TRACKING

### 7.1 Generation Status Board

| Level | Files | Complete | In Progress | Pending | Status |
|-------|-------|----------|-------------|---------|--------|
| L0 | 10 | 0 | 0 | 10 | ⏳ Pending |
| L1 | 7 | 0 | 0 | 7 | ⏳ Pending |
| L2 | 5 | 0 | 0 | 5 | ⏳ Pending |
| L3 | 2 | 0 | 0 | 2 | ⏳ Pending |
| L4 | 4 | 0 | 0 | 4 | ⏳ Pending |
| L5 | 2 | 0 | 0 | 2 | ⏳ Pending |
| L6 | 3 | 0 | 0 | 3 | ⏳ Pending |
| L7 | 44 | 0 | 0 | 44 | ⏳ Pending |
| L8 | 2 | 0 | 0 | 2 | ⏳ Pending |
| L9 | 12 | 0 | 0 | 12 | ⏳ Pending |
| L10 | 10 | 10 | 0 | 0 | ✅ Complete |
| **Total** | **101** | **10** | **0** | **91** | **10% Complete** |

### 7.2 Current File Marker

**Next File:** `contracts/models/game_brief.py`  
**Level:** 0  
**Status:** ⏳ Ready to generate

---

## 8. SUCCESS CRITERIA (Detailed)

### 8.1 Per-Level Exit Criteria

**Level 0 (Contracts):**
- [ ] All 10 files import without errors
- [ ] All Pydantic models validate test fixtures
- [ ] All enums have correct values per forgeue.md
- [ ] API schemas match contracts/api.yaml
- [ ] `contracts/models/__init__.py` exports all models
- [ ] `contracts/__init__.py` exports all submodules

**Level 1 (Core Agents):**
- [ ] All 7 files import without errors
- [ ] architect_agent generates valid ProjectSpec
- [ ] test_agent generates valid TestSpec list
- [ ] repair_loop handles all error types
- [ ] ue5_scanner detects UE5 5.3+ correctly
- [ ] learning_store persists patterns to disk

**Level 2 (Test Gen + Parse):**
- [ ] All 5 files import without errors
- [ ] cpp_test_generator generates valid UE5 test code
- [ ] blueprint_test_validator validates BP JSON schemas
- [ ] test_harness orchestrates UE5 test runner
- [ ] brief_parser extracts GameBrief from raw text

**Level 3 (Scaffold):**
- [ ] project_scaffolder creates valid UE5 project structure
- [ ] Generated .uproject is valid JSON
- [ ] Generated Build.cs compiles
- [ ] Generated .ini configs are valid

**Level 4 (Code Gen):**
- [ ] cpp_generator generates UE5-compliant C++
- [ ] blueprint_generator generates valid BP JSON
- [ ] platform_guards injects correct macros
- [ ] All generated code passes UHT dry-run

**Level 5 (Build):**
- [ ] build_runner invokes UHT correctly
- [ ] build_runner invokes UBT correctly
- [ ] Error parser extracts file/line/message
- [ ] Test runner captures results

**Level 6 (Package + Store):**
- [ ] package_agent cooks content per platform
- [ ] package_agent paks binaries correctly
- [ ] store_agent generates Steam config
- [ ] store_agent generates EGS config

**Level 7 (Server + Dashboard):**
- [ ] All 7 API endpoints respond correctly
- [ ] All 3 Celery workers execute tasks
- [ ] All 6 React pages render
- [ ] All 8 React components render
- [ ] Dashboard builds without errors

**Level 8 (Entry Point):**
- [ ] server/main.py starts without errors
- [ ] `/health` endpoint returns `{"status": "healthy"}`
- [ ] All routers mounted correctly
- [ ] CORS middleware configured

**Level 9 (Tests):**
- [ ] All unit tests pass
- [ ] Integration test passes
- [ ] Code coverage > 80%

### 8.2 Final Success Criteria

Code generation complete when:
- [ ] All 101 files implemented (L0-L9)
- [ ] All imports resolve
- [ ] All type checks pass
- [ ] All unit tests pass
- [ ] Server responds to `/health`
- [ ] Dashboard builds
- [ ] Generated UE5 project compiles
- [ ] Packaged binaries created

---

## 9. NEXT ACTION

**Immediate Next Step:** Generate `contracts/models/game_brief.py`

**Implementation Checklist:**
- [ ] Read existing stub (64 lines)
- [ ] Read dependencies (none - foundation file)
- [ ] Implement all classes with full validation
- [ ] Add `GameBriefRequest` schema
- [ ] Add field validators
- [ ] Update `contracts/models/__init__.py` exports
- [ ] Run: `python -c "from contracts.models.game_brief import GameBrief"`
- [ ] Run: `pytest tests/ -k game_brief -v`
- [ ] Verify against forgeue.md genre/platform lists
- [ ] Mark complete in status board

---

*End of Code Generation Architecture*
