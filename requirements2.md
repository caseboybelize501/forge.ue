# FORGE — Code Generation Requirements (Phase 10)

## 1. OVERVIEW

This document specifies requirements for **sequential code generation** following completion of all 9 planning phases. All stub files exist; this phase replaces stubs with working implementations.

**Prerequisite:** `critic_final.md` must say **APPROVED** ✓

---

## 2. CODE GENERATION PRINCIPLES

### 2.1 Sequential Generation Rule

> "Begin sequential code generation. One file at a time."

**Implementation Order:**
1. Level 0 — Contracts (immutable foundation)
2. Level 1 — Core Agents + Scanners
3. Level 2 — Test Generation + Brief Parsing
4. Level 3 — Project Scaffolding
5. Level 4 — Code Generation
6. Level 5 — Build Execution
7. Level 6 — Packaging + Store
8. Level 7 — Server + Dashboard
9. Level 8 — Server Entry Point
10. Level 9 — Tests
11. Level 10 — Infrastructure

### 2.2 Drift Detection Rule

> "After each file, check against forgeue.md. If drift is detected, stop. Do not patch forward. Return to the phase where drift originated. Regenerate from there."

**Drift Categories:**
| Drift Type | Detection Method | Return Phase |
|------------|------------------|--------------|
| Contract schema mismatch | Pydantic validation fails | Phase 1 (Requirements) |
| Missing import | Module import error | Phase 4 (Module Dependencies) |
| API endpoint mismatch | OpenAPI spec violation | Phase 1 (Requirements) |
| UE5 coding standard violation | UHT/UBT error | Phase 6 (Pre-Build Critic) |
| Platform guard missing | test_platform_guards.py fails | Phase 4 (Module Dependencies) |
| Dependency cycle | Import cycle detected | Phase 3 (Dependency Graph) |

### 2.3 No Patch Forward Rule

> "Do not patch forward."

**Meaning:** If file N has an error, do not fix it by modifying file N+1. Return to the root cause phase and regenerate.

**Example:**
- `engine/cpp_generator.py` has wrong import → Return to Phase 4 (module_dependencies.md)
- `server/api/projects.py` fails type check → Return to Phase 4 (module_dependencies.md)
- `contracts/models/game_brief.py` missing field → Return to Phase 1 (requirements.md)

---

## 3. LEVEL 0 — CONTRACTS (Replace Stub with Implementation)

### 3.1 Files to Implement (8 files)

| File | Stub Lines | Target Lines | Priority |
|------|------------|--------------|----------|
| `contracts/models/game_brief.py` | 64 | 120 | P0 |
| `contracts/models/project_spec.py` | 70 | 180 | P0 |
| `contracts/models/code_artifact.py` | 45 | 100 | P0 |
| `contracts/models/build_result.py` | 110 | 150 | P0 |
| `contracts/models/agent_message.py` | 40 | 90 | P0 |
| `contracts/models/platform_spec.py` | 43 | 110 | P0 |
| `contracts/models/store_spec.py` | 40 | 100 | P0 |
| `contracts/api.yaml` | 250 | 250 | P0 (already complete) |

### 3.2 Implementation Requirements

**game_brief.py:**
- [ ] Implement `Genre` enum with all 7 genres
- [ ] Implement `Platform` enum with all 7 platforms
- [ ] Implement `MechanicSpec` with validation
- [ ] Implement `GameBrief` with all required fields
- [ ] Implement `GameBriefRequest` for API
- [ ] Add field validators (priority 1-5, non-empty strings)

**project_spec.py:**
- [ ] Implement `ModuleType` enum (Core, GameFramework, GenreSystem, UI, Platform)
- [ ] Implement `SubsystemRef` enum (GAS, EnhancedInput, WorldPartition, etc.)
- [ ] Implement `ModuleSpec` with dependency validation
- [ ] Implement `Pattern` for learning store
- [ ] Implement `ProjectSpec` with cycle-free graph validation

**code_artifact.py:**
- [ ] Implement `CppFile` with path validation
- [ ] Implement `HeaderFile` with UCLASS name extraction
- [ ] Implement `BlueprintNode` with pin validation
- [ ] Implement `BlueprintGraph` with connection validation

**build_result.py:**
- [ ] Implement `ErrorReport` with file/line parsing
- [ ] Implement `RepairContext` with coding rules
- [ ] Implement `CompileResult` with timestamp
- [ ] Implement `TestSpec` with assertion types
- [ ] Implement `TestResult` with aggregation
- [ ] Implement `PackageResult` with platform tracking
- [ ] Implement API response models (ProjectResponse, TaskResponse, etc.)

**agent_message.py:**
- [ ] Implement `AgentTask` with priority queue support
- [ ] Implement `AgentResult` with duration tracking
- [ ] Implement `CriticResult` with pass/fail per category

**platform_spec.py:**
- [ ] Implement `PlatformTarget` enum (Win64, Mac, Android, iOS, PS5, Xbox, Switch)
- [ ] Implement `SDKStatus` enum (Available, Missing, Partial)
- [ ] Implement `PackageConfig` with cook/pak flags
- [ ] Implement `PlatformSpec` with SDK detection

**store_spec.py:**
- [ ] Implement `StoreAssets` with screenshot validation
- [ ] Implement `RatingConfig` with board-specific rules
- [ ] Implement `StoreSubmission` with store-specific configs

### 3.3 Validation Checklist (Per File)

After implementing each Level 0 file:
- [ ] File imports without errors
- [ ] All Pydantic models validate test data
- [ ] All enums have correct values
- [ ] Type hints match module_dependencies.md
- [ ] Docstrings describe purpose and attributes
- [ ] No circular imports within contracts/

---

## 4. LEVEL 1 — CORE AGENTS + SCANNERS (Replace Stub with Implementation)

### 4.1 Files to Implement (5 files)

| File | Stub Lines | Target Lines | Priority |
|------|------------|--------------|----------|
| `ai/architect_agent.py` | 95 | 280 | P1 |
| `ai/test_agent.py` | 75 | 180 | P1 |
| `ai/repair_loop.py` | 95 | 220 | P1 |
| `engine/ue5_scanner.py` | 85 | 150 | P1 |
| `engine/learning_store.py` | 95 | 180 | P1 |

### 4.2 Implementation Requirements

**architect_agent.py:**
- [ ] Implement `design_architecture()` → ProjectSpec
- [ ] Implement `_select_subsystems()` based on genre
- [ ] Implement `_design_module_graph()` with cycle detection
- [ ] Implement `_allocate_languages()` (C++ vs Blueprint)
- [ ] Implement `_load_interface_headers()` from templates/
- [ ] Add LLM integration for architecture decisions

**test_agent.py:**
- [ ] Implement `generate_test_specs()` → List[TestSpec]
- [ ] Implement `_generate_cpp_test_specs()` for UE5 automation
- [ ] Implement `_generate_blueprint_test_specs()` for BP validation
- [ ] Implement `_generate_platform_guard_specs()` for safety

**repair_loop.py:**
- [ ] Implement `repair_file()` with max 3 attempts
- [ ] Implement `classify_error()` for UBT/UHT errors
- [ ] Implement `_build_repair_prompt()` with UE5 coding rules
- [ ] Implement `_validate_repair()` for fix verification
- [ ] Add LLM integration for repair generation

**ue5_scanner.py:**
- [ ] Implement `scan_ue5_install()` with version check (≥ 5.3)
- [ ] Implement `detect_platform_sdks()` for all 7 platforms
- [ ] Implement `_verify_ue5_version()` from Engine/Build/Build.version
- [ ] Implement `_find_ue5_root()` from UNREAL_ENGINE_ROOT env
- [ ] Implement `_check_sdk_path()` for each SDK env var

**learning_store.py:**
- [ ] Implement `store_pattern()` with JSON persistence
- [ ] Implement `get_patterns()` filtered by genre
- [ ] Implement `find_similar_project()` with similarity scoring
- [ ] Implement `_load_patterns()` from disk
- [ ] Implement `_save_patterns()` to disk
- [ ] Implement `_compute_similarity()` between briefs

### 4.3 Validation Checklist (Per File)

After implementing each Level 1 file:
- [ ] File imports without errors
- [ ] All class methods have implementations (no `pass`)
- [ ] Type hints match module_dependencies.md
- [ ] LLM integration points documented
- [ ] Error handling for missing files/paths
- [ ] Unit tests pass (if applicable)

---

## 5. GENERATION ORDER (Within Each Level)

**Rule:** Generate files in dependency order. A file can only be generated after all its dependencies are complete.

### Level 0 Order:
1. `contracts/models/game_brief.py` (no internal deps)
2. `contracts/models/platform_spec.py` (no internal deps)
3. `contracts/models/store_spec.py` (no internal deps)
4. `contracts/models/code_artifact.py` (no internal deps)
5. `contracts/models/build_result.py` (deps: code_artifact)
6. `contracts/models/agent_message.py` (no internal deps)
7. `contracts/models/project_spec.py` (deps: game_brief, build_result)
8. `contracts/models/__init__.py` (exports all above)
9. `contracts/__init__.py` (exports models)
10. `contracts/api.yaml` (already complete)

### Level 1 Order:
1. `engine/ue5_scanner.py` (deps: L0 only)
2. `engine/learning_store.py` (deps: L0 only)
3. `ai/test_agent.py` (deps: L0 only)
4. `ai/repair_loop.py` (deps: L0 only)
5. `ai/architect_agent.py` (deps: L0 + templates/)
6. `ai/__init__.py` (exports all ai/)
7. `engine/__init__.py` (exports all engine/)

---

## 6. DRIFT DETECTION CHECKLIST

After generating each file, verify against forgeue.md:

### 6.1 Contract Compliance
- [ ] All Hard Requirements (HR-01 to HR-05) still satisfied
- [ ] All Functional Requirements (FR-01 to FR-22) still covered
- [ ] All Non-Functional Requirements (NFR-01 to NFR-06) still supported

### 6.2 API Compliance
- [ ] All 9 API endpoints still implemented correctly
- [ ] Request/response models match contracts/api.yaml
- [ ] Error handling consistent across endpoints

### 6.3 UE5 Compliance
- [ ] All 10 interface headers still referenced correctly
- [ ] Platform guard macros used where required
- [ ] UE5 coding standards followed (UCLASS, UPROPERTY, UFUNCTION)

### 6.4 Dependency Compliance
- [ ] Import statements match module_dependencies.md
- [ ] No new circular dependencies introduced
- [ ] Topological order preserved

---

## 7. HALT CONDITIONS

Stop code generation immediately if any of the following occur:

| Condition | Action |
|-----------|--------|
| Import error in generated file | Return to Phase 4 (Module Dependencies) |
| Pydantic validation fails | Return to Phase 1 (Requirements) |
| UHT/UBT error in generated C++ | Return to Phase 6 (Pre-Build Critic) |
| API endpoint mismatch | Return to Phase 1 (Requirements) |
| Platform guard missing | Return to Phase 4 (Module Dependencies) |
| Dependency cycle detected | Return to Phase 3 (Dependency Graph) |
| Critic gate fails | Return to Phase 6 (Pre-Build Critic) |

**Do not patch forward.** Return to root cause phase and regenerate.

---

## 8. SUCCESS CRITERIA

Code generation is complete when:

- [ ] All 112 stub files replaced with working implementations
- [ ] All imports resolve without errors
- [ ] All Pydantic models validate test data
- [ ] All API endpoints respond correctly
- [ ] All unit tests pass
- [ ] Integration test (test_full_pipeline.py) passes
- [ ] Server starts and responds to `/health`
- [ ] Dashboard builds without errors
- [ ] Generated UE5 project compiles with UBT
- [ ] Packaged binaries created for at least Win64

---

## 9. NEXT FILE TO GENERATE

**File:** `contracts/models/game_brief.py`  
**Level:** 0  
**Dependencies:** None (foundation file)  
**Target Lines:** 120  
**Stub Lines:** 64  

**Implementation Notes:**
- Add `GameBriefRequest` schema (missing in stub)
- Add field validators for priority (1-5), non-empty strings
- Ensure all enums match forgeue.md genre/platform lists
- Export in `contracts/models/__init__.py`

---

*End of Code Generation Requirements*
