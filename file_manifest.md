# FORGE — Complete File Manifest

## 1. OVERVIEW

This document lists **every file** that will exist in the FORGE project upon completion. Files are organized by topological level from `dependency_graph.md` and cross-referenced with `module_dependencies.md`.

**Total File Count:** 127 files

---

## 2. LEVEL 0 — CONTRACTS (Immutable Foundation)

### 2.1 contracts/models/ (7 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L0-001 | `contracts/models/game_brief.py` | 120 | GameBrief, Genre, Platform, MechanicSpec schemas |
| L0-002 | `contracts/models/project_spec.py` | 180 | ProjectSpec, ModuleSpec, SubsystemRef, Pattern schemas |
| L0-003 | `contracts/models/code_artifact.py` | 100 | CppFile, HeaderFile, BlueprintGraph schemas |
| L0-004 | `contracts/models/build_result.py` | 150 | CompileResult, TestResult, PackageResult, ErrorReport schemas |
| L0-005 | `contracts/models/agent_message.py` | 90 | AgentTask, AgentResult, CriticResult schemas |
| L0-006 | `contracts/models/platform_spec.py` | 110 | PlatformTarget, SDKStatus, PackageConfig schemas |
| L0-007 | `contracts/models/store_spec.py` | 100 | StoreSubmission, StoreAssets, RatingConfig schemas |

### 2.2 contracts/ (1 file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L0-008 | `contracts/api.yaml` | 250 | OpenAPI 3.0 REST API specification |

### 2.3 templates/interfaces/ (10 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L0-009 | `templates/interfaces/IForgeGameMode.h` | 45 | Base GameMode interface |
| L0-010 | `templates/interfaces/IForgeCharacter.h` | 55 | Base Character interface |
| L0-011 | `templates/interfaces/IForgeGameInstance.h` | 50 | Persistent state, save/load interface |
| L0-012 | `templates/interfaces/IForgeInventory.h` | 60 | Inventory system interface |
| L0-013 | `templates/interfaces/IForgeSaveGame.h` | 40 | Save game base class interface |
| L0-014 | `templates/interfaces/IForgeUIManager.h` | 50 | HUD + widget manager interface |
| L0-015 | `templates/interfaces/IForgeAudioManager.h` | 45 | Audio system interface |
| L0-016 | `templates/interfaces/IForgeAchievement.h` | 40 | Achievement/trophy interface |
| L0-017 | `templates/interfaces/IForgePlatformLayer.h` | 55 | Platform abstraction interface |
| L0-018 | `templates/interfaces/IForgeOnlineSubsystem.h` | 65 | Online/multiplayer interface |

**Level 0 Subtotal:** 18 files

---

## 3. LEVEL 1 — CORE AGENTS + SCANNERS

### 3.1 ai/ (3 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L1-001 | `ai/architect_agent.py` | 280 | brief → ProjectSpec + UBT module graph |
| L1-002 | `ai/test_agent.py` | 180 | ProjectSpec → test specs per system |
| L1-003 | `ai/repair_loop.py` | 220 | UBT/UHT errors → targeted repair |

### 3.2 engine/ (2 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L1-004 | `engine/ue5_scanner.py` | 150 | UE5 install + SDK detection |
| L1-005 | `engine/learning_store.py` | 180 | Pattern library per genre + subsystem |

**Level 1 Subtotal:** 5 files

---

## 4. LEVEL 2 — TEST GENERATION + BRIEF PARSING

### 4.1 ai/test_generation/ (3 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L2-001 | `ai/test_generation/cpp_test_generator.py` | 200 | UE5 FAutomationTestBase templates |
| L2-002 | `ai/test_generation/blueprint_test_validator.py` | 180 | BP JSON spec validator |
| L2-003 | `ai/test_generation/test_harness.py` | 150 | Orchestrate UE5 test runner |

### 4.2 engine/ (1 file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L2-004 | `engine/brief_parser.py` | 160 | Raw brief → GameBrief schema |

**Level 2 Subtotal:** 4 files

---

## 5. LEVEL 3 — PROJECT SCAFFOLDING

### 5.1 engine/ (1 file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L3-001 | `engine/project_scaffolder.py` | 250 | GameBrief → folder structure + configs |

**Level 3 Subtotal:** 1 file

---

## 6. LEVEL 4 — CODE GENERATION

### 6.1 engine/ (3 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L4-001 | `engine/cpp_generator.py` | 320 | ModuleSpec → .h + .cpp files |
| L4-002 | `engine/blueprint_generator.py` | 280 | ModuleSpec → BP JSON node graphs |
| L4-003 | `engine/platform_guards.py` | 140 | Inject platform macros + validate |

**Level 4 Subtotal:** 3 files

---

## 7. LEVEL 5 — BUILD EXECUTION

### 7.1 engine/ (1 file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L5-001 | `engine/build_runner.py` | 280 | Invoke UHT → UBT, capture errors |

**Level 5 Subtotal:** 1 file

---

## 8. LEVEL 6 — PACKAGING + STORE

### 8.1 engine/ (2 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L6-001 | `engine/package_agent.py` | 240 | Cook + pak per platform target |
| L6-002 | `engine/store_agent.py` | 200 | Steam/EGS submission config + assets |

**Level 6 Subtotal:** 2 files

---

## 9. LEVEL 7 — SERVER + DASHBOARD (Parallel)

### 9.1 server/api/ (7 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-001 | `server/api/projects.py` | 120 | CRUD projects + trigger generation |
| L7-002 | `server/api/architecture.py` | 60 | GET ProjectSpec for human review |
| L7-003 | `server/api/generation.py` | 140 | Progress, file tree, critic status |
| L7-004 | `server/api/builds.py` | 80 | Compile status, error log, repair history |
| L7-005 | `server/api/packages.py` | 100 | Per-platform build status + download |
| L7-006 | `server/api/store.py` | 70 | Submission assets + config |
| L7-007 | `server/api/auth.py` | 90 | JWT + API key authentication |

### 9.2 server/workers/ (3 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-008 | `server/workers/generation_worker.py` | 180 | Celery: full topo pipeline |
| L7-009 | `server/workers/build_worker.py` | 100 | Celery: UBT compile + test run |
| L7-010 | `server/workers/package_worker.py` | 120 | Celery: cook + pak per platform |

### 9.3 server/models/ (4 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-011 | `server/models/database.py` | 80 | SQLAlchemy ORM models |
| L7-012 | `server/models/project.py` | 60 | Project database model |
| L7-013 | `server/models/build.py` | 50 | Build history database model |
| L7-014 | `server/models/__init__.py` | 20 | SQLAlchemy models export |

### 9.4 dashboard/src/pages/ (6 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-015 | `dashboard/src/pages/ProjectBrief.jsx` | 150 | Submit brief + architecture review |
| L7-016 | `dashboard/src/pages/GenerationProgress.jsx` | 120 | Topo level progress + critic status |
| L7-017 | `dashboard/src/pages/FileTree.jsx` | 100 | Generated UE5 project browser |
| L7-018 | `dashboard/src/pages/BuildConsole.jsx` | 140 | Live UBT output + error highlighting |
| L7-019 | `dashboard/src/pages/PlatformPackages.jsx` | 130 | Per-platform build status + download |
| L7-020 | `dashboard/src/pages/LearningStore.jsx` | 110 | Pattern library browser |

### 9.5 dashboard/src/components/ (8 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-021 | `dashboard/src/components/Header.jsx` | 40 | Navigation header |
| L7-022 | `dashboard/src/components/Sidebar.jsx` | 60 | Navigation sidebar |
| L7-023 | `dashboard/src/components/ProgressBar.jsx` | 50 | Progress indicator component |
| L7-024 | `dashboard/src/components/FileNode.jsx` | 70 | Tree node for file browser |
| L7-025 | `dashboard/src/components/ConsoleOutput.jsx` | 80 | Console output display |
| L7-026 | `dashboard/src/components/StatusBadge.jsx` | 35 | Status indicator badge |
| L7-027 | `dashboard/src/components/DownloadButton.jsx` | 40 | Download action button |
| L7-028 | `dashboard/src/components/index.js` | 30 | Component exports |

### 9.6 dashboard/src/api/ (3 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-029 | `dashboard/src/api/client.js` | 100 | Axios API client configuration |
| L7-030 | `dashboard/src/api/endpoints.js` | 80 | API endpoint definitions |
| L7-031 | `dashboard/src/api/index.js` | 40 | API module exports |

### 9.7 dashboard/src/hooks/ (3 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-032 | `dashboard/src/hooks/useProject.js` | 60 | Project data hook |
| L7-033 | `dashboard/src/hooks/useBuild.js` | 50 | Build status hook |
| L7-034 | `dashboard/src/hooks/index.js` | 20 | Hook exports |

### 9.8 dashboard/src/styles/ (2 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-035 | `dashboard/src/styles/main.css` | 200 | Global styles |
| L7-036 | `dashboard/src/styles/variables.css` | 50 | CSS custom properties |

### 9.9 dashboard/ (4 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-037 | `dashboard/package.json` | 60 | Node.js dependencies |
| L7-038 | `dashboard/vite.config.js` | 40 | Vite build configuration |
| L7-039 | `dashboard/index.html` | 30 | HTML entry point |
| L7-040 | `dashboard/src/main.jsx` | 40 | React entry point |

### 9.10 dashboard/src/ (2 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L7-041 | `dashboard/src/App.jsx` | 80 | Root React component |
| L7-042 | `dashboard/src/index.css` | 30 | Base CSS imports |

**Level 7 Subtotal:** 44 files

---

## 10. LEVEL 8 — SERVER ENTRY POINT

### 10.1 server/ (2 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| L8-001 | `server/main.py` | 100 | FastAPI application entry point |
| L8-002 | `server/__init__.py` | 10 | Server package marker |

**Level 8 Subtotal:** 2 files

---

## 11. TESTS

### 11.1 tests/ (6 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| T-001 | `tests/test_platform_guards.py` | 120 | Safety gate — always first |
| T-002 | `tests/test_architect_agent.py` | 150 | Brief → valid ProjectSpec |
| T-003 | `tests/test_cpp_generator.py` | 140 | ModuleSpec → valid C++ headers |
| T-004 | `tests/test_blueprint_generator.py` | 130 | ModuleSpec → valid BP JSON |
| T-005 | `tests/test_build_runner.py` | 160 | Mock UBT → error parse + repair |
| T-006 | `tests/test_repair_loop.py` | 140 | Inject UBT error → repair fires |

### 11.2 tests/integration/ (2 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| T-007 | `tests/integration/test_full_pipeline.py` | 250 | Live UBT compile of sample project |
| T-008 | `tests/integration/__init__.py` | 10 | Integration tests package marker |

### 11.3 tests/ (2 additional files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| T-009 | `tests/test_dependency_graph.py` | 180 | Graph A + Graph B cycle detection |
| T-010 | `tests/test_module_dependencies.py` | 120 | Validate actual imports match declared |
| T-011 | `tests/__init__.py` | 10 | Tests package marker |
| T-012 | `tests/conftest.py` | 80 | Pytest fixtures + configuration |

**Tests Subtotal:** 12 files

---

## 12. INFRASTRUCTURE

### 12.1 Root Configuration (10 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-001 | `docker-compose.yml` | 80 | Forge server + postgres + redis |
| INF-002 | `.env.example` | 40 | Environment variable template |
| INF-003 | `.gitignore` | 100 | Git ignore patterns |
| INF-004 | `.python-version` | 1 | Python version (3.11) |
| INF-005 | `pyproject.toml` | 80 | Python project configuration |
| INF-006 | `requirements.txt` | 50 | Python dependencies |
| INF-007 | `requirements-dev.txt` | 30 | Development dependencies |
| INF-008 | `PRIVATE_LICENSE.md` | 100 | Proprietary license terms |
| INF-009 | `README.md` | 200 | Project documentation |
| INF-010 | `tasks.md` | 150 | Build checklist |

### 12.2 Documentation (4 files — already created)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-011 | `forgeue.md` | 734 | Original specification (exists) |
| INF-012 | `requirements.md` | 400 | Requirements specification (exists) |
| INF-013 | `architecture.md` | 500 | Architecture specification (exists) |
| INF-014 | `dependency_graph.md` | 600 | Dependency graph specification (exists) |
| INF-015 | `module_dependencies.md` | 800 | Module dependencies specification (exists) |
| INF-016 | `file_manifest.md` | 400 | This file |

### 12.3 .vscode/ (5 files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-017 | `.vscode/settings.json` | 60 | Exclude: Binaries/, Intermediate/, etc. |
| INF-018 | `.vscode/extensions.json` | 30 | pylance, ruff, clangd, UE5 snippets |
| INF-019 | `.vscode/launch.json` | 80 | Debug FORGE server, debug UBT runner |
| INF-020 | `.vscode/tasks.json` | 100 | Build tasks configuration |
| INF-021 | `.vscode/forge.code-workspace` | 50 | Multi-root: forge/ + output/{project}/ |

### 12.4 engine/ (1 additional file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-022 | `engine/__init__.py` | 10 | Engine package marker |

### 12.5 ai/ (1 additional file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-023 | `ai/__init__.py` | 10 | AI package marker |

### 12.6 contracts/ (2 additional files)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-024 | `contracts/__init__.py` | 10 | Contracts package marker |
| INF-025 | `contracts/models/__init__.py` | 50 | Models export |

### 12.7 templates/ (1 additional file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-026 | `templates/__init__.py` | 10 | Templates package marker |

### 12.8 server/api/ (1 additional file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-027 | `server/api/__init__.py` | 50 | API router exports |

### 12.9 server/workers/ (1 additional file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-028 | `server/workers/__init__.py` | 20 | Worker exports |

### 12.10 ai/test_generation/ (1 additional file)

| # | File Path | Lines (est.) | Purpose |
|---|-----------|--------------|---------|
| INF-029 | `ai/test_generation/__init__.py` | 20 | Test generation exports |

**Infrastructure Subtotal:** 45 files

---

## 13. OUTPUT DIRECTORIES (Generated at Runtime)

### 13.1 output/ (Created per project)

```
output/
└── {project_name}/
    ├── {ProjectName}.uproject
    ├── Source/
    │   ├── {ProjectName}.Build.cs
    │   ├── {ProjectName}.Target.cs
    │   ├── {ProjectName}Editor.Target.cs
    │   └── {ProjectName}/
    │       ├── {ProjectName}.h
    │       ├── {ProjectName}.cpp
    │       ├── {ProjectName}GameMode.h
    │       ├── {ProjectName}GameMode.cpp
    │       ├── {ProjectName}Character.h
    │       ├── {ProjectName}Character.cpp
    │       └── ... (generated C++ files)
    ├── Content/
    │   └── Blueprints/
    │       └── *.json (Blueprint graphs → .uasset)
    ├── Config/
    │   ├── DefaultEngine.ini
    │   ├── DefaultGame.ini
    │   ├── DefaultInput.ini
    │   └── Default*.ini (platform-specific)
    └── Build/
        └── {Platform}/
            └── (packaged binaries)
```

### 13.2 .dedup/ (Deduplication store)

```
.dedup/
└── {project_id}:{file_path}:{content_hash}
```

### 13.3 logs/ (Build + generation logs)

```
logs/
├── ue5_scanner.log
├── architect_agent.log
├── cpp_generator.log
├── build_runner.log
├── package_agent.log
└── critic_gates/
    └── {project_id}/
        ├── level_0_critic.log
        ├── level_1_critic.log
        └── ...
```

**Output directories are created at runtime and not tracked in git.**

---

## 14. COMPLETE FILE COUNT

| Category | File Count |
|----------|------------|
| Level 0 — Contracts | 18 |
| Level 1 — Core Agents + Scanners | 5 |
| Level 2 — Test Generation + Brief Parsing | 4 |
| Level 3 — Project Scaffolding | 1 |
| Level 4 — Code Generation | 3 |
| Level 5 — Build Execution | 1 |
| Level 6 — Packaging + Store | 2 |
| Level 7 — Server + Dashboard | 44 |
| Level 8 — Server Entry Point | 2 |
| Tests | 12 |
| Infrastructure | 45 |
| **Total (excluding output/)** | **137** |

---

## 15. FILE INDEX BY PATH

### Root (10 files)
```
forge.ue/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── PRIVATE_LICENSE.md
├── README.md
└── tasks.md
```

### contracts/ (11 files)
```
contracts/
├── __init__.py
├── api.yaml
└── models/
    ├── __init__.py
    ├── game_brief.py
    ├── project_spec.py
    ├── code_artifact.py
    ├── build_result.py
    ├── agent_message.py
    ├── platform_spec.py
    └── store_spec.py
```

### templates/ (11 files)
```
templates/
├── __init__.py
└── interfaces/
    ├── IForgeGameMode.h
    ├── IForgeCharacter.h
    ├── IForgeGameInstance.h
    ├── IForgeInventory.h
    ├── IForgeSaveGame.h
    ├── IForgeUIManager.h
    ├── IForgeAudioManager.h
    ├── IForgeAchievement.h
    ├── IForgePlatformLayer.h
    └── IForgeOnlineSubsystem.h
```

### ai/ (8 files)
```
ai/
├── __init__.py
├── architect_agent.py
├── test_agent.py
├── repair_loop.py
└── test_generation/
    ├── __init__.py
    ├── cpp_test_generator.py
    ├── blueprint_test_validator.py
    └── test_harness.py
```

### engine/ (13 files)
```
engine/
├── __init__.py
├── ue5_scanner.py
├── brief_parser.py
├── project_scaffolder.py
├── cpp_generator.py
├── blueprint_generator.py
├── build_runner.py
├── package_agent.py
├── store_agent.py
├── learning_store.py
└── platform_guards.py
```

### server/ (18 files)
```
server/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   ├── projects.py
│   ├── architecture.py
│   ├── generation.py
│   ├── builds.py
│   ├── packages.py
│   ├── store.py
│   └── auth.py
├── workers/
│   ├── __init__.py
│   ├── generation_worker.py
│   ├── build_worker.py
│   └── package_worker.py
└── models/
    ├── __init__.py
    ├── database.py
    ├── project.py
    └── build.py
```

### dashboard/ (22 files)
```
dashboard/
├── package.json
├── vite.config.js
├── index.html
└── src/
    ├── main.jsx
    ├── index.css
    ├── App.jsx
    ├── api/
    │   ├── client.js
    │   ├── endpoints.js
    │   └── index.js
    ├── components/
    │   ├── Header.jsx
    │   ├── Sidebar.jsx
    │   ├── ProgressBar.jsx
    │   ├── FileNode.jsx
    │   ├── ConsoleOutput.jsx
    │   ├── StatusBadge.jsx
    │   ├── DownloadButton.jsx
    │   └── index.js
    ├── hooks/
    │   ├── useProject.js
    │   ├── useBuild.js
    │   └── index.js
    ├── pages/
    │   ├── ProjectBrief.jsx
    │   ├── GenerationProgress.jsx
    │   ├── FileTree.jsx
    │   ├── BuildConsole.jsx
    │   ├── PlatformPackages.jsx
    │   └── LearningStore.jsx
    └── styles/
        ├── main.css
        └── variables.css
```

### tests/ (12 files)
```
tests/
├── __init__.py
├── conftest.py
├── test_platform_guards.py
├── test_architect_agent.py
├── test_cpp_generator.py
├── test_blueprint_generator.py
├── test_build_runner.py
├── test_repair_loop.py
├── test_dependency_graph.py
├── test_module_dependencies.py
└── integration/
    ├── __init__.py
    └── test_full_pipeline.py
```

### .vscode/ (5 files)
```
.vscode/
├── settings.json
├── extensions.json
├── launch.json
├── tasks.json
└── forge.code-workspace
```

### Documentation (6 files)
```
forge.ue/
├── forgeue.md
├── requirements.md
├── architecture.md
├── dependency_graph.md
├── module_dependencies.md
└── file_manifest.md
```

---

## 16. GENERATION ORDER (Topological)

Files are generated in this exact order during pipeline execution:

```
Phase 1 (L0): contracts/, templates/interfaces/ — Already exist (immutable)
Phase 2 (L1): ai/architect_agent.py, ai/test_agent.py, ai/repair_loop.py, engine/ue5_scanner.py, engine/learning_store.py
Phase 3 (L2): ai/test_generation/*, engine/brief_parser.py
Phase 4 (L3): engine/project_scaffolder.py
Phase 5 (L4): engine/cpp_generator.py, engine/blueprint_generator.py, engine/platform_guards.py
Phase 6 (L5): engine/build_runner.py
Phase 7 (L6): engine/package_agent.py, engine/store_agent.py
Phase 8 (L7): server/api/*, server/workers/*, server/models/*, dashboard/*
Phase 9 (L8): server/main.py
Phase 10:    tests/*, infrastructure files
```

---

## 17. CRITIC GATE FILE VALIDATION

Each topological level must pass 4-pass critic before advancing:

| Level | Files Validated | Pass 1 (Syntax) | Pass 2 (Contract) | Pass 3 (Completeness) | Pass 4 (Logic) |
|-------|-----------------|-----------------|-------------------|----------------------|----------------|
| L0 | 18 | yamllint, clang-format | N/A (foundation) | N/A | N/A |
| L1 | 5 | mypy, ruff | contracts compliance | Agent coverage | Agent logic |
| L2 | 4 | mypy, ruff | contracts compliance | Test coverage | Test logic |
| L3 | 1 | mypy, ruff | contracts compliance | Scaffold coverage | Scaffold logic |
| L4 | 3 | mypy, ruff, UHT | .cpp implements .h | Generator coverage | UE5 logic |
| L5 | 1 | mypy, ruff, UBT | Error parsing | Build coverage | Build logic |
| L6 | 2 | mypy, ruff | contracts compliance | Package coverage | Platform logic |
| L7 | 44 | eslint, mypy | API contracts | Endpoint coverage | API logic |
| L8 | 2 | mypy, ruff | API integration | Server coverage | Server logic |

---

*End of File Manifest*
