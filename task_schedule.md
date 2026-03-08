# FORGE — Task Schedule

## 1. OVERVIEW

This document breaks down all **137 files** from `file_manifest.md` into atomic, executable tasks with explicit dependencies. Tasks are organized by topological level and sequenced for optimal parallel execution.

**Total Tasks:** 137 (one per file)  
**Critical Path:** 9 phases (L0 → L8)  
**Max Parallel:** 44 tasks (Level 7)

---

## 2. TASK DEPENDENCY MODEL

### Task Schema

```yaml
task_id: string          # Unique identifier (e.g., "L0-001")
file_path: string        # Target file path
phase: integer           # Topological level (0-8)
dependencies: string[]   # Task IDs that must complete first
estimated_lines: integer # Expected line count
task_type: enum          # contract, agent, engine, server, dashboard, test, infra
parallel_group: string   # Parallel execution group identifier
```

### Dependency Rules

1. **Level N tasks depend on all Level N-1 tasks** in their dependency chain
2. **Same-level tasks can run in parallel** if no inter-dependencies exist
3. **L0 tasks have no dependencies** (foundation layer)
4. **Infrastructure tasks can run anytime after L0**

---

## 3. PHASE 0 — CONTRACTS (Immutable Foundation)

**Parallel Group:** `phase_0_foundation`  
**Tasks:** 18  
**Dependencies:** None  
**Estimated Time:** 2 hours (manual review after generation)

### 3.1 contracts/models/ (7 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L0-001 | `contracts/models/game_brief.py` | 120 | None | phase_0_models |
| L0-002 | `contracts/models/project_spec.py` | 180 | None | phase_0_models |
| L0-003 | `contracts/models/code_artifact.py` | 100 | None | phase_0_models |
| L0-004 | `contracts/models/build_result.py` | 150 | None | phase_0_models |
| L0-005 | `contracts/models/agent_message.py` | 90 | None | phase_0_models |
| L0-006 | `contracts/models/platform_spec.py` | 110 | None | phase_0_models |
| L0-007 | `contracts/models/store_spec.py` | 100 | None | phase_0_models |

**Generation Order:** All 7 can be generated in parallel.

### 3.2 contracts/ (1 task)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L0-008 | `contracts/api.yaml` | 250 | None | phase_0_api |

### 3.3 templates/interfaces/ (10 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L0-009 | `templates/interfaces/IForgeGameMode.h` | 45 | None | phase_0_interfaces |
| L0-010 | `templates/interfaces/IForgeCharacter.h` | 55 | None | phase_0_interfaces |
| L0-011 | `templates/interfaces/IForgeGameInstance.h` | 50 | None | phase_0_interfaces |
| L0-012 | `templates/interfaces/IForgeInventory.h` | 60 | None | phase_0_interfaces |
| L0-013 | `templates/interfaces/IForgeSaveGame.h` | 40 | None | phase_0_interfaces |
| L0-014 | `templates/interfaces/IForgeUIManager.h` | 50 | None | phase_0_interfaces |
| L0-015 | `templates/interfaces/IForgeAudioManager.h` | 45 | None | phase_0_interfaces |
| L0-016 | `templates/interfaces/IForgeAchievement.h` | 40 | None | phase_0_interfaces |
| L0-017 | `templates/interfaces/IForgePlatformLayer.h` | 55 | None | phase_0_interfaces |
| L0-018 | `templates/interfaces/IForgeOnlineSubsystem.h` | 65 | None | phase_0_interfaces |

**Generation Order:** All 10 can be generated in parallel.

### Phase 0 Task Chain

```
chord(
    group(
        L0-001, L0-002, L0-003, L0-004, L0-005, L0-006, L0-007,  # models/
        L0-008,  # api.yaml
        L0-009, L0-010, L0-011, L0-012, L0-013,  # interfaces/
        L0-014, L0-015, L0-016, L0-017, L0-018
    ),
    critic_gate.s(phase=0)
)
```

---

## 4. PHASE 1 — CORE AGENTS + SCANNERS

**Parallel Group:** `phase_1_core`  
**Tasks:** 5  
**Dependencies:** All Phase 0 tasks complete  
**Estimated Time:** 3 hours

### 4.1 ai/ (3 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L1-001 | `ai/architect_agent.py` | 280 | L0-001, L0-002, L0-009–L0-018 | phase_1_ai |
| L1-002 | `ai/test_agent.py` | 180 | L0-001, L0-004 | phase_1_ai |
| L1-003 | `ai/repair_loop.py` | 220 | L0-001, L0-004 | phase_1_ai |

**Detailed Dependencies:**
- `L1-001` (architect_agent.py): Requires `GameBrief` (L0-001), `ProjectSpec` (L0-002), all 10 interface headers (L0-009–L0-018)
- `L1-002` (test_agent.py): Requires `GameBrief` (L0-001), `CompileResult/TestResult` (L0-004)
- `L1-003` (repair_loop.py): Requires `GameBrief` (L0-001), `ErrorReport/RepairContext` (L0-004)

### 4.2 engine/ (2 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L1-004 | `engine/ue5_scanner.py` | 150 | L0-001 | phase_1_engine |
| L1-005 | `engine/learning_store.py` | 180 | L0-001, L0-002 | phase_1_engine |

**Detailed Dependencies:**
- `L1-004` (ue5_scanner.py): Requires `Platform` enum (L0-001)
- `L1-005` (learning_store.py): Requires `GameBrief/Genre` (L0-001), `ProjectSpec/Pattern` (L0-002)

### Phase 1 Task Chain

```
chord(
    group(
        L1-001, L1-002, L1-003,  # ai/
        L1-004, L1-005  # engine/
    ),
    critic_gate.s(phase=1)
)
```

**Prerequisite:** Phase 0 critic gate passed.

---

## 5. PHASE 2 — TEST GENERATION + BRIEF PARSING

**Parallel Group:** `phase_2_test_parse`  
**Tasks:** 4  
**Dependencies:** All Phase 1 tasks complete  
**Estimated Time:** 2 hours

### 5.1 ai/test_generation/ (3 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L2-001 | `ai/test_generation/cpp_test_generator.py` | 200 | L0-001, L0-002, L1-002 | phase_2_test |
| L2-002 | `ai/test_generation/blueprint_test_validator.py` | 180 | L0-001, L0-002, L1-002 | phase_2_test |
| L2-003 | `ai/test_generation/test_harness.py` | 150 | L0-001, L0-002, L1-002 | phase_2_test |

### 5.2 engine/ (1 task)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L2-004 | `engine/brief_parser.py` | 160 | L0-001, L0-002, L1-001 | phase_2_engine |

**Detailed Dependencies:**
- `L2-001/002/003`: Require `GameBrief` (L0-001), `ProjectSpec/TestSpec` (L0-002/L0-004), `TestAgent` (L1-002)
- `L2-004`: Requires `GameBrief` (L0-001), `ProjectSpec` (L0-002), `ArchitectAgent` (L1-001)

### Phase 2 Task Chain

```
chord(
    group(
        L2-001, L2-002, L2-003,  # test_generation/
        L2-004  # brief_parser.py
    ),
    critic_gate.s(phase=2)
)
```

**Prerequisite:** Phase 1 critic gate passed.

---

## 6. PHASE 3 — PROJECT SCAFFOLDING

**Parallel Group:** `phase_3_scaffold`  
**Tasks:** 1  
**Dependencies:** All Phase 2 tasks complete  
**Estimated Time:** 1 hour

### 6.1 engine/ (1 task)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L3-001 | `engine/project_scaffolder.py` | 250 | L0-001, L0-002, L0-009–L0-018, L2-004 | phase_3_scaffold |

**Detailed Dependencies:**
- Requires `GameBrief/Platform` (L0-001), `ProjectSpec/ModuleSpec` (L0-002)
- Requires all interface headers (L0-009–L0-018)
- Requires `BriefParser` (L2-004)

### Phase 3 Task Chain

```
chord(
    group(L3-001),
    critic_gate.s(phase=3)
)
```

**Prerequisite:** Phase 2 critic gate passed.

---

## 7. PHASE 4 — CODE GENERATION

**Parallel Group:** `phase_4_codegen`  
**Tasks:** 3  
**Dependencies:** All Phase 3 tasks complete  
**Estimated Time:** 3 hours

### 7.1 engine/ (3 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L4-001 | `engine/cpp_generator.py` | 320 | L0-001, L0-002, L0-003, L0-009–L0-018, L3-001 | phase_4_engine |
| L4-002 | `engine/blueprint_generator.py` | 280 | L0-001, L0-002, L3-001 | phase_4_engine |
| L4-003 | `engine/platform_guards.py` | 140 | L0-001, L0-006 | phase_4_engine |

**Detailed Dependencies:**
- `L4-001`: Requires `GameBrief/Genre` (L0-001), `ProjectSpec/ModuleSpec` (L0-002), `CppFile/HeaderFile` (L0-003), interfaces (L0-009–L0-018), `ProjectScaffolder` (L3-001)
- `L4-002`: Requires `GameBrief` (L0-001), `ProjectSpec` (L0-002), `ProjectScaffolder` (L3-001)
- `L4-003`: Requires `Platform` (L0-001), `PlatformTarget/SDKStatus` (L0-006)

### Phase 4 Task Chain

```
chord(
    group(L4-001, L4-002, L4-003),
    critic_gate.s(phase=4)
)
```

**Prerequisite:** Phase 3 critic gate passed.

---

## 8. PHASE 5 — BUILD EXECUTION

**Parallel Group:** `phase_5_build`  
**Tasks:** 1  
**Dependencies:** All Phase 4 tasks complete  
**Estimated Time:** 1 hour

### 8.1 engine/ (1 task)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L5-001 | `engine/build_runner.py` | 280 | L0-001, L0-004, L4-001, L1-002 | phase_5_build |

**Detailed Dependencies:**
- Requires `GameBrief` (L0-001), `CompileResult/TestResult/ErrorReport` (L0-004)
- Requires `CppGenerator` (L4-001), `TestAgent` (L1-002)

### Phase 5 Task Chain

```
chord(
    group(L5-001),
    critic_gate.s(phase=5)
)
```

**Prerequisite:** Phase 4 critic gate passed.

---

## 9. PHASE 6 — PACKAGING + STORE

**Parallel Group:** `phase_6_package`  
**Tasks:** 2  
**Dependencies:** All Phase 5 tasks complete  
**Estimated Time:** 2 hours

### 9.1 engine/ (2 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L6-001 | `engine/package_agent.py` | 240 | L0-001, L0-005, L0-006, L5-001 | phase_6_engine |
| L6-002 | `engine/store_agent.py` | 200 | L0-001, L0-007, L6-001 | phase_6_engine |

**Detailed Dependencies:**
- `L6-001`: Requires `Platform` (L0-001), `AgentMessage` (L0-005), `PlatformSpec` (L0-006), `BuildRunner` (L5-001)
- `L6-002`: Requires `GameBrief` (L0-001), `StoreSpec` (L0-007), `PackageAgent` (L6-001)

### Phase 6 Task Chain

```
chord(
    group(L6-001, L6-002),
    critic_gate.s(phase=6)
)
```

**Prerequisite:** Phase 5 critic gate passed.

---

## 10. PHASE 7 — SERVER + DASHBOARD (Max Parallel)

**Parallel Group:** `phase_7_server_dashboard`  
**Tasks:** 44  
**Dependencies:** All Phase 6 tasks complete  
**Estimated Time:** 8 hours (parallel execution)

### 10.1 server/api/ (7 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-001 | `server/api/projects.py` | 120 | L0-001, L0-002, L0-008, L2-004, L3-001 | phase_7_api |
| L7-002 | `server/api/architecture.py` | 60 | L0-001, L0-002, L0-008, L1-001 | phase_7_api |
| L7-003 | `server/api/generation.py` | 140 | L0-001, L0-002, L0-008, L4-001, L4-002, L5-001 | phase_7_api |
| L7-004 | `server/api/builds.py` | 80 | L0-001, L0-004, L0-008, L5-001 | phase_7_api |
| L7-005 | `server/api/packages.py` | 100 | L0-001, L0-006, L0-008, L6-001 | phase_7_api |
| L7-006 | `server/api/store.py` | 70 | L0-001, L0-007, L0-008, L6-002 | phase_7_api |
| L7-007 | `server/api/auth.py` | 90 | L0-001, L0-008 | phase_7_api |

### 10.2 server/workers/ (3 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-008 | `server/workers/generation_worker.py` | 180 | L0-001, L0-002, L2-004, L3-001, L4-001, L4-002 | phase_7_workers |
| L7-009 | `server/workers/build_worker.py` | 100 | L0-001, L0-004, L5-001 | phase_7_workers |
| L7-010 | `server/workers/package_worker.py` | 120 | L0-001, L0-006, L6-001 | phase_7_workers |

### 10.3 server/models/ (4 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-011 | `server/models/database.py` | 80 | L0-008 | phase_7_models |
| L7-012 | `server/models/project.py` | 60 | L7-011 | phase_7_models |
| L7-013 | `server/models/build.py` | 50 | L7-011 | phase_7_models |
| L7-014 | `server/models/__init__.py` | 20 | L7-011, L7-012, L7-013 | phase_7_models |

### 10.4 dashboard/src/pages/ (6 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-015 | `dashboard/src/pages/ProjectBrief.jsx` | 150 | L0-008 | phase_7_pages |
| L7-016 | `dashboard/src/pages/GenerationProgress.jsx` | 120 | L0-008 | phase_7_pages |
| L7-017 | `dashboard/src/pages/FileTree.jsx` | 100 | L0-008 | phase_7_pages |
| L7-018 | `dashboard/src/pages/BuildConsole.jsx` | 140 | L0-008 | phase_7_pages |
| L7-019 | `dashboard/src/pages/PlatformPackages.jsx` | 130 | L0-008 | phase_7_pages |
| L7-020 | `dashboard/src/pages/LearningStore.jsx` | 110 | L0-008 | phase_7_pages |

### 10.5 dashboard/src/components/ (8 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-021 | `dashboard/src/components/Header.jsx` | 40 | None | phase_7_components |
| L7-022 | `dashboard/src/components/Sidebar.jsx` | 60 | None | phase_7_components |
| L7-023 | `dashboard/src/components/ProgressBar.jsx` | 50 | None | phase_7_components |
| L7-024 | `dashboard/src/components/FileNode.jsx` | 70 | None | phase_7_components |
| L7-025 | `dashboard/src/components/ConsoleOutput.jsx` | 80 | None | phase_7_components |
| L7-026 | `dashboard/src/components/StatusBadge.jsx` | 35 | None | phase_7_components |
| L7-027 | `dashboard/src/components/DownloadButton.jsx` | 40 | None | phase_7_components |
| L7-028 | `dashboard/src/components/index.js` | 30 | L7-021–L7-027 | phase_7_components |

### 10.6 dashboard/src/api/ (3 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-029 | `dashboard/src/api/client.js` | 100 | None | phase_7_api_client |
| L7-030 | `dashboard/src/api/endpoints.js` | 80 | None | phase_7_api_client |
| L7-031 | `dashboard/src/api/index.js` | 40 | L7-029, L7-030 | phase_7_api_client |

### 10.7 dashboard/src/hooks/ (3 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-032 | `dashboard/src/hooks/useProject.js` | 60 | L7-029 | phase_7_hooks |
| L7-033 | `dashboard/src/hooks/useBuild.js` | 50 | L7-029 | phase_7_hooks |
| L7-034 | `dashboard/src/hooks/index.js` | 20 | L7-032, L7-033 | phase_7_hooks |

### 10.8 dashboard/src/styles/ (2 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-035 | `dashboard/src/styles/main.css` | 200 | None | phase_7_styles |
| L7-036 | `dashboard/src/styles/variables.css` | 50 | None | phase_7_styles |

### 10.9 dashboard/ (4 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-037 | `dashboard/package.json` | 60 | None | phase_7_dashboard_root |
| L7-038 | `dashboard/vite.config.js` | 40 | None | phase_7_dashboard_root |
| L7-039 | `dashboard/index.html` | 30 | None | phase_7_dashboard_root |
| L7-040 | `dashboard/src/main.jsx` | 40 | None | phase_7_dashboard_root |

### 10.10 dashboard/src/ (2 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L7-041 | `dashboard/src/App.jsx` | 80 | L7-015–L7-020, L7-021–L7-027 | phase_7_dashboard_src |
| L7-042 | `dashboard/src/index.css` | 30 | L7-035, L7-036 | phase_7_dashboard_src |

### Phase 7 Task Chain

```
chord(
    group(
        # server/api/ (7 tasks)
        L7-001, L7-002, L7-003, L7-004, L7-005, L7-006, L7-007,
        # server/workers/ (3 tasks)
        L7-008, L7-009, L7-010,
        # server/models/ (4 tasks, internal deps)
        L7-011, L7-012, L7-013, L7-014,
        # dashboard/pages/ (6 tasks)
        L7-015, L7-016, L7-017, L7-018, L7-019, L7-020,
        # dashboard/components/ (8 tasks)
        L7-021, L7-022, L7-023, L7-024, L7-025, L7-026, L7-027, L7-028,
        # dashboard/api/ (3 tasks)
        L7-029, L7-030, L7-031,
        # dashboard/hooks/ (3 tasks)
        L7-032, L7-033, L7-034,
        # dashboard/styles/ (2 tasks)
        L7-035, L7-036,
        # dashboard root (4 tasks)
        L7-037, L7-038, L7-039, L7-040,
        # dashboard src (2 tasks)
        L7-041, L7-042
    ),
    critic_gate.s(phase=7)
)
```

**Prerequisite:** Phase 6 critic gate passed.

---

## 11. PHASE 8 — SERVER ENTRY POINT

**Parallel Group:** `phase_8_entry`  
**Tasks:** 2  
**Dependencies:** All Phase 7 tasks complete  
**Estimated Time:** 30 minutes

### 11.1 server/ (2 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| L8-001 | `server/main.py` | 100 | L7-001–L7-010, L7-014 | phase_8_entry |
| L8-002 | `server/__init__.py` | 10 | None | phase_8_entry |

**Detailed Dependencies:**
- `L8-001`: Requires all API routers (L7-001–L7-007), all workers (L7-008–L7-010), models export (L7-014)
- `L8-002`: No dependencies (package marker)

### Phase 8 Task Chain

```
chord(
    group(L8-001, L8-002),
    critic_gate.s(phase=8)
)
```

**Prerequisite:** Phase 7 critic gate passed.

---

## 12. PHASE 9 — TESTS

**Parallel Group:** `phase_9_tests`  
**Tasks:** 12  
**Dependencies:** All Phase 8 tasks complete (can run parallel with Phase 10)  
**Estimated Time:** 4 hours

### 12.1 tests/ (12 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| T-001 | `tests/test_platform_guards.py` | 120 | L4-003 | phase_9_tests |
| T-002 | `tests/test_architect_agent.py` | 150 | L1-001 | phase_9_tests |
| T-003 | `tests/test_cpp_generator.py` | 140 | L4-001 | phase_9_tests |
| T-004 | `tests/test_blueprint_generator.py` | 130 | L4-002 | phase_9_tests |
| T-005 | `tests/test_build_runner.py` | 160 | L5-001 | phase_9_tests |
| T-006 | `tests/test_repair_loop.py` | 140 | L1-003 | phase_9_tests |
| T-007 | `tests/integration/test_full_pipeline.py` | 250 | All engine modules | phase_9_integration |
| T-008 | `tests/integration/__init__.py` | 10 | None | phase_9_integration |
| T-009 | `tests/test_dependency_graph.py` | 180 | None | phase_9_tests |
| T-010 | `tests/test_module_dependencies.py` | 120 | All modules | phase_9_tests |
| T-011 | `tests/__init__.py` | 10 | None | phase_9_tests |
| T-012 | `tests/conftest.py` | 80 | All modules | phase_9_tests |

### Phase 9 Task Chain

```
chord(
    group(
        T-001, T-002, T-003, T-004, T-005, T-006,  # unit tests
        T-007, T-008,  # integration tests
        T-009, T-010, T-011, T-012  # infrastructure tests
    ),
    critic_gate.s(phase=9)
)
```

**Prerequisite:** Phase 8 critic gate passed.

---

## 13. PHASE 10 — INFRASTRUCTURE

**Parallel Group:** `phase_10_infra`  
**Tasks:** 29  
**Dependencies:** Can run parallel with Phases 1-9 (no blocking deps)  
**Estimated Time:** 2 hours

### 13.1 Root Configuration (10 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| INF-001 | `docker-compose.yml` | 80 | None | phase_10_root |
| INF-002 | `.env.example` | 40 | None | phase_10_root |
| INF-003 | `.gitignore` | 100 | None | phase_10_root |
| INF-004 | `.python-version` | 1 | None | phase_10_root |
| INF-005 | `pyproject.toml` | 80 | None | phase_10_root |
| INF-006 | `requirements.txt` | 50 | None | phase_10_root |
| INF-007 | `requirements-dev.txt` | 30 | None | phase_10_root |
| INF-008 | `PRIVATE_LICENSE.md` | 100 | None | phase_10_root |
| INF-009 | `README.md` | 200 | All docs | phase_10_root |
| INF-010 | `tasks.md` | 150 | None | phase_10_root |

### 13.2 Documentation (6 tasks — already complete)

| Task ID | File Path | Lines | Dependencies | Status |
|---------|-----------|-------|--------------|--------|
| INF-011 | `forgeue.md` | 734 | None | ✓ EXISTS |
| INF-012 | `requirements.md` | 400 | None | ✓ EXISTS |
| INF-013 | `architecture.md` | 500 | None | ✓ EXISTS |
| INF-014 | `dependency_graph.md` | 600 | None | ✓ EXISTS |
| INF-015 | `module_dependencies.md` | 800 | None | ✓ EXISTS |
| INF-016 | `file_manifest.md` | 400 | None | ✓ EXISTS |
| INF-017 | `critic_prebuild.md` | 500 | None | ✓ EXISTS |

### 13.3 .vscode/ (5 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| INF-018 | `.vscode/settings.json` | 60 | None | phase_10_vscode |
| INF-019 | `.vscode/extensions.json` | 30 | None | phase_10_vscode |
| INF-020 | `.vscode/launch.json` | 80 | L8-001, L5-001 | phase_10_vscode |
| INF-021 | `.vscode/tasks.json` | 100 | None | phase_10_vscode |
| INF-022 | `.vscode/forge.code-workspace` | 50 | None | phase_10_vscode |

### 13.4 Package Markers (9 tasks)

| Task ID | File Path | Lines | Dependencies | Parallel Group |
|---------|-----------|-------|--------------|----------------|
| INF-023 | `engine/__init__.py` | 10 | None | phase_10_markers |
| INF-024 | `ai/__init__.py` | 10 | None | phase_10_markers |
| INF-025 | `contracts/__init__.py` | 10 | None | phase_10_markers |
| INF-026 | `contracts/models/__init__.py` | 50 | L0-001–L0-007 | phase_10_markers |
| INF-027 | `templates/__init__.py` | 10 | None | phase_10_markers |
| INF-028 | `server/api/__init__.py` | 50 | L7-001–L7-007 | phase_10_markers |
| INF-029 | `server/workers/__init__.py` | 20 | L7-008–L7-010 | phase_10_markers |
| INF-030 | `ai/test_generation/__init__.py` | 20 | L2-001–L2-003 | phase_10_markers |

### Phase 10 Task Chain

```
# Can run in parallel with all other phases
group(
    # Root config (10 tasks)
    INF-001, INF-002, INF-003, INF-004, INF-005, INF-006, INF-007, INF-008, INF-009, INF-010,
    # .vscode (5 tasks)
    INF-018, INF-019, INF-020, INF-021, INF-022,
    # Package markers (9 tasks, some with deps)
    INF-023, INF-024, INF-025, INF-026, INF-027, INF-028, INF-029, INF-030
)
```

**Note:** `INF-011` through `INF-017` already exist (Phase 1-6 outputs).

---

## 14. COMPLETE TASK CHAIN (Celery Orchestration)

```python
from celery import chain, chord, group

def build_full_pipeline():
    """
    Build complete Celery task chain for FORGE pipeline.
    """
    return chain(
        # Phase 0 — Foundation (18 tasks, parallel)
        chord(
            group(
                L0_001, L0_002, L0_003, L0_004, L0_005, L0_006, L0_007,
                L0_008,
                L0_009, L0_010, L0_011, L0_012, L0_013,
                L0_014, L0_015, L0_016, L0_017, L0_018
            ),
            critic_gate.s(phase=0)
        ),
        
        # Phase 1 — Core Agents (5 tasks, parallel)
        chord(
            group(L1_001, L1_002, L1_003, L1_004, L1_005),
            critic_gate.s(phase=1)
        ),
        
        # Phase 2 — Test + Parse (4 tasks, parallel)
        chord(
            group(L2_001, L2_002, L2_003, L2_004),
            critic_gate.s(phase=2)
        ),
        
        # Phase 3 — Scaffold (1 task)
        chord(
            group(L3_001),
            critic_gate.s(phase=3)
        ),
        
        # Phase 4 — Code Gen (3 tasks, parallel)
        chord(
            group(L4_001, L4_002, L4_003),
            critic_gate.s(phase=4)
        ),
        
        # Phase 5 — Build (1 task)
        chord(
            group(L5_001),
            critic_gate.s(phase=5)
        ),
        
        # Phase 6 — Package + Store (2 tasks, parallel)
        chord(
            group(L6_001, L6_002),
            critic_gate.s(phase=6)
        ),
        
        # Phase 7 — Server + Dashboard (44 tasks, parallel)
        chord(
            group(
                # API (7)
                L7_001, L7_002, L7_003, L7_004, L7_005, L7_006, L7_007,
                # Workers (3)
                L7_008, L7_009, L7_010,
                # Models (4)
                L7_011, L7_012, L7_013, L7_014,
                # Pages (6)
                L7_015, L7_016, L7_017, L7_018, L7_019, L7_020,
                # Components (8)
                L7_021, L7_022, L7_023, L7_024, L7_025, L7_026, L7_027, L7_028,
                # API client (3)
                L7_029, L7_030, L7_031,
                # Hooks (3)
                L7_032, L7_033, L7_034,
                # Styles (2)
                L7_035, L7_036,
                # Dashboard root (4)
                L7_037, L7_038, L7_039, L7_040,
                # Dashboard src (2)
                L7_041, L7_042
            ),
            critic_gate.s(phase=7)
        ),
        
        # Phase 8 — Entry Point (2 tasks, parallel)
        chord(
            group(L8_001, L8_002),
            critic_gate.s(phase=8)
        ),
        
        # Phase 9 — Tests (12 tasks, parallel)
        chord(
            group(
                T_001, T_002, T_003, T_004, T_005, T_006,
                T_007, T_008,
                T_009, T_010, T_011, T_012
            ),
            critic_gate.s(phase=9)
        ),
        
        # Final gate
        finalize_pipeline.s()
    )
```

---

## 15. CRITIC GATE TASKS

Each phase ends with a critic gate task:

```python
@app.task
def critic_gate(phase_results: Dict, phase: int) -> CriticResult:
    """
    Run 4-pass critic on phase outputs.
    
    Pass 1: Syntax (no LLM)
    Pass 2: Contract (no LLM)
    Pass 3: Completeness (LLM)
    Pass 4: Logic (LLM)
    
    Returns: CriticResult { passed: bool, errors: [], warnings: [] }
    """
    pass

@app.task
def finalize_pipeline(phase_results: Dict) -> PipelineResult:
    """
    Final validation after all phases complete.
    Generate critic_final.md.
    """
    pass
```

---

## 16. EXECUTION TIMELINE

| Phase | Tasks | Parallel Groups | Est. Time | Cumulative |
|-------|-------|-----------------|-----------|------------|
| P0 | 18 | 3 | 2h | 2h |
| P1 | 5 | 2 | 3h | 5h |
| P2 | 4 | 2 | 2h | 7h |
| P3 | 1 | 1 | 1h | 8h |
| P4 | 3 | 1 | 3h | 11h |
| P5 | 1 | 1 | 1h | 12h |
| P6 | 2 | 1 | 2h | 14h |
| P7 | 44 | 10 | 8h | 22h |
| P8 | 2 | 1 | 0.5h | 22.5h |
| P9 | 12 | 2 | 4h | 26.5h |
| P10 | 29 | 4 | 2h | 28.5h |

**Total Estimated Time:** ~28.5 hours (with parallel execution)

**Critical Path (sequential phases):** P0 → P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9

---

## 17. TASK PRIORITY MATRIX

| Priority | Tasks | Reason |
|----------|-------|--------|
| **P0 (Critical)** | L0-001–L0-018 | Foundation — all other tasks depend on these |
| **P1 (High)** | L1-001, L2-004, L3-001 | Architect + brief parser + scaffolder chain |
| **P2 (High)** | L4-001, L4-002, L5-001 | Code generators + build runner |
| **P3 (Medium)** | L7-001–L7-010 | Server API + workers |
| **P4 (Medium)** | L7-015–L7-042 | Dashboard components |
| **P5 (Low)** | T-001–T-012 | Tests (can run after code complete) |
| **P6 (Low)** | INF-001–INF-030 | Infrastructure (can run anytime) |

---

## 18. DEPENDENCY VISUALIZATION

```
Phase 0 (18 tasks) ─────────────────────────────────────────────┐
  │                                                              │
  ▼                                                              │
Phase 1 (5 tasks) ───────────────────────────────────────────┐  │
  │                                                          │  │
  ▼                                                          │  │
Phase 2 (4 tasks) ───────────────────────────────────────┐  │  │
  │                                                      │  │  │
  ▼                                                      │  │  │
Phase 3 (1 task) ───────────────────────────────────┐  │  │  │
  │                                                 │  │  │  │
  ▼                                                 │  │  │  │
Phase 4 (3 tasks) ──────────────────────────────┐  │  │  │  │
  │                                             │  │  │  │  │
  ▼                                             │  │  │  │  │
Phase 5 (1 task) ───────────────────────────┐  │  │  │  │  │
  │                                         │  │  │  │  │  │
  ▼                                         │  │  │  │  │  │
Phase 6 (2 tasks) ──────────────────────┐  │  │  │  │  │  │
  │                                     │  │  │  │  │  │  │
  ▼                                     │  │  │  │  │  │  │
Phase 7 (44 tasks) ─────────────────┐  │  │  │  │  │  │  │
  │                                 │  │  │  │  │  │  │  │
  ▼                                 │  │  │  │  │  │  │  │
Phase 8 (2 tasks) ──────────────┐  │  │  │  │  │  │  │  │
  │                             │  │  │  │  │  │  │  │  │
  ▼                             │  │  │  │  │  │  │  │  │
Phase 9 (12 tasks) ─────────────┼──┼──┼──┼──┼──┼──┼──┘
  │                             │  │  │  │  │  │  │
  ▼                             │  │  │  │  │  │  │
Phase 10 (29 tasks) ────────────┴──┴──┴──┴──┴──┴──┘ (parallel)
```

---

*End of Task Schedule*
