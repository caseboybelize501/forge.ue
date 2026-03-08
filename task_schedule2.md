# FORGE — Code Generation Task Schedule (task_schedule2.md)

## 1. OVERVIEW

This document breaks down all **101 code generation files** from `file_manifest2.md` into atomic, executable tasks with explicit dependencies. Based on `critic_prebuild2.md` approval and `dependency_graph2.md` generation order.

**Total Tasks:** 101 (one per code generation file)  
**Generation Phases:** 15 (L0 through L9)  
**Max Parallel:** 10 tasks (Phase 1 — L0)  
**Estimated Total Time:** ~40 hours

---

## 2. TASK DEPENDENCY MODEL

### 2.1 Task Schema

```yaml
task_id: string          # Unique identifier (e.g., "CG-L0-01")
file_path: string        # Target file path
phase: integer           # Generation phase (1-15)
dependencies: string[]   # Task IDs that must complete first
stub_lines: integer      # Current stub line count
target_lines: integer    # Target implementation line count
estimated_minutes: integer  # Estimated implementation time
task_type: enum          # contract, agent, engine, api, worker, model, dashboard, test
parallel_group: string   # Parallel execution group identifier
```

### 2.2 Dependency Rules

1. **Phase N tasks depend on all Phase N-1 tasks** in their dependency chain
2. **Same-phase tasks can run in parallel** if no inter-dependencies exist
3. **L0 tasks have no dependencies** (foundation layer)
4. **Infrastructure tasks already complete** (no generation needed)

### 2.3 Generation Principles (from critic_prebuild2.md)

> "Begin sequential code generation. One file at a time. After each file, check against forgeue.md. If drift is detected, stop. Do not patch forward. Return to the phase where drift originated. Regenerate from there."

**Implementation:**
- Generate files in topological order (dependency_graph2.md §5.2)
- Validate each file after generation
- Run phase validation gate before proceeding to next phase
- If drift detected: return to root cause phase (requirements2.md §6)

---

## 3. PHASE 1 — CONTRACTS (L0 Foundation)

**Parallel Group:** `phase_1_contracts`  
**Tasks:** 10  
**Dependencies:** None  
**Estimated Time:** 4 hours  
**Validation Gate:** Pydantic model validation + import check

### 3.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L0-01 | `contracts/models/game_brief.py` | 64 | 120 | 30 | None | p1_l0_models |
| CG-L0-02 | `contracts/models/platform_spec.py` | 43 | 110 | 30 | None | p1_l0_models |
| CG-L0-03 | `contracts/models/store_spec.py` | 40 | 100 | 25 | None | p1_l0_models |
| CG-L0-04 | `contracts/models/code_artifact.py` | 45 | 100 | 25 | None | p1_l0_models |
| CG-L0-05 | `contracts/models/build_result.py` | 110 | 150 | 35 | CG-L0-04 | p1_l0_models |
| CG-L0-06 | `contracts/models/agent_message.py` | 40 | 90 | 25 | None | p1_l0_models |
| CG-L0-07 | `contracts/models/project_spec.py` | 70 | 180 | 45 | CG-L0-01, CG-L0-05 | p1_l0_models |
| CG-L0-08 | `contracts/models/__init__.py` | 36 | 50 | 15 | CG-L0-01 to CG-L0-07 | p1_l0_export |
| CG-L0-09 | `contracts/__init__.py` | 28 | 30 | 10 | CG-L0-08 | p1_l0_export |
| CG-L0-10 | `contracts/api.yaml` | 250 | 250 | 0 | None | p1_l0_complete |

**Note:** CG-L0-10 (api.yaml) already complete — 0 minutes.

### 3.2 Parallel Execution Plan

```
T0:    [CG-L0-01, CG-L0-02, CG-L0-03, CG-L0-04, CG-L0-06] — 5 tasks parallel (no deps)
       │
T+30m: [CG-L0-05] — depends on CG-L0-04
       │
T+60m: [CG-L0-07] — depends on CG-L0-01, CG-L0-05
       │
T+105m:[CG-L0-08] — depends on all models
       │
T+120m:[CG-L0-09] — depends on CG-L0-08
       │
T+130m:[CG-L0-10] — already complete (skip)
       │
T+130m:PHASE 1 COMPLETE → Validation Gate
```

### 3.3 Validation Gate (Phase 1)

```python
def validate_phase_1_contracts() -> ValidationResult:
    """
    Validate all Phase 1 contract files.
    
    Checks:
    - All files import without errors
    - All Pydantic models validate test data
    - All enums have correct values
    - __init__.py exports are complete
    - No circular imports
    """
    result = ValidationResult()
    
    # Import check
    for file in PHASE_1_FILES:
        try:
            import_module(file.path)
        except ImportError as e:
            result.add_error(f"Import error in {file.path}: {e}")
    
    # Pydantic validation
    test_data = load_test_fixtures()
    for model in PYDANTIC_MODELS:
        try:
            model(**test_data[model.__name__])
        except ValidationError as e:
            result.add_error(f"Validation error in {model.__name__}: {e}")
    
    # Enum check
    for enum_class in [Genre, Platform, ModuleType, SubsystemRef]:
        expected_values = get_expected_enum_values(enum_class)
        actual_values = [e.value for e in enum_class]
        if set(expected_values) != set(actual_values):
            result.add_error(f"Enum {enum_class.__name__} mismatch")
    
    return result
```

---

## 4. PHASE 2 — CORE AGENTS + SCANNERS (L1)

**Parallel Group:** `phase_2_core_agents`  
**Tasks:** 7  
**Dependencies:** All Phase 1 tasks complete  
**Estimated Time:** 5 hours  
**Validation Gate:** Import check + type check (mypy)

### 4.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L1-01 | `engine/ue5_scanner.py` | 85 | 150 | 45 | CG-L0-09 | p2_l1_engine |
| CG-L1-02 | `engine/learning_store.py` | 95 | 180 | 50 | CG-L0-09 | p2_l1_engine |
| CG-L1-03 | `ai/test_agent.py` | 75 | 180 | 50 | CG-L0-09 | p2_l1_ai |
| CG-L1-04 | `ai/repair_loop.py` | 95 | 220 | 60 | CG-L0-09 | p2_l1_ai |
| CG-L1-05 | `ai/architect_agent.py` | 95 | 280 | 75 | CG-L0-09 | p2_l1_ai |
| CG-L1-06 | `ai/__init__.py` | 14 | 20 | 10 | CG-L1-03, CG-L1-04, CG-L1-05 | p2_l1_export |
| CG-L1-07 | `engine/__init__.py` | 24 | 30 | 10 | CG-L1-01, CG-L1-02 | p2_l1_export |

### 4.2 Parallel Execution Plan

```
Phase 1 Complete
       │
       ▼
T0:    [CG-L1-01, CG-L1-02, CG-L1-03, CG-L1-04, CG-L1-05] — 5 tasks parallel
       │
T+75m: [CG-L1-06, CG-L1-07] — 2 tasks parallel (exports)
       │
T+85m: PHASE 2 COMPLETE → Validation Gate
```

### 4.3 Validation Gate (Phase 2)

```python
def validate_phase_2_agents() -> ValidationResult:
    """
    Validate all Phase 2 agent files.
    
    Checks:
    - All files import without errors
    - Type hints are correct (mypy)
    - Agent classes instantiate correctly
    - Method signatures match stubs
    """
    result = ValidationResult()
    
    # Import check
    modules = [
        'engine.ue5_scanner',
        'engine.learning_store',
        'ai.test_agent',
        'ai.repair_loop',
        'ai.architect_agent',
    ]
    for module in modules:
        try:
            import_module(module)
        except ImportError as e:
            result.add_error(f"Import error in {module}: {e}")
    
    # Type check
    mypy_result = run_mypy(['engine/', 'ai/'])
    if mypy_result.errors:
        result.add_errors(mypy_result.errors)
    
    # Instantiation check
    try:
        agent = ArchitectAgent(templates_dir=Path('templates'))
        assert hasattr(agent, 'design_architecture')
    except Exception as e:
        result.add_error(f"ArchitectAgent instantiation failed: {e}")
    
    return result
```

---

## 5. PHASE 3 — TEST GENERATION + PARSING (L2)

**Parallel Group:** `phase_3_test_gen`  
**Tasks:** 5  
**Dependencies:** All Phase 2 tasks complete  
**Estimated Time:** 3 hours  
**Validation Gate:** Import check + unit test generation

### 5.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L2-01 | `ai/test_generation/cpp_test_generator.py` | 80 | 200 | 55 | CG-L0-09, CG-L1-03 | p3_l2_test |
| CG-L2-02 | `ai/test_generation/blueprint_test_validator.py` | 75 | 180 | 50 | CG-L0-09, CG-L1-03 | p3_l2_test |
| CG-L2-03 | `ai/test_generation/test_harness.py` | 70 | 150 | 45 | CG-L0-09, CG-L1-03 | p3_l2_test |
| CG-L2-04 | `ai/test_generation/__init__.py` | 14 | 20 | 10 | CG-L2-01, CG-L2-02, CG-L2-03 | p3_l2_export |
| CG-L2-05 | `engine/brief_parser.py` | 85 | 160 | 50 | CG-L0-09, CG-L1-05 | p3_l2_engine |

### 5.2 Parallel Execution Plan

```
Phase 2 Complete
       │
       ▼
T0:    [CG-L2-01, CG-L2-02, CG-L2-03, CG-L2-05] — 4 tasks parallel
       │
T+55m: [CG-L2-04] — export file
       │
T+65m: PHASE 3 COMPLETE → Validation Gate
```

### 5.3 Validation Gate (Phase 3)

```python
def validate_phase_3_test_gen() -> ValidationResult:
    """
    Validate all Phase 3 test generation files.
    
    Checks:
    - All files import without errors
    - Test generators produce valid TestSpec
    - Brief parser extracts GameBrief from raw text
    """
    result = ValidationResult()
    
    # Import check
    modules = [
        'ai.test_generation.cpp_test_generator',
        'ai.test_generation.blueprint_test_validator',
        'ai.test_generation.test_harness',
        'engine.brief_parser',
    ]
    for module in modules:
        try:
            import_module(module)
        except ImportError as e:
            result.add_error(f"Import error in {module}: {e}")
    
    # Test spec generation check
    from ai.test_agent import TestAgent
    from contracts.models.project_spec import ProjectSpec
    
    test_agent = TestAgent(output_dir=Path('output'))
    test_specs = test_agent.generate_test_specs(sample_project_spec)
    
    for spec in test_specs:
        if not spec.test_name or not spec.test_type:
            result.add_error(f"Invalid test spec: {spec}")
    
    return result
```

---

## 6. PHASE 4 — PROJECT SCAFFOLDING (L3)

**Parallel Group:** `phase_4_scaffold`  
**Tasks:** 2  
**Dependencies:** All Phase 3 tasks complete  
**Estimated Time:** 1.5 hours  
**Validation Gate:** Project structure validation

### 6.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L3-01 | `engine/project_scaffolder.py` | 110 | 250 | 80 | CG-L0-09, CG-L2-05 | p4_l3_engine |
| CG-L3-02 | `templates/__init__.py` | 10 | 10 | 0 | None | p4_l3_complete |

**Note:** CG-L3-02 (templates/__init__.py) already complete — 0 minutes.

### 6.2 Parallel Execution Plan

```
Phase 3 Complete
       │
       ▼
T0:    [CG-L3-01] — single task
       │
T+80m: [CG-L3-02] — already complete (skip)
       │
T+80m: PHASE 4 COMPLETE → Validation Gate
```

### 6.3 Validation Gate (Phase 4)

```python
def validate_phase_4_scaffold() -> ValidationResult:
    """
    Validate all Phase 4 scaffolding files.
    
    Checks:
    - Project scaffolder creates valid directory structure
    - Generated .uproject is valid JSON
    - Generated Build.cs compiles
    - Generated .ini configs are valid
    """
    result = ValidationResult()
    
    from engine.project_scaffolder import ProjectScaffolder
    from contracts.models.game_brief import GameBrief
    from contracts.models.project_spec import ProjectSpec
    
    scaffolder = ProjectScaffolder(output_base=Path('output'))
    
    # Create test project
    test_brief = GameBrief(
        title="TestProject",
        genre=Genre.ACTION,
        platforms=[Platform.PC],
        mechanics=[],
        description="Test"
    )
    test_spec = ProjectSpec(...)  # Sample spec
    
    project_path = scaffolder.scaffold_project(test_brief, test_spec)
    
    # Validate structure
    required_dirs = ['Source', 'Content', 'Config']
    for dir_name in required_dirs:
        if not (project_path / dir_name).exists():
            result.add_error(f"Missing directory: {dir_name}")
    
    # Validate .uproject
    uproject_file = project_path / "TestProject.uproject"
    try:
        with open(uproject_file) as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        result.add_error(f"Invalid .uproject: {e}")
    
    return result
```

---

## 7. PHASE 5 — CODE GENERATION (L4)

**Parallel Group:** `phase_5_codegen`  
**Tasks:** 4  
**Dependencies:** All Phase 4 tasks complete  
**Estimated Time:** 4 hours  
**Validation Gate:** C++ header validation + UHT dry-run

### 7.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L4-01 | `engine/cpp_generator.py` | 123 | 320 | 90 | CG-L0-09, CG-L3-01 | p5_l4_engine |
| CG-L4-02 | `engine/blueprint_generator.py` | 105 | 280 | 80 | CG-L0-09, CG-L3-01 | p5_l4_engine |
| CG-L4-03 | `engine/platform_guards.py` | 95 | 140 | 45 | CG-L0-09 | p5_l4_engine |
| CG-L4-04 | `engine/__init__.py` (update) | 24 | 30 | 10 | CG-L4-01, CG-L4-02, CG-L4-03 | p5_l4_export |

### 7.2 Parallel Execution Plan

```
Phase 4 Complete
       │
       ▼
T0:    [CG-L4-01, CG-L4-02, CG-L4-03] — 3 tasks parallel
       │
T+90m: [CG-L4-04] — export update
       │
T+100m:PHASE 5 COMPLETE → Validation Gate
```

### 7.3 Validation Gate (Phase 5)

```python
def validate_phase_5_codegen() -> ValidationResult:
    """
    Validate all Phase 5 code generation files.
    
    Checks:
    - C++ generator produces valid UE5 headers
    - Blueprint generator produces valid JSON
    - Platform guards inject correct macros
    - Generated headers pass UHT dry-run
    """
    result = ValidationResult()
    
    from engine.cpp_generator import CppGenerator
    from engine.blueprint_generator import BlueprintGenerator
    from engine.platform_guards import PlatformGuards
    
    # C++ header validation
    cpp_gen = CppGenerator(scaffolder=None)
    header = cpp_gen._generate_header(sample_module, "TestCharacter")
    
    required_macros = ['UCLASS', 'GENERATED_BODY', 'UPROPERTY', 'UFUNCTION']
    for macro in required_macros:
        if macro not in header.content:
            result.add_error(f"Missing macro {macro} in generated header")
    
    # Blueprint JSON validation
    bp_gen = BlueprintGenerator(scaffolder=None)
    bp_graph = bp_gen.generate_blueprint(sample_spec, "TestSystem")
    
    # Validate JSON structure
    if not bp_graph.nodes or not bp_graph.connections:
        result.add_error("Invalid Blueprint graph structure")
    
    # Platform guards validation
    guards = PlatformGuards()
    guarded_code = guards.wrap_code("SDK_CODE", Platform.PS5)
    
    if "#if PLATFORM_PS5" not in guarded_code:
        result.add_error("Platform guard not injected correctly")
    
    return result
```

---

## 8. PHASE 6 — BUILD EXECUTION (L5)

**Parallel Group:** `phase_6_build`  
**Tasks:** 2  
**Dependencies:** All Phase 5 tasks complete  
**Estimated Time:** 1.5 hours  
**Validation Gate:** Mock UBT compile + error parsing

### 8.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L5-01 | `engine/build_runner.py` | 110 | 280 | 80 | CG-L0-09, CG-L4-01, CG-L1-03 | p6_l5_engine |
| CG-L5-02 | `engine/__init__.py` (update) | 24 | 30 | 10 | CG-L5-01 | p6_l5_export |

### 8.2 Parallel Execution Plan

```
Phase 5 Complete
       │
       ▼
T0:    [CG-L5-01] — single task
       │
T+80m: [CG-L5-02] — export update
       │
T+90m: PHASE 6 COMPLETE → Validation Gate
```

### 8.3 Validation Gate (Phase 6)

```python
def validate_phase_6_build() -> ValidationResult:
    """
    Validate all Phase 6 build execution files.
    
    Checks:
    - Build runner invokes UHT correctly
    - Build runner invokes UBT correctly
    - Error parser extracts file/line/message
    - Test runner captures results
    """
    result = ValidationResult()
    
    from engine.build_runner import BuildRunner
    from contracts.models.build_result import CompileResult
    
    runner = BuildRunner(ue_root=Path('/mock/ue5'))
    
    # Mock UHT run
    uht_result = runner.run_uht(project_path=Path('/mock/project'))
    
    if not isinstance(uht_result, CompileResult):
        result.add_error("UHT result is not CompileResult")
    
    # Error parsing check
    mock_stderr = "D:\\Project\\Source\\Test.cpp(42): error: syntax error"
    errors = runner.parse_ubt_errors(mock_stderr)
    
    if len(errors) != 1:
        result.add_error(f"Expected 1 error, got {len(errors)}")
    elif errors[0].line_number != 42:
        result.add_error(f"Expected line 42, got {errors[0].line_number}")
    
    return result
```

---

## 9. PHASE 7 — PACKAGING + STORE (L6)

**Parallel Group:** `phase_7_package`  
**Tasks:** 3  
**Dependencies:** All Phase 6 tasks complete  
**Estimated Time:** 2.5 hours  
**Validation Gate:** Mock cook + pak validation

### 9.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L6-01 | `engine/package_agent.py` | 95 | 240 | 70 | CG-L0-09, CG-L5-01 | p7_l6_engine |
| CG-L6-02 | `engine/store_agent.py` | 90 | 200 | 60 | CG-L0-09, CG-L6-01 | p7_l6_engine |
| CG-L6-03 | `engine/__init__.py` (update) | 24 | 30 | 10 | CG-L6-01, CG-L6-02 | p7_l6_export |

### 9.2 Parallel Execution Plan

```
Phase 6 Complete
       │
       ▼
T0:    [CG-L6-01] — single task (CG-L6-02 depends on it)
       │
T+70m: [CG-L6-02] — depends on CG-L6-01
       │
T+130m:[CG-L6-03] — export update
       │
T+140m:PHASE 7 COMPLETE → Validation Gate
```

### 9.3 Validation Gate (Phase 7)

```python
def validate_phase_7_package() -> ValidationResult:
    """
    Validate all Phase 7 packaging files.
    
    Checks:
    - Package agent cooks content per platform
    - Package agent paks binaries correctly
    - Store agent generates Steam config
    - Store agent generates EGS config
    """
    result = ValidationResult()
    
    from engine.package_agent import PackageAgent
    from engine.store_agent import StoreAgent
    
    package_agent = PackageAgent(build_runner=None)
    store_agent = StoreAgent(package_agent=package_agent)
    
    # Mock package validation
    platforms = [PlatformTarget.WIN64, PlatformTarget.ANDROID]
    package_result = package_agent.package_project(
        project_path=Path('/mock/project'),
        platforms=platforms
    )
    
    if not package_result.success:
        result.add_warning("Package result not successful (expected for mock)")
    
    # Store config validation
    store_submission = store_agent.generate_submission(
        brief=sample_brief,
        package_result=package_result
    )
    
    if not store_submission.store or not store_submission.assets:
        result.add_error("Invalid store submission")
    
    return result
```

---

## 10. PHASE 8 — SERVER PYTHON (L7-Python)

**Parallel Group:** `phase_8_server_python`  
**Tasks:** 16  
**Dependencies:** All Phase 7 tasks complete  
**Estimated Time:** 6 hours  
**Validation Gate:** API endpoint tests + import check

### 10.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L7-01 | `server/api/projects.py` | 50 | 120 | 40 | CG-L0-09, CG-L2-05, CG-L3-01 | p8_l7_api |
| CG-L7-02 | `server/api/architecture.py` | 30 | 60 | 25 | CG-L0-09, CG-L1-05 | p8_l7_api |
| CG-L7-03 | `server/api/generation.py` | 60 | 140 | 45 | CG-L0-09, CG-L4-01, CG-L4-02, CG-L5-01 | p8_l7_api |
| CG-L7-04 | `server/api/builds.py` | 35 | 80 | 30 | CG-L0-09, CG-L5-01 | p8_l7_api |
| CG-L7-05 | `server/api/packages.py` | 52 | 100 | 35 | CG-L0-09, CG-L6-01 | p8_l7_api |
| CG-L7-06 | `server/api/store.py` | 35 | 70 | 30 | CG-L0-09, CG-L6-02 | p8_l7_api |
| CG-L7-07 | `server/api/auth.py` | 40 | 90 | 35 | CG-L0-09 | p8_l7_api |
| CG-L7-08 | `server/api/__init__.py` | 20 | 50 | 15 | CG-L7-01 to CG-L7-07 | p8_l7_api_export |
| CG-L7-09 | `server/workers/generation_worker.py` | 55 | 180 | 55 | CG-L0-09, CG-L2-05, CG-L3-01, CG-L4-01, CG-L4-02 | p8_l7_workers |
| CG-L7-10 | `server/workers/build_worker.py` | 40 | 100 | 35 | CG-L0-09, CG-L5-01 | p8_l7_workers |
| CG-L7-11 | `server/workers/package_worker.py` | 35 | 120 | 40 | CG-L0-09, CG-L6-01 | p8_l7_workers |
| CG-L7-12 | `server/workers/__init__.py` | 15 | 20 | 10 | CG-L7-09, CG-L7-10, CG-L7-11 | p8_l7_workers_export |
| CG-L7-13 | `server/models/database.py` | 30 | 80 | 30 | External only | p8_l7_models |
| CG-L7-14 | `server/models/project.py` | 45 | 60 | 25 | CG-L7-13 | p8_l7_models |
| CG-L7-15 | `server/models/build.py` | 35 | 50 | 20 | CG-L7-13 | p8_l7_models |
| CG-L7-16 | `server/models/__init__.py` | 20 | 20 | 10 | CG-L7-13, CG-L7-14, CG-L7-15 | p8_l7_models_export |

### 10.2 Parallel Execution Plan

```
Phase 7 Complete
       │
       ▼
T0:    [CG-L7-01, CG-L7-02, CG-L7-04, CG-L7-05, CG-L7-06, CG-L7-07, CG-L7-13] — 7 tasks parallel
       │
T+40m: [CG-L7-03] — depends on CG-L7-04 + L4/L5 modules
       │
T+55m: [CG-L7-09] — depends on L4 modules
       │
T+70m: [CG-L7-10, CG-L7-11] — depend on L5/L6
       │
T+80m: [CG-L7-14, CG-L7-15] — depend on CG-L7-13
       │
T+95m: [CG-L7-08, CG-L7-12, CG-L7-16] — export files
       │
T+105m:PHASE 8 COMPLETE → Validation Gate
```

### 10.3 Validation Gate (Phase 8)

```python
def validate_phase_8_server() -> ValidationResult:
    """
    Validate all Phase 8 server Python files.
    
    Checks:
    - All API endpoints import without errors
    - All workers import without errors
    - All models import without errors
    - API endpoints respond correctly (mock test)
    """
    result = ValidationResult()
    
    # Import check
    api_modules = [
        'server.api.projects',
        'server.api.architecture',
        'server.api.generation',
        'server.api.builds',
        'server.api.packages',
        'server.api.store',
        'server.api.auth',
    ]
    for module in api_modules:
        try:
            import_module(module)
        except ImportError as e:
            result.add_error(f"Import error in {module}: {e}")
    
    # Worker check
    worker_modules = [
        'server.workers.generation_worker',
        'server.workers.build_worker',
        'server.workers.package_worker',
    ]
    for module in worker_modules:
        try:
            import_module(module)
        except ImportError as e:
            result.add_error(f"Import error in {module}: {e}")
    
    # Model check
    model_modules = [
        'server.models.database',
        'server.models.project',
        'server.models.build',
    ]
    for module in model_modules:
        try:
            import_module(module)
        except ImportError as e:
            result.add_error(f"Import error in {module}: {e}")
    
    return result
```

---

## 11. PHASE 9 — DASHBOARD CONFIG (L7-JS-Config)

**Parallel Group:** `phase_9_dashboard_config`  
**Tasks:** 10  
**Dependencies:** All Phase 8 tasks complete (can run parallel with Phase 8)  
**Estimated Time:** 2 hours  
**Validation Gate:** npm install + build check

### 11.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L7-17 | `dashboard/package.json` | 25 | 60 | 15 | None | p9_l7_config |
| CG-L7-18 | `dashboard/vite.config.js` | 15 | 40 | 15 | None | p9_l7_config |
| CG-L7-19 | `dashboard/index.html` | 13 | 30 | 10 | None | p9_l7_config |
| CG-L7-20 | `dashboard/src/api/client.js` | 40 | 100 | 25 | None | p9_l7_api |
| CG-L7-21 | `dashboard/src/api/endpoints.js` | 45 | 80 | 20 | None | p9_l7_api |
| CG-L7-22 | `dashboard/src/api/index.js` | 12 | 40 | 10 | CG-L7-20, CG-L7-21 | p9_l7_api |
| CG-L7-34 | `dashboard/src/styles/variables.css` | 40 | 50 | 15 | None | p9_l7_styles |
| CG-L7-35 | `dashboard/src/styles/main.css` | 90 | 200 | 40 | CG-L7-34 | p9_l7_styles |
| CG-L7-21 | `dashboard/src/index.css` | 10 | 30 | 10 | CG-L7-34, CG-L7-35 | p9_l7_styles |
| CG-L7-44 | `dashboard/src/index.css` (duplicate fix) | 10 | 30 | 10 | CG-L7-34, CG-L7-35 | p9_l7_styles |

**Note:** Task IDs corrected from dependency_graph2.md numbering.

### 11.2 Parallel Execution Plan

```
Phase 8 Complete (or parallel)
       │
       ▼
T0:    [CG-L7-17, CG-L7-18, CG-L7-19, CG-L7-20, CG-L7-21, CG-L7-34] — 6 tasks parallel
       │
T+25m: [CG-L7-22] — depends on CG-L7-20, CG-L7-21
       │
T+55m: [CG-L7-35] — depends on CG-L7-34
       │
T+65m: [CG-L7-44] — depends on CG-L7-35
       │
T+75m: PHASE 9 COMPLETE → Validation Gate
```

### 11.3 Validation Gate (Phase 9)

```python
def validate_phase_9_dashboard_config() -> ValidationResult:
    """
    Validate all Phase 9 dashboard config files.
    
    Checks:
    - package.json has all dependencies
    - vite.config.js is valid
    - API client connects correctly
    - CSS builds without errors
    """
    result = ValidationResult()
    
    # package.json check
    with open('dashboard/package.json') as f:
        package_json = json.load(f)
    
    required_deps = ['react', 'react-dom', 'axios', 'react-router-dom']
    for dep in required_deps:
        if dep not in package_json.get('dependencies', {}):
            result.add_error(f"Missing dependency: {dep}")
    
    # vite.config.js check
    try:
        with open('dashboard/vite.config.js') as f:
            content = f.read()
        assert 'defineConfig' in content
        assert 'react' in content
    except (FileNotFoundError, AssertionError) as e:
        result.add_error(f"Invalid vite.config.js: {e}")
    
    return result
```

---

## 12. PHASE 10 — DASHBOARD COMPONENTS (L7-JS-Comp)

**Parallel Group:** `phase_10_dashboard_components`  
**Tasks:** 8  
**Dependencies:** All Phase 9 tasks complete  
**Estimated Time:** 2 hours  
**Validation Gate:** ESLint + component render check

### 12.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L7-23 | `dashboard/src/components/Header.jsx` | 20 | 40 | 20 | None | p10_l7_comp |
| CG-L7-24 | `dashboard/src/components/Sidebar.jsx` | 20 | 60 | 25 | None | p10_l7_comp |
| CG-L7-25 | `dashboard/src/components/ProgressBar.jsx` | 25 | 50 | 20 | None | p10_l7_comp |
| CG-L7-26 | `dashboard/src/components/FileNode.jsx` | 35 | 70 | 25 | None | p10_l7_comp |
| CG-L7-27 | `dashboard/src/components/ConsoleOutput.jsx` | 35 | 80 | 30 | None | p10_l7_comp |
| CG-L7-28 | `dashboard/src/components/StatusBadge.jsx` | 18 | 35 | 15 | None | p10_l7_comp |
| CG-L7-29 | `dashboard/src/components/DownloadButton.jsx` | 30 | 40 | 20 | None | p10_l7_comp |
| CG-L7-30 | `dashboard/src/components/index.js` | 12 | 30 | 10 | CG-L7-23 to CG-L7-29 | p10_l7_export |

### 12.2 Parallel Execution Plan

```
Phase 9 Complete
       │
       ▼
T0:    [CG-L7-23, CG-L7-24, CG-L7-25, CG-L7-26, CG-L7-27, CG-L7-28, CG-L7-29] — 7 tasks parallel
       │
T+30m: [CG-L7-30] — export file
       │
T+40m: PHASE 10 COMPLETE → Validation Gate
```

---

## 13. PHASE 11 — DASHBOARD HOOKS (L7-JS-Hooks)

**Parallel Group:** `phase_11_dashboard_hooks`  
**Tasks:** 3  
**Dependencies:** All Phase 9 tasks complete (API must exist)  
**Estimated Time:** 1 hour  
**Validation Gate:** Hook functionality test

### 13.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L7-31 | `dashboard/src/hooks/useProject.js` | 35 | 60 | 25 | CG-L7-20 | p11_l7_hooks |
| CG-L7-32 | `dashboard/src/hooks/useBuild.js` | 35 | 50 | 20 | CG-L7-20 | p11_l7_hooks |
| CG-L7-33 | `dashboard/src/hooks/index.js` | 8 | 20 | 10 | CG-L7-31, CG-L7-32 | p11_l7_export |

### 13.2 Parallel Execution Plan

```
Phase 9 Complete (API)
       │
       ▼
T0:    [CG-L7-31, CG-L7-32] — 2 tasks parallel
       │
T+25m: [CG-L7-33] — export file
       │
T+35m: PHASE 11 COMPLETE → Validation Gate
```

---

## 14. PHASE 12 — DASHBOARD PAGES (L7-JS-Pages)

**Parallel Group:** `phase_12_dashboard_pages`  
**Tasks:** 6  
**Dependencies:** Phases 9, 10, 11 complete  
**Estimated Time:** 3 hours  
**Validation Gate:** Page render check + routing test

### 14.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L7-36 | `dashboard/src/pages/ProjectBrief.jsx` | 64 | 150 | 40 | CG-L7-20, CG-L7-21 | p12_l7_pages |
| CG-L7-37 | `dashboard/src/pages/GenerationProgress.jsx` | 55 | 120 | 35 | CG-L7-20, CG-L7-21 | p12_l7_pages |
| CG-L7-38 | `dashboard/src/pages/FileTree.jsx` | 45 | 100 | 30 | CG-L7-20, CG-L7-21, CG-L7-26 | p12_l7_pages |
| CG-L7-39 | `dashboard/src/pages/BuildConsole.jsx` | 65 | 140 | 40 | CG-L7-20, CG-L7-21, CG-L7-27 | p12_l7_pages |
| CG-L7-40 | `dashboard/src/pages/PlatformPackages.jsx` | 70 | 130 | 35 | CG-L7-20, CG-L7-21, CG-L7-29 | p12_l7_pages |
| CG-L7-41 | `dashboard/src/pages/LearningStore.jsx` | 65 | 110 | 30 | CG-L7-20, CG-L7-21 | p12_l7_pages |

### 14.2 Parallel Execution Plan

```
Phases 9, 10, 11 Complete
       │
       ▼
T0:    [CG-L7-36, CG-L7-37, CG-L7-38, CG-L7-39, CG-L7-40, CG-L7-41] — 6 tasks parallel
       │
T+40m: PHASE 12 COMPLETE → Validation Gate
```

---

## 15. PHASE 13 — DASHBOARD APP ENTRY (L7-JS-App)

**Parallel Group:** `phase_13_dashboard_app`  
**Tasks:** 3  
**Dependencies:** Phases 10, 11, 12 complete  
**Estimated Time:** 1 hour  
**Validation Gate:** Full app build

### 15.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L7-42 | `dashboard/src/App.jsx` | 35 | 80 | 30 | CG-L7-36 to CG-L7-41, CG-L7-23, CG-L7-24 | p13_l7_app |
| CG-L7-43 | `dashboard/src/main.jsx` | 12 | 40 | 15 | CG-L7-42, CG-L7-44 | p13_l7_app |
| CG-L7-44 | `dashboard/src/index.css` | 10 | 30 | 10 | CG-L7-34, CG-L7-35 | p13_l7_app |

### 15.2 Parallel Execution Plan

```
Phases 10, 11, 12 Complete
       │
       ▼
T0:    [CG-L7-44] — CSS first
       │
T+10m: [CG-L7-42] — App.jsx
       │
T+40m: [CG-L7-43] — main.jsx (depends on App + CSS)
       │
T+55m: PHASE 13 COMPLETE → Validation Gate
```

### 15.3 Validation Gate (Phase 13)

```python
def validate_phase_13_dashboard_app() -> ValidationResult:
    """
    Validate all Phase 13 dashboard app entry files.
    
    Checks:
    - App.jsx imports all pages and components
    - main.jsx renders App correctly
    - Full dashboard build succeeds
    """
    result = ValidationResult()
    
    # App.jsx check
    with open('dashboard/src/App.jsx') as f:
        content = f.read()
    
    required_imports = [
        'ProjectBrief',
        'GenerationProgress',
        'FileTree',
        'BuildConsole',
        'PlatformPackages',
        'LearningStore',
        'Header',
        'Sidebar',
    ]
    for imp in required_imports:
        if imp not in content:
            result.add_error(f"Missing import in App.jsx: {imp}")
    
    # Build check
    build_result = run_command('cd dashboard && npm run build')
    if build_result.returncode != 0:
        result.add_error(f"Dashboard build failed: {build_result.stderr}")
    
    return result
```

---

## 16. PHASE 14 — SERVER ENTRY POINT (L8)

**Parallel Group:** `phase_14_server_entry`  
**Tasks:** 2  
**Dependencies:** Phase 8 complete  
**Estimated Time:** 30 minutes  
**Validation Gate:** Server health check

### 16.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L8-01 | `server/main.py` | 90 | 100 | 20 | CG-L7-08, CG-L7-12, CG-L7-16 | p14_l8_entry |
| CG-L8-02 | `server/__init__.py` | 10 | 10 | 0 | None | p14_l8_complete |

**Note:** CG-L8-02 already complete — 0 minutes.

### 16.2 Parallel Execution Plan

```
Phase 8 Complete
       │
       ▼
T0:    [CG-L8-01] — single task
       │
T+20m: [CG-L8-02] — already complete (skip)
       │
T+20m: PHASE 14 COMPLETE → Validation Gate
```

### 16.3 Validation Gate (Phase 14)

```python
def validate_phase_14_server_entry() -> ValidationResult:
    """
    Validate all Phase 14 server entry point files.
    
    Checks:
    - server/main.py imports all routers
    - Server starts without errors
    - /health endpoint responds
    """
    result = ValidationResult()
    
    # Import check
    try:
        from server.main import app
    except ImportError as e:
        result.add_error(f"server.main import failed: {e}")
        return result
    
    # Health check
    import httpx
    try:
        response = httpx.get('http://localhost:8000/health', timeout=5)
        if response.status_code != 200:
            result.add_error(f"Health endpoint returned {response.status_code}")
        elif response.json().get('status') != 'healthy':
            result.add_error("Health endpoint status not 'healthy'")
    except httpx.ConnectError:
        result.add_warning("Server not running (start for full validation)")
    
    return result
```

---

## 17. PHASE 15 — TESTS (L9)

**Parallel Group:** `phase_15_tests`  
**Tasks:** 12  
**Dependencies:** All previous phases complete  
**Estimated Time:** 4 hours  
**Validation Gate:** All tests pass

### 17.1 Task Breakdown

| Task ID | File Path | Stub | Target | Est. Min | Dependencies | Parallel Group |
|---------|-----------|------|--------|----------|--------------|----------------|
| CG-L9-01 | `tests/__init__.py` | 10 | 10 | 0 | None | p15_l9_complete |
| CG-L9-02 | `tests/conftest.py` | 60 | 80 | 30 | None | p15_l9_config |
| CG-L9-03 | `tests/test_platform_guards.py` | 45 | 120 | 40 | CG-L4-03 | p15_l9_test |
| CG-L9-04 | `tests/test_architect_agent.py` | 80 | 150 | 45 | CG-L1-05 | p15_l9_test |
| CG-L9-05 | `tests/test_cpp_generator.py` | 50 | 140 | 40 | CG-L4-01 | p15_l9_test |
| CG-L9-06 | `tests/test_blueprint_generator.py` | 50 | 130 | 40 | CG-L4-02 | p15_l9_test |
| CG-L9-07 | `tests/test_build_runner.py` | 55 | 160 | 45 | CG-L5-01 | p15_l9_test |
| CG-L9-08 | `tests/test_repair_loop.py` | 65 | 140 | 40 | CG-L1-04 | p15_l9_test |
| CG-L9-09 | `tests/test_dependency_graph.py` | 120 | 180 | 50 | None | p15_l9_test |
| CG-L9-10 | `tests/test_module_dependencies.py` | 60 | 120 | 35 | All modules | p15_l9_test |
| CG-L9-11 | `tests/integration/__init__.py` | 10 | 10 | 0 | None | p15_l9_complete |
| CG-L9-12 | `tests/integration/test_full_pipeline.py` | 70 | 250 | 60 | All modules | p15_l9_integration |

### 17.2 Parallel Execution Plan

```
All Previous Phases Complete
       │
       ▼
T0:    [CG-L9-02, CG-L9-03, CG-L9-04, CG-L9-05, CG-L9-06, CG-L9-07, CG-L9-08, CG-L9-09, CG-L9-10] — 9 tasks parallel
       │
T+50m: [CG-L9-12] — integration test (depends on all)
       │
T+110m:PHASE 15 COMPLETE → Validation Gate
```

### 17.3 Validation Gate (Phase 15)

```python
def validate_phase_15_tests() -> ValidationResult:
    """
    Validate all Phase 15 test files.
    
    Checks:
    - All test files import without errors
    - All unit tests pass
    - Integration test passes
    - Code coverage > 80%
    """
    result = ValidationResult()
    
    # Run all tests
    test_result = run_command('pytest tests/ -v --tb=short')
    
    if test_result.returncode != 0:
        result.add_error(f"Tests failed: {test_result.stdout}")
    
    # Check coverage
    coverage_result = run_command('pytest tests/ --cov=. --cov-report=term')
    
    coverage_line = extract_coverage_line(coverage_result.stdout)
    if coverage_line.percentage < 80:
        result.add_warning(f"Code coverage {coverage_line.percentage}% < 80%")
    
    return result
```

---

## 18. COMPLETE TASK CHAIN (Execution Order)

```python
from celery import chain, chord, group

def build_code_generation_pipeline():
    """
    Build complete Celery task chain for code generation.
    """
    return chain(
        # Phase 1 — Contracts (10 tasks, max 5 parallel)
        chord(
            group(
                CG_L0_01, CG_L0_02, CG_L0_03, CG_L0_04, CG_L0_06,  # no deps
                chord(
                    group(CG_L0_04),
                    CG_L0_05  # depends on CG-L0-04
                ),
                chord(
                    group(CG_L0_01, CG_L0_05),
                    CG_L0_07  # depends on CG-L0-01, CG-L0-05
                ),
            ),
            validate_phase_1.s()
        ),
        
        # Phase 2 — Core Agents (7 tasks, max 5 parallel)
        chord(
            group(CG_L1_01, CG_L1_02, CG_L1_03, CG_L1_04, CG_L1_05),
            chord(
                group(CG_L1_03, CG_L1_04, CG_L1_05),
                CG_L1_06  # ai/__init__.py
            ),
            validate_phase_2.s()
        ),
        
        # Phase 3 — Test Gen (5 tasks)
        chord(
            group(CG_L2_01, CG_L2_02, CG_L2_03, CG_L2_05),
            CG_L2_04,  # test_generation/__init__.py
            validate_phase_3.s()
        ),
        
        # Phase 4 — Scaffold (2 tasks)
        chord(
            group(CG_L3_01),
            CG_L3_02,  # already complete
            validate_phase_4.s()
        ),
        
        # Phase 5 — Code Gen (4 tasks)
        chord(
            group(CG_L4_01, CG_L4_02, CG_L4_03),
            CG_L4_04,  # engine/__init__.py update
            validate_phase_5.s()
        ),
        
        # Phase 6 — Build (2 tasks)
        chord(
            group(CG_L5_01),
            CG_L5_02,  # engine/__init__.py update
            validate_phase_6.s()
        ),
        
        # Phase 7 — Package (3 tasks)
        chord(
            group(CG_L6_01),
            chord(
                group(CG_L6_01),
                CG_L6_02  # depends on CG-L6-01
            ),
            CG_L6_03,  # engine/__init__.py update
            validate_phase_7.s()
        ),
        
        # Phase 8 — Server Python (16 tasks)
        chord(
            group(
                CG_L7_01, CG_L7_02, CG_L7_04, CG_L7_05, CG_L7_06, CG_L7_07, CG_L7_13,
                chord(group(CG_L7_04, CG_L4_01, CG_L4_02, CG_L5_01), CG_L7_03),
                chord(group(CG_L4_01, CG_L4_02), CG_L7_09),
                chord(group(CG_L5_01), CG_L7_10),
                chord(group(CG_L6_01), CG_L7_11),
                chord(group(CG_L7_13), CG_L7_14, CG_L7_15),
            ),
            group(CG_L7_08, CG_L7_12, CG_L7_16),
            validate_phase_8.s()
        ),
        
        # Phase 9-13 — Dashboard (30 tasks, can run parallel with Phase 8)
        # ... (similar structure)
        
        # Phase 14 — Server Entry (2 tasks)
        chord(
            group(CG_L8_01),
            CG_L8_02,  # already complete
            validate_phase_14.s()
        ),
        
        # Phase 15 — Tests (12 tasks)
        chord(
            group(
                CG_L9_02, CG_L9_03, CG_L9_04, CG_L9_05, CG_L9_06,
                CG_L9_07, CG_L9_08, CG_L9_09, CG_L9_10,
            ),
            CG_L9_12,  # integration test
            validate_phase_15.s()
        ),
        
        # Final gate
        finalize_code_generation.s()
    )
```

---

## 19. EXECUTION TIMELINE

| Phase | Tasks | Parallel Count | Est. Time | Cumulative |
|-------|-------|----------------|-----------|------------|
| P1 — Contracts | 10 | 5 | 4h | 4h |
| P2 — Core Agents | 7 | 5 | 5h | 9h |
| P3 — Test Gen | 5 | 4 | 3h | 12h |
| P4 — Scaffold | 2 | 1 | 1.5h | 13.5h |
| P5 — Code Gen | 4 | 3 | 4h | 17.5h |
| P6 — Build | 2 | 1 | 1.5h | 19h |
| P7 — Package | 3 | 1 | 2.5h | 21.5h |
| P8 — Server Py | 16 | 7 | 6h | 27.5h |
| P9 — Dash Config | 10 | 6 | 2h | 29.5h |
| P10 — Dash Comp | 8 | 7 | 2h | 31.5h |
| P11 — Dash Hooks | 3 | 2 | 1h | 32.5h |
| P12 — Dash Pages | 6 | 6 | 3h | 35.5h |
| P13 — Dash App | 3 | 1 | 1h | 36.5h |
| P14 — Server Entry | 2 | 1 | 0.5h | 37h |
| P15 — Tests | 12 | 9 | 4h | 41h |

**Total Estimated Time:** ~41 hours (with parallel execution)

**Critical Path:** P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P14 → P15

---

## 20. NEXT ACTION

**Immediate Next Task:** CG-L0-01 — `contracts/models/game_brief.py`

**Implementation Checklist:**
- [ ] Read existing stub (64 lines)
- [ ] Add `field_validator` import from pydantic
- [ ] Add `GameBriefRequest` schema
- [ ] Add field validators for priority (1-5), non-empty strings
- [ ] Ensure all enums match forgeue.md genre/platform lists
- [ ] Run: `python -c "from contracts.models.game_brief import GameBrief"`
- [ ] Verify against forgeue.md
- [ ] Mark complete in status board
- [ ] Proceed to CG-L0-02 through CG-L0-06 (parallel)

---

*End of Code Generation Task Schedule*
