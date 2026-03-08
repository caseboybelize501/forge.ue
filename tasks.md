# FORGE Build Tasks

## Step 0 — Contracts + UE5 Interface Headers (Immutable)

- [ ] contracts/models/game_brief.py
- [ ] contracts/models/project_spec.py
- [ ] contracts/models/code_artifact.py
- [ ] contracts/models/build_result.py
- [ ] contracts/models/agent_message.py
- [ ] contracts/models/platform_spec.py
- [ ] contracts/models/store_spec.py
- [ ] contracts/api.yaml
- [ ] templates/interfaces/IForgeGameMode.h
- [ ] templates/interfaces/IForgeCharacter.h
- [ ] templates/interfaces/IForgeGameInstance.h
- [ ] templates/interfaces/IForgeInventory.h
- [ ] templates/interfaces/IForgeSaveGame.h
- [ ] templates/interfaces/IForgeUIManager.h
- [ ] templates/interfaces/IForgeAudioManager.h
- [ ] templates/interfaces/IForgeAchievement.h
- [ ] templates/interfaces/IForgePlatformLayer.h
- [ ] templates/interfaces/IForgeOnlineSubsystem.h

## AI Meta-Layer (Level 1-2)

- [ ] ai/architect_agent.py (FR-03, FR-13–FR-22)
- [ ] ai/test_agent.py (FR-08)
- [ ] ai/repair_loop.py (FR-09, NFR-03, NFR-04)
- [ ] ai/test_generation/cpp_test_generator.py
- [ ] ai/test_generation/blueprint_test_validator.py
- [ ] ai/test_generation/test_harness.py

## Engine Pipeline (Levels 1-6)

- [ ] engine/ue5_scanner.py (FR-01)
- [ ] engine/brief_parser.py (FR-02)
- [ ] engine/project_scaffolder.py (FR-06)
- [ ] engine/cpp_generator.py (FR-04, NFR-03)
- [ ] engine/blueprint_generator.py (FR-05, NFR-05)
- [ ] engine/build_runner.py (FR-07, NFR-01, NFR-04)
- [ ] engine/package_agent.py (FR-10)
- [ ] engine/store_agent.py (FR-11)
- [ ] engine/learning_store.py (FR-12)
- [ ] engine/platform_guards.py (NFR-06)

## Server (Level 7-8)

- [ ] server/api/projects.py
- [ ] server/api/architecture.py
- [ ] server/api/generation.py
- [ ] server/api/builds.py
- [ ] server/api/packages.py
- [ ] server/api/store.py
- [ ] server/api/auth.py
- [ ] server/workers/generation_worker.py
- [ ] server/workers/build_worker.py
- [ ] server/workers/package_worker.py
- [ ] server/main.py

## Dashboard (Level 7, Parallel with Server)

- [ ] dashboard/src/pages/ProjectBrief.jsx
- [ ] dashboard/src/pages/GenerationProgress.jsx
- [ ] dashboard/src/pages/FileTree.jsx
- [ ] dashboard/src/pages/BuildConsole.jsx
- [ ] dashboard/src/pages/PlatformPackages.jsx
- [ ] dashboard/src/pages/LearningStore.jsx

## Tests

- [ ] tests/test_platform_guards.py (safety gate)
- [ ] tests/test_architect_agent.py
- [ ] tests/test_cpp_generator.py
- [ ] tests/test_blueprint_generator.py
- [ ] tests/test_build_runner.py
- [ ] tests/test_repair_loop.py
- [ ] tests/integration/test_full_pipeline.py

## Infrastructure

- [ ] docker-compose.yml
- [ ] .vscode/ workspace config
- [ ] PRIVATE_LICENSE.md
- [ ] README.md
- [ ] tasks.md (this file)

---

## Build Order

1. **Phase 0**: Contracts + Interface Headers (L0)
2. **Phase 1**: Core Agents + Scanners (L1)
3. **Phase 2**: Test Generation + Brief Parsing (L2)
4. **Phase 3**: Project Scaffolding (L3)
5. **Phase 4**: Code Generation (L4)
6. **Phase 5**: Build Execution (L5)
7. **Phase 6**: Packaging + Store (L6)
8. **Phase 7**: Server + Dashboard (L7)
9. **Phase 8**: Server Entry Point (L8)
10. **Phase 9**: Tests
11. **Phase 10**: Infrastructure

Each phase must pass 4-pass critic gate before proceeding to next phase.
