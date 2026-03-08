# FORGE — Architecture Specification

## 1. SYSTEM ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                         GAME BRIEF INPUT                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ai/ (META-LAYER)                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ architect_agent │  │   test_agent    │  │   repair_loop   │    │
│  │   (Level 1)     │  │   (Level 1)     │  │   (Level 1)     │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
│         │                      │                      │            │
│         ▼                      ▼                      ▼            │
│  ProjectSpec           Test Specs            Error Reports        │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  engine/ (PIPELINE)                                 │
│  ue5_scanner → brief_parser → project_scaffolder → cpp_generator  │
│     → blueprint_generator → build_runner → package_agent          │
│     → store_agent → learning_store                                │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              output/{project_name}/ (UE5 PROJECT)                   │
│  Source/    Content/    Config/    Build/    {Project}.uproject   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. MODULE DEPENDENCY GRAPH (Graph A — Pipeline)

### Level 0 — Contracts (Immutable Foundation)
```
contracts/models/game_brief.py          → No dependencies
contracts/models/project_spec.py        → No dependencies
contracts/models/code_artifact.py       → No dependencies
contracts/models/build_result.py        → No dependencies
contracts/models/agent_message.py       → No dependencies
contracts/models/platform_spec.py       → No dependencies
contracts/models/store_spec.py          → No dependencies
contracts/api.yaml                      → No dependencies
templates/interfaces/*.h                → No dependencies (UE5 headers)
```

### Level 1 — Core Agents + Scanners
```
ai/architect_agent.py                   → deps: [contracts, templates/interfaces]
ai/test_agent.py                        → deps: [contracts]
ai/repair_loop.py                       → deps: [contracts]
engine/ue5_scanner.py                   → deps: [contracts]
engine/learning_store.py                → deps: [contracts]
```

### Level 2 — Test Generation + Brief Parsing
```
ai/test_generation/cpp_test_generator.py → deps: [contracts, ai/test_agent]
ai/test_generation/blueprint_test_validator.py → deps: [contracts]
ai/test_generation/test_harness.py      → deps: [contracts, ai/test_agent]
engine/brief_parser.py                  → deps: [contracts, ai/architect_agent]
```

### Level 3 — Project Scaffolding
```
engine/project_scaffolder.py            → deps: [contracts, templates/interfaces, engine/brief_parser]
```

### Level 4 — Code Generation
```
engine/cpp_generator.py                 → deps: [contracts, templates/interfaces, engine/project_scaffolder]
engine/blueprint_generator.py           → deps: [contracts, engine/project_scaffolder]
```

### Level 5 — Build Execution
```
engine/build_runner.py                  → deps: [contracts, engine/cpp_generator, ai/test_agent]
```

### Level 6 — Packaging + Store
```
engine/package_agent.py                 → deps: [contracts, engine/build_runner]
engine/store_agent.py                   → deps: [contracts, engine/package_agent]
```

### Level 7 — Server + Dashboard (Parallel)
```
server/api/projects.py                  → deps: [contracts, api.yaml, engine/*]
server/api/architecture.py              → deps: [contracts, api.yaml, ai/architect_agent]
server/api/generation.py                → deps: [contracts, api.yaml, engine/*]
server/api/builds.py                    → deps: [contracts, api.yaml, engine/build_runner]
server/api/packages.py                  → deps: [contracts, api.yaml, engine/package_agent]
server/api/store.py                     → deps: [contracts, api.yaml, engine/store_agent]
server/api/auth.py                      → deps: [contracts, api.yaml]
server/workers/generation_worker.py     → deps: [contracts, engine/*, Celery]
server/workers/build_worker.py          → deps: [contracts, engine/build_runner, Celery]
server/workers/package_worker.py        → deps: [contracts, engine/package_agent, Celery]
dashboard/src/pages/ProjectBrief.jsx    → deps: [api.yaml]
dashboard/src/pages/GenerationProgress.jsx → deps: [api.yaml]
dashboard/src/pages/FileTree.jsx        → deps: [api.yaml]
dashboard/src/pages/BuildConsole.jsx    → deps: [api.yaml]
dashboard/src/pages/PlatformPackages.jsx → deps: [api.yaml]
dashboard/src/pages/LearningStore.jsx   → deps: [api.yaml]
```

### Level 8 — Server Entry Point
```
server/main.py                          → deps: [server/api/*, server/workers/*]
```

---

## 3. UBT MODULE DEPENDENCY GRAPH (Graph B — Generated per Project)

### Standard Module Graph Template
```
{Project}Core.Build.cs          → No UE5 game module deps
     │
     ▼
{Project}GameFramework.Build.cs → deps: {Project}Core
     │
     ▼
{Project}[Genre]Systems.Build.cs → deps: {Project}GameFramework
     │
     ▼
{Project}UI.Build.cs            → deps: {Project}Core, {Project}GameFramework, {Project}[Genre]Systems
     │
     ▼
{Project}Platform.Build.cs      → deps: All above modules
```

### Cycle Detection Algorithm
```python
def detect_cycles(graph: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    """DFS-based cycle detection for UBT module graph."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    cycles = []
    
    def dfs(node: str, path: List[str]) -> bool:
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
                return True
            if color[neighbor] == WHITE and dfs(neighbor, path + [neighbor]):
                return True
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            dfs(node, [node])
    
    return (len(cycles) > 0, cycles)
```

---

## 4. AGENT ARCHITECTURES

### 4.1 architect_agent.py

**Responsibility:** Transform GameBrief → ProjectSpec + UBT Module Graph

**Input:** `GameBrief` (from `contracts/models/game_brief.py`)

**Output:** `ProjectSpec` containing:
```python
ProjectSpec(
    project_id: str,
    project_name: str,
    modules: List[ModuleSpec],
    subsystems: List[SubsystemRef],
    cpp_files: List[str],
    blueprint_files: List[str],
    ubt_module_deps: Dict[str, List[str]],  # Graph B
    platform_targets: List[PlatformTarget],
    estimated_compile_min: int,
    genre_patterns: List[str]
)
```

**Decision Logic:**
```python
def select_subsystems(genre: Genre) -> List[SubsystemRef]:
    if genre in [Genre.ACTION, Genre.RPG]:
        return [SubsystemRef.GAS, SubsystemRef.ENHANCED_INPUT]
    if genre == Genre.OPEN_WORLD:
        return [SubsystemRef.WORLD_PARTITION, SubsystemRef.LEVEL_STREAMING]
    if genre == Genre.MULTIPLAYER:
        return [SubsystemRef.ONLINE_SUBSYSTEM, SubsystemRef.REPLICATION]
    if genre == Genre.MOBILE:
        return [SubsystemRef.REDUCED_TICK, SubsystemRef.AGGRESSIVE_LOD]
    return [SubsystemRef.CUSTOM_STATE_MACHINE]
```

### 4.2 test_agent.py

**Responsibility:** Generate test specifications per generated system

**Test Types Generated:**
1. **UE5 Automation Tests (C++)** — `ai/test_generation/{SystemName}.test.cpp`
2. **Blueprint Validation Specs (JSON)** — `ai/test_generation/*.spec.json`
3. **Platform Guard Tests (Python)** — `ai/test_generation/test_platform_guards.py`

**Test Harness Interface:**
```python
class TestSpec(BaseModel):
    test_name: str
    test_type: Literal["automation", "blueprint", "platform_guard"]
    target_system: str
    assertions: List[AssertionSpec]
    expected_result: TestResult

class AssertionSpec(BaseModel):
    assertion_type: Literal["equals", "greater_than", "contains", "not_null"]
    actual_value: str
    expected_value: Any
    error_message: str
```

### 4.3 repair_loop.py

**Responsibility:** Parse UBT/UHT errors → Targeted file repair → Recompile

**Repair Context:**
```python
class RepairContext(BaseModel):
    failing_file: str
    error_text: str
    error_line: Optional[int]
    ue5_version: str
    module_deps: List[str]
    interface_header: Optional[str]  # Immutable reference
    prior_attempts: List[str]
    ue5_coding_standard_rules: str
```

**UE5 Coding Standard Rules (Injected into every repair prompt):**
```
"UE5 C++ rules:
- UCLASS() before every UObject-derived class
- GENERATED_BODY() after every UCLASS declaration
- UPROPERTY() before every Blueprint-visible or replicated field
- UFUNCTION() before every Blueprint-callable function
- Never use raw pointers for UObject refs — use TObjectPtr<>
- Never call delete on UObjects — use garbage collector
- Platform-specific code MUST be wrapped in platform guards"
```

**Repair Algorithm:**
```python
def repair_file(context: RepairContext) -> Optional[str]:
    if len(context.prior_attempts) >= 3:
        return None  # HALT
    
    # Parse error type
    error_type = classify_ue_error(context.error_text)
    
    # Generate repair prompt with context
    prompt = build_repair_prompt(context, error_type)
    
    # LLM generates fix
    repaired_content = llm_inference(prompt)
    
    # Validate repair
    if validate_repair(repaired_content, context):
        return repaired_content
    
    context.prior_attempts.append(repaired_content)
    return repair_file(context)  # Recursive retry
```

---

## 5. CRITIC GATE ARCHITECTURE

### 4-Pass Validation Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│  LEVEL N FILES GENERATED                                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PASS 1 — SYNTAX (No LLM)                                           │
│  Python: ast.parse() + mypy --strict + ruff check                  │
│  C++ .h: clang-format + UHT dry-run                                │
│  C++ .cpp: UBT compile (single file)                               │
│  Blueprint JSON: Schema validation                                 │
│  YAML: yamllint + openapi-spec-validator                           │
└─────────────────────────────────────────────────────────────────────┘
                                │ PASS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PASS 2 — CONTRACT (No LLM)                                         │
│  ✓ Every .cpp implements its paired .h exactly                     │
│  ✓ All UCLASS/UPROPERTY/UFUNCTION macros present                   │
│  ✓ No console SDK symbols without platform guards                  │
│  ✓ Blueprint JSON: valid node connections                          │
│  ✓ Agent outputs typed per schemas                                 │
└─────────────────────────────────────────────────────────────────────┘
                                │ PASS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PASS 3 — COMPLETENESS (LLM)                                        │
│  ✓ No NotImplemented in FR-required systems                        │
│  ✓ ProjectSpec covers all mechanics from brief                     │
│  ✓ All platform targets have cook config                           │
│  ✓ UBT error parser handles all known error types                  │
└─────────────────────────────────────────────────────────────────────┘
                                │ PASS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PASS 4 — LOGIC (LLM, UE5-specific)                                │
│  ✓ UCLASS hierarchy correct                                        │
│  ✓ GAS attributes registered in AttributeSet                       │
│  ✓ Enhanced Input mappings bound in PlayerController               │
│  ✓ Save game serialization covers UPROPERTY(SaveGame) fields       │
│  ✓ Platform abstraction compiles with no SDK (stub)                │
└─────────────────────────────────────────────────────────────────────┘
                                │ PASS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LEVEL LOCKED → ADVANCE TO LEVEL N+1                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. DATA FLOW ARCHITECTURE

### 6.1 Project Creation Flow
```
POST /api/projects { brief: string }
    │
    ▼
server/api/projects.py
    │
    ▼
engine/brief_parser.py → GameBrief (Pydantic)
    │
    ▼
ai/architect_agent.py → ProjectSpec
    │
    ▼
server/api/architecture.py → Return for human review (GATE-1)
```

### 6.2 Generation Flow
```
POST /api/projects/:id/generate
    │
    ▼
server/workers/generation_worker.py (Celery)
    │
    ├─→ engine/project_scaffolder.py → Folder structure + configs
    ├─→ engine/cpp_generator.py → .h + .cpp files
    ├─→ engine/blueprint_generator.py → BP JSON graphs
    │
    ▼
engine/build_runner.py
    │
    ├─→ UHT dry-run
    ├─→ UBT compile
    └─→ Capture errors → repair_loop.py (if needed)
    │
    ▼
ai/test_agent.py → Generate tests
    │
    ▼
engine/build_runner.py → Run tests
    │
    ▼
Lock Level → Advance
```

### 6.3 Packaging Flow
```
POST /api/projects/:id/package { platforms: [] }
    │
    ▼
server/workers/package_worker.py (Celery)
    │
    ├─→ engine/package_agent.py
    │       │
    │       ├─→ Validate SDK availability per platform
    │       ├─→ Cook content (UE5-cmd)
    │       ├─→ Pak binaries
    │       └─→ Output: output/{project}/Build/{Platform}/
    │
    ▼
engine/store_agent.py → Generate submission assets
    │
    ▼
GET /api/projects/:id/package/:platform → Download
```

---

## 7. API ARCHITECTURE

### REST Endpoints (FastAPI)

```python
# server/main.py
app = FastAPI(title="FORGE API", version="1.0.0")

# Project CRUD
@app.post("/api/projects")
async def create_project(brief: GameBriefRequest) -> ProjectResponse

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str) -> ProjectResponse

@app.get("/api/projects/{project_id}/architecture")
async def get_architecture(project_id: str) -> ProjectSpec

# Generation Control
@app.post("/api/projects/{project_id}/generate")
async def trigger_generation(project_id: str) -> TaskResponse

@app.get("/api/projects/{project_id}/progress")
async def get_progress(project_id: str) -> ProgressResponse

@app.get("/api/projects/{project_id}/files")
async def get_file_tree(project_id: str) -> FileTreeResponse

# Build + Package
@app.get("/api/projects/{project_id}/build")
async def get_build_status(project_id: str) -> BuildStatusResponse

@app.post("/api/projects/{project_id}/package")
async def trigger_packaging(project_id: str, platforms: List[str]) -> TaskResponse

@app.get("/api/projects/{project_id}/package/{platform}")
async def download_package(project_id: str, platform: str) -> FileResponse

# Audit
@app.get("/api/projects/{project_id}/critic-log")
async def get_critic_log(project_id: str) -> CriticLogResponse
```

### Celery Task Queue

```python
# server/workers/generation_worker.py
@app.task(bind=True, max_retries=3)
def run_generation_pipeline(self, project_id: str):
    chain(
        chord(
            group(generate_level_0.s(project_id)),
            critic_gate.s(project_id, level=0)
        ),
        chord(
            group(generate_level_1.s(project_id)),
            critic_gate.s(project_id, level=1)
        ),
        # ... through level 8
        finalize_generation.s(project_id)
    ).apply_async()
```

---

## 8. FILE DEDUPLICATION ARCHITECTURE

### Dedup Key Generation
```python
def generate_dedup_key(project_id: str, file_path: str, content: str) -> str:
    """Generate unique key for file deduplication."""
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"{project_id}:{file_path}:{content_hash}"
```

### Dedup Storage
```python
class DedupStore:
    def __init__(self):
        self.index: Dict[str, str] = {}  # key → storage_path
    
    def exists(self, key: str) -> bool:
        return key in self.index
    
    def store(self, key: str, content: str) -> str:
        if self.exists(key):
            return self.index[key]  # Return existing path
        
        storage_path = f".dedup/{key}"
        with open(storage_path, 'w') as f:
            f.write(content)
        self.index[key] = storage_path
        return storage_path
```

---

## 9. PLATFORM GUARD ARCHITECTURE

### Platform Guard Injection
```python
# engine/platform_guards.py
PLATFORM_GUARDS = {
    "PS5": "#if PLATFORM_PS5",
    "XBOX": "#if PLATFORM_XBOXONE",
    "SWITCH": "#if PLATFORM_SWITCH",
    "ANDROID": "#if PLATFORM_ANDROID",
    "IOS": "#if PLATFORM_IOS",
}

def wrap_platform_specific(code: str, platform: str) -> str:
    guard = PLATFORM_GUARDS.get(platform)
    if not guard:
        return code
    return f"{guard}\n{code}\n#endif"
```

### Platform Guard Validation
```python
def validate_platform_guards(file_content: str) -> List[Violation]:
    violations = []
    sdk_symbols = ["sce", "nx", "Xbl", "android", "iOS"]
    
    for line_num, line in enumerate(file_content.split('\n'), 1):
        for symbol in sdk_symbols:
            if symbol in line and not is_platform_guarded(line, file_content, line_num):
                violations.append(Violation(
                    line=line_num,
                    symbol=symbol,
                    message=f"SDK symbol '{symbol}' used without platform guard"
                ))
    
    return violations
```

---

## 10. LEARNING STORE ARCHITECTURE

### Pattern Storage
```python
# engine/learning_store.py
class LearningStore:
    def __init__(self):
        self.patterns: Dict[str, Pattern] = {}
    
    def store_pattern(self, genre: str, system: str, pattern: Pattern):
        key = f"{genre}:{system}"
        self.patterns[key] = pattern
    
    def get_patterns(self, genre: str) -> List[Pattern]:
        return [p for k, p in self.patterns.items() if k.startswith(genre)]
    
    def get_similar_project(self, brief: GameBrief) -> Optional[ProjectSpec]:
        # Find most similar past project for pattern reuse
        pass
```

### Pattern Schema
```python
class Pattern(BaseModel):
    pattern_id: str
    genre: Genre
    system_type: str
    cpp_templates: List[str]
    blueprint_templates: List[str]
    ubt_module_config: ModuleSpec
    common_errors: List[ErrorPattern]
    repair_strategies: List[str]
    success_rate: float
    avg_repair_cycles: int
```

---

## 11. SELF-REPAIR ARCHITECTURE (Runtime)

### Error Detection + Response Matrix

| Error Type | Detection Method | Response |
|------------|------------------|----------|
| UBT compile failure | Parse stderr for `Error` | repair_loop.py → fix → recompile |
| LLM inference OOM | CUDA out of memory in logs | Drop quant level, resume |
| UE5 editor crash | Process exit + crash dump | Retry headless, HALT if fails |
| Platform SDK missing | SDK path validation | Skip platform, log, continue |
| Blueprint import failure | UE commandlet error | Re-generate JSON, fallback to C++ |

### OOM Recovery Flow
```python
def handle_llm_oom():
    """Graceful degradation when LLM + UE5 compete for VRAM."""
    current_model = get_current_model()
    
    if current_model == "Llama-3-70B-Q4":
        switch_model("Llama-3-34B-Q8")
    elif current_model == "Llama-3-34B-Q8":
        switch_model("Llama-3-34B-Q4")
    else:
        log_health_flag("LLM_DEGRADED_MODE")
        return  # Already at lowest quant
    
    resume_generation()
    log_health_flag(f"LLM_DOWNGRADED_FROM_{current_model}")
```

---

## 12. DIRECTORY STRUCTURE

```
forge.ue/
├── contracts/
│   └── models/
│       ├── game_brief.py
│       ├── project_spec.py
│       ├── code_artifact.py
│       ├── build_result.py
│       ├── agent_message.py
│       ├── platform_spec.py
│       └── store_spec.py
├── templates/
│   └── interfaces/
│       ├── IForgeGameMode.h
│       ├── IForgeCharacter.h
│       ├── IForgeGameInstance.h
│       ├── IForgeInventory.h
│       ├── IForgeSaveGame.h
│       ├── IForgeUIManager.h
│       ├── IForgeAudioManager.h
│       ├── IForgeAchievement.h
│       ├── IForgePlatformLayer.h
│       └── IForgeOnlineSubsystem.h
├── ai/
│   ├── architect_agent.py
│   ├── test_agent.py
│   ├── repair_loop.py
│   └── test_generation/
│       ├── cpp_test_generator.py
│       ├── blueprint_test_validator.py
│       └── test_harness.py
├── engine/
│   ├── ue5_scanner.py
│   ├── brief_parser.py
│   ├── project_scaffolder.py
│   ├── cpp_generator.py
│   ├── blueprint_generator.py
│   ├── build_runner.py
│   ├── package_agent.py
│   ├── store_agent.py
│   ├── learning_store.py
│   └── platform_guards.py
├── server/
│   ├── main.py
│   ├── api/
│   │   ├── projects.py
│   │   ├── architecture.py
│   │   ├── generation.py
│   │   ├── builds.py
│   │   ├── packages.py
│   │   ├── store.py
│   │   └── auth.py
│   └── workers/
│       ├── generation_worker.py
│       ├── build_worker.py
│       └── package_worker.py
├── dashboard/
│   └── src/
│       └── pages/
│           ├── ProjectBrief.jsx
│           ├── GenerationProgress.jsx
│           ├── FileTree.jsx
│           ├── BuildConsole.jsx
│           ├── PlatformPackages.jsx
│           └── LearningStore.jsx
├── tests/
│   ├── test_platform_guards.py
│   ├── test_architect_agent.py
│   ├── test_cpp_generator.py
│   ├── test_blueprint_generator.py
│   ├── test_build_runner.py
│   ├── test_repair_loop.py
│   └── integration/
│       └── test_full_pipeline.py
├── .vscode/
│   ├── settings.json
│   ├── extensions.json
│   ├── launch.json
│   ├── tasks.json
│   └── forge.code-workspace
├── output/                          # Generated projects
├── .dedup/                          # Deduplication store
├── docker-compose.yml
├── .env.example
├── PRIVATE_LICENSE.md
├── README.md
└── tasks.md
```

---

## 13. CRITICAL PATH ANALYSIS

### Build Critical Path (7 hops)
```
contracts → architect_agent → brief_parser → project_scaffolder 
→ cpp_generator → build_runner → package_agent
```

### Widest Parallel Point
**Level 7:** ~12 files generated in parallel
- 7 server API modules
- 3 Celery workers
- 6 dashboard pages

### Estimated Compile Time (7950X)
| Phase | Time |
|-------|------|
| UHT dry-run | ~30 sec |
| UBT full compile | 4-6 min |
| Automation tests | 2-3 min |
| Platform packaging (Win64) | 3-5 min |
| **Total** | **~10-15 min** |

---

## 14. SECURITY ARCHITECTURE

### Authentication
- JWT tokens for API access
- API key for service-to-service communication
- Role-based access: `admin`, `developer`, `viewer`

### Secrets Management
- All secrets in environment variables (`.env`)
- Never commit `.env` — use `.env.example` template
- SDK paths and credentials injected at runtime only

### Audit Logging
- All API requests logged with timestamp, user, action
- Critic gate results stored in `critic-log` endpoint
- Repair attempts tracked per file

---

*End of Architecture Specification*
