AUTONOMOUS UNREAL ENGINE GAME DEVELOPMENT PLATFORM — FORGE
"Takes a game brief, architects complete UE5 project structure,
generates C++ systems with Blueprint-exposed interfaces, validates
through automated testing and live compilation, packages for all
platforms including console, and ships — humans provide creative
direction, FORGE provides every line of code"

LICENSE
───────
This project: PRIVATE REPOSITORY — All Rights Reserved
  → Source code, generated game code, pipeline tooling: proprietary
  → No redistribution, no forking, no public disclosure
  → See PRIVATE_LICENSE.md for terms

Generated game output (your shipped games):
  → You own 100% of all generated C++ and Blueprint code
  → Unreal Engine royalty: 5% of gross revenue after first $1M USD
    per product per calendar year (Epic Games EULA — standard)
  → No FORGE royalty on shipped games — you keep revenue
  → Steam: 30% platform cut (negotiable above $10M)
  → EGS: 12% platform cut
  → Console: platform-specific rev share (Sony/MS/Nintendo vary)

Third-party deps in pipeline: Apache 2.0 / MIT only.
PRIVATE_LICENSE.md included in every build output.

REFERENCE HARDWARE (this prompt optimized for):
  CPU:     AMD Ryzen 9 7950X (16C/32T, 4.5GHz)
  GPU:     NVIDIA RTX 5090 (32GB VRAM)
  RAM:     128GB DDR5-5600
  Storage: 16TB NVMe (4× Samsung 990/9100 PRO)
  LLM:     Llama-3-70B Q4_K_M (~20GB VRAM) — runs alongside UE5 editor
           Leaves ~12GB VRAM headroom for editor GPU usage

THE SPACE
─────────
Game development is 70% boilerplate. Every project needs the same
systems: character movement, inventory, save/load, UI framework,
input mapping, achievement hooks, audio manager, game state machine,
platform abstraction layer, online subsystem integration, packaging
pipeline. A mid-tier studio of 20 engineers spends 18 months on
systems before shipping a single piece of content.

FORGE inverts this. Give it a game brief — genre, mechanics, target
platforms, art style direction. The architect_agent designs the full
UE5 project architecture: which C++ base classes, which subsystems,
which Blueprint interfaces, which third-party plugins. The code agents
generate every .h and .cpp file, every Blueprint graph as structured
JSON, every .ini configuration. The test agent validates compilation
and logic. The repair loop fixes what fails. The packaging agent
builds distributable binaries for every target platform.

The human's job: write the brief, approve the architecture, make
creative decisions about content. FORGE handles every line of code.

After 10 shipped projects, FORGE's learning store contains patterns
for every genre, every UE5 subsystem interaction, every platform
quirk. Project 11 generates faster and with fewer repair cycles than
Project 1. The knowledge compounds.

SYSTEM PROMPT
─────────────
Build FORGE: an autonomous Unreal Engine 5 game development platform.
architect_agent reads game brief → designs project structure →
code agents generate C++ and Blueprint systems → test_agent validates
→ repair_loop fixes failures → package_agent builds platform binaries
→ store_agent prepares submission assets. All agents coordinate through
the ai/ meta-layer. Generated output is a complete UE5 project ready
to open in the editor and ship.

HARD REQUIREMENTS
─────────────────
1. UE5 BOOTSTRAP: scan for UNREAL_ENGINE_ROOT (UnrealBuildTool,
   UE5Editor binary). Verify version ≥ 5.3. Scan for platform SDKs:
   ANDROID_SDK_ROOT, IOS_TOOLCHAIN, SWITCH_SDK_ROOT, PS5_SDK_ROOT,
   XBOX_GDK_ROOT. Writes EngineProfile. UE5 required. Platform SDKs
   optional — gates platform-specific packaging only.
2. CONTRACTS FIRST (Step 0): all C++ interface headers (.h),
   Pydantic schemas for pipeline, and API contracts generated before
   any implementation. Immutable after Step 0 human review.
3. CRITIC GATE: no topo level advances until 4-pass critic clears.
   For C++ files: pass 1 includes UnrealBuildTool compilation check.
   Max 3 repair attempts per file. HALT on failure.
4. DEDUP: generated files keyed by (project_id + file_path +
   content_hash). Never regenerate identical unchanged files.
5. PLATFORM SDK GATE: console packaging requires explicit
   PLATFORM_SDK_AVAILABLE=true env flag + SDK path validation.
   Agent generates + validates code for all platforms. Packaging
   binary artifacts for console gates on SDK presence only.

Return valid JSON: { "files": [{ "path", "content", "language" }] }.
Minimum 50 files. Placeholder implementations acceptable.
Raw JSON only. No markdown, no code fences.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 0 — CONTRACT GENERATION (immutable ground truth)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  TWO CONTRACT LAYERS — both generated in Step 0:                   │
│                                                                     │
│  LAYER A — PIPELINE CONTRACTS (Pydantic, govern agent behavior)    │
│  contracts/models/                                                  │
│    game_brief.py      GameBrief, Genre, Platform, MechanicSpec     │
│    project_spec.py    ProjectSpec, ModuleSpec, SubsystemRef        │
│    code_artifact.py   CppFile, HeaderFile, BlueprintGraph          │
│    build_result.py    CompileResult, TestResult, PackageResult     │
│    agent_message.py   AgentTask, AgentResult, CriticResult         │
│    platform_spec.py   PlatformTarget, SDKStatus, PackageConfig     │
│    store_spec.py      StoreSubmission, StoreAssets, RatingConfig   │
│                                                                     │
│  contracts/api.yaml   (OpenAPI — FORGE REST API)                   │
│  POST /api/projects                  create from GameBrief         │
│  GET  /api/projects/:id/architecture architect plan for review     │
│  POST /api/projects/:id/generate     trigger full generation       │
│  GET  /api/projects/:id/progress     topo level + critic status    │
│  GET  /api/projects/:id/files        generated file tree           │
│  GET  /api/projects/:id/build        compilation status            │
│  POST /api/projects/:id/package      trigger platform packaging    │
│  GET  /api/projects/:id/package/:platform  download binary/zip    │
│  GET  /api/projects/:id/critic-log   full critic audit trail       │
│                                                                     │
│  LAYER B — UE5 C++ INTERFACE HEADERS (generated first, immutable)  │
│  These are the .h files that define all system interfaces.         │
│  Generated from GameBrief before any .cpp is written.             │
│  Every .cpp is written to implement these headers — never reverse. │
│                                                                     │
│  templates/interfaces/                                              │
│    IForgeGameMode.h        base GameMode interface all projects    │
│    IForgeCharacter.h       base Character with common interface    │
│    IForgeGameInstance.h    persistent state, save/load interface   │
│    IForgeInventory.h       inventory system interface              │
│    IForgeSaveGame.h        save game base class interface          │
│    IForgeUIManager.h       HUD + widget manager interface          │
│    IForgeAudioManager.h    audio system interface                  │
│    IForgeAchievement.h     achievement/trophy interface            │
│    IForgePlatformLayer.h   platform abstraction interface          │
│    IForgeOnlineSubsystem.h online/multiplayer interface            │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1 — REQUIREMENTS EXTRACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  PIPELINE REQUIREMENTS (FORGE platform itself)                     │
│  FR-01  Scan UE5 install, version check, platform SDK detection   │
│  FR-02  Parse GameBrief → RequirementSpec via LLM                 │
│  FR-03  architect_agent: brief → full UE5 project architecture    │
│  FR-04  Generate C++ .h + .cpp for all designed systems           │
│  FR-05  Generate Blueprint graphs as structured JSON              │
│  FR-06  Generate .uproject, Build.cs, Target.cs, .ini configs     │
│  FR-07  Compile via UnrealBuildTool — capture errors per file     │
│  FR-08  test_agent: generate test cases per generated system      │
│  FR-09  repair_loop: UBT error → targeted fix → recompile        │
│  FR-10  package_agent: cook + pak for each available platform     │
│  FR-11  store_agent: generate Steam/EGS submission config         │
│  FR-12  LearningStore: pattern library per genre + subsystem      │
│                                                                     │
│  UE5 SYSTEM REQUIREMENTS (what architect_agent must know)         │
│  FR-13  GameMode / GameState / PlayerState architecture            │
│  FR-14  Character + Pawn + Controller hierarchy                   │
│  FR-15  UE5 Subsystem pattern (GameInstanceSubsystem etc)        │
│  FR-16  Enhanced Input System (UE 5.1+)                           │
│  FR-17  Gameplay Ability System (GAS) for combat/skills           │
│  FR-18  Lumen + Nanite rendering pipeline configs                 │
│  FR-19  World Partition for open world games                      │
│  FR-20  Online Subsystem (EOS + Steam) integration                │
│  FR-21  Platform abstraction: one codebase, all targets           │
│  FR-22  UnrealBuildTool module dependency graph per project       │
│                                                                     │
│  NON-FUNCTIONAL REQUIREMENTS                                        │
│  NFR-01  Full UBT compile of generated project < 10min (7950X)   │
│  NFR-02  LLM inference runs alongside UE5 editor simultaneously   │
│          (20GB VRAM for model, 12GB headroom for editor)          │
│  NFR-03  Generated C++ follows UE5 coding standards (UCLASS,     │
│          UPROPERTY, UFUNCTION macros correct)                     │
│  NFR-04  All generated code passes UnrealHeaderTool (UHT) first  │
│  NFR-05  Blueprint JSON round-trips to valid .uasset import       │
│  NFR-06  No generated code references SDK symbols without        │
│          platform guard macros (#if PLATFORM_PS5 etc)            │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2 — ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  GAME BRIEF                                                         │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ai/  (META-LAYER — agents that run the pipeline)            │  │
│  │  ┌─────────────────┐  ┌──────────────────────────────────┐  │  │
│  │  │ architect_agent │  │ test_agent                       │  │  │
│  │  │ .py             │  │ .py                              │  │  │
│  │  │ - reads brief   │  │ - generates test per C++ class   │  │  │
│  │  │ - designs arch  │  │ - validates Blueprint graphs     │  │  │
│  │  │ - selects UE5   │  │ - test_generation/               │  │  │
│  │  │   subsystems    │  │     *.test.cpp                   │  │  │
│  │  │ - emits         │  │     *.spec.json (BP tests)       │  │  │
│  │  │   ProjectSpec   │  └──────────────────────────────────┘  │  │
│  │  └─────────────────┘                                         │  │
│  │  ┌──────────────────────────────────────────────────────┐   │  │
│  │  │ repair_loop.py                                        │   │  │
│  │  │ - catches UBT compile errors                         │   │  │
│  │  │ - catches UHT errors (macro violations)              │   │  │
│  │  │ - targeted file repair (never modify .h interfaces)  │   │  │
│  │  │ - recompile + verify after each attempt              │   │  │
│  │  │ - max 3 attempts → HALT + page human                 │   │  │
│  │  └──────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│       │ ProjectSpec                                                 │
│       ▼                                                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  engine/  (FORGE PIPELINE)                                   │  │
│  │  brief_parser → project_scaffolder → cpp_generator          │  │
│  │  → blueprint_generator → build_runner → package_agent       │  │
│  │  → store_agent → learning_store                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  output/{project_name}/  (GENERATED UE5 PROJECT)             │  │
│  │  Source/         ← generated C++ (.h + .cpp)                │  │
│  │  Content/        ← Blueprint JSON → .uasset imports         │  │
│  │  Config/         ← .ini platform configs                    │  │
│  │  Build/          ← UBT output, cooked content               │  │
│  │  {Name}.uproject ← project descriptor                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

ARCHITECT AGENT DECISION TREE:
┌─────────────────────────────────────────────────────────────────────┐
│  INPUT: GameBrief { genre, mechanics[], platforms[], style }       │
│                                                                     │
│  STEP 1 — SUBSYSTEM SELECTION (from LearningStore + rules)        │
│  genre = action/RPG      → GAS (Gameplay Ability System) required │
│  genre = open_world      → World Partition + Level Streaming      │
│  genre = multiplayer     → Online Subsystem + replication rules   │
│  genre = mobile          → reduced tick rate + LOD aggressive     │
│  genre = puzzle/strategy → custom state machine over GAS          │
│                                                                     │
│  STEP 2 — LANGUAGE ALLOCATION per system                          │
│  C++ (performance-critical, architect decides):                    │
│    Physics, AI behavior trees, networking/replication             │
│    Core game loop, input handling, GAS attributes                 │
│    Platform abstraction layer, save/load serialization            │
│  Blueprint (designer-facing, LLM generates as JSON node graph):   │
│    Gameplay event responses, UI logic, level scripting            │
│    Ability effects, animation state machines                      │
│    Pickup/trigger volumes, NPC dialogue flow                      │
│                                                                     │
│  STEP 3 — MODULE GRAPH (maps to UBT Build.cs dependencies)        │
│  Core → GameFramework → [Genre-specific] → UI → Platform         │
│  Output: ModuleSpec[] with explicit dependency ordering            │
│  This becomes the UBT dependency graph AND the topo sort input    │
│                                                                     │
│  STEP 4 — EMIT ProjectSpec (human reviews at GATE-1)              │
│  { modules[], subsystems[], cpp_files[], blueprint_files[],       │
│    ubt_module_deps[], platform_targets[], estimated_compile_min } │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 — DEPENDENCY GRAPH + CYCLE DETECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  TWO DEPENDENCY GRAPHS — both must be cycle-free:                  │
│                                                                     │
│  GRAPH A — PIPELINE MODULES (Python, governs build order)          │
│                                                                     │
│  [C0] contracts/models/*.py          no deps                       │
│  [C1] contracts/api.yaml             no deps                       │
│  [C2] templates/interfaces/*.h       no deps (UE5 headers)        │
│                                                                     │
│  [AI0] ai/architect_agent.py         deps: [C0, C2]               │
│  [AI1] ai/test_agent.py              deps: [C0]                    │
│  [AI1] ai/repair_loop.py             deps: [C0]                    │
│  [AI2] ai/test_generation/           deps: [C0, AI0, AI1]         │
│           cpp_test_generator.py                                    │
│           blueprint_test_validator.py                              │
│           test_harness.py                                          │
│                                                                     │
│  [E0] engine/ue5_scanner.py          deps: [C0]                   │
│  [E1] engine/brief_parser.py         deps: [C0, AI0]              │
│  [E2] engine/project_scaffolder.py   deps: [C0, C2, E1]           │
│  [E3] engine/cpp_generator.py        deps: [C0, C2, E2]           │
│  [E3] engine/blueprint_generator.py  deps: [C0, E2]               │
│  [E4] engine/build_runner.py         deps: [C0, E3, AI1]          │
│  [E5] engine/package_agent.py        deps: [C0, E4]               │
│  [E6] engine/store_agent.py          deps: [C0, E5]               │
│  [E6] engine/learning_store.py       deps: [C0]                   │
│                                                                     │
│  [S0] server/api/*.py                deps: [C0, C1, all E*]       │
│  [S1] server/workers/*.py            deps: [C0, all E*, Celery]   │
│  [S2] server/main.py                 deps: [S0, S1]               │
│  [D0] dashboard/src/pages/*.jsx      deps: [C1]                   │
│                                                                     │
│  GRAPH B — UBT MODULE DEPS (C++, governs compile order)           │
│  Generated dynamically by architect_agent per project.            │
│  Always follows: Core → GameFramework → GenreModules → UI         │
│  Cycle detection runs on Graph B before any C++ generation starts.│
│  Cycle in UBT graph = architect_agent revises ModuleSpec.         │
│                                                                     │
│  CYCLE CHECK (both graphs): DFS → no back edges → proceed        │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 4 — TOPOLOGICAL SORT → DERIVED BUILD PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  PIPELINE TOPO LEVELS (Kahn's on Graph A):                         │
│                                                                     │
│  LEVEL 0 — contracts/models/*.py, contracts/api.yaml,             │
│             templates/interfaces/*.h                               │
│                                                                     │
│  LEVEL 1 — ai/architect_agent.py, ai/test_agent.py,              │
│             ai/repair_loop.py, engine/ue5_scanner.py,             │
│             engine/learning_store.py                               │
│                                                                     │
│  LEVEL 2 — ai/test_generation/*.py, engine/brief_parser.py       │
│                                                                     │
│  LEVEL 3 — engine/project_scaffolder.py                           │
│                                                                     │
│  LEVEL 4 — engine/cpp_generator.py, engine/blueprint_generator.py│
│                                                                     │
│  LEVEL 5 — engine/build_runner.py                                 │
│                                                                     │
│  LEVEL 6 — engine/package_agent.py, engine/store_agent.py        │
│                                                                     │
│  LEVEL 7 — server/api/*.py, server/workers/*.py,                  │
│             dashboard/src/pages/*.jsx                              │
│                                                                     │
│  LEVEL 8 — server/main.py                                         │
│                                                                     │
│  UE5 C++ TOPO (Graph B — generated per project by architect):     │
│  LEVEL 0 — {Project}Core.Build.cs      (no UE5 game deps)        │
│  LEVEL 1 — {Project}GameFramework      (deps: Core)               │
│  LEVEL 2 — {Project}[Genre]Systems     (deps: GameFramework)      │
│  LEVEL 3 — {Project}UI                 (deps: all above)          │
│  LEVEL 4 — {Project}Platform           (deps: all above)          │
│                                                                     │
│  CELERY PLAN (pipeline levels, auto-derived):                      │
│  chain(chord(group(L0), critic_L0), ... chord(group(L8), critic_L8))│
│                                                                     │
│  CRITICAL PATH: C0→AI0→E1→E2→E3→E4→E5 (7 hops)                  │
│  WIDEST PARALLEL: Level 7 (api + workers + dashboard, ~12 files)  │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 5 — PER-LEVEL PARALLEL GENERATION + 4-PASS CRITIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  PASS 1 — SYNTAX (no LLM):                                        │
│  Python files: ast.parse() + mypy --strict + ruff check           │
│  C++ .h files: clang-format check + UHT dry-run                   │
│  C++ .cpp files: UnrealBuildTool compile (single file mode)       │
│  Blueprint JSON: schema validation against BP node graph spec      │
│  YAML: yamllint + openapi-spec-validator                           │
│                                                                     │
│  PASS 2 — CONTRACT (no LLM):                                      │
│  → Every .cpp implements its paired .h exactly                    │
│  → All UCLASS/UPROPERTY/UFUNCTION macros present where required   │
│  → No console SDK symbols without platform guard macros           │
│    (#if PLATFORM_PS5, #if PLATFORM_XBOXONE etc)                   │
│  → Blueprint JSON: all node connections reference valid node IDs  │
│  → ai/ agents: all outputs typed as contracts/models/ schemas     │
│                                                                     │
│  PASS 3 — COMPLETENESS (LLM):                                     │
│  → cpp_generator: no NotImplemented in FR-required systems        │
│  → architect_agent: ProjectSpec covers all mechanics from brief   │
│  → package_agent: all active platform targets have cook config    │
│  → repair_loop: UBT error parser handles all known error types    │
│                                                                     │
│  PASS 4 — LOGIC (LLM, UE5-specific):                             │
│  → UCLASS hierarchy correct (ACharacter not AActor for characters)│
│  → GAS attributes correctly registered in AttributeSet            │
│  → Enhanced Input mappings correctly bound in PlayerController    │
│  → Save game serialization covers all UPROPERTY(SaveGame) fields │
│  → Platform abstraction layer compiles clean with no SDK (stub)   │
│                                                                     │
│  ALL PASS → lock level → advance                                   │
│  ANY FAIL → Phase 6 repair (C++ errors go to repair_loop.py)     │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 6 — MICRO-REPAIR LOOP (repair_loop.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  TRIGGER TYPES:                                                     │
│  UBT compile error  → parse error, locate file+line, repair .cpp  │
│  UHT error          → macro violation in .h → repair .h           │
│                        (interface headers are immutable —          │
│                         only project-specific .h files repaired)  │
│  Linker error       → missing symbol → check module Build.cs deps │
│  Blueprint invalid  → node graph schema violation → repair JSON   │
│                                                                     │
│  REPAIR CONTEXT:                                                    │
│  { failing_file, error_text, error_line, ue5_version,            │
│    module_deps[], interface_header (immutable ref),               │
│    prior_attempts[], ue5_coding_standard_rules }                  │
│                                                                     │
│  UE5 CODING STANDARD RULES (appended to every repair prompt):     │
│  "UE5 C++ rules: UCLASS() before every UObject-derived class.    │
│   GENERATED_BODY() after every UCLASS declaration.                │
│   UPROPERTY() before every replicated or Blueprint-visible field. │
│   UFUNCTION() before every Blueprint-callable function.           │
│   Never use raw pointers for UObject refs — use TObjectPtr<>.     │
│   Never call delete on UObjects — use garbage collector.          │
│   Platform-specific code MUST be wrapped in platform guards."     │
│                                                                     │
│  Max 3 attempts → HALT + CRITIC_BLOCKED.md + human page          │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 7 — TEST GENERATION (ai/test_agent.py + ai/test_generation/)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  TYPE 1 — UE5 AUTOMATION TESTS (C++, UE5 test framework):         │
│  ai/test_generation/{SystemName}.test.cpp                          │
│  Uses: FAutomationTestBase, ADD_LATENT_AUTOMATION_COMMAND          │
│  Example: ForgeInventoryTest.test.cpp                              │
│    → AddItem: add 5 items → assert count == 5                     │
│    → RemoveItem: remove beyond capacity → assert clamped at 0     │
│    → SaveLoad: serialize → deserialize → assert identical state   │
│    → WeightLimit: exceed weight cap → assert item rejected        │
│                                                                     │
│  TYPE 2 — BLUEPRINT VALIDATION (ai/test_generation/*.spec.json):  │
│  ai/blueprint_test_validator.py consumes these specs              │
│  Checks: all node input pins connected, no dangling exec pins,    │
│  all variable references resolve to valid Blueprint properties    │
│                                                                     │
│  TYPE 3 — PLATFORM GUARD TESTS (mechanical, run first):          │
│  ai/test_generation/test_platform_guards.py                        │
│    → grep all .cpp/.h for PS5/Xbox/Switch SDK symbols             │
│    → assert every occurrence wrapped in platform guard macro      │
│    → assert no raw pointer UObject refs (TObjectPtr check)        │
│    → assert GENERATED_BODY() present in all UCLASS headers        │
│                                                                     │
│  TYPE 4 — ACCEPTANCE TESTS (per FR):                              │
│  test_architect_agent.py                                           │
│    → FR-03: action brief → ProjectSpec contains GAS module        │
│    → FR-03: multiplayer brief → replication rules in ModuleSpec   │
│    → FR-22: ModuleSpec UBT deps are cycle-free (Graph B check)   │
│  test_build_runner.py                                              │
│    → FR-07: valid project → UBT exits 0                           │
│    → FR-09: injected error → repair_loop fires + fixes            │
│    → NFR-04: UHT runs before UBT, errors caught first             │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 8 — TEST EXECUTION + BUILD PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  ORDER:                                                             │
│  1. test_platform_guards.py    safety — always first               │
│  2. UHT dry-run on all .h     header tool validation               │
│  3. UBT compile               full project compile (7950X ~4-6min) │
│  4. UE5 Automation Tests      in-engine test runner                │
│  5. Blueprint validation      all BP JSON specs                    │
│  6. Package (per platform):                                        │
│     a. PC (Win64)             always — no SDK required            │
│     b. Mac                    if APPLE_TOOLCHAIN available         │
│     c. Android                if ANDROID_SDK_ROOT set             │
│     d. iOS                    if IOS_TOOLCHAIN set                │
│     e. PS5                    PLATFORM_SDK_GATE — SDK required    │
│     f. Xbox                   PLATFORM_SDK_GATE — GDK required    │
│     g. Switch                 PLATFORM_SDK_GATE — SDK required    │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 9 — SELF-REPAIR LOOP (runtime)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  T1 — UBT compile failure during package                           │
│       → parse error → repair_loop.py → recompile → re-package    │
│                                                                     │
│  T2 — LLM inference OOM (editor + model competing for VRAM)       │
│       → detect: CUDA OOM in inference log                         │
│       → pause: close editor GPU usage estimate                    │
│       → drop: one quant level (70B Q4 → 34B Q8 → 34B Q4)        │
│       → resume: with degraded model, flag in /health              │
│                                                                     │
│  T3 — UE5 editor crash during packaging                            │
│       → detect: UE4Editor-*.log FATAL or process exit             │
│       → retry: headless cook mode (no editor, UE5-cmd)            │
│       → if retry fails: HALT + log crash dump path                │
│                                                                     │
│  T4 — Platform SDK not found for requested target                  │
│       → graceful: skip that platform, continue others             │
│       → log: PLATFORM_SDK_REQUIRED for {platform}                 │
│       → never HALT on missing SDK — degrade gracefully            │
│                                                                     │
│  T5 — Blueprint JSON import failure (.uasset conversion)           │
│       → detect: UE commandlet import error                        │
│       → repair: re-generate Blueprint JSON for failing graph      │
│       → fallback: generate equivalent C++ if BP repair fails 3x  │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FILES PER MODULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  contracts/               ← LEVEL 0, immutable                    │
│    models/game_brief.py                                             │
│    models/project_spec.py                                           │
│    models/code_artifact.py                                          │
│    models/build_result.py                                           │
│    models/agent_message.py                                          │
│    models/platform_spec.py                                          │
│    models/store_spec.py                                             │
│    api.yaml                                                         │
│                                                                     │
│  templates/interfaces/    ← LEVEL 0, immutable UE5 headers        │
│    IForgeGameMode.h                                                 │
│    IForgeCharacter.h                                                │
│    IForgeGameInstance.h                                             │
│    IForgeInventory.h                                                │
│    IForgeSaveGame.h                                                 │
│    IForgeUIManager.h                                                │
│    IForgeAudioManager.h                                             │
│    IForgeAchievement.h                                              │
│    IForgePlatformLayer.h                                            │
│    IForgeOnlineSubsystem.h                                          │
│                                                                     │
│  ai/                      ← META-LAYER (Level 1-2)                │
│    architect_agent.py     brief → ProjectSpec + UBT module graph  │
│    test_agent.py          ProjectSpec → test specs per system      │
│    repair_loop.py         UBT/UHT errors → targeted repair        │
│    test_generation/                                                 │
│      cpp_test_generator.py   UE5 FAutomationTestBase templates    │
│      blueprint_test_validator.py  BP JSON spec validator           │
│      test_harness.py          orchestrate UE5 test runner          │
│                                                                     │
│  engine/                  ← PIPELINE (Levels 1-6)                 │
│    ue5_scanner.py         UE5 install + SDK detection             │
│    brief_parser.py        raw brief → GameBrief schema            │
│    project_scaffolder.py  GameBrief → folder structure + configs  │
│    cpp_generator.py       ModuleSpec → .h + .cpp files            │
│    blueprint_generator.py ModuleSpec → BP JSON node graphs        │
│    build_runner.py        invoke UHT → UBT, capture errors        │
│    package_agent.py       cook + pak per platform target          │
│    store_agent.py         Steam/EGS submission config + assets    │
│    learning_store.py      pattern library per genre + subsystem   │
│    platform_guards.py     inject platform macros + validate       │
│                                                                     │
│  server/                                                            │
│    main.py                                                          │
│    api/                                                             │
│      projects.py          CRUD projects + trigger generation       │
│      architecture.py      GET ProjectSpec for human review        │
│      generation.py        progress, file tree, critic log         │
│      builds.py            compile status, error log, repair hist  │
│      packages.py          platform build status + download        │
│      store.py             submission assets + config              │
│      auth.py              JWT + API key                           │
│    workers/                                                         │
│      generation_worker.py Celery: full topo pipeline              │
│      build_worker.py      Celery: UBT compile + test run          │
│      package_worker.py    Celery: cook + pak per platform         │
│    models/                SQLAlchemy ORM                           │
│                                                                     │
│  dashboard/src/pages/                                               │
│    ProjectBrief.jsx       submit brief + architecture review       │
│    GenerationProgress.jsx topo level progress + critic status      │
│    FileTree.jsx           generated UE5 project browser           │
│    BuildConsole.jsx       live UBT output + error highlighting    │
│    PlatformPackages.jsx   per-platform build status + download    │
│    LearningStore.jsx      pattern library browser                 │
│                                                                     │
│  tests/                                                             │
│    test_platform_guards.py     safety — always first              │
│    test_architect_agent.py     brief → valid ProjectSpec           │
│    test_cpp_generator.py       ModuleSpec → valid C++ headers      │
│    test_blueprint_generator.py ModuleSpec → valid BP JSON         │
│    test_build_runner.py        mock UBT → error parse + repair    │
│    test_package_agent.py       mock cook → platform output        │
│    test_repair_loop.py         inject UBT error → repair fires    │
│    integration/                                                     │
│      test_full_pipeline.py     live UBT compile of sample project │
│                                                                     │
│  .vscode/                                                           │
│    settings.json          exclude: Binaries/, Intermediate/,      │
│                                    Saved/, DerivedDataCache/       │
│    extensions.json        pylance, ruff, clangd, UE5 snippets    │
│    launch.json            debug FORGE server, debug UBT runner    │
│    tasks.json             (below)                                  │
│    forge.code-workspace   multi-root: forge/ + output/{project}/  │
│                                                                     │
│  PRIVATE_LICENSE.md       proprietary terms                        │
│  tasks.md                 build checklist                          │
│  docker-compose.yml       forge server + postgres + redis          │
│  .env.example                                                       │
│  README.md                                                          │
└─────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASKS.MD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────────────────────────┐
│  # FORGE Build Tasks                                                │
│                                                                     │
│  ## Step 0 — Contracts + UE5 Interface Headers (immutable)         │
│  ( ) contracts/models/game_brief.py                                │
│  ( ) contracts/models/project_spec.py                              │
│  ( ) contracts/models/code_artifact.py                             │
│  ( ) contracts/models/build_result.py                              │
│  ( ) contracts/models/agent_message.py                             │
│  ( ) contracts/models/platform_spec.py                             │
│  ( ) contracts/models/store_spec.py                                │
│  ( ) contracts/api.yaml                                             │
│  ( ) templates/interfaces/IForgeGameMode.h                         │
│  ( ) templates/interfaces/IForgeCharacter.h                        │
│  ( ) templates/interfaces/IForgeGameInstance.h                     │
│  ( ) templates/interfaces/IForgeInventory.h                        │
│  ( ) templates/interfaces/IForgeSaveGame.h                         │
│  ( ) templates/interfaces/IForgeUIManager.h                        │
│  ( ) templates/interfaces/IForgeAudioManager.h                     │
│  ( ) templates/interfaces/IForgeAchievement.h                      │
│  ( ) templates/interfaces/IForgePlatformLayer.h                    │
│  ( ) templates/interfaces/IForgeOnlineSubsystem.h                  │
│                                                                     │
│  ## AI Meta-Layer (Level 1-2)                                      │
│  ( ) ai/architect_agent.py            FR-03, FR-13–FR-22          │
│  ( ) ai/test_agent.py                 FR-08                        │
│  ( ) ai/repair_loop.py                FR-09, NFR-03, NFR-04        │
│  ( ) ai/test_generation/cpp_test_generator.py                      │
│  ( ) ai/test_generation/blueprint_test_validator.py                │
│  ( ) ai/test_generation/test_harness.py                            │
│                                                                     │
│  ## Engine Pipeline (Levels 1-6)                                   │
│  ( ) engine/ue5_scanner.py            FR-01                        │
│  ( ) engine/brief_parser.py           FR-02                        │
│  ( ) engine/project_scaffolder.py     FR-06                        │
│  ( ) engine/cpp_generator.py          FR-04, NFR-03                │
│  ( ) engine/blueprint_generator.py    FR-05, NFR-05                │
│  ( ) engine/build_runner.py           FR-07, NFR-01, NFR-04        │
│  ( ) engine/package_agent.py          FR-10                        │
│  ( ) engine/store_agent.py            FR-11                        │
│  ( ) engine/learning_store.py         FR-12                        │
│  ( ) engine/platform_guards.py        NFR-06                       │
│                                                                     │
│  ## Server (Level 7-8)                                             │
│  ( ) server/api/projects.py                                         │
│  ( ) server/api/architecture.py                                     │
│  ( ) server/api/generation.py                                       │
│  ( ) server/api/builds.py                                           │
│  ( ) server/api/packages.py                                         │
│  ( ) server/api/store.py                                            │
│  ( ) server/api/auth.py                                             │
│  ( ) server/workers/generation_worker.py                            │
│  ( ) server/workers/build_worker.py                                 │
│  ( ) server/workers/package_worker.py                               │
│  ( ) server/main.py                                                  │
│                                                                     │
│  ## Dashboard (Level 7, parallel with server)                      │
│  ( ) ProjectBrief.jsx                                               │
│  ( ) GenerationProgress.jsx                                         │
│  ( ) FileTree.jsx                                                   │
│  ( ) BuildConsole.jsx                                               │
│  ( ) PlatformPackages.jsx                                           │
│  ( ) LearningStore.jsx                                              │
│                                                                     │
│  ## Tests                                                           │
│  ( ) test_platform_guards.py          safety gate                  │
│  ( ) test_architect_agent.py                                        │
│  ( ) test_cpp_generator.py                                          │
│  ( ) test_blueprint_generator.py                                    │
│  ( ) test_build_runner.py                                           │
│  ( ) test_repair_loop.py                                            │
│  ( ) integration/test_full_pipeline.py                              │
│                                                                     │
│  ## Infrastructure                                                  │
│  ( ) docker-compose.yml                                             │
│  ( ) .vscode/ workspace config                                      │
│  ( ) PRIVATE_LICENSE.md                                             │
│  ( ) README.md                                                      │
└─────────────────────────────────────────────────────────────────────┘

.VSCODE/TASKS.JSON:
┌─────────────────────────────────────────────────────────────────────┐
│  "Start FORGE Server"  → docker-compose up                         │
│  "Run Architect Agent" → python ai/architect_agent.py              │
│  "Run Test Agent"      → python ai/test_agent.py                   │
│  "Run Repair Loop"     → python ai/repair_loop.py                  │
│  "UBT Compile"         → {UE_ROOT}/Build.bat {Project} Win64 Dev  │
│  "UHT Check"           → {UE_ROOT}/UnrealHeaderTool {Project}     │
│  "Test: Safety Guards" → pytest tests/test_platform_guards.py -v  │
│  "Test: All"           → pytest tests/ -v --tb=short              │
│  "Package: Win64"      → python engine/package_agent.py Win64     │
│  "Package: All"        → python engine/package_agent.py all       │
└─────────────────────────────────────────────────────────────────────┘

PRICING / BUSINESS MODEL:
┌─────────────────────────────────────────────────────────────────────┐
│  PRIVATE TOOL — personal/studio use                                │
│  No SaaS pricing. You own it, you run it, you ship with it.       │
│                                                                     │
│  REVENUE MODEL (your shipped games):                               │
│  → You keep all revenue minus platform cuts and UE5 royalty       │
│  → PC: 70% (after Steam 30%) or 88% (after EGS 12%)              │
│  → UE5 royalty: 5% gross after first $1M/product/year            │
│  → Console: platform-specific (typically 70-80% to developer)    │
│                                                                     │
│  STUDIO SCALE ESTIMATE:                                            │
│  → FORGE generates a complete 7B-style indie game scaffold        │
│    in < 2 hours on your hardware                                   │
│  → Human work: content, art, narrative, level design              │
│  → Time to shippable demo: weeks not years                        │
└─────────────────────────────────────────────────────────────────────┘

README.md spec:
┌─────────────────────────────────────────────────────────────────────┐
│  # FORGE — Autonomous Unreal Engine Game Development Platform      │
│  ## License: Private — see PRIVATE_LICENSE.md                     │
│  ## Prerequisites                                                   │
│  - Unreal Engine 5.3+ installed (UNREAL_ENGINE_ROOT in .env)     │
│  - Python 3.11+, Node 20+                                         │
│  - LLM: Llama-3-70B Q4_K_M recommended (see inference runtime)   │
│  - Platform SDKs optional (gates console packaging only)          │
│  ## Start                                                           │
│  cp .env.example .env   # set UNREAL_ENGINE_ROOT + LLM endpoint  │
│  docker-compose up -d                                              │
│  ## Submit a Game Brief                                             │
│  POST /api/projects { "brief": "3D action RPG, single player,    │
│    skill-based combat, open world, PC + console" }                │
│  GET  /api/projects/:id/architecture  → review before generating  │
│  POST /api/projects/:id/generate      → full pipeline starts      │
│  ## Human Gates                                                     │
│  GATE-1: approve ProjectSpec + UE5 module graph                   │
│  GATE-2: review generated C++ + Blueprint structure               │
│  GATE-3: approve platform packaging                               │
│  GATE-4: any CRITIC HALT (repair loop exhausted)                  │
│  ## Output                                                          │
│  output/{project_name}/   → complete UE5 project, open in editor  │
│  output/{project_name}/Build/  → packaged binaries per platform  │
└─────────────────────────────────────────────────────────────────────┘