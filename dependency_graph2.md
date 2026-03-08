# FORGE — Code Generation Dependency Graph (dependency_graph2.md)

## 1. OVERVIEW

This document specifies the **detailed dependency graph** for code generation, based on `architecture2.md` and the complete folder structure. Two graphs are defined:

- **Graph A (Code Generation):** Python/JS implementation dependencies
- **Graph B (Runtime):** Runtime import dependencies

Both graphs must be cycle-free.

---

## 2. GRAPH A — CODE GENERATION DEPENDENCIES

### 2.1 Node Definitions

| Node ID | File Path | Type | Level | Lines (Target) |
|---------|-----------|------|-------|----------------|
| CG-L0-01 | `contracts/models/game_brief.py` | Pydantic | L0 | 120 |
| CG-L0-02 | `contracts/models/platform_spec.py` | Pydantic | L0 | 110 |
| CG-L0-03 | `contracts/models/store_spec.py` | Pydantic | L0 | 100 |
| CG-L0-04 | `contracts/models/code_artifact.py` | Pydantic | L0 | 100 |
| CG-L0-05 | `contracts/models/build_result.py` | Pydantic | L0 | 150 |
| CG-L0-06 | `contracts/models/agent_message.py` | Pydantic | L0 | 90 |
| CG-L0-07 | `contracts/models/project_spec.py` | Pydantic | L0 | 180 |
| CG-L0-08 | `contracts/models/__init__.py` | Export | L0 | 50 |
| CG-L0-09 | `contracts/__init__.py` | Export | L0 | 30 |
| CG-L0-10 | `contracts/api.yaml` | OpenAPI | L0 | 250 |
| CG-L1-01 | `engine/ue5_scanner.py` | Engine | L1 | 150 |
| CG-L1-02 | `engine/learning_store.py` | Engine | L1 | 180 |
| CG-L1-03 | `ai/test_agent.py` | Agent | L1 | 180 |
| CG-L1-04 | `ai/repair_loop.py` | Agent | L1 | 220 |
| CG-L1-05 | `ai/architect_agent.py` | Agent | L1 | 280 |
| CG-L1-06 | `ai/__init__.py` | Export | L1 | 20 |
| CG-L1-07 | `engine/__init__.py` | Export | L1 | 30 |
| CG-L2-01 | `ai/test_generation/cpp_test_generator.py` | Test | L2 | 200 |
| CG-L2-02 | `ai/test_generation/blueprint_test_validator.py` | Test | L2 | 180 |
| CG-L2-03 | `ai/test_generation/test_harness.py` | Test | L2 | 150 |
| CG-L2-04 | `ai/test_generation/__init__.py` | Export | L2 | 20 |
| CG-L2-05 | `engine/brief_parser.py` | Engine | L2 | 160 |
| CG-L3-01 | `engine/project_scaffolder.py` | Engine | L3 | 250 |
| CG-L3-02 | `templates/__init__.py` | Export | L3 | 10 |
| CG-L4-01 | `engine/cpp_generator.py` | Engine | L4 | 320 |
| CG-L4-02 | `engine/blueprint_generator.py` | Engine | L4 | 280 |
| CG-L4-03 | `engine/platform_guards.py` | Engine | L4 | 140 |
| CG-L5-01 | `engine/build_runner.py` | Engine | L5 | 280 |
| CG-L6-01 | `engine/package_agent.py` | Engine | L6 | 240 |
| CG-L6-02 | `engine/store_agent.py` | Engine | L6 | 200 |
| CG-L7-01 | `server/api/projects.py` | API | L7 | 120 |
| CG-L7-02 | `server/api/architecture.py` | API | L7 | 60 |
| CG-L7-03 | `server/api/generation.py` | API | L7 | 140 |
| CG-L7-04 | `server/api/builds.py` | API | L7 | 80 |
| CG-L7-05 | `server/api/packages.py` | API | L7 | 100 |
| CG-L7-06 | `server/api/store.py` | API | L7 | 70 |
| CG-L7-07 | `server/api/auth.py` | API | L7 | 90 |
| CG-L7-08 | `server/api/__init__.py` | Export | L7 | 50 |
| CG-L7-09 | `server/workers/generation_worker.py` | Worker | L7 | 180 |
| CG-L7-10 | `server/workers/build_worker.py` | Worker | L7 | 100 |
| CG-L7-11 | `server/workers/package_worker.py` | Worker | L7 | 120 |
| CG-L7-12 | `server/workers/__init__.py` | Export | L7 | 20 |
| CG-L7-13 | `server/models/database.py` | Model | L7 | 80 |
| CG-L7-14 | `server/models/project.py` | Model | L7 | 60 |
| CG-L7-15 | `server/models/build.py` | Model | L7 | 50 |
| CG-L7-16 | `server/models/__init__.py` | Export | L7 | 20 |
| CG-L7-17 | `dashboard/package.json` | Config | L7 | 60 |
| CG-L7-18 | `dashboard/vite.config.js` | Config | L7 | 40 |
| CG-L7-19 | `dashboard/index.html` | HTML | L7 | 30 |
| CG-L7-20 | `dashboard/src/main.jsx` | React | L7 | 40 |
| CG-L7-21 | `dashboard/src/index.css` | CSS | L7 | 30 |
| CG-L7-22 | `dashboard/src/App.jsx` | React | L7 | 80 |
| CG-L7-23 | `dashboard/src/api/client.js` | JS | L7 | 100 |
| CG-L7-24 | `dashboard/src/api/endpoints.js` | JS | L7 | 80 |
| CG-L7-25 | `dashboard/src/api/index.js` | JS | L7 | 40 |
| CG-L7-26 | `dashboard/src/components/Header.jsx` | React | L7 | 40 |
| CG-L7-27 | `dashboard/src/components/Sidebar.jsx` | React | L7 | 60 |
| CG-L7-28 | `dashboard/src/components/ProgressBar.jsx` | React | L7 | 50 |
| CG-L7-29 | `dashboard/src/components/FileNode.jsx` | React | L7 | 70 |
| CG-L7-30 | `dashboard/src/components/ConsoleOutput.jsx` | React | L7 | 80 |
| CG-L7-31 | `dashboard/src/components/StatusBadge.jsx` | React | L7 | 35 |
| CG-L7-32 | `dashboard/src/components/DownloadButton.jsx` | React | L7 | 40 |
| CG-L7-33 | `dashboard/src/components/index.js` | JS | L7 | 30 |
| CG-L7-34 | `dashboard/src/hooks/useProject.js` | JS | L7 | 60 |
| CG-L7-35 | `dashboard/src/hooks/useBuild.js` | JS | L7 | 50 |
| CG-L7-36 | `dashboard/src/hooks/index.js` | JS | L7 | 20 |
| CG-L7-37 | `dashboard/src/styles/variables.css` | CSS | L7 | 50 |
| CG-L7-38 | `dashboard/src/styles/main.css` | CSS | L7 | 200 |
| CG-L7-39 | `dashboard/src/pages/ProjectBrief.jsx` | React | L7 | 150 |
| CG-L7-40 | `dashboard/src/pages/GenerationProgress.jsx` | React | L7 | 120 |
| CG-L7-41 | `dashboard/src/pages/FileTree.jsx` | React | L7 | 100 |
| CG-L7-42 | `dashboard/src/pages/BuildConsole.jsx` | React | L7 | 140 |
| CG-L7-43 | `dashboard/src/pages/PlatformPackages.jsx` | React | L7 | 130 |
| CG-L7-44 | `dashboard/src/pages/LearningStore.jsx` | React | L7 | 110 |
| CG-L8-01 | `server/main.py` | Entry | L8 | 100 |
| CG-L8-02 | `server/__init__.py` | Export | L8 | 10 |
| CG-L9-01 | `tests/__init__.py` | Export | L9 | 10 |
| CG-L9-02 | `tests/conftest.py` | Test | L9 | 80 |
| CG-L9-03 | `tests/test_platform_guards.py` | Test | L9 | 120 |
| CG-L9-04 | `tests/test_architect_agent.py` | Test | L9 | 150 |
| CG-L9-05 | `tests/test_cpp_generator.py` | Test | L9 | 140 |
| CG-L9-06 | `tests/test_blueprint_generator.py` | Test | L9 | 130 |
| CG-L9-07 | `tests/test_build_runner.py` | Test | L9 | 160 |
| CG-L9-08 | `tests/test_repair_loop.py` | Test | L9 | 140 |
| CG-L9-09 | `tests/test_dependency_graph.py` | Test | L9 | 180 |
| CG-L9-10 | `tests/test_module_dependencies.py` | Test | L9 | 120 |
| CG-L9-11 | `tests/integration/__init__.py` | Export | L9 | 10 |
| CG-L9-12 | `tests/integration/test_full_pipeline.py` | Test | L9 | 250 |

**Total Nodes:** 101 (excluding L10 infrastructure which is complete)

### 2.2 Edge List (Directed Dependencies)

```
# LEVEL 0 — Foundation (no internal deps)
CG-L0-01: []  # game_brief.py
CG-L0-02: []  # platform_spec.py
CG-L0-03: []  # store_spec.py
CG-L0-04: []  # code_artifact.py
CG-L0-05: [CG-L0-04]  # build_result.py depends on code_artifact
CG-L0-06: []  # agent_message.py
CG-L0-07: [CG-L0-01, CG-L0-05]  # project_spec.py depends on game_brief, build_result
CG-L0-08: [CG-L0-01, CG-L0-02, CG-L0-03, CG-L0-04, CG-L0-05, CG-L0-06, CG-L0-07]
CG-L0-09: [CG-L0-08]
CG-L0-10: []  # api.yaml (already complete)

# LEVEL 1 — Core Agents
CG-L1-01: [CG-L0-09]  # ue5_scanner.py
CG-L1-02: [CG-L0-09]  # learning_store.py
CG-L1-03: [CG-L0-09]  # test_agent.py
CG-L1-04: [CG-L0-09]  # repair_loop.py
CG-L1-05: [CG-L0-09, templates/]  # architect_agent.py
CG-L1-06: [CG-L1-03, CG-L1-04, CG-L1-05]  # ai/__init__.py
CG-L1-07: [CG-L1-01, CG-L1-02]  # engine/__init__.py

# LEVEL 2 — Test Generation + Parsing
CG-L2-01: [CG-L0-09, CG-L1-03]  # cpp_test_generator.py
CG-L2-02: [CG-L0-09, CG-L1-03]  # blueprint_test_validator.py
CG-L2-03: [CG-L0-09, CG-L1-03]  # test_harness.py
CG-L2-04: [CG-L2-01, CG-L2-02, CG-L2-03]  # test_generation/__init__.py
CG-L2-05: [CG-L0-09, CG-L1-05]  # brief_parser.py

# LEVEL 3 — Project Scaffolding
CG-L3-01: [CG-L0-09, CG-L2-05]  # project_scaffolder.py
CG-L3-02: []  # templates/__init__.py

# LEVEL 4 — Code Generation
CG-L4-01: [CG-L0-09, CG-L3-01]  # cpp_generator.py
CG-L4-02: [CG-L0-09, CG-L3-01]  # blueprint_generator.py
CG-L4-03: [CG-L0-09]  # platform_guards.py

# LEVEL 5 — Build Execution
CG-L5-01: [CG-L0-09, CG-L4-01, CG-L1-03]  # build_runner.py

# LEVEL 6 — Packaging + Store
CG-L6-01: [CG-L0-09, CG-L5-01]  # package_agent.py
CG-L6-02: [CG-L0-09, CG-L6-01]  # store_agent.py

# LEVEL 7 — Server + Dashboard (Python)
CG-L7-01: [CG-L0-09, CG-L2-05, CG-L3-01]  # projects.py
CG-L7-02: [CG-L0-09, CG-L1-05]  # architecture.py
CG-L7-03: [CG-L0-09, CG-L4-01, CG-L4-02, CG-L5-01]  # generation.py
CG-L7-04: [CG-L0-09, CG-L5-01]  # builds.py
CG-L7-05: [CG-L0-09, CG-L6-01]  # packages.py
CG-L7-06: [CG-L0-09, CG-L6-02]  # store.py
CG-L7-07: [CG-L0-09]  # auth.py
CG-L7-08: [CG-L7-01, CG-L7-02, CG-L7-03, CG-L7-04, CG-L7-05, CG-L7-06, CG-L7-07]
CG-L7-09: [CG-L0-09, CG-L2-05, CG-L3-01, CG-L4-01, CG-L4-02]  # generation_worker.py
CG-L7-10: [CG-L0-09, CG-L5-01]  # build_worker.py
CG-L7-11: [CG-L0-09, CG-L6-01]  # package_worker.py
CG-L7-12: [CG-L7-09, CG-L7-10, CG-L7-11]
CG-L7-13: [external: sqlalchemy]  # database.py
CG-L7-14: [CG-L7-13]  # project.py
CG-L7-15: [CG-L7-13]  # build.py
CG-L7-16: [CG-L7-13, CG-L7-14, CG-L7-15]

# LEVEL 7 — Dashboard (JavaScript/React)
CG-L7-17: []  # package.json
CG-L7-18: []  # vite.config.js
CG-L7-19: []  # index.html
CG-L7-23: [external: axios]  # client.js
CG-L7-24: []  # endpoints.js
CG-L7-25: [CG-L7-23, CG-L7-24]  # api/index.js
CG-L7-37: []  # variables.css
CG-L7-38: [CG-L7-37]  # main.css
CG-L7-21: [CG-L7-37, CG-L7-38]  # index.css
CG-L7-26: []  # Header.jsx
CG-L7-27: []  # Sidebar.jsx
CG-L7-28: []  # ProgressBar.jsx
CG-L7-29: []  # FileNode.jsx
CG-L7-30: []  # ConsoleOutput.jsx
CG-L7-31: []  # StatusBadge.jsx
CG-L7-32: []  # DownloadButton.jsx
CG-L7-33: [CG-L7-26, CG-L7-27, CG-L7-28, CG-L7-29, CG-L7-30, CG-L7-31, CG-L7-32]
CG-L7-34: [CG-L7-23]  # useProject.js
CG-L7-35: [CG-L7-23]  # useBuild.js
CG-L7-36: [CG-L7-34, CG-L7-35]
CG-L7-39: [CG-L7-23, CG-L7-24]  # ProjectBrief.jsx
CG-L7-40: [CG-L7-23, CG-L7-24]  # GenerationProgress.jsx
CG-L7-41: [CG-L7-23, CG-L7-24, CG-L7-29]  # FileTree.jsx
CG-L7-42: [CG-L7-23, CG-L7-24, CG-L7-30]  # BuildConsole.jsx
CG-L7-43: [CG-L7-23, CG-L7-24, CG-L7-32]  # PlatformPackages.jsx
CG-L7-44: [CG-L7-23, CG-L7-24]  # LearningStore.jsx
CG-L7-22: [CG-L7-39, CG-L7-40, CG-L7-41, CG-L7-42, CG-L7-43, CG-L7-44, CG-L7-26, CG-L7-27]  # App.jsx
CG-L7-20: [CG-L7-22, CG-L7-21]  # main.jsx

# LEVEL 8 — Server Entry Point
CG-L8-01: [CG-L7-08, CG-L7-12, CG-L7-16]  # server/main.py
CG-L8-02: [CG-L8-01]  # server/__init__.py

# LEVEL 9 — Tests
CG-L9-01: []  # tests/__init__.py
CG-L9-02: [external: pytest]  # conftest.py
CG-L9-03: [CG-L4-03]  # test_platform_guards.py
CG-L9-04: [CG-L1-05]  # test_architect_agent.py
CG-L9-05: [CG-L4-01]  # test_cpp_generator.py
CG-L9-06: [CG-L4-02]  # test_blueprint_generator.py
CG-L9-07: [CG-L5-01]  # test_build_runner.py
CG-L9-08: [CG-L1-04]  # test_repair_loop.py
CG-L9-09: [external]  # test_dependency_graph.py
CG-L9-10: [all modules]  # test_module_dependencies.py
CG-L9-11: []  # integration/__init__.py
CG-L9-12: [all modules]  # test_full_pipeline.py
```

### 2.3 Adjacency List (Compact)

```python
GRAPH_A = {
    # L0 — Foundation
    'CG-L0-01': [],
    'CG-L0-02': [],
    'CG-L0-03': [],
    'CG-L0-04': [],
    'CG-L0-05': ['CG-L0-04'],
    'CG-L0-06': [],
    'CG-L0-07': ['CG-L0-01', 'CG-L0-05'],
    'CG-L0-08': ['CG-L0-01', 'CG-L0-02', 'CG-L0-03', 'CG-L0-04', 'CG-L0-05', 'CG-L0-06', 'CG-L0-07'],
    'CG-L0-09': ['CG-L0-08'],
    'CG-L0-10': [],
    
    # L1 — Core Agents
    'CG-L1-01': ['CG-L0-09'],
    'CG-L1-02': ['CG-L0-09'],
    'CG-L1-03': ['CG-L0-09'],
    'CG-L1-04': ['CG-L0-09'],
    'CG-L1-05': ['CG-L0-09'],
    'CG-L1-06': ['CG-L1-03', 'CG-L1-04', 'CG-L1-05'],
    'CG-L1-07': ['CG-L1-01', 'CG-L1-02'],
    
    # L2 — Test Gen + Parse
    'CG-L2-01': ['CG-L0-09', 'CG-L1-03'],
    'CG-L2-02': ['CG-L0-09', 'CG-L1-03'],
    'CG-L2-03': ['CG-L0-09', 'CG-L1-03'],
    'CG-L2-04': ['CG-L2-01', 'CG-L2-02', 'CG-L2-03'],
    'CG-L2-05': ['CG-L0-09', 'CG-L1-05'],
    
    # L3 — Scaffold
    'CG-L3-01': ['CG-L0-09', 'CG-L2-05'],
    'CG-L3-02': [],
    
    # L4 — Code Gen
    'CG-L4-01': ['CG-L0-09', 'CG-L3-01'],
    'CG-L4-02': ['CG-L0-09', 'CG-L3-01'],
    'CG-L4-03': ['CG-L0-09'],
    
    # L5 — Build
    'CG-L5-01': ['CG-L0-09', 'CG-L4-01', 'CG-L1-03'],
    
    # L6 — Package + Store
    'CG-L6-01': ['CG-L0-09', 'CG-L5-01'],
    'CG-L6-02': ['CG-L0-09', 'CG-L6-01'],
    
    # L7 — Server (Python)
    'CG-L7-01': ['CG-L0-09', 'CG-L2-05', 'CG-L3-01'],
    'CG-L7-02': ['CG-L0-09', 'CG-L1-05'],
    'CG-L7-03': ['CG-L0-09', 'CG-L4-01', 'CG-L4-02', 'CG-L5-01'],
    'CG-L7-04': ['CG-L0-09', 'CG-L5-01'],
    'CG-L7-05': ['CG-L0-09', 'CG-L6-01'],
    'CG-L7-06': ['CG-L0-09', 'CG-L6-02'],
    'CG-L7-07': ['CG-L0-09'],
    'CG-L7-08': ['CG-L7-01', 'CG-L7-02', 'CG-L7-03', 'CG-L7-04', 'CG-L7-05', 'CG-L7-06', 'CG-L7-07'],
    'CG-L7-09': ['CG-L0-09', 'CG-L2-05', 'CG-L3-01', 'CG-L4-01', 'CG-L4-02'],
    'CG-L7-10': ['CG-L0-09', 'CG-L5-01'],
    'CG-L7-11': ['CG-L0-09', 'CG-L6-01'],
    'CG-L7-12': ['CG-L7-09', 'CG-L7-10', 'CG-L7-11'],
    'CG-L7-13': [],  # external deps only
    'CG-L7-14': ['CG-L7-13'],
    'CG-L7-15': ['CG-L7-13'],
    'CG-L7-16': ['CG-L7-13', 'CG-L7-14', 'CG-L7-15'],
    
    # L7 — Dashboard (JS)
    'CG-L7-17': [],
    'CG-L7-18': [],
    'CG-L7-19': [],
    'CG-L7-20': ['CG-L7-21', 'CG-L7-22'],
    'CG-L7-21': ['CG-L7-37', 'CG-L7-38'],
    'CG-L7-22': ['CG-L7-39', 'CG-L7-40', 'CG-L7-41', 'CG-L7-42', 'CG-L7-43', 'CG-L7-44', 'CG-L7-26', 'CG-L7-27'],
    'CG-L7-23': [],
    'CG-L7-24': [],
    'CG-L7-25': ['CG-L7-23', 'CG-L7-24'],
    'CG-L7-26': [],
    'CG-L7-27': [],
    'CG-L7-28': [],
    'CG-L7-29': [],
    'CG-L7-30': [],
    'CG-L7-31': [],
    'CG-L7-32': [],
    'CG-L7-33': ['CG-L7-26', 'CG-L7-27', 'CG-L7-28', 'CG-L7-29', 'CG-L7-30', 'CG-L7-31', 'CG-L7-32'],
    'CG-L7-34': ['CG-L7-23'],
    'CG-L7-35': ['CG-L7-23'],
    'CG-L7-36': ['CG-L7-34', 'CG-L7-35'],
    'CG-L7-37': [],
    'CG-L7-38': ['CG-L7-37'],
    'CG-L7-39': ['CG-L7-23', 'CG-L7-24'],
    'CG-L7-40': ['CG-L7-23', 'CG-L7-24'],
    'CG-L7-41': ['CG-L7-23', 'CG-L7-24', 'CG-L7-29'],
    'CG-L7-42': ['CG-L7-23', 'CG-L7-24', 'CG-L7-30'],
    'CG-L7-43': ['CG-L7-23', 'CG-L7-24', 'CG-L7-32'],
    'CG-L7-44': ['CG-L7-23', 'CG-L7-24'],
    
    # L8 — Entry
    'CG-L8-01': ['CG-L7-08', 'CG-L7-12', 'CG-L7-16'],
    'CG-L8-02': ['CG-L8-01'],
    
    # L9 — Tests
    'CG-L9-01': [],
    'CG-L9-02': [],
    'CG-L9-03': ['CG-L4-03'],
    'CG-L9-04': ['CG-L1-05'],
    'CG-L9-05': ['CG-L4-01'],
    'CG-L9-06': ['CG-L4-02'],
    'CG-L9-07': ['CG-L5-01'],
    'CG-L9-08': ['CG-L1-04'],
    'CG-L9-09': [],
    'CG-L9-10': [],
    'CG-L9-11': [],
    'CG-L9-12': [],
}
```

---

## 3. GRAPH B — RUNTIME IMPORT DEPENDENCIES

### 3.1 Python Runtime Graph

```
# Contracts (imported by all)
contracts.models.game_brief       → pydantic, enum
contracts.models.platform_spec    → pydantic, enum
contracts.models.store_spec       → pydantic
contracts.models.code_artifact    → pydantic
contracts.models.build_result     → pydantic, datetime
contracts.models.agent_message    → pydantic, datetime
contracts.models.project_spec     → pydantic, contracts.models.game_brief
contracts.models                  → all above
contracts                         → contracts.models

# AI Module
ai.test_agent                     → contracts.models
ai.repair_loop                    → contracts.models
ai.architect_agent                → contracts.models, templates.interfaces
ai                                → ai.*

# Engine Module
engine.ue5_scanner                → contracts.models
engine.learning_store             → contracts.models, json
engine.brief_parser               → contracts.models, ai.architect_agent
engine.project_scaffolder         → contracts.models, engine.brief_parser
engine.cpp_generator              → contracts.models, engine.project_scaffolder
engine.blueprint_generator        → contracts.models, engine.project_scaffolder
engine.platform_guards            → contracts.models
engine.build_runner               → contracts.models, engine.cpp_generator, ai.test_agent
engine.package_agent              → contracts.models, engine.build_runner
engine.store_agent                → contracts.models, engine.package_agent
engine                            → engine.*

# Server Module
server.api.projects               → contracts.models, engine.brief_parser, engine.project_scaffolder
server.api.architecture           → contracts.models, ai.architect_agent
server.api.generation             → contracts.models, engine.cpp_generator, engine.blueprint_generator, engine.build_runner
server.api.builds                 → contracts.models, engine.build_runner
server.api.packages               → contracts.models, engine.package_agent
server.api.store                  → contracts.models, engine.store_agent
server.api.auth                   → contracts.models, jwt
server.api                        → server.api.*
server.workers.generation_worker  → contracts.models, engine.*, celery
server.workers.build_worker       → contracts.models, engine.build_runner, celery
server.workers.package_worker     → contracts.models, engine.package_agent, celery
server.workers                    → server.workers.*
server.models.database            → sqlalchemy
server.models.project             → server.models.database, sqlalchemy
server.models.build               → server.models.database, sqlalchemy
server.models                     → server.models.*
server.main                       → server.api.*, server.workers.*, server.models.*, fastapi
```

### 3.2 JavaScript Runtime Graph

```
# Dashboard API
dashboard/src/api/client          → axios
dashboard/src/api/endpoints       → (constants)
dashboard/src/api                 → client, endpoints

# Dashboard Components
dashboard/src/components/Header        → react, react-router-dom
dashboard/src/components/Sidebar       → react, react-router-dom
dashboard/src/components.ProgressBar   → react
dashboard/src/components.FileNode      → react
dashboard/src/components.ConsoleOutput → react
dashboard/src/components.StatusBadge   → react
dashboard/src/components.DownloadButton→ react
dashboard/src/components               → all components

# Dashboard Hooks
dashboard/src/hooks.useProject    → react, api/client, api/endpoints
dashboard/src/hooks.useBuild      → react, api/client, api/endpoints
dashboard/src/hooks               → hooks.*

# Dashboard Styles
dashboard/src/styles.variables    → (css)
dashboard/src/styles.main         → variables.css
dashboard/src/index.css           → variables.css, main.css

# Dashboard Pages
dashboard/src/pages.ProjectBrief       → react, react-hook-form, react-router-dom, api/*
dashboard/src/pages.GenerationProgress → react, api/*, components/*
dashboard/src/pages.FileTree           → react, api/*, components/*
dashboard/src/pages.BuildConsole       → react, api/*, components/*
dashboard/src/pages.PlatformPackages   → react, api/*, components/*
dashboard/src/pages.LearningStore      → react, api/*

# Dashboard App
dashboard/src/App                 → react, react-router-dom, pages/*, components/*
dashboard/src/main.jsx            → react, react-dom, App, index.css
```

---

## 4. CYCLE DETECTION

### 4.1 DFS Cycle Detection (Graph A)

```python
def detect_cycles_graph_a() -> Tuple[bool, List[List[str]]]:
    """
    Detect cycles in Graph A (code generation dependencies).
    
    Returns:
        (has_cycle, list_of_cycles)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in GRAPH_A}
    cycles = []
    
    def dfs(node: str, path: List[str]) -> bool:
        color[node] = GRAY
        for neighbor in GRAPH_A.get(node, []):
            if neighbor not in color:
                continue
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
                return True
            if color[neighbor] == WHITE and dfs(neighbor, path + [neighbor]):
                return True
        color[node] = BLACK
        return False
    
    for node in GRAPH_A:
        if color[node] == WHITE:
            dfs(node, [node])
    
    return (len(cycles) > 0, cycles)


# Expected result: (False, []) — No cycles
```

### 4.2 Kahn's Algorithm for Topological Sort

```python
def topological_sort_graph_a() -> List[str]:
    """
    Perform topological sort on Graph A.
    
    Returns:
        List of nodes in valid generation order
    """
    from collections import deque, defaultdict
    
    # Calculate in-degrees
    in_degree = defaultdict(int)
    for node in GRAPH_A:
        if node not in in_degree:
            in_degree[node] = 0
        for neighbor in GRAPH_A[node]:
            in_degree[neighbor] += 1
    
    # Initialize queue with nodes having in-degree 0
    queue = deque([node for node in GRAPH_A if in_degree[node] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in GRAPH_A.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != len(GRAPH_A):
        raise ValueError("Cycle detected in Graph A")
    
    return result


# Expected: 101 nodes in valid generation order
```

---

## 5. TOPOLOGICAL LEVELS (Generation Order)

### 5.1 Computed Levels

| Level | Nodes | Count | Cumulative |
|-------|-------|-------|------------|
| L0 | CG-L0-01 to CG-L0-10 | 10 | 10 |
| L1 | CG-L1-01 to CG-L1-07 | 7 | 17 |
| L2 | CG-L2-01 to CG-L2-05 | 5 | 22 |
| L3 | CG-L3-01 to CG-L3-02 | 2 | 24 |
| L4 | CG-L4-01 to CG-L4-03 | 3 | 27 |
| L5 | CG-L5-01 | 1 | 28 |
| L6 | CG-L6-01 to CG-L6-02 | 2 | 30 |
| L7 (Python) | CG-L7-01 to CG-L7-16 | 16 | 46 |
| L7 (JS Config) | CG-L7-17 to CG-L7-19, CG-L7-23 to CG-L7-25, CG-L7-37 to CG-L7-38 | 10 | 56 |
| L7 (JS Components) | CG-L7-26 to CG-L7-33 | 8 | 64 |
| L7 (JS Hooks) | CG-L7-34 to CG-L7-36 | 3 | 67 |
| L7 (JS Pages) | CG-L7-39 to CG-L7-44 | 6 | 73 |
| L7 (JS App) | CG-L7-20 to CG-L7-22 | 3 | 76 |
| L8 | CG-L8-01 to CG-L8-02 | 2 | 78 |
| L9 | CG-L9-01 to CG-L9-12 | 12 | 90 |

**Note:** 11 files are infrastructure (L10) already complete.

### 5.2 Generation Sequence

```
Phase 1:  L0 (10 files)  — Contracts foundation
Phase 2:  L1 (7 files)   — Core agents
Phase 3:  L2 (5 files)   — Test gen + parsing
Phase 4:  L3 (2 files)   — Scaffolding
Phase 5:  L4 (3 files)   — Code generators
Phase 6:  L5 (1 file)    — Build runner
Phase 7:  L6 (2 files)   — Package + store
Phase 8:  L7-Python (16 files) — Server API + workers + models
Phase 9:  L7-JS-Config (10 files) — Dashboard config + api + styles
Phase 10: L7-JS-Comp (8 files) — Dashboard components
Phase 11: L7-JS-Hooks (3 files) — Dashboard hooks
Phase 12: L7-JS-Pages (6 files) — Dashboard pages
Phase 13: L7-JS-App (3 files) — Dashboard app entry
Phase 14: L8 (2 files) — Server entry
Phase 15: L9 (12 files) — Tests
```

---

## 6. CRITICAL PATH ANALYSIS

### 6.1 Longest Path (Graph A)

```
Critical Path (15 hops):
CG-L0-01 → CG-L0-07 → CG-L0-08 → CG-L0-09 → 
CG-L1-05 → CG-L2-05 → CG-L3-01 → 
CG-L4-01 → CG-L5-01 → CG-L6-01 → CG-L6-02 → 
CG-L7-06 → CG-L7-08 → CG-L8-01 → CG-L8-02

Path Description:
game_brief → project_spec → models/__init__ → contracts/__init__ →
architect_agent → brief_parser → project_scaffolder →
cpp_generator → build_runner → package_agent → store_agent →
store API → api/__init__ → server/main → server/__init__
```

### 6.2 Parallel Generation Opportunities

| Phase | Parallel Count | Files |
|-------|---------------|-------|
| L0 | 7 | game_brief, platform_spec, store_spec, code_artifact, agent_message (no deps) |
| L1 | 5 | ue5_scanner, learning_store, test_agent, repair_loop, architect_agent |
| L2 | 4 | cpp_test_generator, blueprint_test_validator, test_harness, brief_parser |
| L7-JS-Config | 7 | package.json, vite.config, index.html, client.js, endpoints.js, variables.css, main.css |
| L7-JS-Comp | 7 | All components (no inter-deps) |

---

## 7. DEPENDENCY VALIDATION

### 7.1 Pre-Generation Validation

```python
def validate_graph_a() -> ValidationResult:
    """
    Validate Graph A before code generation.
    
    Returns:
        ValidationResult with any issues
    """
    result = ValidationResult()
    
    # Check for cycles
    has_cycle, cycles = detect_cycles_graph_a()
    if has_cycle:
        result.add_error(f"Cycles detected: {cycles}")
    
    # Check all nodes exist
    for node, deps in GRAPH_A.items():
        for dep in deps:
            if dep not in GRAPH_A:
                result.add_error(f"Unknown dependency: {dep} (from {node})")
    
    # Check topological sort works
    try:
        order = topological_sort_graph_a()
        result.generation_order = order
    except ValueError as e:
        result.add_error(str(e))
    
    return result
```

### 7.2 Post-Generation Validation

```python
def validate_generated_code() -> ValidationResult:
    """
    Validate generated code matches dependency graph.
    
    Returns:
        ValidationResult with any issues
    """
    result = ValidationResult()
    
    # Check all files exist
    for node_id, file_path in NODE_FILES.items():
        if not Path(file_path).exists():
            result.add_error(f"Missing file: {file_path}")
    
    # Check imports match graph
    for node_id, deps in GRAPH_A.items():
        file_path = NODE_FILES[node_id]
        actual_imports = extract_imports(file_path)
        
        for dep in deps:
            if dep.startswith('CG-'):
                expected_module = NODE_FILES[dep]
                if not is_imported(expected_module, actual_imports):
                    result.add_error(f"Missing import in {file_path}: {expected_module}")
    
    return result
```

---

## 8. VISUALIZATION

### 8.1 High-Level Dependency Diagram

```
                    ┌─────────────────┐
                    │   L0: Contracts │
                    │   (10 files)    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │ L1: Agents  │ │ L2: Test    │ │ L3: Scaffold│
    │ (7 files)   │ │ (5 files)   │ │ (2 files)   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ L4: Code    │
                    │ (3 files)   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ L5: Build   │
                    │ (1 file)    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ L6: Package │
                    │ (2 files)   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │ L7: Server  │ │ L7: Dash    │ │ L8: Entry   │
    │ (16 files)  │ │ (28 files)  │ │ (2 files)   │
    └─────────────┘ └─────────────┘ └──────┬──────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │ L9: Tests   │
                                    │ (12 files)  │
                                    └─────────────┘
```

---

## 9. NEXT FILE TO GENERATE

Based on topological sort:

**Next File:** `contracts/models/game_brief.py` (CG-L0-01)
- **Dependencies:** None
- **Target Lines:** 120
- **Stub Lines:** 64
- **Implementation:** Full Pydantic models with validators

---

*End of Code Generation Dependency Graph*
