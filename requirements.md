# FORGE — Requirements Specification

## 1. SYSTEM OVERVIEW

**FORGE** is an autonomous Unreal Engine 5 game development platform that takes a game brief and generates a complete UE5 project structure, C++ systems with Blueprint-exposed interfaces, validates through automated testing and live compilation, packages for all platforms, and ships.

**Core Value Proposition:** Game development is 70% boilerplate. FORGE automates systems generation (character movement, inventory, save/load, UI framework, input mapping, achievement hooks, audio manager, game state machine, platform abstraction layer, online subsystem integration, packaging pipeline) so humans can focus on creative direction and content.

---

## 2. HARD REQUIREMENTS

| ID | Requirement | Validation |
|----|-------------|------------|
| HR-01 | **UE5 Bootstrap:** Scan for `UNREAL_ENGINE_ROOT`, verify version ≥ 5.3, detect platform SDKs (`ANDROID_SDK_ROOT`, `IOS_TOOLCHAIN`, `SWITCH_SDK_ROOT`, `PS5_SDK_ROOT`, `XBOX_GDK_ROOT`) | `engine/ue5_scanner.py` |
| HR-02 | **Contracts First:** All C++ interface headers (.h), Pydantic schemas, and API contracts generated before implementation. Immutable after Step 0 human review. | Step 0 gate |
| HR-03 | **Critic Gate:** No topological level advances until 4-pass critic clears. C++ files require UBT compilation check. Max 3 repair attempts per file. HALT on failure. | `ai/repair_loop.py` |
| HR-04 | **Deduplication:** Generated files keyed by `(project_id + file_path + content_hash)`. Never regenerate identical unchanged files. | All generators |
| HR-05 | **Platform SDK Gate:** Console packaging requires explicit `PLATFORM_SDK_AVAILABLE=true` env flag + SDK path validation. Packaging gates on SDK presence only. | `engine/package_agent.py` |

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 Pipeline Requirements (FORGE Platform)

| ID | Requirement | Module |
|----|-------------|--------|
| FR-01 | Scan UE5 install, version check, platform SDK detection | `engine/ue5_scanner.py` |
| FR-02 | Parse GameBrief → RequirementSpec via LLM | `engine/brief_parser.py` |
| FR-03 | architect_agent: brief → full UE5 project architecture | `ai/architect_agent.py` |
| FR-04 | Generate C++ .h + .cpp for all designed systems | `engine/cpp_generator.py` |
| FR-05 | Generate Blueprint graphs as structured JSON | `engine/blueprint_generator.py` |
| FR-06 | Generate .uproject, Build.cs, Target.cs, .ini configs | `engine/project_scaffolder.py` |
| FR-07 | Compile via UnrealBuildTool — capture errors per file | `engine/build_runner.py` |
| FR-08 | test_agent: generate test cases per generated system | `ai/test_agent.py` |
| FR-09 | repair_loop: UBT error → targeted fix → recompile | `ai/repair_loop.py` |
| FR-10 | package_agent: cook + pak for each available platform | `engine/package_agent.py` |
| FR-11 | store_agent: generate Steam/EGS submission config | `engine/store_agent.py` |
| FR-12 | LearningStore: pattern library per genre + subsystem | `engine/learning_store.py` |

### 3.2 UE5 System Requirements (Architect Knowledge)

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-13 | GameMode / GameState / PlayerState architecture | Base game state machine |
| FR-14 | Character + Pawn + Controller hierarchy | Player and NPC entities |
| FR-15 | UE5 Subsystem pattern | GameInstanceSubsystem, LocalSubsystem, EngineSubsystem |
| FR-16 | Enhanced Input System (UE 5.1+) | Input mapping and binding |
| FR-17 | Gameplay Ability System (GAS) | Combat/skills for action/RPG genres |
| FR-18 | Lumen + Nanite rendering pipeline configs | Next-gen rendering |
| FR-19 | World Partition for open world games | Large world streaming |
| FR-20 | Online Subsystem (EOS + Steam) integration | Multiplayer and achievements |
| FR-21 | Platform abstraction | One codebase, all targets |
| FR-22 | UnrealBuildTool module dependency graph | Per-project module resolution |

---

## 4. NON-FUNCTIONAL REQUIREMENTS

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Full UBT compile of generated project | < 10min on AMD Ryzen 9 7950X |
| NFR-02 | LLM inference runs alongside UE5 editor | 20GB VRAM for model, 12GB headroom for editor |
| NFR-03 | Generated C++ follows UE5 coding standards | UCLASS, UPROPERTY, UFUNCTION macros correct |
| NFR-04 | All generated code passes UnrealHeaderTool (UHT) | First pass, no manual fixes |
| NFR-05 | Blueprint JSON round-trips to valid .uasset import | Import via UE5 commandlet |
| NFR-06 | No generated code references SDK symbols without platform guards | `#if PLATFORM_PS5`, `#if PLATFORM_XBOXONE` etc. |

---

## 5. CONTRACT LAYER REQUIREMENTS

### 5.1 Layer A — Pipeline Contracts (Pydantic)

| File | Schema | Purpose |
|------|--------|---------|
| `contracts/models/game_brief.py` | `GameBrief`, `Genre`, `Platform`, `MechanicSpec` | Input brief schema |
| `contracts/models/project_spec.py` | `ProjectSpec`, `ModuleSpec`, `SubsystemRef` | Architecture output |
| `contracts/models/code_artifact.py` | `CppFile`, `HeaderFile`, `BlueprintGraph` | Generated code |
| `contracts/models/build_result.py` | `CompileResult`, `TestResult`, `PackageResult` | Build validation |
| `contracts/models/agent_message.py` | `AgentTask`, `AgentResult`, `CriticResult` | Agent communication |
| `contracts/models/platform_spec.py` | `PlatformTarget`, `SDKStatus`, `PackageConfig` | Platform targets |
| `contracts/models/store_spec.py` | `StoreSubmission`, `StoreAssets`, `RatingConfig` | Store submission |
| `contracts/api.yaml` | OpenAPI 3.0 | REST API specification |

### 5.2 Layer B — UE5 C++ Interface Headers (Immutable)

| Header | Interface |
|--------|-----------|
| `templates/interfaces/IForgeGameMode.h` | Base GameMode for all projects |
| `templates/interfaces/IForgeCharacter.h` | Base Character with common interface |
| `templates/interfaces/IForgeGameInstance.h` | Persistent state, save/load interface |
| `templates/interfaces/IForgeInventory.h` | Inventory system interface |
| `templates/interfaces/IForgeSaveGame.h` | Save game base class interface |
| `templates/interfaces/IForgeUIManager.h` | HUD + widget manager interface |
| `templates/interfaces/IForgeAudioManager.h` | Audio system interface |
| `templates/interfaces/IForgeAchievement.h` | Achievement/trophy interface |
| `templates/interfaces/IForgePlatformLayer.h` | Platform abstraction interface |
| `templates/interfaces/IForgeOnlineSubsystem.h` | Online/multiplayer interface |

---

## 6. API ENDPOINT REQUIREMENTS

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/projects` | Create project from GameBrief |
| GET | `/api/projects/:id/architecture` | Get architect plan for review |
| POST | `/api/projects/:id/generate` | Trigger full generation |
| GET | `/api/projects/:id/progress` | Get topo level + critic status |
| GET | `/api/projects/:id/files` | Get generated file tree |
| GET | `/api/projects/:id/build` | Get compilation status |
| POST | `/api/projects/:id/package` | Trigger platform packaging |
| GET | `/api/projects/:id/package/:platform` | Download binary/zip |
| GET | `/api/projects/:id/critic-log` | Get full critic audit trail |

---

## 7. ARCHITECT AGENT DECISION TREE

### 7.1 Subsystem Selection (by Genre)

| Genre | Subsystems |
|-------|------------|
| Action/RPG | GAS (Gameplay Ability System) required |
| Open World | World Partition + Level Streaming |
| Multiplayer | Online Subsystem + replication rules |
| Mobile | Reduced tick rate + aggressive LOD |
| Puzzle/Strategy | Custom state machine over GAS |

### 7.2 Language Allocation

| System Type | Implementation |
|-------------|----------------|
| Performance-critical | C++ (Physics, AI behavior trees, networking/replication, core game loop, input handling, GAS attributes, platform abstraction, save/load serialization) |
| Designer-facing | Blueprint JSON (Gameplay event responses, UI logic, level scripting, ability effects, animation state machines, pickup/trigger volumes, NPC dialogue flow) |

---

## 8. DEPENDENCY GRAPH REQUIREMENTS

### 8.1 Graph A — Pipeline Modules (Python)

Must be cycle-free. Topological levels:

| Level | Modules |
|-------|---------|
| L0 | `contracts/models/*.py`, `contracts/api.yaml`, `templates/interfaces/*.h` |
| L1 | `ai/architect_agent.py`, `ai/test_agent.py`, `ai/repair_loop.py`, `engine/ue5_scanner.py`, `engine/learning_store.py` |
| L2 | `ai/test_generation/*.py`, `engine/brief_parser.py` |
| L3 | `engine/project_scaffolder.py` |
| L4 | `engine/cpp_generator.py`, `engine/blueprint_generator.py` |
| L5 | `engine/build_runner.py` |
| L6 | `engine/package_agent.py`, `engine/store_agent.py` |
| L7 | `server/api/*.py`, `server/workers/*.py`, `dashboard/src/pages/*.jsx` |
| L8 | `server/main.py` |

### 8.2 Graph B — UBT Module Dependencies (C++)

Generated per project by architect_agent. Must be cycle-free. Standard pattern:

```
Core → GameFramework → GenreModules → UI → Platform
```

---

## 9. CRITIC GATE REQUIREMENTS (4-PASS)

### Pass 1 — Syntax (No LLM)

| File Type | Validation |
|-----------|------------|
| Python | `ast.parse()` + `mypy --strict` + `ruff check` |
| C++ .h | `clang-format` check + UHT dry-run |
| C++ .cpp | UnrealBuildTool compile (single file mode) |
| Blueprint JSON | Schema validation against BP node graph spec |
| YAML | `yamllint` + `openapi-spec-validator` |

### Pass 2 — Contract (No LLM)

- Every .cpp implements its paired .h exactly
- All UCLASS/UPROPERTY/UFUNCTION macros present where required
- No console SDK symbols without platform guard macros
- Blueprint JSON: all node connections reference valid node IDs
- ai/ agents: all outputs typed as contracts/models/ schemas

### Pass 3 — Completeness (LLM)

- cpp_generator: no NotImplemented in FR-required systems
- architect_agent: ProjectSpec covers all mechanics from brief
- package_agent: all active platform targets have cook config
- repair_loop: UBT error parser handles all known error types

### Pass 4 — Logic (LLM, UE5-specific)

- UCLASS hierarchy correct (ACharacter not AActor for characters)
- GAS attributes correctly registered in AttributeSet
- Enhanced Input mappings correctly bound in PlayerController
- Save game serialization covers all UPROPERTY(SaveGame) fields
- Platform abstraction layer compiles clean with no SDK (stub)

---

## 10. TEST GENERATION REQUIREMENTS

| Type | Generator | Purpose |
|------|-----------|---------|
| Type 1 — UE5 Automation Tests (C++) | `ai/test_generation/{SystemName}.test.cpp` | Uses FAutomationTestBase, ADD_LATENT_AUTOMATION_COMMAND |
| Type 2 — Blueprint Validation | `ai/test_generation/*.spec.json` | Validates node connections, pin types, variable references |
| Type 3 — Platform Guard Tests | `ai/test_generation/test_platform_guards.py` | Verifies platform macros, TObjectPtr usage, GENERATED_BODY presence |
| Type 4 — Acceptance Tests | `tests/test_*.py` | Validates all FR requirements met |

---

## 11. BUILD PIPELINE ORDER

1. `test_platform_guards.py` — Safety gate (always first)
2. UHT dry-run on all .h — Header tool validation
3. UBT compile — Full project compile (~4-6min on 7950X)
4. UE5 Automation Tests — In-engine test runner
5. Blueprint validation — All BP JSON specs
6. Package per platform:
   - PC (Win64) — Always, no SDK required
   - Mac — If `APPLE_TOOLCHAIN` available
   - Android — If `ANDROID_SDK_ROOT` set
   - iOS — If `IOS_TOOLCHAIN` set
   - PS5 — PLATFORM_SDK_GATE (SDK required)
   - Xbox — PLATFORM_SDK_GATE (GDK required)
   - Switch — PLATFORM_SDK_GATE (SDK required)

---

## 12. SELF-REPAIR SCENARIOS

| Type | Trigger | Response |
|------|---------|----------|
| T1 | UBT compile failure during package | Parse error → repair_loop.py → recompile → re-package |
| T2 | LLM inference OOM | Detect CUDA OOM → drop quant level → resume with degraded model |
| T3 | UE5 editor crash during packaging | Detect FATAL/crash → retry headless cook mode → HALT if fails |
| T4 | Platform SDK not found | Graceful skip → log PLATFORM_SDK_REQUIRED → continue other platforms |
| T5 | Blueprint JSON import failure | Detect import error → re-generate BP JSON → fallback to C++ if 3x fail |

---

## 13. REFERENCE HARDWARE

| Component | Specification |
|-----------|---------------|
| CPU | AMD Ryzen 9 7950X (16C/32T, 4.5GHz) |
| GPU | NVIDIA RTX 5090 (32GB VRAM) |
| RAM | 128GB DDR5-5600 |
| Storage | 16TB NVMe (4× Samsung 990/9100 PRO) |
| LLM | Llama-3-70B Q4_K_M (~20GB VRAM) |

---

## 14. LICENSING

### FORGE Platform
- **License:** PRIVATE — proprietary, all rights reserved
- **Source code, generated game code, pipeline tooling:** Proprietary
- **No redistribution, no forking, no public disclosure**

### Generated Game Output
- **Ownership:** 100% owned by developer
- **Unreal Engine royalty:** 5% of gross revenue after first $1M USD per product per calendar year
- **No FORGE royalty on shipped games**

### Platform Cuts (Developer Revenue Share)
| Platform | Cut | Developer Share |
|----------|-----|-----------------|
| Steam | 30% | 70% |
| EGS | 12% | 88% |
| Console (Sony/MS/Nintendo) | Varies | ~70-80% |

---

## 15. HUMAN GATES

| Gate | Trigger | Action |
|------|---------|--------|
| GATE-1 | After architect_agent | Approve ProjectSpec + UE5 module graph |
| GATE-2 | After code generation | Review generated C++ + Blueprint structure |
| GATE-3 | Before packaging | Approve platform packaging targets |
| GATE-4 | CRITIC HALT | Repair loop exhausted — human intervention required |

---

## 16. FILE STRUCTURE REQUIREMENTS

Generated project must contain minimum 50 files across:

- `contracts/` — Pydantic models, API spec
- `templates/interfaces/` — UE5 C++ interface headers
- `ai/` — Agent meta-layer
- `engine/` — Pipeline modules
- `server/` — REST API + Celery workers
- `dashboard/src/pages/` — React UI components
- `tests/` — Unit + integration tests
- `.vscode/` — Editor configuration
- Infrastructure: `docker-compose.yml`, `.env.example`, `PRIVATE_LICENSE.md`, `README.md`, `tasks.md`

---

## 17. SUCCESS CRITERIA

1. **Step 0 Complete:** All contracts and interface headers generated and immutable
2. **Pipeline Builds:** All Python modules pass syntax + type checking
3. **UE5 Project Compiles:** Generated project passes UHT + UBT with zero errors
4. **Tests Pass:** All acceptance tests (FR-01 through FR-22, NFR-01 through NFR-06) pass
5. **Packages Generated:** At minimum Win64 package; console packages if SDKs available
6. **Learning Store Populated:** Patterns stored for future project generation

---

*End of Requirements Specification*
