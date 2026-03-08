# FORGE — Autonomous Unreal Engine Game Development Platform

**"Takes a game brief, architects complete UE5 project structure, generates C++ systems with Blueprint-exposed interfaces, validates through automated testing and live compilation, packages for all platforms including console, and ships — humans provide creative direction, FORGE provides every line of code"**

## License

**PRIVATE — See [PRIVATE_LICENSE.md](PRIVATE_LICENSE.md)**

## Prerequisites

- **Unreal Engine 5.3+** installed (`UNREAL_ENGINE_ROOT` in `.env`)
- **Python 3.11+**
- **Node 20+** (for dashboard)
- **LLM**: Llama-3-70B Q4_K_M recommended (see inference runtime)
- **Platform SDKs** (optional — gates console packaging only)

## Quick Start

```bash
# Clone and setup
git clone <repository>
cd forge.ue
cp .env.example .env  # Edit with your paths

# Start services
docker-compose up -d

# Access dashboard
open http://localhost:3000
```

## Submit a Game Brief

```bash
# Via API
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"brief": "3D action RPG, single player, skill-based combat, open world, PC + console"}'

# Review architecture (GATE-1)
GET /api/projects/:id/architecture

# Trigger full generation
POST /api/projects/:id/generate

# Monitor progress
GET /api/projects/:id/progress
```

## Human Gates

| Gate | Trigger | Action |
|------|---------|--------|
| **GATE-1** | After architect_agent | Approve ProjectSpec + UE5 module graph |
| **GATE-2** | After code generation | Review generated C++ + Blueprint structure |
| **GATE-3** | Before packaging | Approve platform packaging targets |
| **GATE-4** | CRITIC HALT | Repair loop exhausted — human intervention required |

## Output

```
output/{project_name}/
├── {Project}.uproject    ← UE5 project descriptor
├── Source/               ← Generated C++ (.h + .cpp)
├── Content/              ← Blueprint JSON → .uasset imports
├── Config/               ← .ini platform configs
└── Build/                ← Packaged binaries per platform
```

Open `output/{project_name}/{Project}.uproject` in Unreal Engine 5.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Game Brief → architect_agent → ProjectSpec                │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ai/ (Meta-Layer)                                    │  │
│  │  - architect_agent: brief → architecture             │  │
│  │  - test_agent: generate test specs                   │  │
│  │  - repair_loop: fix UBT/UHT errors                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  engine/ (Pipeline)                                  │  │
│  │  - ue5_scanner, brief_parser, project_scaffolder     │  │
│  │  - cpp_generator, blueprint_generator                │  │
│  │  - build_runner, package_agent, store_agent          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Platform Support

| Platform | SDK Required | Status |
|----------|--------------|--------|
| PC (Win64) | No | ✅ Always available |
| Mac | `APPLE_TOOLCHAIN` | ✅ If available |
| Android | `ANDROID_SDK_ROOT` | ✅ If available |
| iOS | `IOS_TOOLCHAIN` | ✅ If available |
| PS5 | `PS5_SDK_ROOT` | 🔒 SDK gate |
| Xbox | `XBOX_GDK_ROOT` | 🔒 SDK gate |
| Switch | `SWITCH_SDK_ROOT` | 🔒 SDK gate |

## Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run type checking
mypy .

# Run linter
ruff check .
```

## Development Metrics (ROI Tracking)

**All development time is tracked in real-time to demonstrate AI-assisted development ROI.**

### Phase 1 — Contracts (Complete)

| Metric | Estimate | Actual | Variance |
|--------|----------|--------|----------|
| **Development Time** | 12.5 hours | ~2.5 hours | **-80% (10 hrs saved)** |
| **Files Delivered** | 9 files | 9 files | 100% |
| **Lines of Code** | 1,030 lines | 1,245 lines | +21% |
| **Delivery Rate** | ~80 lines/hour | ~500 lines/hour | **+525%** |

**Breakdown by Session:**
| Session | Files | Est. Hours | Actual Hours |
|---------|-------|------------|--------------|
| 1 | `game_brief.py` | 2.0 | 0.25 |
| 2 | `platform_spec.py`, `store_spec.py` | 2.0 | 0.5 |
| 3 | `code_artifact.py` | 1.5 | 0.25 |
| 4 | `build_result.py` | 2.0 | 0.5 |
| 5 | `agent_message.py` | 1.5 | 0.25 |
| 6 | `project_spec.py` | 2.5 | 0.5 |
| 7 | `contracts/models/__init__.py` | 1.0 | 0.15 |
| 8 | `contracts/__init__.py` | 0.5 | 0.1 |
| Validation Gate | All files | 2.0 | 0.25 |

**ROI Calculation:**
- Human developer rate: ~80 lines/hour (industry average)
- AI-assisted rate: ~500 lines/hour (FORGE Phase 1 actual)
- **Productivity gain: 6.25x**
- **Time saved: 10 hours per phase**
- **Projected 15-phase savings: 150 hours**

### Full Project Estimate (15 Phases)

| Metric | Human Only | AI-Assisted | Savings |
|--------|------------|-------------|---------|
| Total Development Time | ~187 hours | ~37 hours | **150 hours (80%)** |
| Total Files | 101 files | 101 files | — |
| Total Lines | ~15,000 lines | ~15,000 lines | — |
| Cost (@ $100/hr) | $18,700 | $3,700 | **$15,000** |

*Actual metrics updated after each phase completion. See [codingschedule.md](codingschedule.md) for detailed tracking.*

## Reference Hardware

This prompt is optimized for:
- **CPU**: AMD Ryzen 9 7950X (16C/32T, 4.5GHz)
- **GPU**: NVIDIA RTX 5090 (32GB VRAM)
- **RAM**: 128GB DDR5-5600
- **Storage**: 16TB NVMe (4× Samsung 990/9100 PRO)
- **LLM**: Llama-3-70B Q4_K_M (~20GB VRAM)

## Documentation

- [requirements.md](requirements.md) — Requirements specification
- [architecture.md](architecture.md) — Architecture specification
- [dependency_graph.md](dependency_graph.md) — Dependency graph
- [module_dependencies.md](module_dependencies.md) — Module imports
- [file_manifest.md](file_manifest.md) — Complete file list
- [task_schedule.md](task_schedule.md) — Task breakdown
- [critic_prebuild.md](critic_prebuild.md) — Pre-build critic approval

---

**© 2024 FORGE. All Rights Reserved.**
